from data.console.colors import Colors

class Variables:
    """
    A class used to store program metadata and banner.

    Attributes:
    ----------
    __owner : str
        The owner of the program.
    __version : str
        The version of the program.
    __repo : str
        The github repository of the program.
    banner : str
        The banner displayed for the program.
    """
    __owner     = "oromos" 
    __version   = "1.0.1" 
    __repo      = "github.com/RootkitWizzrds" 
    banner      = f"""{Colors.foreground}
   _______________                                                   |*\\_/*|________
  |  ___________  |                   .-.     .-.                   ||_/-\\_|______  |
  | |           | |                  .****. .****.                  | |           | |
  | |   0   0   | |                  .*****.*****.                  | |   0   0   | |
  | |     -     | |                   .*********.                   | |     -     | |
  | |   /---\\   | |                    .*******.                    | |   \\___/   | |                 Author.....: {__owner}
  | |___     ___| |                     .*****.                     | |___________| |                 Version....: {__version}
  |_____|\\_/|_____|                      .***.                      |_______________|                 Repo.......: {__repo}
    _|__|/ \\|_|_...........................*..........................._|________|_
   / ********** \\                                                     / ********** \\
 /  ************  \\                     XS?SCAN                     /  ************  \\
 --------------------                                              --------------------
{Colors.reset}
    """


class DisplayBanner:
    """
    A class used to display the program banner.

    Methods:
    -------
    show():
        Prints the banner from the Variables class.
    """
    @staticmethod
    def show():
        """
        Prints the program banner stored in the Variables class.
        """
        print(Variables.banner)
