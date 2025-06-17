# Secret Santa Assignment System

This project implements an automated Secret Santa assignment system for Acme company. The system assigns secret children to employees while following specific rules and constraints.

## Features

- Parses employee information from CSV files
- Assigns secret children following specific rules:
  - No self-assignments
  - No repeat assignments from previous year
  - One-to-one mapping between employees and secret children
- Generates output CSV with assignments
- Includes comprehensive error handling
- Includes unit tests

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd secret-santa
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Input File Format

The input CSV file should contain the following columns:
- Employee_Name
- Employee_EmailID

Example:
```csv
Employee_Name,Employee_EmailID
John Doe,john.doe@acme.com
Jane Smith,jane.smith@acme.com
```

### Previous Year's Assignments Format

The previous year's assignments CSV file should contain:
- Employee_Name
- Employee_EmailID
- Secret_Child_Name
- Secret_Child_EmailID

### Running the Program

```bash
python -m src.main --input data/employees.csv --previous data/previous_assignments.csv --output data/new_assignments.csv
```

After Running this command you can see the new file generated in /data folder.

Like below you can add dynamic path too.

```bash
python -m src.main --input <Input data list file path> --previous <Previous data list file path> --output <Output data list file path>
```

### Running Tests

```bash
pytest tests/
```

### You can also view your Streamlit app in your browser.
```bash   
streamlit run src/app.py
```

If you get any error related to module when trying to run streamlit command then you can fix it using below command.
```bash
pip install -e .
```
## Project Structure

```
secret-santa/
├── data/
│   ├── employees.csv
│   ├── previous_assignments.csv
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── santa_assigner.py
│   └── exceptions.py
├── tests/
│   ├── __init__.py
│   ├── test_santa_assigner.py
│   └── test_data/
├── requirements.txt
├── .gitignore
├── setup.py
└── README.md
```

## Error Handling

The system handles various error cases including:
- Missing or invalid input files
- Malformed CSV files
- Invalid employee data
- Impossible assignment scenarios