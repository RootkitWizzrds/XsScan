# main.py

import argparse
from typing import Optional
from modules.logger.log import Logger
from x64.network.alive import Connection
from data.banner.banner import DisplayBanner
from core.console_scripts.exit import ExitConsole
from core.console_scripts.clear import ClearScreen
from xsscan.scanner import run_scanner

class Worker:
    """
    A class to manage and execute the XSS scanning process.

    Attributes:
        url (str): Target URL with a placeholder for payload injection.
        payloads (str): Path to the file containing XSS payloads.
        driver (str): Path to the Chrome WebDriver executable.
        method (str): HTTP method to use ("GET" or "POST").
        data (Optional[str]): JSON data to send with POST requests.
        headless (bool): Whether to run Chrome in headless mode.
        disable_gpu (bool): Whether to disable GPU hardware acceleration.
        no_sandbox (bool): Whether to disable sandboxing.
        disable_dev_shm_usage (bool): Whether to disable /dev/shm usage.
        save_file (Optional[str]): Path to save the results.
        timeout_alert (int): Timeout for waiting for alerts.
        waf (bool): Whether to apply WAF bypass techniques.
    """
    
    def __init__(
        self,
        url: str,
        payloads: str,
        driver: str,
        method: str,
        data: Optional[str],
        headless: bool,
        disable_gpu: bool,
        no_sandbox: bool,
        disable_dev_shm_usage: bool,
        save_file: Optional[str],
        timeout_alert: int,
        waf: bool,
    ) -> None:
        """
        Initializes the Worker with the provided configuration.

        Args:
            url (str): Target URL with a placeholder for payload injection.
            payloads (str): Path to the file containing XSS payloads.
            driver (str): Path to the Chrome WebDriver executable.
            method (str): HTTP method to use ("GET" or "POST").
            data (Optional[str]): JSON data to send with POST requests.
            headless (bool): Whether to run Chrome in headless mode.
            disable_gpu (bool): Whether to disable GPU hardware acceleration.
            no_sandbox (bool): Whether to disable sandboxing.
            disable_dev_shm_usage (bool): Whether to disable /dev/shm usage.
            save_file (Optional[str]): Path to save the results.
            timeout_alert (int): Timeout for waiting for alerts.
            waf (bool): Whether to apply WAF bypass techniques.
        """
        self.url = url
        self.payloads = payloads
        self.driver = driver
        self.method = method
        self.data = data
        self.headless = headless
        self.disable_gpu = disable_gpu
        self.no_sandbox = no_sandbox
        self.disable_dev_shm_usage = disable_dev_shm_usage
        self.save_file = save_file
        self.timeout_alert = timeout_alert
        self.waf = waf

    def main(self) -> None:
        """
        Starts the XSS scanning process and logs the beginning of the operation.
        Calls the `run_scanner` function to perform the scanning.
        """
        Logger.__client_logger__("Starting XSS Scanner")
        run_scanner(
            self.url,
            self.payloads,
            self.driver,
            self.method,
            self.data,
            headless=self.headless,
            disable_gpu=self.disable_gpu,
            no_sandbox=self.no_sandbox,
            disable_dev_shm_usage=self.disable_dev_shm_usage,
            save_file=self.save_file,
            timeout_alert=self.timeout_alert,
            waf=self.waf,
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Simple XSS Scanner using Selenium WebDriver."
    )
    parser.add_argument(
        "-u",
        "--url",
        type=str,
        required=True,
        help="Target URL with {fuzz} placeholder.",
    )
    parser.add_argument(
        "-p", "--payloads", type=str, required=True, help="File path for XSS payloads."
    )
    parser.add_argument(
        "-d",
        "--driver",
        type=str,
        required=True,
        help="Path to the Chrome WebDriver executable.",
    )
    parser.add_argument(
        "-m", "--method", type=str, choices=["GET", "POST"], default="GET", help="HTTP method to use (default is GET)."
    )
    parser.add_argument(
        "-j", "--json", type=str, help="JSON data to send with POST requests."
    )
    parser.add_argument(
        "-t",
        "--timeout-alert",
        type=float,
        default=3.0,
        help="Timeout duration for waiting for alerts.",
    )
    parser.add_argument(
        "-hh", "--headless", action="store_true", help="Run Chrome in headless mode."
    )
    parser.add_argument(
        "-sf", "--save-file", type=str, help="Path to save the found XSS payloads."
    )
    parser.add_argument(
        "-dg",
        "--disable-gpu",
        action="store_true",
        help="Disable GPU hardware acceleration.",
    )
    parser.add_argument(
        "-ns", "--no-sandbox", action="store_true", help="Disable sandboxing."
    )
    parser.add_argument(
        "-ds",
        "--disable-dev-shm-usage",
        action="store_true",
        help="Overcome limited resource problems."
    )
    parser.add_argument(
        "--waf", action="store_true", help="Apply WAF bypass techniques to payloads."
    )
    args = parser.parse_args()

    try:
        ClearScreen.clear()
        DisplayBanner.show()
        Connection.check_wifi()
        worker = Worker(
            args.url,
            args.payloads,
            args.driver,
            args.method,
            args.json,
            headless=args.headless,
            disable_gpu=args.disable_gpu,
            no_sandbox=args.no_sandbox,
            disable_dev_shm_usage=args.disable_dev_shm_usage,
            save_file=args.save_file,
            timeout_alert=args.timeout_alert,
            waf=args.waf,
        )
        worker.main()
    except KeyboardInterrupt:
        ExitConsole.exit()
