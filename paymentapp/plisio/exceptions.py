import requests
from requests import JSONDecodeError


class PlisioException(Exception):
    """
    Plisio Exception.
    """


class PlisioAPIException(PlisioException):
    """
    Plisio Exception.
    """

    def __init__(self, response: requests.Response):
        """
        Constructor.

        Args:
            response (Response): Response.
        """
        self.code = 0
        self.name = ""

        try:
            json_res = response.json()
        except JSONDecodeError:
            self.message = f"Invalid JSON error message from Plisio: {response.text}"
        else:
            data = json_res["data"]
            self.code = data["code"]
            self.message = data["message"]
            self.name = data["name"]

        self.response = response
        self.status_code = response.status_code
        self.request = getattr(response, "request", None)

    def __str__(self) -> str:
        """
        String representation.

        Returns:
            str: String representation.
        """

        return f"APIError(code={self.code}, name={self.name}): {self.message}"


class PlisioRequestException(PlisioException):
    """
    Plisio Request Exception.
    """

    def __init__(self, message: str):
        """
        Constructor.

        Args:
            message (str): Message.
        """

        self.message = message

    def __str__(self) -> str:
        """
        String representation.

        Returns:
            str: String representation.
        """

        return f"PlisioRequestException: {self.message}"
