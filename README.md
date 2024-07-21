 <div align="center"> <h1> XSS Scanner </h1> </div>

<br />
<div align="center">
  <a href="https://github.com/RootkitWizzrds/XsScan">
    <img src="https://github.com/user-attachments/assets/50a58baa-068a-45eb-8049-f082723a0144" alt="Logo" width="100" height="100">
  </a>

  <h3 align="center">XSS Scanner</h3>

  <p align="center">
    Identify XSS vulnerabilities with ease
    <br />
    <a href="https://github.com/RootkitWizzrds/XsScan"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/RootkitWizzrds/XsScan#usage">View Demo</a>
    ·
    <a href="https://github.com/RootkitWizzrds/XsScan/issues">Report Bug</a>
    ·
    <a href="https://github.com/RootkitWizzrds/XsScan/issues">Request Feature</a>
  </p>
</div>

![image](https://github.com/user-attachments/assets/f81cd124-a53e-40bb-91b3-ec9b895d4b56)


Welcome to the XSS Scanner! This tool helps automate the detection of Cross-Site Scripting (XSS) vulnerabilities in web applications. By leveraging Selenium WebDriver and customizable payloads, it simplifies the process of finding XSS vulnerabilities.

## Table of Contents

- [Documentation](#documentation)
- [How It Works](#how-it-works)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Documentation

The XSS Scanner provides a comprehensive solution for identifying potential XSS vulnerabilities in web applications.

### Classes and Methods

- **`SimpleXSSScanner`**: The main class responsible for performing the XSS scan. It takes configuration parameters like `driver_path`, `chrome_path`, `method`, and more.
- **`Logger`**: Handles logging of various events and results during the scanning process.

For more details, refer to the [source code](path/to/your/source/code).

## How It Works

1. **Initialization**: The `SimpleXSSScanner` class is initialized with the target URL, HTTP method, and other configurations.
2. **Payload Execution**: The scanner uses Selenium WebDriver to navigate to the target URL and inject various XSS payloads.
3. **Detection**: The tool monitors for XSS vulnerabilities by checking for JavaScript alerts or other indicators of a successful XSS attack.
4. **Logging**: The process and results are logged for further analysis.

## Installation

To install the XSS Scanner, follow these steps:

1. **Clone the Repository**:

    ```bash
    git clone https://github.com/RootkitWizzrds/XsScan.git
    ```

2. **Navigate to the Project Directory**:

    ```bash
    cd xss-scanner
    ```

3. **Install the Required Modules**:

    Install the required Python modules using pip:

    ```bash
    pip install -r prerequisites/modules.txt
    ```

4. **Download the ChromeDriver** and place it in the `driver/` directory.

## Configuration

### `scanner.py`

The `SimpleXSSScanner` class is used to perform XSS scanning. You can configure it with:

- `driver_path`: Path to the ChromeDriver executable.
- `chrome_path`: (Optional) Path to the Chrome binary.
- `method`: HTTP method to use ("GET" or "POST").
- `data`: (Optional) Data to be sent in POST requests.
- `headless`: Whether to run Chrome in headless mode.
- `disable_gpu`, `no_sandbox`, `disable_dev_shm_usage`: Chrome options for restricted environments.
- `save_file`: (Optional) File path to save the results.
- `timeout_alert`: Timeout for waiting for alerts.
- `max_payload_size`: Maximum size of the payload to test.
- `waf`: Whether to apply WAF bypass techniques.

### `main.py`

Run the scanner with command-line arguments to configure the scan:

- `-u`, `--url`: Target URL with `{fuzz}` placeholder.
- `-p`, `--payloads`: Path to the file containing XSS payloads.
- `-d`, `--driver`: Path to the Chrome WebDriver executable.
- `-m`, `--method`: HTTP method to use ("GET" or "POST").
- `-j`, `--json`: (Optional) JSON data to send with POST requests.
- `-t`, `--timeout-alert`: Timeout duration for waiting for alerts.
- `-hh`, `--headless`: Run Chrome in headless mode.
- `-sf`, `--save-file`: (Optional) Path to save the found XSS payloads.
- `-dg`, `--disable-gpu`: Disable GPU hardware acceleration.
- `-ns`, `--no-sandbox`: Disable sandboxing.
- `-ds`, `--disable-dev-shm-usage`: Overcome limited resource problems.
- `--waf`: Apply WAF bypass techniques to payloads.

## Usage

To run the scanner, use the command line interface:

```bash
python main.py -u "http://example.com?search={fuzz}" -p "payloads/xss.txt" -d "driver/chromedriver" -m "GET" -j '{"param": "value"}' -t 5 -hh -sf "results.txt" 
```

## Example 

To create a simple scan using default settings:

```bash
python main.py -u "http://example.com?search={fuzz}" -p "payloads/xss.txt" -d "driver/chromedriver" -m "GET" -t 5 -hh --waf
```

## Contributing

We welcome contributions to improve the Project Structure Generator! To contribute:

1. **Fork the Repository**.
2. **Create a Feature Branch**.
3. **Commit Your Changes**.
4. **Push to the Branch**.
5. **Open a Pull Request**.

Please ensure your code adheres to the project's coding standards and includes appropriate tests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
