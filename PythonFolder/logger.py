import logging

# Set up logging configuration
logging.basicConfig(level=logging.DEBUG, filename='app.log', filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')

class Logger:
    @staticmethod
    def log_message(error_code, extra_info=None):
        """Logs messages based on an error code and optional extra information."""
        messages = {
            201: "No error - operation successful.",
            204: "No error - operation successful.",
            304: "Docker image already in requested state.",
            400: "Bad parameter - a provided parameter is incorrect.",
            404: "No such image - specified Docker image does not exist.",
            406: "Impossible to attach - container not running.",
            409: "Conflict - conflicting state or request.",
            500: "Server error - internal server error occurred."
        }
        
        if error_code in messages:
            message = messages[error_code]
            if error_code == 201 or error_code == 204:
                logging.info(f"{message} {extra_info if extra_info else ''}")
            elif error_code in {304, 400, 404, 406, 409, 500}:
                logging.error(f"{message} {extra_info if extra_info else ''}")
            else:
                logging.warning(f"Unhandled error code: {error_code} - {extra_info if extra_info else ''}")
        else:
            logging.warning(f"Unknown error code: {error_code} - {extra_info if extra_info else ''}")

    @staticmethod
    def info(message):
        """Log an informational message."""
        logging.info(message)

    @staticmethod
    def error(message):
        """Log an error message."""
        logging.error(message)
