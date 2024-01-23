from app.core.configs import settings


async def is_admin(identity: dict):
    return identity['role'] == settings.admin_role
