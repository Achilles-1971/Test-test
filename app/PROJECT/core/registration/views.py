from rest_framework.generics import CreateAPIView 
from rest_framework.request import HttpRequest 
from .serializers import (UserRegistrationSerializer)
from rest_framework. response import Response
from django.core.files.uploadedfile import InMemoryUploadedFile 
from django.contrib.auth.hashers import make_password
from . import permissions
from sqlalchemy.sql import select
from models.models import *
from models.config import session
from sqlalchemy.types import NULLTYPE
import random
class UserRegistrationAPIView(CreateAPIView):
    serializer_class = UserRegistrationSerializer
    def get_queryset(self):
        users_sql = select(User)
        users = session.scalars(users_sql)
        return users
    def unique_id_number() -> int:
        id_number: int = random.randint(0, 1000000) 
        try:
            while True:
                id_number = random. randint(0, 1000000)
                users_sql_row = select(User)
                users = session.scalars(users_sql_row).all()
                check_id_number: bool = False
                for i in range(len(users)):
                    if users[i].id_number == id_number:
                        check_id_number = True
                        break

                    if not check_id_number:
                        return id_number
        except:
            return id_number
            
    def create(self, request, *args, **kwargs):
        response = {}
        id_number = self.unique_id_number()
        full_name = request.POST.get('full_name')
        gender = request.POST.get('gender')
        role = request.POST.get('role')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        direction = request.POST.get('direction')
        event = request.POST.get('event')
        photo: InMemoryUploadedFile = request.FILES.get('photo')
        username = request.POST.get('username')
        password = request.POST.get('password')
        roles_sql_row = select(Role).where(Role.name == role)
        role_obj = session.scalar(roles_sql_row)
        if role_obj:
            role_id = role_obj.id
        else:
            role_id = NULLTYPE
        directions_sql_row = select(Direction).where(Direction.name == direction)
        direction_obj = session.scalar(directions_sql_row)
        if direction_obj:
            direction_id = direction_obj.id
        else:
            session.add(Direction(name=direction))
            session.commit()
            created_direction_sql = select(Direction).where(Direction.name == direction)
            created_direction = session.scalar(created_direction_sql)
            direction_id = created_direction.id 
            hash_password = make_password(password)
            lastname, firstname = full_name.split(' ')     
            event_sql = select(Event).where(Event.title == event)
            events = session.scalars(event_sql)
            if events: event_id = events.one().id
            else: event_id = NULLTYPE
            try:
                user = User(
                    id_number=id_number, username=username, password=hash_password,
                    role_id=role_id,
                    gender=gender,
                    firstname=firstname,
                    lastname=lastname,
                    photo=photo. read(),
                    email=email,
                    phone=phone,
                    direction_id=direction_id,
                    event_id=event_id
                )
                session.add(user)
                session.commit()
            except Exception as e:
                return Response({
                "info": f"Пользователь не был создан: {e}"
                }, status=400)
            finally:
                session.close()
            response["number_id"] = id_number
            response["password"] = hash_password
            return Response(response, status=200)   