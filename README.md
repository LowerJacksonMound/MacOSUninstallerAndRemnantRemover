# macOS Application Uninstaller and Remnant Remover

# A versatile Python script to uninstall applications on macOS, handling different installation types such as `.app` bundles, Homebrew packages, Python packages installed via `pip`, and Docker containers/images. The script also manages backups of leftover files and supports restoration from backups

# permalink: /MacOSUninstallerAndRemnantRemover/

## Features

- **Automatic Detection:** Identifies the installation type of the specified application.
- **Uninstallation Methods:**
  - `.app` bundles
  - Homebrew packages
  - Python packages (`pip`)
  - Docker containers and images
- **Backup Management:** Automatically backups leftover files before uninstallation.
- **Restoration:** Restore files from a previous backup.
- **Silent Mode:** Perform operations without user confirmations.
- **Dry Run:** Simulate the uninstallation process without making any changes.
- **Logging:** Logs all actions and errors to a specified log file.

## Requirements

- **Operating System:** macOS
- **Python Version:** Python 3.6 or higher
- **Dependencies:** None (uses only standard Python libraries)

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/macos-uninstaller.git
   cd macos-uninstaller

2. **(Optional) Create a Virtual Environment:**

  ```bash  
    python3 -m venv venv
    source venv/bin/activate

3. **Usage:**
  ```bash
  python uninstaller.py <application_name> [options]

4. **Positional Arguments:**
application_name
Name of the application to uninstall.s:**

5. **Optional Arguments:**
--silent
Perform the uninstallation without user confirmation.
--dry-run
Simulate the uninstallation process without making any changes.
--backup DIR
Backup files to the specified directory before deletion.
--restore
Restore from a previous backup instead of uninstalling.
--restore-path PATH
Path to restore backup files. Defaults to the user's home directory.
--log-file FILE
Path to the log file. Defaults to uninstaller.log.
-h, --help
Show the help message and exit.

**Examples**

1. **Uninstall an Application with Backup:**
python3 uninstall.py MyApp --backup /path/to/backup

2. **Uninstall Silently Without Confirmations:**
python3 uninstall.py MyApp --silent

3. **Perform a Dry Run:**
python3 uninstall.py MyApp --dry-run

4. **Restore from a Backup:**
python3 uninstall.py MyApp --restore --backup /path/to/backup

5. **Specify a Custom Restore Path and Log File:**
python3 uninstall.py MyApp --restore --backup /path/to/backup --restore-path /desired/restore/path --log-file /path/to/logfile.log

**Logging**
All actions and errors are logged to a file specified by the --log-file argument. By default, logs are saved to uninstaller.log in the current directory.

**Notes**

**Permissions:**
Some uninstallation steps may require elevated permissions. Even when using sudo, macOS enforces password authentication to ensure security. You will be prompted to enter an admin password when necessary. There is no supported method to bypass this security feature, and attempting to do so is strongly discouraged as it can compromise your system's security.
**Backup Restoration:**
Ensure that the restore path has the appropriate permissions and sufficient space to accommodate the restored files.
**Docker Uninstallation:**
When uninstalling Docker containers or images, the script attempts to remove them. Ensure that no dependent services are using these containers or images to avoid disruptions.
