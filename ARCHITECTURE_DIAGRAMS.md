# 🏗️ Architecture & Flow Diagrams

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    USER'S BROWSER                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │         React Application (Next.js)                 │   │
│  ├──────────────────────────────────────────────────────┤   │
│  │                                                      │   │
│  │  Dashboard Component                                │   │
│  │  ├─ Upload Section                                  │   │
│  │  │  └─ File Input → Excel Parser → Validator       │   │
│  │  │                                                  │   │
│  │  ├─ Analysis Section                               │   │
│  │  │  ├─ Statistics Cards                            │   │
│  │  │  ├─ Tabs                                         │   │
│  │  │  │  ├─ Top Performers Tab → DataTable          │   │
│  │  │  │  ├─ Subject Analysis Tab → DataTable         │   │
│  │  │  │  ├─ Charts Tab → Chart.js Components        │   │
│  │  │  │  └─ Student Data Tab → Filter → DataTable   │   │
│  │  │  └─ Data Processor Functions                   │   │
│  │  │                                                  │   │
│  │  └─ Report Section                                 │   │
│  │     ├─ CSV Generator                               │   │
│  │     ├─ PDF Generator                               │   │
│  │     └─ Export Buttons                              │   │
│  │                                                      │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  Data Processing (Client-Side - No Server!)               │
│  ├─ data-processor.ts                                      │
│  │  ├─ processExcelData()                                 │
│  │  ├─ getStatistics()                                    │
│  │  ├─ getToppers()                                       │
│  │  ├─ getWeakSubjects()                                  │
│  │  └─ getStrongSubjects()                                │
│  ├─ excel-handler.ts                                       │
│  │  ├─ parseExcelFile()                                   │
│  │  ├─ validateData()                                     │
│  │  └─ downloadSampleExcel()                              │
│  └─ report-generator.ts                                    │
│     ├─ generatePDFReport()                                │
│     └─ generateCSV()                                      │
│                                                              │
│  Styling (Tailwind CSS)                                     │
│  ├─ globals.css                                             │
│  └─ Dark Glassmorphism Theme                               │
│                                                              │
└─────────────────────────────────────────────────────────────┘
         ↓↓↓ DEPLOYMENT ↓↓↓
┌─────────────────────────────────────────────────────────────┐
│                    VERCEL HOSTING                           │
│  (Global CDN + Serverless + Auto-scaling)                   │
└─────────────────────────────────────────────────────────────┘
```

---

## Data Flow Diagram

```
┌────────────────────────────────────────────────────────────┐
│  1. USER UPLOADS EXCEL FILE                                │
└────────────────────────────────────────────────────────────┘
                        ↓
┌────────────────────────────────────────────────────────────┐
│  2. BROWSER READS FILE (FileReader API)                    │
│     Excel file → Raw binary data                           │
└────────────────────────────────────────────────────────────┘
                        ↓
┌────────────────────────────────────────────────────────────┐
│  3. PARSE EXCEL (XLSX.js library)                          │
│     Binary → JSON array of objects                         │
│     [                                                       │
│       { Student_Name, Roll_No, Math, English, ... },      │
│       { ... }                                              │
│     ]                                                      │
└────────────────────────────────────────────────────────────┘
                        ↓
┌────────────────────────────────────────────────────────────┐
│  4. VALIDATE DATA                                          │
│     ✓ Check required columns exist                        │
│     ✓ Check marks in 0-100 range                          │
│     ✓ Check no missing values                             │
│     If errors → Display errors                            │
└────────────────────────────────────────────────────────────┘
                        ↓ (If valid)
┌────────────────────────────────────────────────────────────┐
│  5. PROCESS DATA                                           │
│     For each student:                                     │
│     ├─ Calculate Average = sum(marks) / count             │
│     ├─ getGrade(Average) → A+, A, B+, B, C+, C, F        │
│     ├─ calculateGPA(Average) → 0.0 to 4.0 scale         │
│     └─ Status = "PASS" if Average >= 40, else "FAIL"     │
└────────────────────────────────────────────────────────────┘
                        ↓
┌────────────────────────────────────────────────────────────┐
│  6. CALCULATE STATISTICS                                   │
│     ├─ Total Students                                     │
│     ├─ Pass Count / Fail Count                            │
│     ├─ Pass % / Fail %                                    │
│     ├─ Class Average                                      │
│     ├─ Highest Score / Lowest Score                       │
│     └─ Class GPA                                          │
└────────────────────────────────────────────────────────────┘
                        ↓
┌────────────────────────────────────────────────────────────┐
│  7. GENERATE ANALYTICS                                     │
│     ├─ getToppers() → Top 10 students                    │
│     ├─ getStrongSubjects() → Best performing subjects    │
│     ├─ getWeakSubjects() → Lowest performing subjects    │
│     └─ Subject-wise averages                             │
└────────────────────────────────────────────────────────────┘
                        ↓
