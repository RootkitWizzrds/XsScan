import sys
import subprocess
from x64.system.detect import SystemDetection
from modules.logger.log import Logger

class Connection:
    """
    A class for checking wifi connection status.
    """

    @staticmethod
    def check_wifi():
        """
        Check the status of the wifi connection.

        This method uses the appropriate command to determine the status of the wifi connection
        based on the operating system.
        If the command is not found, an error message is logged, and the program exits.
        If the wifi connection is inactive, a message is logged, and the program exits.
        If an active wifi connection is found, a message is logged.

        Note: This method is designed to run on a Linux, macOS, or Windows system with wireless support.

        Raises:
        - FileNotFoundError: If the command is not found.
        """
        try:
            os_type = SystemDetection.detect()

            def check_linux():
                try:
                    result = subprocess.run(['nmcli'], capture_output=True, text=True)
                    output = result.stdout.strip()
                    if 'connected to' in output:
                        Logger.__client_logger__("Active wifi connection found")
                    else:
                        Logger.__client_logger__("Make sure you have an active wifi connection")
                        sys.exit()
                except FileNotFoundError as e:
                    Logger.__client_logger__(f"Error: Command not found. {str(e)}")
                    sys.exit()

            def check_macos():
                try:
                    result = subprocess.run(['/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport', '-I'], capture_output=True, text=True)
                    output = result.stdout
                    if 'AirPort' in output and 'SSID:' in output:
                        Logger.__client_logger__("Active wifi connection found")
                    else:
                        Logger.__client_logger__("Make sure you have an active wifi connection")
                        sys.exit()
                except FileNotFoundError as e:
                    Logger.__client_logger__(f"Error: Command not found. {str(e)}")
                    sys.exit()

            def check_windows():
                result = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], capture_output=True, text=True)
                output = result.stdout
                if 'disconnected' in output.lower():
                    Logger.__client_logger__("Make sure you have an active wifi connection")
                    sys.exit()
                else:
                    Logger.__client_logger__("Active wifi connection found")

            def unsupported_os():
                Logger.__client_logger__("Unsupported operating system")
                sys.exit()

            os_cases = {
                "Linux": check_linux,
                "macOS": check_macos,
                "Windows": check_windows,
            }

            os_cases.get(os_type, unsupported_os)()

        except FileNotFoundError as e:
            Logger.__client_logger__(f"Error: Command not found. {str(e)}")
            sys.exit()
