from sqlalchemy.orm import Session
from app.modules.user.repository import get_user_by_id, update_user, delete_user, verify_email, save_reset_token
from app.modules.user.models import User
def get_user_Profile(db: Session, user_id: int)->User:
    return get_user_by_id(db, user_id)

def change_password():
    pass


def forgot_password():
        pass

def reset_password():
    pass


def verify_email():
    pass


def update_profile():
    pass

