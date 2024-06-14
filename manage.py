import os
import subprocess
import sys
import venv

VENV_DIR = 'venv'
REQUIREMENTS = 'requirements.txt'
PYTHON = sys.executable

def create_venv():
    """Create a virtual environment."""
    if not os.path.exists(VENV_DIR):
        print("Creating virtual environment...")
        venv.create(VENV_DIR, with_pip=True)
    else:
        print("Virtual environment already exists.")

def install_dependencies():
    """Install dependencies from requirements.txt."""
    if os.name == 'nt':
        pip_executable = os.path.join(VENV_DIR, 'Scripts', 'pip.exe')
    else:
        pip_executable = os.path.join(VENV_DIR, 'bin', 'pip')

    print("Installing dependencies...")
    subprocess.check_call([pip_executable, 'install', '-r', REQUIREMENTS])

def run_bot():
    """Run the bot."""
    if os.name == 'nt':
        python_executable = os.path.join(VENV_DIR, 'Scripts', 'python.exe')
    else:
        python_executable = os.path.join(VENV_DIR, 'bin', 'python')

    print("Running bot...")
    subprocess.check_call([python_executable, 'bot.py'])

def install_lib(library_name):
    """Install a specific library and update requirements.txt."""
    if os.name == 'nt':
        pip_executable = os.path.join(VENV_DIR, 'Scripts', 'pip.exe')
    else:
        pip_executable = os.path.join(VENV_DIR, 'bin', 'pip')

    print(f"Installing {library_name}...")
    subprocess.check_call([pip_executable, 'install', library_name])
    subprocess.check_call([pip_executable, 'freeze'], stdout=open(REQUIREMENTS, 'w'))

def remove_lib(library_name):
    """Remove a specific library and update requirements.txt."""
    if os.name == 'nt':
        pip_executable = os.path.join(VENV_DIR, 'Scripts', 'pip.exe')
    else:
        pip_executable = os.path.join(VENV_DIR, 'bin', 'pip')

    print(f"Removing {library_name}...")
    subprocess.check_call([pip_executable, 'uninstall', '-y', library_name])
    subprocess.check_call([pip_executable, 'freeze'], stdout=open(REQUIREMENTS, 'w'))

def main():
    if len(sys.argv) < 2:
        print("Usage: python manage.py [create-venv|install|run|install-lib|remove-lib] [library_name]")
        sys.exit(1)

    command = sys.argv[1]

    if command == 'create-venv':
        create_venv()
    elif command == 'install':
        create_venv()
        install_dependencies()
    elif command == 'run':
        run_bot()
    elif command == 'install-lib' and len(sys.argv) == 3:
        install_lib(sys.argv[2])
    elif command == 'remove-lib' and len(sys.argv) == 3:
        remove_lib(sys.argv[2])
    else:
        print("Invalid command or missing library name.")
        print("Usage: python manage.py [create-venv|install|run|install-lib|remove-lib] [library_name]")

if __name__ == '__main__':
    main()
