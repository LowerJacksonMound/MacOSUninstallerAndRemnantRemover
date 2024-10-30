import os
import shutil
import subprocess
import logging
import sys
import argparse
from datetime import datetime

def setup_logging(log_file="uninstaller.log"):
    """Setup logging configuration."""
    logging.basicConfig(
        filename=log_file,
        filemode='a',
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    logging.info("Logging started for uninstallation process.")

def find_app_paths(app_name):
    """Find common locations for leftover files related to the given application name."""
    home = os.path.expanduser("~")
    potential_paths = [
        f"/Applications/{app_name}.app",
        f"{home}/Library/Application Support/{app_name}",
        f"{home}/Library/Preferences/{app_name}.plist",
        f"{home}/Library/Caches/{app_name}",
        f"{home}/Library/Logs/{app_name}",
        f"{home}/Library/Containers/{app_name}",
        f"{home}/Library/Saved Application State/{app_name}.savedState"
    ]
    return [path for path in potential_paths if os.path.exists(path)]

def create_backup(backup_dir, paths_to_backup):
    """Create a backup of the specified files and directories."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(backup_dir, f"backup_{timestamp}")
    os.makedirs(backup_path, exist_ok=True)
    logging.info(f"Creating backup at {backup_path}")

    for path in paths_to_backup:
        try:
            if os.path.isdir(path):
                shutil.copytree(path, os.path.join(backup_path, os.path.basename(path)))
            else:
                shutil.copy2(path, backup_path)
            logging.info(f"Backed up: {path}")
            print(f"Backed up: {path}")
        except Exception as e:
            logging.error(f"Failed to backup {path}: {e}")
            print(f"Failed to backup {path}: {e}")

    return backup_path

def restore_backup(backup_dir, restore_path):
    """Restore a backup from the specified directory."""
    try:
        for item in os.listdir(backup_dir):
            s = os.path.join(backup_dir, item)
            d = os.path.join(restore_path, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                shutil.copy2(s, d)
        logging.info(f"Restored backup from {backup_dir} to {restore_path}")
        print(f"Restored backup from {backup_dir} to {restore_path}")
    except Exception as e:
        logging.error(f"Failed to restore backup from {backup_dir}: {e}")
        print(f"Failed to restore backup from {backup_dir}: {e}")

def uninstall_via_brew(app_name):
    """Uninstall an application using Homebrew."""
    try:
        result = subprocess.run(["brew", "uninstall", app_name], check=True, capture_output=True, text=True)
        logging.info(f"Uninstalled {app_name} using brew.")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to uninstall {app_name} via brew: {e.stderr}")
        print(f"Failed to uninstall {app_name} via brew:\n{e.stderr}")

def uninstall_via_pip(app_name):
    """Uninstall a Python package using pip."""
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "uninstall", "-y", app_name], check=True, capture_output=True, text=True)
        logging.info(f"Uninstalled {app_name} using pip.")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to uninstall {app_name} via pip: {e.stderr}")
        print(f"Failed to uninstall {app_name} via pip:\n{e.stderr}")

def uninstall_docker(app_name, silent_mode=False):
    """Uninstall a Docker image or container."""
    try:
        # Confirmation prompt for Docker container removal
        if not silent_mode:
            confirm = input(f"Do you want to remove the Docker container named '{app_name}'? (y/n): ").strip().lower()
            if confirm != 'y':
                logging.info(f"Skipping Docker container removal for {app_name}.")
                print(f"Skipping Docker container removal for {app_name}.")
            else:
                subprocess.run(["docker", "rm", "-f", app_name], check=True, capture_output=True, text=True)
                logging.info(f"Removed Docker container: {app_name}")
                print(f"Removed Docker container: {app_name}")
        else:
            # Remove without confirmation if in silent mode
            subprocess.run(["docker", "rm", "-f", app_name], check=True, capture_output=True, text=True)
            logging.info(f"Removed Docker container: {app_name}")
            print(f"Removed Docker container: {app_name}")
    except subprocess.CalledProcessError as e:
        logging.info(f"No Docker container named {app_name} found or failed to remove: {e.stderr}")

    try:
        # Confirmation prompt for Docker image removal
        if not silent_mode:
            confirm = input(f"Do you want to remove the Docker image named '{app_name}'? (y/n): ").strip().lower()
            if confirm != 'y':
                logging.info(f"Skipping Docker image removal for {app_name}.")
                print(f"Skipping Docker image removal for {app_name}.")
            else:
                subprocess.run(["docker", "rmi", "-f", app_name], check=True, capture_output=True, text=True)
                logging.info(f"Removed Docker image: {app_name}")
                print(f"Removed Docker image: {app_name}")
        else:
            # Remove without confirmation if in silent mode
            subprocess.run(["docker", "rmi", "-f", app_name], check=True, capture_output=True, text=True)
            logging.info(f"Removed Docker image: {app_name}")
            print(f"Removed Docker image: {app_name}")
    except subprocess.CalledProcessError as e:
        logging.info(f"No Docker image named {app_name} found or failed to remove: {e.stderr}")

def detect_installation_type(app_name):
    """Automatically detect the installation type of the application."""
    app_path = f"/Applications/{app_name}.app"
    if os.path.exists(app_path):
        logging.info(f"Detected {app_name} as a .app installation.")
        return "app"
    if shutil.which("brew") and subprocess.run(["brew", "list", app_name], capture_output=True).returncode == 0:
        logging.info(f"Detected {app_name} as a Homebrew installation.")
        return "brew"
    if shutil.which("pip") and subprocess.run([sys.executable, "-m", "pip", "show", app_name], capture_output=True).returncode == 0:
        logging.info(f"Detected {app_name} as a pip installation.")
        return "pip"
    if shutil.which("docker") and app_name in subprocess.run(["docker", "ps", "-a", "--format", "{{.Names}}"], capture_output=True, text=True).stdout:
        logging.info(f"Detected {app_name} as a Docker container or image.")
        return "docker"
    # Add other installation types here as needed
    logging.warning(f"Could not detect installation type for {app_name}")
    return None

def uninstall_app(app_name, silent_mode=False, dry_run=False, backup_dir=None, restore=False, restore_path=None, log_file="uninstaller.log"):
    """Uninstall the specified application and remove leftover files."""
    setup_logging(log_file)
    logging.info(f"Starting {'restoration' if restore else 'uninstallation'} process for {app_name}.")

    if restore and backup_dir:
        restore_backup(backup_dir, restore_path if restore_path else os.path.expanduser("~"))
        return

    # Step 1: Backup before uninstallation if backup_dir is provided
    if backup_dir:
        backup_path = create_backup(backup_dir, find_app_paths(app_name))
        logging.info(f"Backup created at {backup_path}")

    # Detect the installation type and handle accordingly
    installation_type = detect_installation_type(app_name)
    if installation_type == "app":
        app_path = f"/Applications/{app_name}.app"
        if os.path.exists(app_path):
            if dry_run:
                logging.info(f"[DRY RUN] Would move {app_path} to Trash.")
                print(f"[DRY RUN] Would move {app_path} to Trash.")
            else:
                try:
                    subprocess.run([
                        "osascript",
                        "-e",
                        f'tell application "Finder" to move POSIX file "{app_path}" to trash'
                    ], check=True, capture_output=True, text=True)
                    logging.info(f"Moved {app_path} to Trash.")
                    print(f"Moved {app_path} to Trash.")
                except subprocess.CalledProcessError as e:
                    logging.error(f"Failed to move {app_path} to Trash: {e.stderr}")
                    print(f"Failed to move {app_path} to Trash:\n{e.stderr}")
    elif installation_type == "brew":
        uninstall_via_brew(app_name)
    elif installation_type == "pip":
        uninstall_via_pip(app_name)
    elif installation_type == "docker":
        uninstall_docker(app_name, silent_mode)
    else:
        logging.warning(f"Installation type for {app_name} not handled.")
        print(f"Installation type for {app_name} not handled.")

    # Step 2: Handle leftover files after uninstallation
    if backup_dir:
        leftover_paths = find_app_paths(app_name)
        if leftover_paths:
            logging.info("Backing up leftover files after uninstallation.")
            backup_path = create_backup(backup_dir, leftover_paths)
            logging.info(f"Backup of leftover files created at {backup_path}")
        else:
            logging.info("No leftover files found to backup.")

    logging.info(f"{'Restoration' if restore else 'Uninstallation'} and cleanup for {app_name} completed.")
    print(f"\n{'Restoration' if restore else 'Uninstallation'} and cleanup for {app_name} completed.")

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Uninstall applications and remove leftover files on macOS."
    )
    parser.add_argument("application_name", help="Name of the application to uninstall.")
    parser.add_argument("--silent", action="store_true", help="Perform the uninstallation without user confirmation.")
    parser.add_argument("--dry-run", action="store_true", help="Simulate the uninstallation process without making any changes.")
    parser.add_argument("--backup", metavar="DIR", help="Backup files to the specified directory before deletion.")
    parser.add_argument("--restore", action="store_true", help="Restore from a previous backup instead of uninstalling.")
    parser.add_argument("--restore-path", metavar="PATH", help="Path to restore backup files. Defaults to the user's home directory.")
    parser.add_argument("--log-file", metavar="FILE", default="uninstaller.log", help="Path to the log file. Defaults to 'uninstaller.log'.")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()

    app_name = args.application_name
    silent_mode = args.silent
    dry_run = args.dry_run
    backup_dir = args.backup
    restore = args.restore
    restore_path = args.restore_path
    log_file = args.log_file

    # Validate backup directory if provided
    if backup_dir and not os.path.isdir(backup_dir):
        try:
            os.makedirs(backup_dir, exist_ok=True)
            print(f"Created backup directory at {backup_dir}")
        except Exception as e:
            print(f"Error: Could not create backup directory '{backup_dir}': {e}")
            sys.exit(1)

    # Run the uninstallation or restoration
    uninstall_app(
        app_name,
        silent_mode=silent_mode,
        dry_run=dry_run,
        backup_dir=backup_dir,
        restore=restore,
        restore_path=restore_path,
        log_file=log_file
    )
