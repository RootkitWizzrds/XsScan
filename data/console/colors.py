from cutepy import HEX

class Colors:
    """
    A class for defining color codes used for console output.

    Attributes:
        logger (str): The color code for logger output.
        time (str): The color code for logger time.
        foreground (str): The color code for foreground.
        reset (str): The color code to reset formatting.
    """

    green           = HEX.print("c5e2c4")
    logger          = HEX.print("350c98")
    time            = HEX.print("9e0063")
    foreground      = HEX.print("dddddd")
    reset           = HEX.reset