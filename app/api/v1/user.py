from typing import List
from fastapi import APIRouter, Depends
from fastapi import HTTPException

from fastapiplugins.exceptions import HandlableException


from app.utils.password import compare_passwords

from app.schemas.user import (
    UserCreateProtected,
    UserUpdateProtected,
    UserInDBProtected,
)
from app.schemas.password import Password

from app.controllers import user as user_controller
from app.controllers import code as code_controller

from app.utils.deps import identify_request


ERROROR_TAGS = {
    "bad_code": 'BLOG_USER-BAD_CODE'
}


api = APIRouter()


@api.get('/', response_model=UserInDBProtected)
async def get_by_id(
    user_id: int
):
    if user := await user_controller.get_by_id(user_id):
        return user
    else:
        raise HTTPException(404)


@api.get('/all', response_model=List[UserInDBProtected])
async def get_all():
    if user := await user_controller.get_all():
        return user
    else:
        raise HTTPException(404)


# @api.get('/discord-id', response_model=UserInDBProtected)
# async def get_by_discord_id(
#     discord_id: int,
# ):
#     if user := await user_controller.get_by_discord_id(
#         str(discord_id)
#     ):
#         return user
#     else:
#         raise HTTPException(404)


@api.post('/', response_model=UserInDBProtected)
async def create_user(
    user_data: UserCreateProtected,
):
    if not await code_controller.get_by_code(user_data.code):
        # raise HTTPException(403, 'Wrong auth code! Contact admin to get auth code.')
        raise HandlableException(ERROROR_TAGS['bad_code'], 403, title="Wrong auth code.")
    if user := await user_controller.save(user_data):
        return user
    else:
        raise HTTPException(404)


@api.put('/', response_model=UserInDBProtected)
async def update_user(
    user_data: UserUpdateProtected,
    identity: dict = Depends(identify_request),
):
    if user := await user_controller.update(
        identity['sub'],
        user_data,
    ):
        return user
    else:
        raise HTTPException(404)


@api.delete('/', response_model=UserInDBProtected)
async def delete_user(
    identity: dict = Depends(identify_request),
):
    if user := await user_controller.delete(identity['sub']):
        return user
    else:
        raise HTTPException(404)


async def change_password(
    password: Password,
    identity: dict = Depends(identify_request)
):
    if user := await user_controller.set_password(
        identity['sub'],
        password
    ):
        return user
    else:
        raise HTTPException(404)


# @api.post('/email', response_model=UserInDBProtected)
# async def connect_email(
#     email: str,
#     identity: dict = Depends(identify_request),
# ):
#     if user := await user_controller.add_email(
#         identity['sub'],
#         email
#     ):
#         return user
#     else:
#         raise HTTPException(404)


# @api.delete('/email', response_model=UserInDBProtected)
# async def disconnect_email(
#     email: str,
#     identity: dict = Depends(identify_request),
# ):
#     if user := await user_controller.remove_email(
#         identity['sub'],
#         email,
#     ):
#         return user
#     else:
#         raise HTTPException(404)
