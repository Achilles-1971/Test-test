from django.core. management.base import BaseCommand
from models.models import Base, Role
from models.config import session
from sqlalchemy.sql import select
class Command(BaseCommand):
    help = "Эта команда создает таблицы в базе данных"
    def handle(self, *args, **options):
        try:
            Base. metadata.create_all(session.get_bind())
            # Создаем роли
            roles_sql_row = select(Role)
            roles = session.scalars(roles_sql_row).all()
            if len(roles) == 0:
                roles = [
                    Role(name="пользователь"),
                    Role(name="организатор"),
                    Role(name="жюри"),
                    Role(name="модератор"),
                ]
                # Сохраняем роли в базу данных
                session.add_all(roles)
                session.commit()
            self.stdout.write(self.style.SUCCESS("Таблицы успешно созданы!"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Ошибка при создании таблиц: {e}"))