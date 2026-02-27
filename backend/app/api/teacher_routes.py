from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.classroom import Classroom
from app.models.classroom_student import ClassroomStudent
from app.models.user import User
from app.models.attempt import Attempt
from app.models.mastery import Mastery
from app.models.risk_history import RiskHistory
from app.schemas.classroom_schema import ClassroomCreate, ClassroomResponse
from app.schemas.analytics_schema import ClassAnalyticsResponse, DashboardResponse, InsightResponse
from app.core.dependencies import require_role
from app.models.user import RoleEnum
from app.core.service_container import get_service_container
from app.core.exceptions import NotFoundError
from app.services.core.student_state import StudentState

router = APIRouter(prefix="/teacher", tags=["Teacher"])


def _get_student_state(db: Session, user_id: int) -> StudentState:
    """Load student state from database"""
    state = StudentState(student_id=user_id)
    
    # Load mastery
    mastery_rows = db.query(Mastery).filter(Mastery.user_id == user_id).all()
    for row in mastery_rows:
        state.mastery_dict[row.concept] = row.mastery_value
        state.confidence_metrics[row.concept] = row.confidence
    
    # Load latest risk profile
    latest_risk = db.query(RiskHistory).filter(
        RiskHistory.student_id == str(user_id)
    ).order_by(RiskHistory.timestamp.desc()).first()
    
    if latest_risk:
        state.risk_profile = {
            "risk_probability": latest_risk.risk_score,
            "risk_label": latest_risk.risk_label,
            "risk_level": "high" if latest_risk.risk_score > 0.6 else "medium" if latest_risk.risk_score > 0.3 else "low"
        }
    
    return state


@router.post("/classroom", response_model=ClassroomResponse)
def create_classroom(
    data: ClassroomCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(RoleEnum.teacher))
):
    classroom = Classroom(
        name=data.name,
        subject=data.subject,
        teacher_id=current_user.id,
        syllabus_scope=data.syllabus_scope,
        exam_pattern=data.exam_pattern,
        progress_topics=data.progress_topics
    )

    db.add(classroom)
    db.commit()
    db.refresh(classroom)

    return classroom


@router.get("/classrooms")
def get_teacher_classrooms(
    db: Session = Depends(get_db),
    current_user = Depends(require_role(RoleEnum.teacher))
):
    """
    Get all classrooms for the current teacher
    """
    try:
        classrooms = db.query(Classroom).filter(
            Classroom.teacher_id == current_user.id
        ).all()
        
        return [
            {
                "id": c.id,
                "name": c.name,
                "subject": c.subject,
                "teacher_id": c.teacher_id,
                "syllabus_scope": c.syllabus_scope,
                "exam_pattern": c.exam_pattern,
                "progress_topics": c.progress_topics,
                "created_at": c.created_at.isoformat() if hasattr(c, 'created_at') else None
            }
            for c in classrooms
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get classrooms: {str(e)}")


@router.get("/classroom/{classroom_id}/students")
def get_classroom_students(
    classroom_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(RoleEnum.teacher))
):
    """
    Get all students enrolled in a classroom
    """
    try:
        classroom = db.query(Classroom).filter(Classroom.id == classroom_id).first()
        if not classroom:
            raise NotFoundError("Classroom", classroom_id)
        
        if classroom.teacher_id != current_user.id:
            raise HTTPException(status_code=403, detail="You do not have access to this classroom")
        
        students = db.query(ClassroomStudent).filter(
            ClassroomStudent.classroom_id == classroom_id
        ).all()
        
        student_list = []
        for cs in students:
            student = db.query(User).filter(User.id == cs.student_id).first()
            if student:
                state = _get_student_state(db, student.id)
                student_list.append({
                    "id": student.id,
                    "email": student.email,
                    "role": student.role,
                    "mastery": state.mastery_dict,
                    "risk": state.risk_profile.get("risk_probability", 0) if state.risk_profile else 0,
                    "risk_level": state.risk_profile.get("risk_level", "low") if state.risk_profile else "low"
                })
        
        return student_list
    except HTTPException:
        raise
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get classroom students: {str(e)}")


