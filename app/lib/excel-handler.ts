import * as XLSX from 'xlsx';
import { ProcessedStudent } from './data-processor';

export async function parseExcelFile(file: File): Promise<any[]> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();

    reader.onload = (e) => {
      try {
        const data = e.target?.result;
        const workbook = XLSX.read(data, { type: 'array' });
        const firstSheetName = workbook.SheetNames[0];
        const worksheet = workbook.Sheets[firstSheetName];
        const jsonData = XLSX.utils.sheet_to_json(worksheet);
        resolve(jsonData);
      } catch (error) {
        reject(error);
      }
    };

    reader.onerror = () => {
      reject(new Error('Failed to read file'));
    };

    reader.readAsArrayBuffer(file);
  });
}

export function validateData(data: any[]): { isValid: boolean; errors: string[] } {
  const errors: string[] = [];

  if (!data || data.length === 0) {
    errors.push('File is empty');
    return { isValid: false, errors };
  }

  // Check for required columns
  const firstRow = data[0];
  const hasStudentName = 'Student_Name' in firstRow || 'studentName' in firstRow;
  const hasRollNo = 'Roll_No' in firstRow || 'rollNo' in firstRow;

  if (!hasStudentName || !hasRollNo) {
    errors.push('Required columns: Student_Name and Roll_No');
  }

  // Check for subject columns
  const subjectCols = Object.keys(firstRow).filter(
    (key) => !['Student_Name', 'Roll_No', 'studentName', 'rollNo'].includes(key)
  );

  if (subjectCols.length === 0) {
    errors.push('No subject columns found (only Student_Name and Roll_No)');
  }

  // Check for missing values and invalid marks
  data.forEach((row, index) => {
    subjectCols.forEach((col) => {
      const value = row[col];
      if (value === null || value === undefined || value === '') {
        errors.push(`Missing marks for ${row['Student_Name']} in ${col}`);
      } else {
        const num = parseFloat(value);
        if (isNaN(num) || num < 0 || num > 100) {
          errors.push(`Invalid marks for ${row['Student_Name']} in ${col}: ${value}`);
        }
      }
    });
  });

  return {
    isValid: errors.length === 0,
    errors: [...new Set(errors)], // Remove duplicates
  };
}

export function createSampleExcel(): Blob {
  const sampleData = [
    {
      Student_Name: 'Aarav Patel',
      Roll_No: 101,
      Math: 92,
      English: 88,
      Science: 95,
      History: 85,
      Computer: 89,
    },
    {
      Student_Name: 'Bhavna Singh',
      Roll_No: 102,
      Math: 78,
      English: 92,
      Science: 85,
      History: 88,
      Computer: 80,
    },
    {
      Student_Name: 'Chirag Verma',
      Roll_No: 103,
      Math: 85,
      English: 79,
      Science: 92,
      History: 78,
      Computer: 95,
    },
    {
      Student_Name: 'Deepika Nair',
      Roll_No: 104,
      Math: 88,
      English: 85,
      Science: 80,
      History: 92,
      Computer: 87,
    },
    {
      Student_Name: 'Esha Sharma',
      Roll_No: 105,
      Math: 95,
      English: 90,
      Science: 88,
      History: 87,
      Computer: 91,
    },
    {
      Student_Name: 'Fahad Khan',
      Roll_No: 106,
      Math: 72,
      English: 76,
      Science: 75,
      History: 70,
      Computer: 82,
    },
    {
      Student_Name: 'Gita Desai',
      Roll_No: 107,
      Math: 81,
      English: 88,
      Science: 90,
      History: 84,
      Computer: 86,
    },
    {
      Student_Name: 'Harsh Gupta',
      Roll_No: 108,
      Math: 89,
      English: 82,
      Science: 86,
      History: 80,
      Computer: 93,
    },
    {
      Student_Name: 'Isha Reddy',
      Roll_No: 109,
      Math: 76,
      English: 94,
      Science: 85,
      History: 88,
      Computer: 79,
    },
    {
      Student_Name: 'Jatin Malhotra',
      Roll_No: 110,
      Math: 84,
      English: 87,
      Science: 91,
      History: 86,
      Computer: 89,
    },
  ];

  const worksheet = XLSX.utils.json_to_sheet(sampleData);
  const workbook = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(workbook, worksheet, 'Marks');

  const buf = XLSX.write(workbook, { bookType: 'xlsx', type: 'array' });
  return new Blob([buf], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
}

export function downloadSampleExcel(): void {
  const blob = createSampleExcel();
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = 'sample_marks.xlsx';
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}
