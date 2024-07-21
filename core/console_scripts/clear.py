import os
from modules.logger.log import Logger
from x64.system.detect import SystemDetection

class ClearScreen:
    """
    A utility class for clearing the terminal screen.

    This class uses the SystemDetection class to detect the underlying operating system
    and clears the terminal screen accordingly.

    Methods:
        clear() -> None: Clear the terminal screen based on the detected operating system.

    Attributes:
        None
    """
    
    @staticmethod
    def clear() -> None:
        """
        Clear the terminal screen based on the detected operating system.

        This static method uses the SystemDetection class to detect the operating system
        and executes the appropriate command to clear the terminal screen.

        Returns:
            None
        """
        os_type = SystemDetection.detect()
        
        if os_type == "Linux" or os_type == "macOS":
            os.system('clear')
        elif os_type == "Windows":
            os.system('cls')
        else:
            Logger.__client_logger__("Unsupported operating system. Cannot clear the screen.")
