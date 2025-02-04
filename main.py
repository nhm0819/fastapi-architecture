import uvicorn

import directories

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        log_level="debug",
        reload=True,
        log_config="log_conf.yaml",
    )
