import getpass
import uuid

from werkzeug.security import generate_password_hash

from database import execute, fetch_one
from validators import password


def create_demo_user(user_password):
    user_email = "demo@washworld.invalid"
    if fetch_one("SELECT user_id FROM users WHERE email = %s", (user_email,)):
        raise ValueError("Demo user already exists; its password has not been changed.")

    validated_password = password({"password": user_password})
    execute(
        """
        INSERT INTO users (
            user_id, first_name, email, password_hash, license_plate, location_id, plan_id
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
        (
            uuid.uuid4().hex,
            "Docker Demo",
            user_email,
            generate_password_hash(validated_password),
            "DE 12345",
            1,
            1,
        ),
    )
    return user_email


if __name__ == "__main__":
    chosen_password = getpass.getpass("Choose a demo password (at least 8 characters): ")
    try:
        print(f"Demo account created: {create_demo_user(chosen_password)}")
    except ValueError as error:
        print(error)
        raise SystemExit(1)
