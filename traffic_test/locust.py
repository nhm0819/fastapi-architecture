import os
import uuid

import dotenv

dotenv.load_dotenv(dotenv_path=".env.locust", override=True)

from locust import HttpUser, between, events, tag, task

from tests.support.test_db_coordinator import TestDbCoordinator

HOST = "http://localhost:8000"
print("WRITER DB URL :", os.getenv("WRITER_DB_URL"))

test_db_coordinator = TestDbCoordinator()
test_db_coordinator.apply_alembic()
print("DB tables Created")


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    test_db_coordinator.truncate_all()


class AppUser(HttpUser):
    host = HOST
    wait_time = between(0.5, 3)

    def on_start(self):
        self.protocol = "http"
        self.size = 2048
        self.dtype = "float16"
        self.user_id = str(uuid.uuid4())
        body = {
            "email": f"{self.user_id}@id.e",
            "password1": "password",
            "password2": "password",
            "nickname": self.user_id,
            "favorite": "coding",
            "lat": 0,
            "lng": 0,
        }

        with self.client.post(
            "/api/v1/user",
            json=body,
            name="create user",
        ) as create_user_response:
            assert create_user_response.status_code == 200, "CREATE USER ERROR"
        print("Created User")

        with self.client.post(
            "/api/v1/user/login",
            name="login",
            json={"email": body["email"], "password": body["password1"]},
        ) as login_response:
            tokens = login_response.json()
            assert login_response.status_code == 200, "LOGIN ERROR"

        self.headers = {"Authorization": f"Bearer {tokens.get('access_token')}"}

        params = {
            "protocol": self.protocol,
            "size": self.size,
            "dtype": self.dtype,
        }
        with self.client.post(
            f"/api/v1/personalization/user",
            name="create user feature",
            headers=self.headers,
            catch_response=True,
            json=params,
        ) as response:
            data = response.json()
            assert response.status_code == 200

    @task
    def update_user_feature(self):
        print("update user feature start")
        params = {
            "protocol": self.protocol,
            "size": self.size,
            "dtype": self.dtype,
        }
        with self.client.patch(
            f"/api/v1/personalization/user",
            name="update user feature",
            catch_response=True,
            headers=self.headers,
            json=params,
        ) as response:
            data = response.json()
            assert response.status_code == 200
        print("Updatee feature")
