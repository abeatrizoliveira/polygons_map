# env para conexão com o postgres
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:123@localhost:5432/areas_db",
)
