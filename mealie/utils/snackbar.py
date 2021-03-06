class SnackResponse:
    @staticmethod
    def _create_response(message: str, type: str, additional_data: dict = None) -> dict:

        snackbar = {"snackbar": {"text": message, "type": type}}

        if additional_data:
            snackbar.update(additional_data)

        return snackbar

    @staticmethod
    def success(message: str, additional_data: dict = None) -> dict:
        return SnackResponse._create_response(message, "success", additional_data)

    @staticmethod
    def info(message: str, additional_data: dict = None) -> dict:
        return SnackResponse._create_response(message, "info", additional_data)

    @staticmethod
    def warning(message: str, additional_data: dict = None) -> dict:
        return SnackResponse._create_response(message, "warning", additional_data)

    @staticmethod
    def error(message: str, additional_data: dict = None) -> dict:
        return SnackResponse._create_response(message, "error", additional_data)
