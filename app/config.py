import enum

SQLALCHEMY_DATABASE_URL = "sqlite:///./tasks.db"

SECRET_KEY = "secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


TOKEN_TYPE = "bearer"


class Role(str, enum.Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"


class TaskStatus(str, enum.Enum):
    TODO = "TODO"
    IN_PROGRESS = "In Progress"
    DONE = "Done"


class TaskPriority(str, enum.Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