@router.get("/classroom/{classroom_id}/insights")
def get_class_insights(
    classroom_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(RoleEnum.teacher))
) -> ClassAnalyticsResponse:
    """
    Get analytics insights for an entire classroom.
    """
    try:
        classroom = db.query(Classroom).filter(Classroom.id == classroom_id).first()
        if not classroom:
            raise NotFoundError("Classroom", classroom_id)
        
        if classroom.teacher_id != current_user.id:
            raise HTTPException(status_code=403, detail="You do not have access to this classroom")
        
        services = get_service_container(db)
        
        # Get all students in class
        students = db.query(ClassroomStudent).filter(
            ClassroomStudent.classroom_id == classroom_id
        ).all()
        
        student_ids = [s.student_id for s in students]
        
        if not student_ids:
            return ClassAnalyticsResponse(
                class_id=classroom_id,
                average_mastery=0.0,
                at_risk_count=0,
                total_students=0,
                weak_concepts=[],
                heatmap={}
            )
        
        # Calculate class-level metrics
        student_mastery_averages = []
        at_risk_count = 0
        concept_totals = {}
        concept_counts = {}
        
        for student_id in student_ids:
            state = _get_student_state(db, student_id)
            
            # Get risk
            if state.risk_profile and state.risk_profile.get("risk_probability", 0) > 0.6:
                at_risk_count += 1
            
            # Aggregate mastery by concept
            student_total = 0.0
            for concept, value in state.mastery_dict.items():
                concept_totals[concept] = concept_totals.get(concept, 0) + value
                concept_counts[concept] = concept_counts.get(concept, 0) + 1
                student_total += value
            
            # Average per student
            if state.mastery_dict:
                student_mastery_averages.append(student_total / len(state.mastery_dict))
        
        # Calculate class average from per-student averages
        total_mastery_score = sum(student_mastery_averages) / len(student_mastery_averages) if student_mastery_averages else 0.0
        
        weak_concepts = sorted(
            [
                (concept, concept_totals[concept] / concept_counts[concept])
                for concept in concept_totals
            ],
            key=lambda x: x[1]
        )[:5]
        
        weak_concept_names = [c[0] for c in weak_concepts]
        
        heatmap = {
            concept: round(concept_totals.get(concept, 0) / max(concept_counts.get(concept, 1), 1), 2)
            for concept in concept_totals
        }
        
        return ClassAnalyticsResponse(
            class_id=classroom_id,
            average_mastery=round(total_mastery_score, 2),
            at_risk_count=at_risk_count,
            total_students=len(student_ids),
            weak_concepts=weak_concept_names,
            heatmap=heatmap
        )
    
    except HTTPException:
        raise
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get class insights: {str(e)}")


@router.get("/student/{student_id}/dashboard")
def get_student_dashboard(
    student_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(RoleEnum.teacher))
) -> DashboardResponse:
    """
    Get detailed dashboard for a specific student.
    """
    try:
        # Verify teacher can access this student
        student = db.query(User).filter(User.id == student_id).first()
        if not student:
            raise NotFoundError("User", student_id)
        
        # Check if student is in any of teacher's classrooms
        has_access = db.query(ClassroomStudent).join(
            Classroom,
            Classroom.id == ClassroomStudent.classroom_id
        ).filter(
            ClassroomStudent.student_id == student_id,
            Classroom.teacher_id == current_user.id
        ).first()
        
        if not has_access and current_user.id != student_id:
            raise HTTPException(status_code=403, detail="Access denied")
        
        services = get_service_container(db)
        student_state = _get_student_state(db, student_id)
        
        # Generate insights
        try:
            weak_topics = services.insight_generator.weak_topics(db, student_id)
            calibration_gap = services.insight_generator.calibration_gap(db, student_id)
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
            Attempt.user_id == student_id
        ).order_by(Attempt.id.desc()).limit(10).all()
        
        recent_data = [
            {"question_id": a.question_id, "is_correct": a.is_correct, "confidence": a.confidence}
            for a in recent_attempts
        ]
        
        # Calculate risk if not in history
        risk_score = 0
        if student_state.risk_profile:
            risk_score = float(student_state.risk_profile.get("risk_probability", 0))
        elif student_state.mastery_dict:
            # Estimate risk from mastery (1 - average mastery)
            avg_mastery = sum(student_state.mastery_dict.values()) / len(student_state.mastery_dict)
            risk_score = max(0, min(1, (100 - avg_mastery) / 100))  # Normalize to 0-1
        
        return DashboardResponse(
            user_id=student_id,
            mastery=student_state.mastery_dict,
            risk_score=risk_score,
            insights=insights,
            recent_attempts=recent_data
        )
    
    except HTTPException:
        raise
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get student dashboard: {str(e)}")