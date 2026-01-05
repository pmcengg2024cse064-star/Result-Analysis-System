"""
Data Processing Module
Handles data validation, calculations for grades, GPA, and pass/fail status
"""

import pandas as pd
import numpy as np
from typing import Tuple, Dict, List

# Configuration constants
PASS_MARKS = 40
MIN_MARKS = 0
MAX_MARKS = 100

# Grade cutoff points (in ascending order)
GRADE_CUTOFFS = {
    'A+': 90,
    'A': 80,
    'B+': 70,
    'B': 60,
    'C+': 50,
    'C': 40,
    'F': 0
}


class DataProcessor:
    """Handle data validation and processing for exam results"""
    
    def __init__(self):
        """Initialize the data processor"""
        self.df = None
        self.validation_errors = []
    
    def load_excel(self, file_path: str) -> Tuple[bool, str]:
        """
        Load Excel file with validation
        
        Args:
            file_path: Path to Excel file
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            self.df = pd.read_excel(file_path)
            
            # Basic validation
            if self.df.empty:
                return False, "File is empty"
            
            if 'Student_Name' not in self.df.columns or 'Roll_No' not in self.df.columns:
                return False, "Required columns 'Student_Name' and 'Roll_No' not found"
            
            return True, "File loaded successfully"
        except Exception as e:
            return False, f"Error loading file: {str(e)}"
    
    def validate_data(self) -> Tuple[bool, List[str]]:
        """
        Validate data quality
        
        Returns:
            Tuple of (is_valid: bool, errors: List[str])
        """
        self.validation_errors = []
        
        if self.df is None:
            return False, ["No data loaded"]
        
        # Check for required columns
        required_cols = ['Student_Name', 'Roll_No']
        subject_cols = [col for col in self.df.columns if col not in required_cols]
        
        if not subject_cols:
            self.validation_errors.append("No subject columns found (only Student_Name and Roll_No)")
            return False, self.validation_errors
        
        # Check for missing values
        missing_mask = self.df[subject_cols].isna().any(axis=1)
        if missing_mask.any():
            missing_students = self.df[missing_mask]['Student_Name'].tolist()
            self.validation_errors.append(
                f"Missing marks for students: {', '.join(missing_students)}"
            )
        
        # Check for invalid marks (not in 0-100 range)
        for col in subject_cols:
            invalid_mask = (self.df[col] < MIN_MARKS) | (self.df[col] > MAX_MARKS)
            if invalid_mask.any():
                invalid_students = self.df[invalid_mask]['Student_Name'].tolist()
                self.validation_errors.append(
                    f"Invalid marks in {col} for: {', '.join(invalid_students)}"
                )
        
        return len(self.validation_errors) == 0, self.validation_errors
    
    def calculate_grades(self) -> pd.DataFrame:
        """
        Calculate grades for all students based on average marks
        
        Returns:
            DataFrame with student data and calculated grades
        """
        if self.df is None:
            return None
        
        df_result = self.df.copy()
        
        # Get subject columns (all except Student_Name and Roll_No)
        subject_cols = [col for col in df_result.columns 
                       if col not in ['Student_Name', 'Roll_No']]
        
        # Calculate average marks
        df_result['Average'] = df_result[subject_cols].mean(axis=1)
        
        # Calculate GPA (assuming 4.0 scale)
        df_result['GPA'] = df_result['Average'].apply(self._calculate_gpa)
        
        # Assign grades
        df_result['Grade'] = df_result['Average'].apply(self._get_grade)
        
        # Determine pass/fail (average >= 40)
        df_result['Status'] = df_result['Average'].apply(
            lambda x: 'PASS' if x >= PASS_MARKS else 'FAIL'
        )
        
        self.df = df_result
        return df_result
    
    def _get_grade(self, marks: float) -> str:
        """
        Determine grade based on marks
        
        Args:
            marks: Average marks
            
        Returns:
            Grade letter
        """
        for grade, cutoff in sorted(GRADE_CUTOFFS.items(), 
                                   key=lambda x: x[1], reverse=True):
            if marks >= cutoff:
                return grade
        return 'F'
    
    def _calculate_gpa(self, marks: float) -> float:
        """
        Calculate GPA on 4.0 scale (90-100: 4.0, 0-10: 0.0)
        
        Args:
            marks: Average marks
            
        Returns:
            GPA value
        """
        if marks >= 90:
            return 4.0
        elif marks >= 80:
            return 3.5
        elif marks >= 70:
            return 3.0
        elif marks >= 60:
            return 2.5
        elif marks >= 50:
            return 2.0
        elif marks >= 40:
            return 1.5
        else:
            return 0.0
    
    def get_subject_columns(self) -> List[str]:
        """
        Get list of subject columns (excluding Student_Name and Roll_No)
        
        Returns:
            List of subject column names
        """
        if self.df is None:
            return []
        return [col for col in self.df.columns 
               if col not in ['Student_Name', 'Roll_No', 'Average', 'GPA', 'Grade', 'Status']]
    
    def get_processed_data(self) -> pd.DataFrame:
        """
        Get the processed data with all calculations
        
        Returns:
            Processed DataFrame
        """
        return self.df
