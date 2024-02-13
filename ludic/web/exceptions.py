from starlette.exceptions import HTTPException


class ClientError(HTTPException):
    def __init__(
        self,
        detail: str = "Client Error",
        headers: dict[str, str] | None = None,
        status_code: int = 400,
    ) -> None:
        super().__init__(status_code=status_code, detail=detail, headers=headers)


class BadRequestError(ClientError):
    def __init__(
        self,
        detail: str = "Bad Request",
        headers: dict[str, str] | None = None,
    ) -> None:
        super().__init__(status_code=400, detail=detail, headers=headers)


class UnauthorizedError(ClientError):
    def __init__(
        self,
        detail: str = "Unauthorized",
        headers: dict[str, str] | None = None,
    ) -> None:
        super().__init__(status_code=401, detail=detail, headers=headers)


class PaymentRequiredError(ClientError):
    def __init__(
        self,
        detail: str = "Payment Required",
        headers: dict[str, str] | None = None,
    ) -> None:
        super().__init__(status_code=402, detail=detail, headers=headers)


class ForbiddenError(ClientError):
    def __init__(
        self,
        detail: str = "Forbidden",
        headers: dict[str, str] | None = None,
    ) -> None:
        super().__init__(status_code=403, detail=detail, headers=headers)


class NotFoundError(ClientError):
    def __init__(
        self,
        detail: str = "Not Found",
        headers: dict[str, str] | None = None,
    ) -> None:
        super().__init__(status_code=404, detail=detail, headers=headers)


class MethodNotAllowedError(ClientError):
    def __init__(
        self,
        detail: str = "Method Not Allowed",
        headers: dict[str, str] | None = None,
    ) -> None:
        super().__init__(status_code=405, detail=detail, headers=headers)


class TooManyRequestsError(ClientError):
    def __init__(
        self,
        detail: str = "Too Many Requests",
        headers: dict[str, str] | None = None,
    ) -> None:
        super().__init__(status_code=429, detail=detail, headers=headers)


class ServerError(HTTPException):
    def __init__(
        self,
        detail: str = "Server Error",
        headers: dict[str, str] | None = None,
        status_code: int = 500,
    ) -> None:
        super().__init__(status_code=status_code, detail=detail, headers=headers)


class InternalServerError(ServerError):
    def __init__(
        self,
        detail: str = "Internal Server Error",
        headers: dict[str, str] | None = None,
    ) -> None:
        super().__init__(status_code=500, detail=detail, headers=headers)


class NotImplementedError(ServerError):
    def __init__(
        self,
        detail: str = "Not Implemented",
        headers: dict[str, str] | None = None,
    ) -> None:
        super().__init__(status_code=501, detail=detail, headers=headers)


class BadGatewayError(ServerError):
    def __init__(
        self,
        detail: str = "Bad Gateway",
        headers: dict[str, str] | None = None,
    ) -> None:
        super().__init__(status_code=502, detail=detail, headers=headers)


class ServiceUnavailableError(ServerError):
    def __init__(
        self,
        detail: str = "Service Unavailable",
        headers: dict[str, str] | None = None,
    ) -> None:
        super().__init__(status_code=503, detail=detail, headers=headers)


class GatewayTimeoutError(ServerError):
    def __init__(
        self,
        detail: str = "Gateway Timeout",
        headers: dict[str, str] | None = None,
    ) -> None:
        super().__init__(status_code=504, detail=detail, headers=headers)
