import os
import uuid

import dotenv
from locust import HttpUser, between, events, tag, task

from tests.support.test_db_coordinator import TestDbCoordinator

if os.path.exists(".env.locust"):
    dotenv.load_dotenv(dotenv_path=".env.locust", override=True)


HOST = os.getenv("HOST", "http://localhost:8000")


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
        self.protocol = "grpc"
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
            assert create_user_response.status_code == 200, create_user_response.text

        with self.client.post(
            "/api/v1/user/login",
            name="login",
            json={"email": body["email"], "password": body["password1"]},
        ) as login_response:
            tokens = login_response.json()
            assert login_response.status_code == 200, login_response.text

        self.headers = {"Authorization": f"Bearer {tokens.get('access_token')}"}

        params = {
            "protocol": self.protocol,
            "size": self.size,
            "dtype": self.dtype,
        }
        with self.client.post(
            f"/api/v1/personalization/user/octet",
            name="create user feature",
            headers=self.headers,
            catch_response=True,
            json=params,
        ) as response:
            assert response.status_code == 200, response.text

    @tag("http")
    @task
    def get_user_feature(self):
        params = {
            "protocol": self.protocol,
            "size": self.size,
            "dtype": self.dtype,
        }
        with self.client.get(
            f"/api/v1/personalization/user",
            name="get user feature",
            catch_response=True,
            headers=self.headers,
            json=params,
        ) as response:
            # data = response.json()
            assert response.status_code == 200, response.text

    @tag("http")
    @task
    def update_user_feature(self):
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
            # data = response.json()
            assert response.status_code == 200, response.text

    @tag("http-octet")
    @task
    def get_user_feature(self):
        params = {
            "protocol": "http-octet",
            "size": self.size,
            "dtype": self.dtype,
        }
        with self.client.get(
            f"/api/v1/personalization/user/octet",
            name="get user feature",
            catch_response=True,
            headers=self.headers,
            json=params,
        ) as response:
            # data = response.json()
            assert response.status_code == 200, response.text

    @tag("http-octet")
    @task
    def update_user_feature(self):
        params = {
            "protocol": "http-octet",
            "size": self.size,
            "dtype": self.dtype,
        }
        with self.client.patch(
            f"/api/v1/personalization/user/octet",
            name="update user feature",
            catch_response=True,
            headers=self.headers,
            json=params,
        ) as response:
            # data = response.json()
            assert response.status_code == 200, response.text
