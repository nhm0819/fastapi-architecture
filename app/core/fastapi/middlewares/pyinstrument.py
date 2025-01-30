from pyinstrument import Profiler
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from directories import profiles_api


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
