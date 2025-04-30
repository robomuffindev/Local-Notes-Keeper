# Local Notes Keeper

Local Notes Keeper is a web-based note-taking application that runs on your local network. It allows you to create, edit, and manage notes and files from any device on your network without storing your data online.

![Local Notes KeeperApp](https://github.com/user-attachments/assets/e1677298-039a-4b5d-a109-bd94504c7a6c)


## Features

- **Note Management**: Create, edit, view, and delete notes
- **File Uploads**: Upload and download files
- **User Accounts**: Secure personal notes with user authentication
- **Admin Controls**: Add/remove users and reset passwords
- **Mobile Responsive**: Access from any device with a web browser
- **Copy Button**: Easily copy note contents to clipboard
- **Local Storage**: All data is stored locally on your machine

## Installation

### Prerequisites

- Python 3.8 or higher
- Windows (for the installer script)

### Installation Steps

1. Extract all files to a directory of your choice
2. Run `installer.bat` to set up the application
   - This will create a virtual environment
   - Install the required dependencies
   - Set up the application structure

## Running the Application

1. Run `run.bat` to start the application
2. Open your web browser and navigate to:
   - `http://localhost:5000` (on the host machine)
   - `http://<your-ip-address>:5000` (from other devices on the network)
3. Log in with the default admin credentials:
   - Username: `admin`
   - Password: `admin`
4. **Important**: Change the default admin password immediately after first login

## User Guide

### First-time Setup

1. Log in with the default admin account
2. Go to the Admin panel and create user accounts for everyone who needs access
3. Change the admin password in the Settings page

### Creating Notes

1. On the Dashboard, click "New Note"
2. Enter a title and content for your note
3. Click "Save" to create the note

### Managing Notes

- **View**: Click on the "View" button to see the full note
- **Edit**: Click on the "Edit" button to modify a note
- **Delete**: Click on the "Delete" button to remove a note
- **Copy**: When viewing a note, click the "Copy" button to copy its contents to your clipboard

### Managing Files

- **Upload**: Use the file upload form on the Dashboard
- **Download**: Click the "Download" button next to a file
- **Delete**: Click the "Delete" button next to a file

### User Settings

- Go to the Settings page to change your password

### Admin Functions

- **Add User**: Create new user accounts
- **Reset Password**: Reset a user's password if they forgot it
- **Toggle Admin**: Grant or revoke admin privileges
- **Delete User**: Remove a user account and all their data

## Security Notes

- The application runs on your local network, so anyone on the same network can access the login page
- User passwords are stored securely using hashing
- For additional security, consider setting up a firewall or running the application on a dedicated device

## License

This software is provided as-is, free to use for personal purposes.