┌────────────────────────────────────────────────────────────┐
│  8. RENDER VISUALIZATIONS                                  │
│     ├─ Grade Distribution Chart (Bar)                     │
│     ├─ Pass/Fail Distribution (Pie)                       │
│     ├─ Average Marks Distribution (Histogram)             │
│     ├─ Subject Performance (Bar)                          │
│     └─ GPA Distribution (Bar)                             │
│                                                            │
│     Using Chart.js + react-chartjs-2                     │
└────────────────────────────────────────────────────────────┘
                        ↓
┌────────────────────────────────────────────────────────────┐
│  9. USER ACTIONS                                           │
│     ├─ View Statistics Cards                              │
│     ├─ Click Tabs to explore data                         │
│     ├─ Filter students by Pass/Fail                       │
│     └─ Download reports                                   │
└────────────────────────────────────────────────────────────┘
                        ↓
┌────────────────────────────────────────────────────────────┐
│  10. EXPORT DATA                                           │
│      ├─ CSV Export                                         │
│      │  └─ Convert to CSV format → Download              │
│      │                                                     │
│      └─ PDF Export                                        │
│         ├─ HTML to Canvas (html2canvas)                  │
│         ├─ Canvas to Image                               │
│         ├─ Image to PDF (jsPDF)                          │
│         └─ Download                                       │
└────────────────────────────────────────────────────────────┘
                        ↓
┌────────────────────────────────────────────────────────────┐
│  11. FILES DOWNLOADED TO USER'S DEVICE                     │
│      ✓ exam_results.csv                                   │
│      ✓ exam_report_TIMESTAMP.pdf                          │
└────────────────────────────────────────────────────────────┘
```

---

## Component Hierarchy

```
Page (app/page.tsx)
│
└─ Dashboard Component (app/components/dashboard.tsx)
   │
   ├─ State Management
   │  ├─ currentStep: 'upload' | 'analysis' | 'report'
   │  ├─ rawData: any[] | null
   │  ├─ processedData: ProcessedStudent[] | null
   │  ├─ statistics: Statistics | null
   │  ├─ validationErrors: string[]
   │  ├─ isLoading: boolean
   │  └─ filterStatus: 'All' | 'PASS' | 'FAIL'
   │
   ├─ Header Section
   │  ├─ Main Title
   │  └─ Subtitle
   │
   ├─ Navigation Tabs
   │  ├─ 📤 Upload Tab Button
   │  ├─ 📈 Analysis Tab Button
   │  └─ 📄 Report Tab Button
   │
   ├─ Upload Section (UploadSection Component)
   │  ├─ GlassCard Component
   │  │  ├─ Instructions Text
   │  │  └─ Sample Download Button
   │  ├─ File Input
   │  ├─ Error Display (if any)
   │  └─ Data Preview Table
   │
   ├─ Analysis Section (AnalysisSection Component)
   │  ├─ GlassCard (Statistics)
   │  │  └─ MetricCard Components (Grid)
   │  │     ├─ Class Average
   │  │     ├─ Class GPA
   │  │     ├─ Highest Score
   │  │     └─ Lowest Score
   │  │
   │  └─ Tabs Component (4 tabs)
   │     │
   │     ├─ Tab 1: Top Performers
   │     │  └─ DataTable Component
   │     │
   │     ├─ Tab 2: Subject Analysis
   │     │  ├─ DataTable (Strong Subjects)
   │     │  └─ DataTable (Weak Subjects)
   │     │
   │     ├─ Tab 3: Charts
   │     │  ├─ GradeDistributionChart
   │     │  ├─ PassFailChart
   │     │  ├─ AverageDistributionChart
   │     │  ├─ SubjectPerformanceChart
   │     │  └─ GPADistributionChart
   │     │
   │     └─ Tab 4: Student Data
   │        ├─ Filter Dropdown
   │        └─ DataTable Component
   │
   └─ Report Section (ReportSection Component)
      ├─ Export Buttons
      │  ├─ Download CSV Button
      │  └─ Download PDF Button
      │
      └─ Report Preview (id="pdf-report")
         ├─ GlassCard
         │  ├─ Title
         │  ├─ Generation Date
         │  ├─ Statistics Section
         │  │  └─ MetricCard Components
         │  ├─ Top Performers Section
         │  │  └─ DataTable
         │  └─ Subject Performance Section
         │     └─ DataTable
         │
         └─ (This HTML is converted to PDF for download)
