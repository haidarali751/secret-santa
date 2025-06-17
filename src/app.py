import streamlit as st
import pandas as pd
from src.santa_assigner import SantaAssigner
from src.exceptions import SecretSantaError

def validate_csv_columns(df, required_columns, file_type):
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        st.error(f"Error in {file_type}: Missing required columns: {', '.join(missing_columns)}")
        return False
    return True

def main():
    st.set_page_config(
        page_title="Secret Santa Assignment System",
        page_icon="🎅",
        layout="wide"
    )

    st.title("🎅 Secret Santa Assignment System")

    # File upload section
    st.header("Upload Files")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Employee List")
        employee_file = st.file_uploader(
            "Upload employee CSV file",
            type=['csv'],
            help="CSV file with Employee_Name and Employee_EmailID columns"
        )

    with col2:
        st.subheader("Previous Assignments (Optional)")
        previous_file = st.file_uploader(
            "Upload previous year's assignments",
            type=['csv'],
            help="CSV file with previous year's assignments"
        )

    # Required columns
    employee_columns = ['Employee_Name', 'Employee_EmailID']
    previous_columns = ['Employee_Name', 'Employee_EmailID', 'Secret_Child_Name', 'Secret_Child_EmailID']

    # Display uploaded data
    employees_df = None
    if employee_file is not None:
        try:
            employees_df = pd.read_csv(employee_file)
            if validate_csv_columns(employees_df, employee_columns, "Employee List"):
                st.subheader("Employee List Preview")
                st.dataframe(employees_df)
        except Exception as e:
            st.error(f"Error reading employee file: {str(e)}")
            st.info("Please make sure your CSV file is properly formatted and not empty.")

    previous_df = None
    if previous_file is not None:
        try:
            previous_df = pd.read_csv(previous_file)
            if validate_csv_columns(previous_df, previous_columns, "Previous Assignments"):
                st.subheader("Previous Assignments Preview")
                st.dataframe(previous_df)
        except Exception as e:
            st.error(f"Error reading previous assignments file: {str(e)}")
            st.info("Please make sure your CSV file is properly formatted and not empty.")

    # Generate assignments button
    if st.button("Generate Assignments", type="primary"):
        if employee_file is None:
            st.error("Please upload an employee list first!")
        elif employees_df is None or not validate_csv_columns(employees_df, employee_columns, "Employee List"):
            st.error("Please fix the issues with the employee list file.")
        else:
            try:
                # Initialize assigner
                assigner = SantaAssigner()
                
                # Load employee data
                assigner.employees = employees_df
                
                # Load previous assignments if provided
                if previous_file is not None and previous_df is not None and validate_csv_columns(previous_df, previous_columns, "Previous Assignments"):
                    assigner.previous_assignments = previous_df
                
                # Generate assignments
                assignments = assigner.generate_assignments()
                
                # Display results
                st.success("Assignments generated successfully!")
                st.subheader("New Assignments")
                st.dataframe(assignments)
                
                # Download button
                csv = assignments.to_csv(index=False)
                st.download_button(
                    label="Download Assignments CSV",
                    data=csv,
                    file_name="secret_santa_assignments.csv",
                    mime="text/csv"
                )
                
            except SecretSantaError as e:
                st.error(f"Error: {str(e)}")
            except Exception as e:
                st.error(f"Unexpected error: {str(e)}")
                st.info("If you're seeing this error, please check that your CSV files are properly formatted and not empty.")

    # Instructions
    with st.expander("📋 Instructions"):
        st.markdown("""
        ### How to use this app:
        
        1. **Upload Employee List**
           - Prepare a CSV file with two columns:
             - `Employee_Name`
             - `Employee_EmailID`
           - Make sure the CSV is not empty and properly formatted
        
        2. **Upload Previous Assignments (Optional)**
           - If you have last year's assignments, upload a CSV file with:
             - `Employee_Name`
             - `Employee_EmailID`
             - `Secret_Child_Name`
             - `Secret_Child_EmailID`
           - Make sure the CSV is not empty and properly formatted
        
        3. **Generate Assignments**
           - Click the "Generate Assignments" button
           - View the results in the table
           - Download the assignments as a CSV file
        
        ### Rules:
        - No one will be assigned to themselves
        - No one will get the same person as last year (if previous assignments provided)
        - Everyone gets exactly one Secret Child
        
        ### Sample CSV Format:
        Employee List (employees.csv):
        ```
        Employee_Name,Employee_EmailID
        John Doe,john@example.com
        Jane Smith,jane@example.com
        ```
        """)

if __name__ == "__main__":
    main() 