import os
import urllib.parse
from typing import Optional, List
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoAlertPresentException,
    WebDriverException,
    TimeoutException,
)
from modules.logger.log import Logger
from data.console.colors import Colors

class SimpleXSSScanner:
    """
    A class to perform simple XSS (Cross-Site Scripting) scanning using Selenium WebDriver.

    Attributes:
        driver_path (str): Path to the ChromeDriver executable.
        chrome_path (Optional[str]): Path to the Chrome binary.
        method (str): HTTP method to use ("GET" or "POST").
        data (Optional[str]): Data to be sent in POST requests.
        save_file (Optional[str]): File path to save the results.
        timeout_alert (float): Timeout for waiting for alerts.
        max_payload_size (int): Maximum size of the payload to test.
        waf (bool): Whether to apply WAF (Web Application Firewall) bypass techniques.
        options (Options): Selenium Chrome options.
        service (Service): Selenium ChromeDriver service.
        driver (webdriver.Chrome): Selenium WebDriver instance.
    """
    
    def __init__(
        self,
        driver_path: str,
        chrome_path: Optional[str] = None,
        method: str = "GET",
        data: Optional[str] = None,
        headless: bool = False,
        disable_gpu: bool = True,
        no_sandbox: bool = True,
        disable_dev_shm_usage: bool = True,
        save_file: Optional[str] = None,
        timeout_alert: float = 3.0,
        max_payload_size: int = 1000,
        waf: bool = False,
    ) -> None:
        """
        Initializes the SimpleXSSScanner with the provided configuration.

        Args:
            driver_path (str): Path to the ChromeDriver executable.
            chrome_path (Optional[str]): Path to the Chrome binary.
            method (str): HTTP method to use ("GET" or "POST").
            data (Optional[str]): Data to be sent in POST requests.
            headless (bool): Whether to run Chrome in headless mode.
            disable_gpu (bool): Whether to disable GPU hardware acceleration.
            no_sandbox (bool): Whether to disable sandboxing.
            disable_dev_shm_usage (bool): Whether to disable /dev/shm usage.
            save_file (Optional[str]): File path to save the results.
            timeout_alert (float): Timeout for waiting for alerts.
            max_payload_size (int): Maximum size of the payload to test.
            waf (bool): Whether to apply WAF bypass techniques.
        """
        self.driver_path = driver_path
        self.chrome_path = chrome_path
        self.method = method
        self.data = data
        self.save_file = save_file
        self.timeout_alert = timeout_alert
        self.max_payload_size = max_payload_size
        self.waf = waf
        self.options = Options()
        if headless:
            self.options.add_argument("--headless")
        if disable_gpu:
            self.options.add_argument("--disable-gpu")
        if no_sandbox:
            self.options.add_argument("--no-sandbox")
        if disable_dev_shm_usage:
            self.options.add_argument("--disable-dev-shm-usage")
        if chrome_path:
            self.options.binary_location = chrome_path
        self.service = Service(executable_path=self.driver_path)
        self.driver = webdriver.Chrome(service=self.service, options=self.options)

    def apply_waf_bypass_techniques(self, payload: str) -> List[str]:
        """
        Applies various WAF (Web Application Firewall) bypass techniques to the payload.

        Args:
            payload (str): The original XSS payload.

        Returns:
            List[str]: A list of payloads with WAF bypass techniques applied.
        """
        bypass_payloads = [
            payload,
            urllib.parse.quote(payload),  # URL encode
            urllib.parse.quote_plus(payload),  # URL encode with plus
            ''.join(['%{0:0>2}'.format(format(ord(char), 'x')) for char in payload]),  # Double URL encode
            payload.replace('<', '&lt;').replace('>', '&gt;'),  # HTML entity encoding
            payload.lower(),  # Lowercase
            payload.upper(),  # Uppercase
            payload[::-1],  # Reverse string
            payload.replace('script', 'sc<script>ript'),  # Keyword splitting
        ]
        return bypass_payloads

    def check_for_and_handle_alert(self):
        """
        Checks for and dismisses any present alert in the browser.
        """
        try:
            alert = Alert(self.driver)
            alert.dismiss()
        except NoAlertPresentException:
            pass  # No alert to handle

    def cleanup(self) -> None:
        """
        Quits the WebDriver and cleans up resources.
        """
        if self.driver:
            self.driver.quit()

    def run(self, url: str, payloads: List[str]) -> None:
        """
        Executes the XSS scan by testing various payloads on the provided URL.

        Args:
            url (str): The target URL with a placeholder for payload injection.
            payloads (List[str]): A list of XSS payloads to test.
        """
        self.check_for_and_handle_alert()  # Ensure no existing alert interferes

        found_xss = []
        for payload in payloads:
            if len(payload) > self.max_payload_size:
                Logger.__client_logger__(f"Payload too large and skipped: {payload}")
                continue

            if self.waf:
                bypass_payloads = self.apply_waf_bypass_techniques(payload)
            else:
                bypass_payloads = [payload]

            for bypass_payload in bypass_payloads:
                test_url = url.format(fuzz=bypass_payload)
                try:
                    if self.method.upper() == "GET":
                        self.driver.get(test_url)
                    elif self.method.upper() == "POST":
                        self.driver.execute_script(f"""
                            var xhr = new XMLHttpRequest();
                            xhr.open('POST', '{url}', true);
                            xhr.setRequestHeader('Content-Type', 'application/json');
                            xhr.send(JSON.stringify({self.data}));
                        """)

                    WebDriverWait(self.driver, self.timeout_alert).until(
                        EC.alert_is_present()
                    )
                    alert = Alert(self.driver)
                    alert_text = alert.text
                    found_xss.append((test_url, alert_text))
                    Logger.__client_logger__(
                        f"{Colors.green}DETECTED{Colors.reset} | {test_url} | Alert Text: {alert_text}"
                    )
                    alert.accept()  # Accept the alert after detection
                    if self.save_file:
                        with open(self.save_file, "a+") as file:
                            file.write(
                                f"| URL: \n|    -> {test_url}\n| Alert Text: \n|    -> {alert_text}\n\n"
                            )
                except NoAlertPresentException:
                    Logger.__client_logger__(f"No alert present for payload: {payload}")
                except TimeoutException:
                    Logger.__client_logger__(
                        f"Timeout waiting for alert with payload: {payload}"
                    )
                except WebDriverException as e:
                    if "unexpected alert open" in str(e):
                        Logger.__client_logger__(
                            f"Unexpected alert detected with payload: {payload}. Handling the alert."
                        )
                        self.check_for_and_handle_alert()  # Attempt to handle unexpected alerts
                    else:
                        Logger.__client_logger__(
                            f"WebDriverException for payload: {payload}. Details: {str(e)}"
                        )
                except Exception as e:
                    Logger.__client_logger__(
                        f"Error with payload: {payload}. Details: {str(e)}"
                    )

