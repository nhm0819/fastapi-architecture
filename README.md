# FastAPI Architecture

### Run server

```shell
# for serve
uvicorn --host 0.0.0.0 --port 8000 app.main:app

# for debug
python main.py
```

### Run test codes

```shell
pytest tests
```

### Run coverage

```shell
coverage run -m pytest
coverage html
```
