from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.classroom import Classroom
from app.models.classroom_student import ClassroomStudent
from app.core.dependencies import require_role
from app.models.user import RoleEnum

router = APIRouter(prefix="/student", tags=["Student"])


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