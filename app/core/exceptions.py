import typing

from fastapi import Request, status
from fastapi.responses import ORJSONResponse

from app.core.enums import JSENDStatus


class BackendError(Exception):
    """
        Exception for Backend errors with JSEND adaptation.
    """

    def __init__(
        self,
        *,
        status: JSENDStatus = JSENDStatus.FAIL,
        data = None,
        message: str,
        code: int = status.HTTP_400_BAD_REQUEST,
    ) -> None:
        """Initializer for BackException.

        Keyword Args:
            status (JSENDStatus): status for JSEND
            data: any detail or data for this exception.
            message (str): any text detail for this exception.
            code (int): HTTP status code or custom code from Back-end.
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
            "status": self.status.value if isinstance(self.status, JSENDStatus) else self.status,
            "data": self.data,
            "message": self.message,
            "code": self.code,
        }


def backend_exception_handler(request: Request, exc: BackendError) -> ORJSONResponse:
    """Handler for BackendException.

    Args:
        request (Request): FastAPI Request instance.
        exc (BackendError): Error that Back-end raises.

    Returns:
        result (ORJSONResponse): Transformed JSON response from Back-end exception.
    """
    return ORJSONResponse(content=exc.dict(), status_code=exc.code)
