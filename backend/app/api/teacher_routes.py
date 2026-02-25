from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.classroom import Classroom
from app.schemas.classroom_schema import ClassroomCreate, ClassroomResponse
from app.core.dependencies import require_role
from app.models.user import RoleEnum

router = APIRouter(prefix="/teacher", tags=["Teacher"])


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