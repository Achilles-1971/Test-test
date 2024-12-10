from rest_framework.generics import CreateAPIView 
from rest_framework.request import HttpRequest 
from .serializers import (UserRegistrationSerializer)
from rest_framework. response import Response
from django.core.files.uploadedfile import InMemoryUploadedFile 
from django.contrib.auth.hashers import make_password
from . import permissions
from sqlalchemy.sql import select
from models.models import *
from .serializers import (UserImportExcelSerializer)
from models.config import session
from sqlalchemy.types import NULLTYPE
import random
import pandas
import requests

def unique_id_number() -> int:
    id_number: int = random.randint(0, 1000000) 
    try:
        while True:
            id_number = random. randint(0, 1000000)
            users_sql_row = select(User)
            users = session.scalars(users_sql_row).all()
            check_id_number: bool = False
            
            if len(users) == 0: return id_number

            for i in range(len(users)):
                if users[i].id_number == id_number:
                    check_id_number = True
                    break

                if not check_id_number:
                    return id_number
    except:
        return id_number

class UserRegistrationAPIView(CreateAPIView):
    serializer_class = UserRegistrationSerializer
    def get_queryset(self):
        users_sql = select(User)
        users = session.scalars(users_sql)
        return users
            
    def create(self, request, *args, **kwargs):
        response = {}
        id_number = unique_id_number()
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
            role_id = None
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
        try:
            event_id = events.one().id
        except:
            event_id = None
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
class UsersImportExcel(CreateAPIView):
    serializer_class = UserImportExcelSerializer
    permission_classes = (permissions.IsOrganizer, )
    def get_queryset(self):
        try:
            users_sql = select(User)
            queryset = session.scalars(users_sql)
        except:
                queryset = []
        return queryset
    def parse_excel(excel_file):
        try:
            df = pandas.read_excel(excel_file)
            users = [] 
            counter = 0 
            stop = len(df.values)
            for row in df.values: 
                counter += 1 
                if counter == stop: 
                    break
                user_dict = {}
                user_dict["id_number"] = row[0] 
                user_dict["username"] = row[0] 
                user_dict["password"] = make_password(row[1])
                user_dict["first_name"] = row[2] 
                user_dict["last_nane"] = row[3] 
                user_dict ["role"] = row[4] 
                image_url = row[5] 
                user_dict["gender"] = row[6] 
                user_dict["email"] = row[7] 
                user_dict["phone"] = row[8] 
                user_dict["direction"] = row[9]
                user_dict["event"] = row[10]
                response = requests.get(urt=image_url) 
                if response.status_code == 200: 
                    user_dict["photo"] = response.content
                else:
                    bimage = None 
                    user_dict["photo"] = bimage
                users.append(user_dict)
            return users
        except ValueError as e:
            print(e)
            return "BAD_REQUEST"
    def create(self, request: HttpRequest, *args, **kwargs):
        excel_file: InMemoryUploadedFile = request.FILES['file']
        parsed = self.parse_excel(excel_file)
        if parsed == "BAD_REQUEST":
            return Response({"info": "Пользователи не были добавлены"}, status=400)
        for user in parsed:
            id_number = user["id_number"] 
            id_number = user["id_number"]
            username = user["username"]
            password = user["password"] 
            first_name = user["first_name"]
            last_name = user["last_name"]
            role = user["role"]
            gender = user["gender"]
            email = user["email"] 
            phone = user["phone"] 
            direction = user["direction"] 
            event = user["event"] 
            photo = user["photo"]
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
            event_sql = select(Event).where(Event.title == event) 
            events = session.scalars(event_sql)
            try:
                event_id = events.one().id 
            except:
                event_id = NULLTYPE
            try:
                user = User(
                    id_number=id_number,
                    username=username, 
                    password=password, 
                    role_id=role_id,
                    gender=gender,
                    firstname=first_name, 
                    lastname=last_name,
                    photo=photo.read(),
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
                },status=400) 
            finally: 
                session.close()
        return Response({"info": "Пальзователи успешно созданы"}, status=200)
