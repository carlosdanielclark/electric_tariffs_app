import sqlite3
from decimal import Decimal
from infrastructure.repositories.sqlite_user_repository import SQLiteUserRepository
from infrastructure.repositories.sqlite_reading_repository import SQLiteReadingRepository
from application.services.reading_service import ReadingService, NewReading
from application.services.auth_service import AuthService

def test_record_reading_and_query() -> None:
    conn = sqlite3.connect(":memory:")
    user_repo = SQLiteUserRepository(connection=conn)
    user_repo.create_tables()
    reading_repo = SQLiteReadingRepository(connection=conn)
    reading_repo.create_tables()

    auth = AuthService(user_repo)
    user = auth.create_user(name="Reader", username="reader", password="pw")
    assert user.id is not None

    rs = ReadingService(reading_repo=reading_repo)
    reading = rs.record_reading(NewReading(user_id=user.id, lectura_actual=150.0, lectura_anterior=100.0))
    assert reading is not None
    assert reading.consumo == Decimal("50.0")

    items = rs.get_readings_for_user(user.id)
    assert len(items) >= 1
    assert items[0].consumo == Decimal("50.0")

def test_invalid_reading_raises() -> None:
    conn = sqlite3.connect(":memory:")
    user_repo = SQLiteUserRepository(connection=conn)
    user_repo.create_tables()
    reading_repo = SQLiteReadingRepository(connection=conn)
    reading_repo.create_tables()

    auth = AuthService(user_repo)
    user = auth.create_user(name="U", username="u1", password="p")
    assert user.id is not None

    rs = ReadingService(reading_repo=reading_repo)
    try:
        rs.record_reading(NewReading(user_id=user.id, lectura_actual=90.0, lectura_anterior=100.0))
        assert False, "Should have raised ValueError"
    except ValueError:
        pass