def run_scanner(
    url: str,
    payloads_file: str,
    driver_path: str,
    method: str = "GET",
    data: Optional[str] = None,
    chrome_path: Optional[str] = None,
    headless: bool = True,
    disable_gpu: bool = True,
    no_sandbox: bool = True,
    disable_dev_shm_usage: bool = True,
    save_file: Optional[str] = None,
    timeout_alert: int = 5,
    waf: bool = False,
) -> None:
    """
    Initializes and runs the XSS scanner with the provided configuration.

    Args:
        url (str): The target URL with a placeholder for payload injection.
        payloads_file (str): Path to the file containing XSS payloads.
        driver_path (str): Path to the ChromeDriver executable.
        method (str): HTTP method to use ("GET" or "POST").
        data (Optional[str]): Data to be sent in POST requests.
        chrome_path (Optional[str]): Path to the Chrome binary.
        headless (bool): Whether to run Chrome in headless mode.
        disable_gpu (bool): Whether to disable GPU hardware acceleration.
        no_sandbox (bool): Whether to disable sandboxing.
        disable_dev_shm_usage (bool): Whether to disable /dev/shm usage.
        save_file (Optional[str]): File path to save the results.
        timeout_alert (int): Timeout for waiting for alerts.
        waf (bool): Whether to apply WAF bypass techniques.
    """
    try:
        with open(payloads_file, "r") as file:
            payloads = [line.strip() for line in file]
    except Exception as e:
        Logger.__client_logger__(f"Failed to read payloads file: {str(e)}")
        return

    scanner = None
    try:
        scanner = SimpleXSSScanner(
            driver_path=driver_path,
            chrome_path=chrome_path,
            method=method,
            data=data,
            headless=headless,
            disable_gpu=disable_gpu,
            no_sandbox=no_sandbox,
            disable_dev_shm_usage=disable_dev_shm_usage,
            save_file=save_file,
            timeout_alert=timeout_alert,
            waf=waf,
        )
        scanner.run(url, payloads)
    except Exception as e:
        Logger.__client_logger__(f"An error occurred during scanning: {str(e)}")
    finally:
        if scanner:
            scanner.cleanup()
