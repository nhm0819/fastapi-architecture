import logging.config

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.server:app",
        host="127.0.0.1",
        port=8000,
        log_level="debug",
        reload=True,
    )
