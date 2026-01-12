from .database import SessionLocal
from .models import User
from .auth import get_password_hash

db = SessionLocal()

admin = User(
    username="admin",
    email="admin@admin.com",
    password=get_password_hash("admin123"),
    role="admin"
)

db.add(admin)
db.commit()
db.close()

print("Admin criado com sucesso")