from app.database import Base, engine, SessionLocal
from app.models import User
from app.utils import hash_password

Base.metadata.create_all(bind=engine)

db = SessionLocal()
users = [
    User(username="admin", password=hash_password("admin"), role="admin", email="admin@test"),
    User(username="manager1", password=hash_password("manager1"), role="manager", email="manager1@test"),
    User(username="manager2", password=hash_password("manager2"), role="manager", email="manager2@test"),
    User(username="user1", password=hash_password("user1"), role="user", email="user1@test"),
    User(username="user2", password=hash_password("user2"), role="user", email="user2@test"),
    User(username="user3", password=hash_password("user3"), role="user", email="user3@test"),
    User(username="user4", password=hash_password("user4"), role="user", email="user4@test"),
    User(username="user5", password=hash_password("user5"), role="user", email="user5@test"),
]

db.add_all(users)
db.commit()
db.close()
