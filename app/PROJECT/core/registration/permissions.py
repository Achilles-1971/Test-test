from rest_framework.permissions import BasePermission
from models.config import session
from sqlalchemy import select
from models.models import Role, User
from rest_framework. request import HttpRequest

class IsOrganizer(BasePermission):
    def has_permission(self, request: HttpRequest, view):
        try:
            user_id = request.session.get("user_id")
            auth_user_sql = select(User).where(User.id == user_id)
            auth_user = session.scalar(auth_user_sql)
            role_sql = select(Role).where(Role.name == 'организатор')
            role = session.scalar(role_sql)
        except:
            return False