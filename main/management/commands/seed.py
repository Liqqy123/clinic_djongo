from django.core.management.base import BaseCommand
from main.models import Specialization, Doctor


class Command(BaseCommand):
    help = 'Заполняет базу данных'

    def handle(self, *args, **kwargs):
        # Очищаем
        Specialization.objects.all().delete()
        Doctor.objects.all().delete()

        # Специализации
        specs = {}
        for name in ['Терапевт', 'Кардиолог', 'Невролог', 'Хирург', 'Педиатр']:
            spec = Specialization(name=name)
            spec.save()  # slug сгенерируется автоматически
            specs[name] = spec
            self.stdout.write(f'✓ {name}')

        # Врачи
        doctors = [
            ('Иван Петров', 'Терапевт', 15),
            ('Анна Сидорова', 'Кардиолог', 12),
            ('Михаил Иванов', 'Невролог', 8),
            ('Елена Смирнова', 'Хирург', 20),
            ('Дмитрий Козлов', 'Педиатр', 10),
        ]

        for name, spec_name, exp in doctors:
            doctor = Doctor(
                name=name,
                specialization=specs[spec_name],
                experience=exp,
                bio=f'Врач {spec_name.lower()} с {exp} летним стажем'
            )
            doctor.save()
            self.stdout.write(f'✓ {name}')

        self.stdout.write(self.style.SUCCESS('База данных заполнена!'))