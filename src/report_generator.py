"""
PDF Report Generator Module
Generates professional PDF reports with charts and analytics
"""

import os
import pandas as pd
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime


class PDFReportGenerator:
    """Generate professional PDF reports for exam results"""
    
    def __init__(self, output_dir: str = "outputs/reports"):
        """
        Initialize PDF generator
        
        Args:
            output_dir: Directory to save PDF reports
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def generate_report(self, df: pd.DataFrame, stats: dict, 
                       toppers: pd.DataFrame, weak_subjects: dict,
                       strong_subjects: dict, chart_paths: dict) -> str:
        """
        Generate comprehensive PDF report
        
        Args:
            df: Processed DataFrame
            stats: Statistics dictionary
            toppers: Top performers DataFrame
            weak_subjects: Dictionary of weak subjects
            strong_subjects: Dictionary of strong subjects
            chart_paths: Dictionary of chart file paths
            
        Returns:
            Path to generated PDF file
        """
        # Create PDF document
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        pdf_filename = os.path.join(self.output_dir, f"exam_report_{timestamp}.pdf")
        
        doc = SimpleDocTemplate(pdf_filename, pagesize=letter,
                               rightMargin=0.5*inch, leftMargin=0.5*inch,
                               topMargin=0.5*inch, bottomMargin=0.5*inch)
        
        # Create story for PDF content
        story = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1f4788'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#1f4788'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        )
        
        # Title
        title = Paragraph("EXAM RESULT ANALYSIS REPORT", title_style)
        story.append(title)
        
        # Report metadata
        metadata_text = f"Generated on {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
        metadata = Paragraph(metadata_text, styles['Normal'])
        story.append(metadata)
        story.append(Spacer(1, 0.3*inch))
        
        # Statistics section
        story.append(Paragraph("OVERALL STATISTICS", heading_style))
        stats_data = [['Metric', 'Value']]
        for metric, value in stats.items():
            if 'Count' in metric or 'Students' in metric:
                stats_data.append([metric, str(int(value))])
            elif '%' in metric:
                stats_data.append([metric, f"{value:.2f}%"])
            else:
                stats_data.append([metric, f"{value:.2f}"])
        
        stats_table = Table(stats_data, colWidths=[3*inch, 2*inch])
        stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
        ]))
        story.append(stats_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Top Performers section
        story.append(Paragraph("TOP PERFORMERS", heading_style))
        toppers_data = [['Rank', 'Student Name', 'Roll No', 'Average', 'Grade', 'GPA']]
        for idx, row in enumerate(toppers.itertuples(), 1):
            toppers_data.append([
                str(idx),
                row.Student_Name,
                str(row.Roll_No),
                f"{row.Average:.2f}",
                row.Grade,
                f"{row.GPA:.2f}"
            ])
        
        toppers_table = Table(toppers_data, colWidths=[0.7*inch, 2*inch, 1*inch, 1*inch, 0.7*inch, 0.7*inch])
        toppers_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#28a745')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
        ]))
        story.append(toppers_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Strong Subjects section
        story.append(Paragraph("STRONG SUBJECTS (Highest Average Performance)", heading_style))
        strong_data = [['Subject', 'Average Marks']]
        for subject, avg in list(strong_subjects.items())[:5]:
            strong_data.append([subject, f"{avg:.2f}"])
        
        strong_table = Table(strong_data, colWidths=[3*inch, 2*inch])
        strong_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#17a2b8')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
        ]))
        story.append(strong_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Weak Subjects section
        story.append(Paragraph("WEAK SUBJECTS (Lowest Average Performance)", heading_style))
        weak_data = [['Subject', 'Average Marks']]
        for subject, avg in list(weak_subjects.items())[:5]:
            weak_data.append([subject, f"{avg:.2f}"])
        
        weak_table = Table(weak_data, colWidths=[3*inch, 2*inch])
        weak_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#dc3545')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
        ]))
        story.append(weak_table)
        
        # Add page break before charts
        story.append(PageBreak())
        story.append(Paragraph("PERFORMANCE ANALYSIS CHARTS", heading_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Add charts (if they exist)
        if chart_paths:
            # Limit image width for better layout
            img_width = 5 * inch
            img_height = 3 * inch
            
            if 'grade_distribution' in chart_paths and os.path.exists(chart_paths['grade_distribution']):
                img = Image(chart_paths['grade_distribution'], width=img_width, height=img_height)
                story.append(img)
                story.append(Spacer(1, 0.2*inch))
            
            if 'pass_fail_distribution' in chart_paths and os.path.exists(chart_paths['pass_fail_distribution']):
                img = Image(chart_paths['pass_fail_distribution'], width=img_width, height=img_height)
                story.append(img)
                story.append(Spacer(1, 0.2*inch))
            
            story.append(PageBreak())
            
            if 'subject_performance' in chart_paths and os.path.exists(chart_paths['subject_performance']):
                img = Image(chart_paths['subject_performance'], width=img_width, height=img_height)
                story.append(img)
                story.append(Spacer(1, 0.2*inch))
            
            if 'average_distribution' in chart_paths and os.path.exists(chart_paths['average_distribution']):
                img = Image(chart_paths['average_distribution'], width=img_width, height=img_height)
                story.append(img)
                story.append(Spacer(1, 0.2*inch))
            
            if 'gpa_distribution' in chart_paths and os.path.exists(chart_paths['gpa_distribution']):
                img = Image(chart_paths['gpa_distribution'], width=img_width, height=img_height)
                story.append(img)
        
        # Build PDF
        doc.build(story)
        
        return pdf_filename
