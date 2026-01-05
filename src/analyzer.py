"""
Analytics Module
Performs student-wise and subject-wise analysis with visualizations
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple
import os


class Analyzer:
    """Perform analytics on exam results"""
    
    def __init__(self, df: pd.DataFrame, output_dir: str = "outputs/charts"):
        """
        Initialize analyzer
        
        Args:
            df: Processed DataFrame with calculations
            output_dir: Directory to save charts
        """
        self.df = df
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def get_toppers(self, top_n: int = 5) -> pd.DataFrame:
        """
        Get top performing students
        
        Args:
            top_n: Number of top students to return
            
        Returns:
            DataFrame of top students
        """
        return self.df.nlargest(top_n, 'Average')[
            ['Student_Name', 'Roll_No', 'Average', 'Grade', 'GPA', 'Status']
        ]
    
    def get_weak_subjects(self) -> Dict[str, float]:
        """
        Identify subjects with lowest average marks
        
        Returns:
            Dictionary with subject names and their averages
        """
        subject_cols = [col for col in self.df.columns 
                       if col not in ['Student_Name', 'Roll_No', 'Average', 'GPA', 'Grade', 'Status']]
        
        subject_avgs = {}
        for subject in subject_cols:
            subject_avgs[subject] = self.df[subject].mean()
        
        # Sort by average (lowest first)
        return dict(sorted(subject_avgs.items(), key=lambda x: x[1]))
    
    def get_strong_subjects(self) -> Dict[str, float]:
        """
        Identify subjects with highest average marks
        
        Returns:
            Dictionary with subject names and their averages
        """
        subject_cols = [col for col in self.df.columns 
                       if col not in ['Student_Name', 'Roll_No', 'Average', 'GPA', 'Grade', 'Status']]
        
        subject_avgs = {}
        for subject in subject_cols:
            subject_avgs[subject] = self.df[subject].mean()
        
        # Sort by average (highest first)
        return dict(sorted(subject_avgs.items(), key=lambda x: x[1], reverse=True))
    
    def get_statistics(self) -> Dict[str, float]:
        """
        Get overall statistics
        
        Returns:
            Dictionary with statistics
        """
        return {
            'Total Students': len(self.df),
            'Pass Count': len(self.df[self.df['Status'] == 'PASS']),
            'Fail Count': len(self.df[self.df['Status'] == 'FAIL']),
            'Pass %': (len(self.df[self.df['Status'] == 'PASS']) / len(self.df) * 100),
            'Fail %': (len(self.df[self.df['Status'] == 'FAIL']) / len(self.df) * 100),
            'Class Average': self.df['Average'].mean(),
            'Highest Score': self.df['Average'].max(),
            'Lowest Score': self.df['Average'].min(),
            'Class GPA': self.df['GPA'].mean()
        }
    
    def plot_grade_distribution(self) -> str:
        """
        Create grade distribution chart
        
        Returns:
            Path to saved chart
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        grade_counts = self.df['Grade'].value_counts().sort_index(ascending=False)
        colors = plt.cm.RdYlGn(np.linspace(0.2, 0.8, len(grade_counts)))
        
        grade_counts.plot(kind='bar', ax=ax, color=colors)
        ax.set_title('Grade Distribution', fontsize=14, fontweight='bold')
        ax.set_xlabel('Grade', fontsize=12)
        ax.set_ylabel('Number of Students', fontsize=12)
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        file_path = os.path.join(self.output_dir, 'grade_distribution.png')
        plt.savefig(file_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return file_path
    
    def plot_pass_fail_distribution(self) -> str:
        """
        Create pass/fail distribution pie chart
        
        Returns:
            Path to saved chart
        """
        fig, ax = plt.subplots(figsize=(8, 6))
        
        status_counts = self.df['Status'].value_counts()
        colors = ['#90EE90', '#FFB6C6']
        
        ax.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%',
               startangle=90, colors=colors, textprops={'fontsize': 12})
        ax.set_title('Pass/Fail Distribution', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        file_path = os.path.join(self.output_dir, 'pass_fail_distribution.png')
        plt.savefig(file_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return file_path
    
    def plot_average_marks_distribution(self) -> str:
        """
        Create histogram of average marks distribution
        
        Returns:
            Path to saved chart
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        ax.hist(self.df['Average'], bins=15, color='skyblue', edgecolor='black', alpha=0.7)
        ax.axvline(self.df['Average'].mean(), color='red', linestyle='--', 
                   linewidth=2, label=f"Mean: {self.df['Average'].mean():.2f}")
        ax.axvline(self.df['Average'].median(), color='green', linestyle='--', 
                   linewidth=2, label=f"Median: {self.df['Average'].median():.2f}")
        
        ax.set_title('Distribution of Average Marks', fontsize=14, fontweight='bold')
        ax.set_xlabel('Average Marks', fontsize=12)
        ax.set_ylabel('Frequency', fontsize=12)
        ax.legend()
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        file_path = os.path.join(self.output_dir, 'average_distribution.png')
        plt.savefig(file_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return file_path
    
    def plot_subject_performance(self) -> str:
        """
        Create subject-wise performance comparison chart
        
        Returns:
            Path to saved chart
        """
        subject_cols = [col for col in self.df.columns 
                       if col not in ['Student_Name', 'Roll_No', 'Average', 'GPA', 'Grade', 'Status']]
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        subject_avgs = {subject: self.df[subject].mean() for subject in subject_cols}
        subjects = list(subject_avgs.keys())
        averages = list(subject_avgs.values())
        
        colors = ['#FF6B6B' if avg < 50 else '#FFA500' if avg < 70 else '#4ECDC4' 
                  for avg in averages]
        
        ax.bar(subjects, averages, color=colors, edgecolor='black', alpha=0.8)
        ax.axhline(y=40, color='red', linestyle='--', linewidth=2, label='Pass Marks (40)')
        ax.set_title('Subject-wise Average Performance', fontsize=14, fontweight='bold')
        ax.set_xlabel('Subject', fontsize=12)
        ax.set_ylabel('Average Marks', fontsize=12)
        ax.set_ylim(0, 100)
        ax.legend()
        ax.grid(axis='y', alpha=0.3)
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        file_path = os.path.join(self.output_dir, 'subject_performance.png')
        plt.savefig(file_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return file_path
    
    def plot_gpa_distribution(self) -> str:
        """
        Create GPA distribution chart
        
        Returns:
            Path to saved chart
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        gpa_counts = self.df['GPA'].value_counts().sort_index(ascending=False)
        colors = plt.cm.viridis(np.linspace(0, 1, len(gpa_counts)))
        
        gpa_counts.plot(kind='barh', ax=ax, color=colors)
        ax.set_title('GPA Distribution', fontsize=14, fontweight='bold')
        ax.set_xlabel('Number of Students', fontsize=12)
        ax.set_ylabel('GPA', fontsize=12)
        ax.grid(axis='x', alpha=0.3)
        
        plt.tight_layout()
        file_path = os.path.join(self.output_dir, 'gpa_distribution.png')
        plt.savefig(file_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return file_path
    
    def generate_all_charts(self) -> Dict[str, str]:
        """
        Generate all analysis charts
        
        Returns:
            Dictionary with chart names and file paths
        """
        charts = {
            'grade_distribution': self.plot_grade_distribution(),
            'pass_fail_distribution': self.plot_pass_fail_distribution(),
            'average_distribution': self.plot_average_marks_distribution(),
            'subject_performance': self.plot_subject_performance(),
            'gpa_distribution': self.plot_gpa_distribution()
        }
        
        return charts
