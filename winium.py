from selenium import webdriver
from selenium.webdriver.common.by import By
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
            except (psutil.NoSuchProcess, psutil.AccessDenied,
                    psutil.ZombieProcess):
                pass
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


# Check if WinAppDriver is already running
if not check_if_process_running("WinAppDriver.exe"):
    # Start WinAppDriver from the default installation location
    # Download from: https://github.com/microsoft/WinAppDriver/releases
    winappdriver_path = (r"C:\Program Files (x86)\Windows Application Driver"
                         r"\WinAppDriver.exe")
    if os.path.exists(winappdriver_path):
        subprocess.Popen([winappdriver_path])
    else:
        print(f"WinAppDriver not found at {winappdriver_path}")
        print("Please install WinAppDriver from: https://github.com/microsoft/WinAppDriver/releases")
        exit(1)

# Wait for WinAppDriver to initialize
time.sleep(3)

# Set up desired capabilities for WinAppDriver (Selenium 3 format)
desired_caps = {
    "app": r"C:\windows\system32\notepad.exe",
    "platformName": "Windows",
    "deviceName": "WindowsPC"
}

# Initialize the WinAppDriver (default port is 4723)
driver = webdriver.Remote(
    command_executor="http://127.0.0.1:4723",
    desired_capabilities=desired_caps
)

# Wait for Notepad to open
time.sleep(2)

# Perform some actions here
# You can use Inspect.exe (Windows SDK) or Accessibility Insights to identify elements

# Locate the Notepad text surface and send some text
try:
    text_editor = driver.find_element(By.NAME, "Text editor")
    text_editor.send_keys("Hello, WinAppDriver!")
except Exception as e:
    print(f"An error occurred: {e}")

time.sleep(5)
# Close Notepad
try:
    close_button = driver.find_element(By.NAME, "Close")
    close_button.click()
except Exception as e:
    print(f"An error occurred finding Close button: {e}")

# Wait for the "Do you want to save..." dialog to appear
time.sleep(2)

# Choose "Don't save"
try:
    dont_save_button = driver.find_element(By.NAME, "Don't save")
except Exception:
    try:
        dont_save_button = driver.find_element(By.NAME, "Don't Save")
    except Exception as e:
        print(f"An error occurred locating the Don't save button: {e}")
        dont_save_button = None

if dont_save_button:
    dont_save_button.click()


# Close the driver (this will also close the application)
driver.quit()
