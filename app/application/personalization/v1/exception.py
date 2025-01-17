from app.core.exceptions import CustomException


class EmbeddingException(CustomException):
    code = 404
    error_code = "Embedding_Server Error"
    message = "Embedding Server Error"
