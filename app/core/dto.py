from fastapi.responses import Response


class OctetStreamResponse(Response):
    media_type = "application/octet-stream"
