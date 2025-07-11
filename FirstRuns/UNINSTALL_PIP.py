###########################################################
#                                                         #
#                     ScriptWizard                        #
#               UNINSTALLS ALL REQUIRED                   #
#                 Python Dependencies                     #
#                  Use for reinstall                      #
#                                                         #
###########################################################

import os
import sys
import subprocess
import logging
import platform
import shutil

# Setup logging to file and console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('uninstall_pip.log'),
        logging.StreamHandler(sys.stdout)  # Also log to console for visibility
    ]
)
logger = logging.getLogger(__name__)

# List of packages to uninstall (based on AutoPIP.py)
packages = [
    'flask',
    'flask-socketio',
    'llama-cpp-python',
    'huggingface-hub',
]

def uninstall_package(pip_name):
    """
    Attempt to uninstall a package using pip.
    Returns True if successful or if package wasn't installed, False otherwise.
    """
    pip_cmd = [sys.executable, '-m', 'pip', 'uninstall', '-y', pip_name]
    
    try:
        # Run the pip uninstall command and capture output
        result = subprocess.run(pip_cmd, capture_output=True, text=True, check=True)
        logger.info(f"Uninstalled {pip_name}: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        if 'not installed' in e.stderr.lower():
            logger.info(f"{pip_name} was not installed. Skipping.")
            return True
        logger.error(f"Failed to uninstall {pip_name}: {e.stderr}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error uninstalling {pip_name}: {str(e)}")
        return False

def remove_local_packages_dir():
    """
    Remove the local PIP_Packages directory if it exists.
    """
    target_dir = os.path.abspath('PIP_Packages')
    if os.path.exists(target_dir):
        try:
            shutil.rmtree(target_dir)
            logger.info(f"Removed local PIP_Packages directory: {target_dir}")
            return True
        except Exception as e:
            logger.error(f"Failed to remove PIP_Packages: {str(e)}")
            return False
    else:
        logger.info("PIP_Packages directory does not exist. Skipping.")
        return True

def main():
    """
    Main function to detect OS and uninstall packages.
    """
    os_type = platform.system().lower()
    logger.info(f"Detected operating system: {os_type.capitalize()}")
    
    all_success = True
    
    # Uninstall each package via pip
    for pkg in packages:
        if not uninstall_package(pkg):
            all_success = False
    
    # As a fallback, remove local PIP_Packages dir
    if not remove_local_packages_dir():
        all_success = False
    
    if all_success:
        logger.info("All packages uninstalled successfully. You can now retry AutoPIP.py.")
    else:
        logger.warning("Some uninstallations failed. Check the log for details.")

if __name__ == '__main__':
    main()