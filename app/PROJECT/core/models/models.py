from django.db import models
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, ForeignKey, LargeBinary, Date, BLOB
from django.contrib.auth.hashers import check_password

GENDERS = ["мужчина", "женщина"]
ROLES = ["пользователь", "организатор", "жюри", "модератор"]


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"
    id = Column(
        Integer,
        primary_key=True,
        unique=True,
        nullable=False,
        autoincrement=True,
        comment="Уникальный индетификатор пользователя",
        doc="Уникальный индетификатор пользователя",
        info={
            "name": "id",
            "type": "integer",
            "description": "Уникальный индетификатор пользователя",
            "primary_key": True,
            "unique": True,
            "nullable": False,
        },
    )
    id_number = Column(
        Integer,
        unique=True,
        nullable=False,
        comment="Уникальный индетификатор пользователя",
        doc="Уникальный индетификатор пользователя",
        info={
            "name": "id_number",
            "type": "integer",
            "description": "Уникальный индетификатор пользователя",
            "primary_key": True,
            "unique": True,
            "nullable": False,
        },
    )
    username = Column(
        String(50),
        nullable=False,
        unique=True,
        system=False,
        comment="Логин пользователя",
        doc="Логин пользователя",
        info={
            "name": "username",
            "type": "string",
            "description": "Логин пользователя",
            "unique": True,
            "nullable": False,
            "system": False,
            "max_length": 50,
        },
    )
    password = Column(
        String(50),
        nullable=False,
        system=False,
        comment="Пароль пользователя",
        doc="Пароль пользователя",
        info={
            "name": "password",
            "type": "string",
            "description": "Пароль пользователя",
            "nullable": False,
            "max_length": 50,
        },
    )
    firstname = Column(
        String(255),
        nullable=True,
        comment="Имя пользователя",
        doc="Имя пользователя",
        info={
            "name": "firstname",
            "type": "string",
            "description": "Имя пользователя",
            "nullable": True,
            "max_length": 255,
        },
    )
    lastname = Column(
        String(255),
        nullable=True,
        comment="Фамилия пользователя",
        doc="Фамилия пользователя",
        info={
            "name": "lastname",
            "type": "string",
            "description": "Фамилия пользователя",
            "nullable": True,
            "max_length": 255,
        },
    )
    role_id = Column(
        Integer,
        ForeignKey("role.id"),
        nullable=False,
        comment="Идентификатор роли пользователя",
        doc="Идентификатор роли пользователя",
        info={
            "name": "roleId",
            "type": "integer",
            "description": "Идентификатор роли пользователя",
            "foreign_key": "role.id",
            "nullable": False,
        },
    )
    photo = Column(
        LargeBinary,
        nullable=True,
        doc="Фото пользователя",
        comment="Фото пользователя",
        info={
            "name": "photo",
            "type": "binary",
            "description": "Фото пользователя",
            "nullable": True,
        },
    )
    gender = Column(
        String(10),
        nullable=False,
        doc="Пол пользователя",
        comment="пол пользователя",
        info={
            "name": "gender",
            "type": "string",
            "description": "Пол пользователя",
            "nullable": False,
        },
    )
    email = Column(
        String(255),
        nullable=True,
        unique=True,
        system=False,
        comment="Электронная почта пользователя",
        doc="Электронная почта пользователя",
        info={
            "name": "email",
            "type": "string",
            "description": "Электронная почта пользователя",
            "unique": True,
            "nullable": False,
            "system": False,
            "max_length": 255,
        },
    )
    phone = Column(
        String(17),
        nullable=True,
        comment="Номер телефона пользователя",
        doc="Номер телефона пользователя",
        info={
            "name": "phone",
            "type": "integer",
            "description": "Номер телефона пользователя",
            "nullable": True,
            "max_length": 12,
        },
    )
    direction_id = Column(
        Integer,
        ForeignKey("direction.id"),
        nullable=True,
        comment="Идентификатор направления подготовки пользователя",
        doc="Идентификатор направления подготовки пользователя",
        info={
            "name": "direction_id",
            "type": "integer",
            "description": "Идентификатор направления подготовки пользователя",
            "foreign_key": "direction. id",
            "nullable": True,
        },
    )
    event_id = Column(
        Integer,
        ForeignKey("event.id"),
        nullable=True,
        comment="Идентификатор мероприятия пользователя",
        doc="Идентификатор мероприятия пользователя",
        info={
            "name": "event_id",
            "type": "integer",
            "description": "Идентификатор мероприятия пользователя",
            "foreign_key": "event.id",
            "nullable": True,
        },
    )

    def check_user_password(self, row_password):
        return check_password(row_password, self.password)

    @property
    def full_name(self):
        return f"{self.firstname} {self.lastname}"

    def __repr__(self) -> str:
        return f"{self.username}"


