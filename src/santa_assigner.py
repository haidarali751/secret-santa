import pandas as pd
import random
from typing import Optional, Dict, List, Tuple
from .exceptions import AssignmentError, InputFileError, ValidationError


class SantaAssigner:
    def __init__(self):
        self.employees = None
        self.previous_assignments = None

    def load_employees(self, file_path: str) -> None:
        """
        Load employee data from CSV file.
        
        Args:
            file_path: Path to the CSV file containing employee information
            
        Raises:
            InputFileError: If file cannot be read or has invalid format
        """
        try:
            self.employees = pd.read_csv(file_path)
            self._validate_employee_data()
        except Exception as e:
            raise InputFileError(f"Error loading employee data: {str(e)}")

    def load_previous_assignments(self, file_path: str) -> None:
        """
        Load previous year's Secret Santa assignments.
        
        Args:
            file_path: Path to the CSV file containing previous assignments
            
        Raises:
            InputFileError: If file cannot be read or has invalid format
        """
        try:
            self.previous_assignments = pd.read_csv(file_path)
            self._validate_previous_assignments()
        except Exception as e:
            raise InputFileError(f"Error loading previous assignments: {str(e)}")

    def _validate_employee_data(self) -> None:
        """Validate the employee data format and content."""
        required_columns = {'Employee_Name', 'Employee_EmailID'}
        if not all(col in self.employees.columns for col in required_columns):
            raise ValidationError("Employee data missing required columns")
        
        if self.employees.duplicated(subset=['Employee_EmailID']).any():
            raise ValidationError("Duplicate email IDs found in employee data")

    def _validate_previous_assignments(self) -> None:
        """Validate the previous assignments data format and content."""
        required_columns = {
            'Employee_Name', 'Employee_EmailID',
            'Secret_Child_Name', 'Secret_Child_EmailID'
        }
        if not all(col in self.previous_assignments.columns for col in required_columns):
            raise ValidationError("Previous assignments missing required columns")

    def _get_previous_assignment(self, employee_email: str) -> Optional[str]:
        """Get previous year's secret child for an employee."""
        if self.previous_assignments is None:
            return None
        
        prev = self.previous_assignments[
            self.previous_assignments['Employee_EmailID'] == employee_email
        ]
        return prev['Secret_Child_EmailID'].iloc[0] if not prev.empty else None

    def _is_valid_assignment(self, santa_email: str, child_email: str) -> bool:
        """Check if the assignment is valid based on rules."""
        if santa_email == child_email:
            return False
        
        prev_child = self._get_previous_assignment(santa_email)
        if prev_child and prev_child == child_email:
            return False
            
        return True

    def generate_assignments(self) -> pd.DataFrame:
        """
        Generate Secret Santa assignments following all rules.
        
        Returns:
            DataFrame containing the new assignments
            
        Raises:
            AssignmentError: If valid assignments cannot be generated
        """
        if self.employees is None:
            raise AssignmentError("No employee data loaded")

        max_attempts = 100
        for attempt in range(max_attempts):
            try:
                assignments = self._try_generate_assignments()
                return assignments
            except AssignmentError:
                continue
                
        raise AssignmentError("Could not generate valid assignments after maximum attempts")

    def _try_generate_assignments(self) -> pd.DataFrame:
        """Attempt to generate valid assignments."""
        employees_list = self.employees.to_dict('records')
        available_children = employees_list.copy()
        assignments = []

        random.shuffle(employees_list)
        
        for santa in employees_list:
            valid_children = [
                child for child in available_children
                if self._is_valid_assignment(santa['Employee_EmailID'], child['Employee_EmailID'])
            ]
            
            if not valid_children:
                raise AssignmentError("No valid children available for assignment")
                
            chosen_child = random.choice(valid_children)
            available_children.remove(chosen_child)
            
            assignments.append({
                'Employee_Name': santa['Employee_Name'],
                'Employee_EmailID': santa['Employee_EmailID'],
                'Secret_Child_Name': chosen_child['Employee_Name'],
                'Secret_Child_EmailID': chosen_child['Employee_EmailID']
            })
            
        return pd.DataFrame(assignments)

    def save_assignments(self, assignments: pd.DataFrame, output_file: str) -> None:
        """
        Save the generated assignments to a CSV file.
        
        Args:
            assignments: DataFrame containing the assignments
            output_file: Path where to save the CSV file
            
        Raises:
            InputFileError: If file cannot be written
        """
        try:
            assignments.to_csv(output_file, index=False)
        except Exception as e:
            raise InputFileError(f"Error saving assignments: {str(e)}") 