import uuid
import datetime
import random
from dataclasses import dataclass, field


@dataclass
class User:
    name: str
    id: str = field(default_factory=lambda: uuid.uuid4().hex)


@dataclass
class Category:
    name: str
    id: str = field(default_factory=lambda: uuid.uuid4().hex)


@dataclass
class Record:
    user_id: str
    category_id: str
    created: str
    sum: int
    id: str = field(default_factory=lambda: uuid.uuid4().hex)


def generate_users(names):
    for name in names:
        new_user = User(name)
        yield new_user.id, new_user


def generate_categories(categories):
    for category in categories:
        new_category = Category(category)
        yield new_category.id, new_category


def generate_records(users, categories):
    for user in list(users):
        for category in list(categories):
            sum = random.randint(0, 200)
            created = datetime.datetime(2023, 12,
                                        random.randint(1, 31),
                                        random.randint(0, 23),
                                        random.randint(0, 59),
                                        0)
            record = Record(user.id, category.id, created=str(created), sum=sum)
            yield record.id, record


users = dict(generate_users(["Mikhail", "Andriy", "Den", "David"]))
categories = dict(generate_categories(["Products", "Clothes", "Technologies"]))
records = dict(generate_records(users.values(), categories.values()))
