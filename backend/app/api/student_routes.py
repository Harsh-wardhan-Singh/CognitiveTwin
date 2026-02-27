from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.classroom import Classroom
from app.models.classroom_student import ClassroomStudent
from app.models.mastery import Mastery
from app.models.attempt import Attempt
from app.core.dependencies import require_role, get_current_user
from app.models.user import RoleEnum, User
from app.schemas.analytics_schema import DashboardResponse, InsightResponse
from app.core.service_container import get_service_container
from app.services.core.student_state import StudentState

router = APIRouter(prefix="/student", tags=["Student"])


def _get_student_state(db: Session, user_id: int) -> StudentState:
    """Load student state from database"""
    state = StudentState(student_id=user_id)
    
    # Load mastery
    mastery_rows = db.query(Mastery).filter(Mastery.user_id == user_id).all()
    for row in mastery_rows:
        state.mastery_dict[row.concept] = row.mastery_value
        state.confidence_metrics[row.concept] = row.confidence
    
    return state


@router.post("/join/{classroom_id}")
def join_classroom(
    classroom_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(RoleEnum.student))
):

    classroom = db.query(Classroom).filter(Classroom.id == classroom_id).first()

    if not classroom:
        raise HTTPException(status_code=404, detail="Classroom not found")

    existing = db.query(ClassroomStudent).filter(
        ClassroomStudent.classroom_id == classroom_id,
        ClassroomStudent.student_id == current_user.id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Already joined")

    join = ClassroomStudent(
        classroom_id=classroom_id,
        student_id=current_user.id
    )

    db.add(join)
    db.commit()

    return {"message": "Joined classroom successfully"}


@router.get("/dashboard")
def get_student_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> DashboardResponse:
    """
    Get student's personal dashboard with mastery, risk, and insights.
    """
    try:
        services = get_service_container(db)
        student_state = _get_student_state(db, current_user.id)
        
        # Generate insights
        try:
            weak_topics = services.insight_generator.weak_topics(db, current_user.id)
            calibration_gap = services.insight_generator.calibration_gap(db, current_user.id)
        except:
            weak_topics = list(student_state.mastery_dict.keys())[:3]
            calibration_gap = 0.0
        
        learning_trend = {
            concept: 0.1
            for concept in student_state.mastery_dict
        }
        
        volatility = {
            concept: 0.05
            for concept in student_state.mastery_dict
        }
        
        insights = InsightResponse(
            weak_topics=weak_topics[:3],
            calibration_gap=calibration_gap,
            learning_trend=learning_trend,
            volatility=volatility,
            recommended_topics=weak_topics[:3]
        )
        
        recent_attempts = db.query(Attempt).filter(
            Attempt.user_id == current_user.id
        ).order_by(Attempt.id.desc()).limit(10).all()
        
        recent_data = [
            {"question_id": a.question_id, "is_correct": a.is_correct, "confidence": a.confidence}
            for a in recent_attempts
        ]
        
        return DashboardResponse(
            user_id=current_user.id,
            mastery=student_state.mastery_dict,
            risk_score=float(student_state.risk_profile.get("risk_probability", 0)) if student_state.risk_profile else 0,
            insights=insights,
            recent_attempts=recent_data
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get dashboard: {str(e)}")


@router.get("/classrooms")
def get_student_classrooms(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(RoleEnum.student))
):
    """Get all classrooms the student is enrolled in"""
    try:
        classrooms = db.query(Classroom).join(
            ClassroomStudent,
            Classroom.id == ClassroomStudent.classroom_id
        ).filter(
            ClassroomStudent.student_id == current_user.id
        ).all()
        
        return [
            {
                "id": c.id,
                "name": c.name,
                "subject": c.subject,
                "teacher_id": c.teacher_id
            }
            for c in classrooms
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get classrooms: {str(e)}")