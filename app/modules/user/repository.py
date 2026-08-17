
from sqlalchemy.orm import Session

from app.modules.user.models import User
def create_user(db: Session, user: User)->User:
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_by_email(db: Session, email: str)->User | None:
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: int)->User | None:
    return db.query(User).filter(User.id == user_id).first()



def update_user(db: Session, user_id: int, user_data:User):
    pass


def delete_user(db: Session, user_id: int):
    pass


def verify_email(db: Session, email: str):
    pass    

def save_reset_token(db: Session, token: str, email: str):
    pass    

