## WinAppDriver Notepad Automation

This repository contains a small Python example that launches the **Windows Notepad** app, types some sample text, and closes it without saving. It now uses **WinAppDriver** (Microsoft's official Windows Application Driver) together with Selenium 3.

### What the script does
- checks whether `WinAppDriver.exe` is already running and starts it from the default installation path if needed
- opens Notepad (`C:\Windows\System32\notepad.exe`)
- types `Hello, WinAppDriver!`
- waits briefly so you can see the text
- clicks **Don't save** on the close dialog and quits the session

### Prerequisites
- Windows 10/11 with Developer Mode enabled
- Python 3.8 or newer (the repo currently uses Python 3.13 in a virtual environment)
- [WinAppDriver 1.2.99](https://github.com/microsoft/WinAppDriver/releases) installed to `C:\Program Files (x86)\Windows Application Driver\WinAppDriver.exe`

### Setup
1. (Optional) Create and activate a virtual environment.
2. Install the Python dependencies:
	```powershell
	pip install -r requirements.txt
	```

### Running the automation
1. Start `WinAppDriver.exe` (or let the script start it automatically).
2. Run the script from the repository root:
	```powershell
	python winium.py
	```

### Customising
- Update `desired_caps["app"]` in `winium.py` if you want to automate a different executable.
- Use **Inspect.exe** or **Accessibility Insights** to discover automation properties for additional controls and adjust the Selenium locators accordingly.

### Author
Paul Olphert

