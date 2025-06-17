import pytest
import pandas as pd
from src.santa_assigner import SantaAssigner
from src.exceptions import ValidationError, AssignmentError

@pytest.fixture
def sample_employees():
    return pd.DataFrame({
        'Employee_Name': ['John Doe', 'Jane Smith', 'Bob Wilson', 'Alice Brown'],
        'Employee_EmailID': ['john@acme.com', 'jane@acme.com', 'bob@acme.com', 'alice@acme.com']
    })

@pytest.fixture
def sample_previous_assignments():
    return pd.DataFrame({
        'Employee_Name': ['John Doe', 'Jane Smith', 'Bob Wilson', 'Alice Brown'],
        'Employee_EmailID': ['john@acme.com', 'jane@acme.com', 'bob@acme.com', 'alice@acme.com'],
        'Secret_Child_Name': ['Jane Smith', 'Bob Wilson', 'Alice Brown', 'John Doe'],
        'Secret_Child_EmailID': ['jane@acme.com', 'bob@acme.com', 'alice@acme.com', 'john@acme.com']
    })

def test_validate_employee_data(sample_employees):
    assigner = SantaAssigner()
    assigner.employees = sample_employees
    assigner._validate_employee_data()

def test_validate_employee_data_missing_columns():
    assigner = SantaAssigner()
    assigner.employees = pd.DataFrame({
        'Employee_Name': ['John Doe']
    })
    with pytest.raises(ValidationError):
        assigner._validate_employee_data()

def test_validate_employee_data_duplicate_email():
    assigner = SantaAssigner()
    assigner.employees = pd.DataFrame({
        'Employee_Name': ['John Doe', 'John Smith'],
        'Employee_EmailID': ['john@acme.com', 'john@acme.com']
    })
    with pytest.raises(ValidationError):
        assigner._validate_employee_data()

def test_generate_assignments(sample_employees):
    assigner = SantaAssigner()
    assigner.employees = sample_employees
    
    assignments = assigner.generate_assignments()
    
    # Check that all required columns are present
    assert all(col in assignments.columns for col in [
        'Employee_Name', 'Employee_EmailID',
        'Secret_Child_Name', 'Secret_Child_EmailID'
    ])
    
    # Check that number of assignments matches number of employees
    assert len(assignments) == len(sample_employees)
    
    # Check that no one is assigned to themselves
    for _, row in assignments.iterrows():
        assert row['Employee_EmailID'] != row['Secret_Child_EmailID']
    
    # Check that each person is assigned exactly once as a child
    child_emails = assignments['Secret_Child_EmailID'].tolist()
    assert len(child_emails) == len(set(child_emails))

def test_generate_assignments_with_previous(sample_employees, sample_previous_assignments):
    assigner = SantaAssigner()
    assigner.employees = sample_employees
    assigner.previous_assignments = sample_previous_assignments
    
    assignments = assigner.generate_assignments()
    
    # Check that no one got the same person as last year
    for _, row in assignments.iterrows():
        prev_assignment = sample_previous_assignments[
            sample_previous_assignments['Employee_EmailID'] == row['Employee_EmailID']
        ]
        if not prev_assignment.empty:
            assert row['Secret_Child_EmailID'] != prev_assignment.iloc[0]['Secret_Child_EmailID']

def test_generate_assignments_single_person():
    assigner = SantaAssigner()
    assigner.employees = pd.DataFrame({
        'Employee_Name': ['John Doe'],
        'Employee_EmailID': ['john@acme.com']
    })
    
    with pytest.raises(AssignmentError):
        assigner.generate_assignments() 