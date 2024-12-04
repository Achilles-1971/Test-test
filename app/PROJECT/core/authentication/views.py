from rest_framework.response import Response
from rest_framework.generics import ListAPIView, CreateAPIView
from .serializers import UserSerializer
from models.models import User, Role, Direction
from models.config import session
from sqlalchemy.sql import select
from rest_framework. request import HttpRequest
from datetime import timedelta
class AuthenticationAPIView(CreateAPIView):
    serializer_class = UserSerializer
def get_queryset(self):
    users_sql = select(User)
    users = session.scalars(users_sql)
    return users
def create(self, request: HttpRequest, *args, **kwargs):
    id_number = request.POST.get("id_number")
    password = request.POST.get("password")
    user_sql = select(User).where(User.id_number == id_number)
    user = session.scalar(user_sql)
    if user and user.check_user_password(password):
        request.session["user_id"] = user.id
        request.session.set_expiry(timedelta(days=1))
        return Response({f"{user.username}": "Успешно вошел!"}, status=200)
    return Response({"info": "Такого пользователя нет"}, status=400)