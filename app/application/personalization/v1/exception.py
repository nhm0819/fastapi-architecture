from app.core.exceptions import CustomException


class EmbeddingException(CustomException):
    code = 404
    error_code = "Embedding_Server Error"
    message = "Embedding Server Error"


class UserFeatureNotFoundException(CustomException):
    code = 404
    error_code = "USER_FEATURE__NOT_FOUND"
    message = "user feature not found"


class UserFeatureAlreadyExistException(CustomException):
    code = 404
    error_code = "USER_FEATURE__EXIST"
    message = "user feature is already exists"
