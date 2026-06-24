# Ardhi Pulse Scanner 2025

An automated monitoring tool designed to track updates on public land registry records. It scans specified registry portals, detects structural or content changes, and triggers notifications.

## Features
- **Stealth Scanning**: Custom User-Agents to mimic browser behavior.
- **State Persistence**: Uses SHA-256 hashing to compare registry states.
- **Notification Engine**: Built-in SMTP support for instant email alerts.
- **Logging**: Comprehensive audit trail of all scan attempts.

## Installation
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables (optional for email):
   - `SCANNER_EMAIL`: Your Gmail/SMTP email
   - `SCANNER_PWD`: Your App Password
   - `NOTIFY_EMAIL`: Destination email

## Usage
```bash
python scanner.py
```

*Note: This tool is for educational purposes. Ensure compliance with the target website's robots.txt and Terms of Service.*