class Direction(Base):
    __tablename__ = "direction"
    id = Column(
        Integer,
        primary_key=True,
        unique=True,
        nullable=False,
        autoincrement=True,
        comment="Уникальный индетификатор направления",
        doc="Уникальный индетификатор направления",
        info={
            "name": "id",
            "type": "integer",
            "description": "Уникальный индетификатор направления",
            "primary_key": True,
            "unique": True,
            "nullable": False,
        },
    )
    name = Column(
        String(255),
        nullable=False,
        comment="Наименование направления",
        doc="Наименование направления",
        info={
            "name": "name",
            "type": "string",
            "description": "Наименование направления",
            "nullable": False,
            "max_length": 255,
        },
    )

    def __repr__(self) -> str:
        return f"<Direction(name={self.name})>"


class Role(Base):
    __tablename__ = "role"
    id = Column(
        Integer,
        primary_key=True,
        unique=True,
        nullable=False,
        comment="Уникальный индетификатор роли",
        doc="Уникальный индетификатор роли",
        info={
            "name": "id",
            "type": "integer",
            "description": "Уникальный индетификатор роли",
            "primary_key": True,
            "unique": True,
            "nullable": False,
        },
    )
    name = Column(
        String(255),
        nullable=False,
        comment="Название роли",
        doc="Название роли",
        info={
            "name": "name",
            "type": "string",
            "description": "Название роли",
            "nullable": False,
            "max_length": 255,
        },
    )

    def __repr__(self) -> str:
        return f"{self.name}"


class Event(Base):
    __tablename__ = "event"
    id = Column(
        Integer,
        primary_key=True,
        unique=True,
        nullable=False,
        autoincrement=True,
        comment="Уникальный индетификатор события",
        doc="Уникальный индетификатор события",
        info={
            "name": "id",
            "type": "integer",
            "description": "Уникальный индетификатор события",
            "primary_key": True,
            "unique": True,
            "nullable": False,
        },
    )
    title = Column(
        String(255),
        nullable=False,
        comment="Название события",
        doc="Название события",
        info={
            "name": "title",
            "type": "string",
            "description": "Название события",
            "nullable": False,
            "max_length": 255,
        },
    )
    photo = Column(
        BLOB,
        nullable=True,
        comment="Картинка для мероприятия",
        doc="Картинка для мероприятия",
        info={
            "name": "photo",
            "type": "binary",
            "description": "Картинка для мероприятия",
            "nullable": True,
        },
    )
    date = Column(
        Date,
        nullable=False,
        comment="Дата проведения мероприятия",
        doc="Дата проведения мероприятия",
        info={
            "name": "date",
            "type": "date",
            "description": "Дата проведения мероприятия",
            "nullable": False,
        },
    )
    user_id = Column(
        ForeignKey("user.id"),
        nullable=False,
        comment="Идентификатор пользователя, который отвественен за данное мероприятие",
        doc="Идентификатор пользователя, который отвественен за данное мероприятие",
        info={
            "name": "user_id",
            "type": "integer",
            "description": "Идентификатор пользователя, который отвественен за данное мероприятие",
            "nullable": False,
        },
    )

    def __repr__(self) -> str:
        return f"{self.title}"


class EventUser(Base):
    __tablename__ = "event_user"
    id = Column(
        Integer,
        primary_key=True,
        unique=True,
        nullable=False,
        comment="Уникальный индетификатор записи пользователя на мероприятие",
        doc="Уникальный индетификатор записи пользователя на мероприятие",
        info={
            "name": "id",
            "type": "integer",
            "description": "Уникальный индетификатор записи пользователя на мероприятие",
            "nullable": False,
            "unique": True,
            "primary_key": True,
        },
    )
    event_id = Column(
        ForeignKey("event.id"),
        nullable=False,
        comment="Идентификатор мероприятия, на которое записан пользователь",
        doc="Идентификатор мероприятия, на которое записан пользователь",
        info={
            "name": "event_id",
            "type": "integer",
            "description": "Идентификатор мероприятия, на которое записан пользователь",
            "nullable": False,
        },
    )
    user_id = Column(
        ForeignKey("user.id"),
        nullable=False,
        comment="Идентификатор пользователя, который записан на мероприятие",
        doc="Идентификатор пользователя, который записан на мероприятие",
        info={
            "name": "user_id",
            "type": "integer",
            "description": "Идентификатор пользователя, который записан на мероприятие",
            "nullable": False,
        },
    )


GENDERS = ["мужчина", "женщина"]

ROLES = ["пользователь" "организатор" "жюри", "модератор"]