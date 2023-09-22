from selenium import webdriver
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
        return False;
    except Exception as e:
        print(f"An error occurred: {e}")
        return False;

# Check if Winium Desktop Driver is already running
if not check_if_process_running("Winium.Desktop.Driver.exe"):
    # Get the current working directory
    root = os.getcwd()
    # Start the Winium Desktop Driver
    subprocess.Popen(os.path.join(root, "Winium.Desktop.Driver.exe"))

# Wait for Winium driver to initialize
time.sleep(3)

# Create the desired capabilities
desired_caps = {}
desired_caps["app"] = r"C:\Windows\System32\notepad.exe"

# Initialize the Winium driver
driver = webdriver.Remote(
    command_executor='http://localhost:9999',
    desired_capabilities=desired_caps
)

# Wait for Notepad to open
time.sleep(2)

# Perform some actions here
# You would use details from Windows SDK Inspect.exe to identify the elements

# Locate the "Text Editor" element and send some text
try:
    text_editor = driver.find_element_by_name("Text Editor")
    text_editor.send_keys("Hello, INet!")
except Exception as e:
    print(f"An error occurred: {e}")

# Close Notepad
driver.find_element_by_name("Close").click()


# Wait for the "Do you want to save..." dialog to appear
time.sleep(2)

# Choose "Don't Save"
try:
    dont_save_button = driver.find_element_by_name("Don't Save")
    dont_save_button.click()
except Exception as e:
    print(f"An error occurred: {e}")


# Close the driver (this will also close the application)
driver.quit()
