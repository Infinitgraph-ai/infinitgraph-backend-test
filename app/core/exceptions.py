import typing

from fastapi import Request, status
from fastapi.responses import JSONResponse


class BackendError(Exception):
    """
        Exception for Backend errors with JSEND adaptation.
    """

    def __init__(
        self,
        *,
        status,
        data = None,
        message: str,
        code: int = status.HTTP_400_BAD_REQUEST,
    ) -> None:
        """
        Initializer for BackException.
        """
        self.status = status
        self.data = data
        self.message = message
        self.code = code

    def __repr__(self) -> str:
        """Representation for BackendException."""
        return (
            f'{self.__class__.__name__}(status={self.status}, data={self.data}, message="{self.message}", '
            f"code={self.code})"
        )

    def __str__(self) -> str:
        """String representation for BackendException."""
        return self.__repr__()

    def dict(self) -> dict[str, typing.Any]:
        """Converts BackendException to python dict. Actually used to wrap JSEND response."""
        return {
            "status": self.status,
            "data": self.data,
            "message": self.message,
            "code": self.code,
        }


def backend_exception_handler(request: Request, exc: BackendError) -> JSONResponse:
    """Handler for BackendException.

    Args:
        request (Request): FastAPI Request instance.
        exc (BackendError): Error that Back-end raises.

    Returns:
        result (ORJSONResponse): Transformed JSON response from Back-end exception.
    """
    return JSONResponse(content=exc.dict(), status_code=exc.code)
