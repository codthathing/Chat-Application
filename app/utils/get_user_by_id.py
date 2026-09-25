from uuid import UUID
from models import User
from sqlalchemy.orm import Session


def get_user_by_id(user_id: UUID, db: Session) -> type[User] | None:
    return db.query(User).filter(User.id == user_id).first()