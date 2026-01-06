// Data processing utilities
export interface ProcessedStudent {
  Student_Name: string;
  Roll_No: number;
  [key: string]: string | number;
  Average: number;
  Grade: string;
  GPA: number;
  Status: 'PASS' | 'FAIL';
}

export interface Statistics {
  'Total Students': number;
  'Pass Count': number;
  'Fail Count': number;
  'Pass %': number;
  'Fail %': number;
  'Class Average': number;
  'Highest Score': number;
  'Lowest Score': number;
  'Class GPA': number;
}

const PASS_MARKS = 40;
const MIN_MARKS = 0;
const MAX_MARKS = 100;

const GRADE_CUTOFFS: Record<string, number> = {
  'A+': 90,
  'A': 80,
  'B+': 70,
  'B': 60,
  'C+': 50,
  'C': 40,
  'F': 0,
};

export function getGrade(marks: number): string {
  const sortedCutoffs = Object.entries(GRADE_CUTOFFS).sort((a, b) => b[1] - a[1]);
  for (const [grade, cutoff] of sortedCutoffs) {
    if (marks >= cutoff) return grade;
  }
  return 'F';
}

export function calculateGPA(marks: number): number {
  if (marks >= 90) return 4.0;
  if (marks >= 80) return 3.5;
  if (marks >= 70) return 3.0;
  if (marks >= 60) return 2.5;
  if (marks >= 50) return 2.0;
  if (marks >= 40) return 1.5;
  return 0.0;
}

export function processExcelData(data: any[]): ProcessedStudent[] {
  if (!data || data.length === 0) return [];

  const processed = data.map((row: any) => {
    const studentName = row['Student_Name'] || row['studentName'] || '';
    const rollNo = row['Roll_No'] || row['rollNo'] || '';

    // Get all subject columns
    const subjectCols = Object.keys(row).filter(
      (key) => !['Student_Name', 'Roll_No', 'studentName', 'rollNo'].includes(key)
    );

    // Calculate average
    const marks = subjectCols.map((col) => parseFloat(row[col]) || 0);
    const average = marks.length > 0 ? marks.reduce((a, b) => a + b, 0) / marks.length : 0;

    const grade = getGrade(average);
    const gpa = calculateGPA(average);
    const status = average >= PASS_MARKS ? 'PASS' : 'FAIL';

    return {
      Student_Name: studentName,
      Roll_No: parseInt(rollNo),
      ...row,
      Average: parseFloat(average.toFixed(2)),
      Grade: grade,
      GPA: parseFloat(gpa.toFixed(2)),
      Status: status,
    };
  });

  return processed;
}

export function getStatistics(data: ProcessedStudent[]): Statistics {
  const total = data.length;
  const passCount = data.filter((s) => s.Status === 'PASS').length;
  const failCount = data.filter((s) => s.Status === 'FAIL').length;

  const averages = data.map((s) => s.Average);
  const gpas = data.map((s) => s.GPA);

  return {
    'Total Students': total,
    'Pass Count': passCount,
    'Fail Count': failCount,
    'Pass %': total > 0 ? (passCount / total) * 100 : 0,
    'Fail %': total > 0 ? (failCount / total) * 100 : 0,
    'Class Average': averages.length > 0 ? parseFloat((averages.reduce((a, b) => a + b, 0) / averages.length).toFixed(2)) : 0,
    'Highest Score': averages.length > 0 ? Math.max(...averages) : 0,
    'Lowest Score': averages.length > 0 ? Math.min(...averages) : 0,
    'Class GPA': gpas.length > 0 ? parseFloat((gpas.reduce((a, b) => a + b, 0) / gpas.length).toFixed(2)) : 0,
  };
}

export function getToppers(data: ProcessedStudent[], topN: number = 5): ProcessedStudent[] {
  return [...data]
    .sort((a, b) => b.Average - a.Average)
    .slice(0, topN);
}

export function getWeakSubjects(data: ProcessedStudent[]): Record<string, number> {
  if (data.length === 0) return {};

  const subjectCols = Object.keys(data[0]).filter(
    (key) => !['Student_Name', 'Roll_No', 'Average', 'Grade', 'GPA', 'Status'].includes(key)
  );

  const subjectAvgs: Record<string, number> = {};

  for (const subject of subjectCols) {
    const marks = data.map((s) => parseFloat(String(s[subject])) || 0);
    subjectAvgs[subject] = marks.length > 0 ? parseFloat((marks.reduce((a, b) => a + b, 0) / marks.length).toFixed(2)) : 0;
  }

  return Object.fromEntries(
    Object.entries(subjectAvgs).sort((a, b) => a[1] - b[1])
  );
}

export function getStrongSubjects(data: ProcessedStudent[]): Record<string, number> {
  if (data.length === 0) return {};

  const subjectCols = Object.keys(data[0]).filter(
    (key) => !['Student_Name', 'Roll_No', 'Average', 'Grade', 'GPA', 'Status'].includes(key)
  );

  const subjectAvgs: Record<string, number> = {};

  for (const subject of subjectCols) {
    const marks = data.map((s) => parseFloat(String(s[subject])) || 0);
    subjectAvgs[subject] = marks.length > 0 ? parseFloat((marks.reduce((a, b) => a + b, 0) / marks.length).toFixed(2)) : 0;
  }

  return Object.fromEntries(
    Object.entries(subjectAvgs).sort((a, b) => b[1] - a[1])
  );
}
