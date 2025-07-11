###########################################################
#                                                         #
#                     ScriptWizard                        #
#                INSTALLS ALL REQUIRED                    #
#                 Python Dependencies                     #
#            sO LONG AS pYTHON IS INSTALLED               #
#                                                         #
###########################################################

import os
import sys
import subprocess
import logging
import platform
import importlib

# Setup logging to file and console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('autopip.log'),
        logging.StreamHandler(sys.stdout)  # Also log to console for visibility
    ]
)
logger = logging.getLogger(__name__)

# List of required packages based on the provided codes (Obscyrus1.1.py and HF downloader)
# import_name: for checking if installed, pip_name: for pip install command
packages = [
    {'import_name': 'flask', 'pip_name': 'flask'},
    {'import_name': 'flask_socketio', 'pip_name': 'flask-socketio'},
    {'import_name': 'llama_cpp', 'pip_name': 'llama-cpp-python'},  # Note: May require build tools like cmake on some systems
    {'import_name': 'huggingface_hub', 'pip_name': 'huggingface-hub'},
]

def is_package_installed(import_name):
    """
    Check if a package is installed by trying to import it.
    """
    try:
        importlib.import_module(import_name)
        return True
    except ImportError:
        return False

def install_package(pip_name, method='normal'):
    """
    Install a package using the specified method.
    - normal: Standard pip install (may require root/sudo on Linux/Mac).
    - user: pip install --user (installs to user directory, no root needed).
    - target: pip install --target=PIP_Packages (local dir, no root, modifies sys.path).
    Returns True if successful, False otherwise.
    """
    pip_cmd = [sys.executable, '-m', 'pip', 'install', pip_name]
    
    if method == 'user':
        pip_cmd.append('--user')
        logger.info(f"Trying --user install for {pip_name}")
    
    elif method == 'target':
        target_dir = os.path.abspath('PIP_Packages')
        os.makedirs(target_dir, exist_ok=True)
        pip_cmd.extend(['--target', target_dir])
        # Ensure the target dir is in sys.path for immediate use
        if target_dir not in sys.path:
            sys.path.insert(0, target_dir)
        logger.info(f"Trying --target install to {target_dir} for {pip_name}")
    
    try:
        # Run the pip command and capture output
        result = subprocess.run(pip_cmd, capture_output=True, text=True, check=True)
        logger.info(f"Installed {pip_name} using {method}: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install {pip_name} using {method}: {e.stderr}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error installing {pip_name} using {method}: {str(e)}")
        return False

def main():
    """
    Main function to detect OS and install missing packages.
    """
    os_type = platform.system().lower()
    logger.info(f"Detected operating system: {os_type.capitalize()}")
    
    for pkg in packages:
        if is_package_installed(pkg['import_name']):
            logger.info(f"{pkg['import_name']} is already installed. Skipping.")
            continue
        
        logger.info(f"{pkg['import_name']} is missing. Attempting installation.")
        
        # Try normal install (may require elevated perms)
        if install_package(pkg['pip_name']):
            continue
        
        # Alternative: Try --user install (no root needed)
        if install_package(pkg['pip_name'], method='user'):
            continue
        
        # Fallback: Install to local PIP_Packages dir (no root, modifies sys.path)
        if install_package(pkg['pip_name'], method='target'):
            logger.info(f"Successfully installed {pkg['import_name']} to local PIP_Packages directory.")
            continue
        
        # If all fail, log the failure
        logger.error(f"Could not install {pkg['import_name']} using any method. Manual intervention required.")

if __name__ == '__main__':
    main()