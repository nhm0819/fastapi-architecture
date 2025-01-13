from app.core.exceptions import CustomException


def test_custom_exception():
    # Given
    message = "hongmin"

    # When
    exc = CustomException(message=message)

    # Then
    assert exc.message == message
