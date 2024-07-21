import os
import time
import datetime
from data.console.colors import Colors

class Variables:
    """
    A class for managing global variables used in the application.

    Attributes:
        None
    """

    global start_time, logger_time

    start_time = time.time()
    logger_time = datetime.datetime.now().strftime("%H:%M:%S")


class Logger:
    """
    A class for logging status messages to the console.

    Attributes:
        None

    Methods:
        __client_logger__(status): Log a status message to the console.
    """

    @staticmethod
    def __client_logger__(status: str, file_name: str = "programm.log", path: str = "./logs") -> None:
        """
        Log a status message to the console and write it to a file.

        Args:
            status (str): The status message to be logged.
            file_name (str): The name of the file to write the status message. Defaults to "programm.log".
            path (str): The path to the directory where the file should be saved. Defaults to the current directory.

        Returns:
            None
        """
        # Format the logger time
        logger_time = datetime.datetime.now().strftime("%H:%M:%S")
        
        # Create the log message
        log_message = f"{Colors.time}{logger_time}{Colors.reset} {Colors.logger}__{Logger.__client_logger__}__{Colors.reset}{Colors.foreground} | {status} {Colors.reset}"
        print(log_message)

        # Ensure the directory exists
        if not os.path.exists(path):
            os.makedirs(path)

        # Write to the log file
        with open(os.path.join(path, file_name), 'a') as file:
            file.write(f"__{Logger.__client_logger__}__ | {status}" + '\n')
