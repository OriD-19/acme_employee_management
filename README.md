# Employee Management System

A comprehensive Employee Management System built with Python. This project features a modern **Text User Interface (TUI)** powered by the [Rich](https://github.com/Textualize/rich) library, allowing you to manage employee records, perform CRUD operations, and handle HR, payroll, or administrative needs—all from your terminal.

## Features
- Modern TUI (Text User Interface) with Rich
- Add, update, delete, and view employee records
- Search and filter employees by role
- Manage freelance projects, vacations, and payments
- View employee transactions and logs
- Modular and extensible codebase

## Requirements
- Python 3.8+
- [uv](https://github.com/astral-sh/uv) (Python package manager)
- [Rich](https://github.com/Textualize/rich) (installed automatically via dependencies)

## Setup Instructions

### 1. Clone the Repository
```sh
git clone <repository-url>
cd <project-directory>
```

### 2. Install uv (if not already installed)
With `curl`:
```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

With `pipx`:
```sh
pipx install uv
```

### 3. Install Project Dependencies
```sh
uv pip install -r requirements.txt
```
*Or, if you use a pyproject.toml file:*
```sh
uv pip install .
```

### 4. Create and Activate a Virtual Environment
```sh
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

## Running the Application

This is a terminal-based TUI application. To start the Employee Management System, run:

```sh
python main.py
```

## Usage
- All interactions happen in your terminal window.
- Navigate using the menu options (type the number and press ENTER).
- Add, view, and manage employees, freelance projects, vacations, and payments.
- Logs are saved to `log.txt` in the project directory.

## Project Structure
```
project-directory/
├── main.py                # Entry point for the TUI
├── requirements.txt       # List of dependencies
├── pyproject.toml         # Project metadata
├── employee/              # Employee-related modules
├── menu/                  # TUI screens and components (Rich-based)
├── store/                 # Data storage logic
├── logs/                  # Logging and event system
├── config/                # Configuration files
└── README.md              # This file
```

## Final Considerations

- Make sure you are located into the `main.py` directory
- Store sample `config.json` with custom configuration values for settings used in the system
