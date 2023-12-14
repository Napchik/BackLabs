import uuid
from dataclasses import dataclass, field


@dataclass
class User:
    name: str
    id: str = field(default_factory=lambda: uuid.uuid4().hex)


def generate_users(names):
    for name in names:
        new_user = User(name)
        yield new_user.id, new_user


users = dict(generate_users(["Mikhail", "Andriy", "Den", "David"]))
