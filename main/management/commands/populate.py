from faker import Faker
from main.models import Doctor

fake = Faker()
populator = Faker.getPopulator()
populator.addEntity(Doctor, 5)
insertedPks = populator.execute()
