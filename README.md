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
python src/main.py --input employees.csv --previous previous_year.csv --output assignments.csv
```

### Running Tests

```bash
pytest tests/
```

## Project Structure

```
secret-santa/
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
└── README.md
```

## Error Handling

The system handles various error cases including:
- Missing or invalid input files
- Malformed CSV files
- Invalid employee data
- Impossible assignment scenarios

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 