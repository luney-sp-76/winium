from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.options import BaseOptions
import time
import subprocess
import os
import psutil

# Get the current working directory
root = os.getcwd()

# Function to check if a process is running
def check_if_process_running(process_name):
    try:
        # Iterate over all running processes
        for proc in psutil.process_iter():
            try:
                # Extract process name
                process = proc.name()
                if process == process_name:
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

# Check if WinAppDriver is already running
if not check_if_process_running("WinAppDriver.exe"):
    # Start WinAppDriver from the default installation location
    # Download from: https://github.com/microsoft/WinAppDriver/releases
    winappdriver_path = r"C:\Program Files (x86)\Windows Application Driver\WinAppDriver.exe"
    if os.path.exists(winappdriver_path):
        subprocess.Popen([winappdriver_path])
    else:
        print(f"WinAppDriver not found at {winappdriver_path}")
        print("Please install WinAppDriver from: https://github.com/microsoft/WinAppDriver/releases")
        exit(1)

# Wait for WinAppDriver to initialize
time.sleep(3)

# Create a custom options class for WinAppDriver
class WinAppDriverOptions(BaseOptions):
    def __init__(self):
        # Initialize _caps BEFORE calling super().__init__()
        self._caps = {
            "platformName": "Windows",
            "deviceName": "WindowsPC"
        }
        super().__init__()

    @property
    def default_capabilities(self):
        return {}
    
    def to_capabilities(self):
        # Return only our custom capabilities, excluding any defaults from BaseOptions
        return self._caps.copy()

# Set up desired capabilities for WinAppDriver
options = WinAppDriverOptions()
options._caps["app"] = r"C:\Windows\System32\notepad.exe"

# Initialize the WinAppDriver (default port is 4723)
driver = webdriver.Remote(
    command_executor='http://localhost:4723',
    options=options
)

# Wait for Notepad to open
time.sleep(2)

# Perform some actions here
# You can use Inspect.exe (Windows SDK) or Accessibility Insights to identify elements

# Locate the "Text Editor" element and send some text
try:
    text_editor = driver.find_element(By.NAME, "Text Editor")
    text_editor.send_keys("Hello, WinAppDriver!")
except Exception as e:
    print(f"An error occurred: {e}")

# Close Notepad
try:
    close_button = driver.find_element(By.NAME, "Close")
    close_button.click()
except Exception as e:
    print(f"An error occurred finding Close button: {e}")

# Wait for the "Do you want to save..." dialog to appear
time.sleep(2)

# Choose "Don't Save"
try:
    dont_save_button = driver.find_element(By.NAME, "Don't Save")
    dont_save_button.click()
except Exception as e:
    print(f"An error occurred: {e}")


# Close the driver (this will also close the application)
driver.quit()
