import os
from modules.logger.log import Logger

class ExitConsole:
    """
    A utility class to handle the console exit operations.
    """
    
    @staticmethod
    def exit() -> None:
        """
        Exits the Python interpreter immediately without 
        performing any cleanup actions.

        This method uses os._exit(0) to terminate the process 
        with an exit status of 0, which usually means a 
        successful termination.
        """
        Logger.__client_logger__('Exiting the program')
        os._exit(0)