```

---

## State Flow Diagram

```
┌──────────────────────┐
│   Initial State      │
│  ├─ processedData: null
│  ├─ statistics: null
│  ├─ currentStep: 'upload'
│  └─ validationErrors: []
└──────────────────────┘
         ↓
┌──────────────────────┐
│  User Uploads File   │
│  onFileUpload()      │
│  ├─ setIsLoading(true)
│  ├─ parseExcelFile()
│  ├─ validateData()
│  └─ processExcelData()
└──────────────────────┘
         ↓
    [Is Valid?]
     /      \
    Y        N
    ↓        ↓
   ✓       Error
   │     Display
   ↓     Errors
┌──────────────────────┐
│  Set State          │
│  ├─ rawData         │
│  ├─ processedData   │
│  ├─ statistics      │
│  └─ currentStep:    │
│     'analysis'      │
└──────────────────────┘
         ↓
┌──────────────────────┐
│  Show Analysis Tab   │
│  ├─ Display metrics  │
│  ├─ Render charts    │
│  ├─ Show top 10      │
│  └─ Subject analysis │
└──────────────────────┘
         ↓
    [User Action?]
    /    |     \
   ↓     ↓      ↓
Export Filter Report
Chart  Data   Data
 ↓      ↓     ↓
CSV PDF Filter Report
    |     |     |
    ↓     ↓     ↓
  File  Update  PDF
Download Done  File
```

---

## File Dependencies

```
app/page.tsx
└─ components/dashboard.tsx
   ├─ components/ui.tsx
   │  └─ (Reusable UI components)
   │
   ├─ components/charts.tsx
   │  ├─ lib/data-processor.ts
   │  └─ (Chart.js + react-chartjs-2)
   │
   ├─ lib/data-processor.ts
   │  └─ (Core business logic)
   │
   ├─ lib/excel-handler.ts
   │  └─ (XLSX library)
   │
   └─ lib/report-generator.ts
      ├─ (jsPDF library)
      ├─ (html2canvas library)
      └─ lib/data-processor.ts
```

---

## Processing Pipeline

```
Input
  │
  ├─→ Excel File
  │
Excel Handler (excel-handler.ts)
  │
  ├─→ parseExcelFile() → Raw JSON
  │
  ├─→ validateData() → Validation Report
  │      │
  │      [Valid?]
  │      │
  │      ├─ Yes → Continue
  │      └─ No → Show Errors
  │
Data Processor (data-processor.ts)
  │
  ├─→ processExcelData() → Add calculations
  │      │
  │      For each student:
  │      ├─ Average = mean(marks)
  │      ├─ Grade = getGrade(average)
  │      ├─ GPA = calculateGPA(average)
  │      └─ Status = getStatus(average)
  │
  ├─→ getStatistics() → Class metrics
  │
  ├─→ getToppers() → Top 10 students
  │
  ├─→ getWeakSubjects() → Weak subjects
  │
  └─→ getStrongSubjects() → Strong subjects
      │
Display (Dashboard Component)
  │
  ├─→ Render Cards
  │
  ├─→ Render Tables
  │
  ├─→ Render Charts
  │
  └─→ Enable Exports
      │
Report Generator (report-generator.ts)
  │
  ├─→ generateCSV() → CSV format
  │      │
  │      └─→ downloadCSV() → Browser download
  │
  └─→ generatePDFReport() → PDF format
      │
      └─→ Browser download

Output
  │
  ├─ CSV file (exam_results.csv)
  │
  └─ PDF file (exam_report_TIMESTAMP.pdf)
```

---

## Deployment Flow

```
┌─ Local Development ─┐
│  npm run dev        │
│  http://localhost   │
│  Edit & auto-reload │
└─────────────────────┘
         │
         ↓
┌─ Git Repository ─┐
│  git add .        │
│  git commit       │
│  git push origin  │
│  (to GitHub)      │
└───────────────────┘
         │
         ↓
┌─ Vercel Deployment ─┐
│  Auto-detects       │
│  Framework: Next.js │
│  Install: npm i     │
│  Build: npm run build
│  Deploy: Live! ✓    │
└─────────────────────┘
         │
         ↓
┌─ Global CDN ───┐
│  https://      │
│  your-app      │
│  .vercel.app   │
└─────────────────┘
         │
         ↓
┌─ User Accesses ─┐
│  Opens URL      │
│  Uses app       │
│  Exports data   │
└─────────────────┘
```

---

These diagrams show:
1. **System Architecture** - Overall structure
2. **Data Flow** - How data moves through the app
3. **Component Hierarchy** - UI structure
4. **State Flow** - User interactions
5. **File Dependencies** - How files relate
6. **Processing Pipeline** - Data transformation
7. **Deployment** - How it gets to production

All these work together to create a complete Exam Result Analysis System! 🎉
