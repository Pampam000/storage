from fastapi.security import OAuth2PasswordRequestForm
from storage.database.database import (
    get_db,
    engine
)
from storage.database import tables
from fastapi import (
    Depends,
    APIRouter
)
from starlette import status
from sqlalchemy.orm import Session


from storage.schemas import user as u
from storage.schemas import token as t
from storage.crud import users

tables.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix='/auth'
)


@router.post('/token', response_model=t.Token)
def log_in(
    auth_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    return users.authenticate_user(
        auth_data.username,
        auth_data.password,
        db
    )


@router.post(
    '/sign-up/',
    status_code=status.HTTP_201_CREATED,
)
def sign_up(
        login: str,
        password: str,
        is_seller: bool,

        user_data: u.UserCreate,
        db: Session = Depends(get_db)
):
    user_data.login = login
    user_data.is_seller = is_seller
    user_data.password = password
    if users.register_new_user(user_data, db):
        return f"USER {user_data.login} has been signed up successfully"
    else:
        return "Smth went wrong"



@router.get("/me")
def get_me(current_user: u.User = Depends(users.get_current_user)):
    return current_user
