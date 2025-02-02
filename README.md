# FastAPI Architecture

FastAPI code based on <https://github.com/teamhide/fastapi-boilerplate>

### Base Infra

```shell
# mysql, redis
docker compose up -f docker/docker-compose.yaml -d

# embedding dummy
git clone https://github.com/nhm0819/embedding-dummy.git
cd embedding-dummy

docker build -t embedding:v0.0 -f fastapi_app/Dockerfile .
docker build -t embedding-grpc:v0.0 -f grpc_app/Dockerfile .

docker compose up -d
```

### Install dependency

```shell
poetry shell
poetry install
```

### Apply alembic revision

```shell
alembic upgrade head
```

### Run API server

```shell
# API serving command
uvicorn --host 0.0.0.0 --port 8000 app.main:app

# debuggin run
python main.py
```

### Launch docker conatiner

```shell
docker build -t fastapi-arch:v0.0 -f ./docker/Dockerfile .
docker run -d --cpus 1 -p 8000:8000 --env-file .env --name fastapi-arch fastapi-arch:v0.0
```

### Run test codes

```shell
# pytest run
pytest tests

# if you want pytest report
pip install pytest-html
pytest tests --html=./pytest-report.html
```

Go to `pytest.ini` file to add pytest options.
Default option, you can edit test environment variables in `.env.test`.
After pytest, pyinstrument results saved in `./profiling` folder.

### profiling

If you add environment `PROFILING=True`, pyinstrument middleware will append.
Refer PyInstrumentMiddleWare class in `app\core\fastapi\middlewares\pyinstrument.py`.
When you request to API with `profile=true` query, profile report file will save.

```python
class PyInstrumentMiddleWare(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        if request.query_params.get("profile", False):
            profiler = Profiler(interval=0.001, async_mode="enabled")
            profiler.start()
            response = await call_next(request)
            profiler.stop()
            # Write result to html file
            profiler.write_html(
                profiles_api.joinpath(f"{request.url.path}_profile.html")
            )
            return response
        else:
            return await call_next(request)

```

### Run coverage

```shell
coverage run -m pytest
coverage html
```

### locust (stress test)

```shell
locust -f traffic_test/locustfile.py [--tags]
```
