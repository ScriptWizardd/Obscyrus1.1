###########################################################
#                                                         #
#                     ScriptWizard                        #
#                 VERIFYS ALL REQUIRED                    #
#                 Python Dependencies                     #
#                                                         #
###########################################################

import sys
import importlib

# ANSI escape codes for colors
class Colors:
    GREEN = '\033[92m'  # Green for installed
    RED = '\033[91m'    # Red for not installed
    RESET = '\033[0m'   # Reset color

# List of packages to verify (based on the required ones from previous scripts)
packages = [
    'flask',
    'flask_socketio',
    'llama_cpp',
    'huggingface_hub',
]

def is_package_installed(import_name):
    """
    Check if a package is installed by trying to import it.
    Returns True if installed, False otherwise.
    """
    try:
        importlib.import_module(import_name)
        return True
    except ImportError:
        return False

def main():
    print("Verifying required packages...\n")
    
    all_installed = True
    
    for pkg in packages:
        if is_package_installed(pkg):
            status = f"{Colors.GREEN}Installed{Colors.RESET}"
        else:
            status = f"{Colors.RED}Not Installed{Colors.RESET}"
            all_installed = False
        
        print(f"{pkg}: {status}")
    
    print("\n")
    if all_installed:
        print(f"{Colors.GREEN}All packages are installed successfully!{Colors.RESET}")
    else:
        print(f"{Colors.RED}Some packages are missing. Run AutoPIP.py to install them.{Colors.RESET}")

if __name__ == '__main__':
    main()