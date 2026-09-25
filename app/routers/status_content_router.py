from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import models
from database import get_db
from app.schemas.status_content_schema import StatusContent


router = APIRouter(prefix="/status-contents", tags=["Status"])


@router.get("")
def get_status_contents(db: Session = Depends(get_db)):
    return db.query(models.StatusContent).all()


@router.post("")
def upload_status(status_content: StatusContent, db: Session = Depends(get_db)):
    status_content = models.StatusContent(id=status_content.u_id)
    db.add(status_content)
    db.commit()
    db.refresh(status_content)

    return status_content