from django.core. management.base import BaseCommand
from models.models import Base, Role
from models.config import session
class Command(BaseCommand):
    help = "Эта команда создает таблицы в базе данных"
    def handle(self, *args, **options):
        try:
            Base. metadata.create_all(session.get_bind())
            # Создаем роли
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