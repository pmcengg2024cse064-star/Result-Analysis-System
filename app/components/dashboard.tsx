'use client';

import React, { useState, useCallback } from 'react';
import { GlassCard, Button, DataTable, MetricCard, Tabs } from './ui';
import { parseExcelFile, validateData, downloadSampleExcel } from '@/lib/excel-handler';
import {
  processExcelData,
  getStatistics,
  ProcessedStudent,
  Statistics,
  getToppers,
  getWeakSubjects,
  getStrongSubjects,
} from '@/lib/data-processor';
import {
  GradeDistributionChart,
  PassFailChart,
  AverageDistributionChart,
  SubjectPerformanceChart,
  GPADistributionChart,
} from './charts';
import { generateCSV, downloadCSV, generatePDFReport } from '@/lib/report-generator';

type AppStep = 'upload' | 'analysis' | 'report';

export default function Dashboard() {
  const [currentStep, setCurrentStep] = useState<AppStep>('upload');
  const [rawData, setRawData] = useState<any[] | null>(null);
  const [processedData, setProcessedData] = useState<ProcessedStudent[] | null>(null);
  const [statistics, setStatistics] = useState<Statistics | null>(null);
  const [validationErrors, setValidationErrors] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [filterStatus, setFilterStatus] = useState<'All' | 'PASS' | 'FAIL'>('All');

  const handleFileUpload = useCallback(
    async (event: React.ChangeEvent<HTMLInputElement>) => {
      const file = event.target.files?.[0];
      if (!file) return;

      setIsLoading(true);
      try {
        const data = await parseExcelFile(file);
        const validation = validateData(data);

        if (!validation.isValid) {
          setValidationErrors(validation.errors);
          return;
        }

        setRawData(data);
        setValidationErrors([]);

        // Process data
        const processed = processExcelData(data);
        setProcessedData(processed);
        const stats = getStatistics(processed);
        setStatistics(stats);

        setCurrentStep('analysis');
      } catch (error) {
        setValidationErrors([
          'Error reading file. Please ensure it is a valid Excel file.',
        ]);
      } finally {
        setIsLoading(false);
      }
    },
    []
  );

  const filteredData =
    !processedData || filterStatus === 'All'
      ? processedData
      : processedData.filter((s) => s.Status === filterStatus);

  return (
    <div className="min-h-screen bg-gradient-to-b from-[#071026] to-[#081226] text-white">
      {/* Header */}
      <div className="text-center py-12 px-4">
        <h1 className="main-header">📊 Exam Result Processing System</h1>
        <p className="text-text-muted">Automated analysis, analytics & reporting</p>
      </div>

      {/* Navigation Tabs */}
      <div className="max-w-6xl mx-auto px-4 mb-8">
        <div className="flex gap-4 justify-center mb-8">
          {(['upload', 'analysis', 'report'] as AppStep[]).map((step, idx) => (
            <button
              key={step}
              onClick={() => {
                if (step === 'upload') setCurrentStep(step);
                else if (step === 'analysis' && processedData)
                  setCurrentStep(step);
                else if (step === 'report' && processedData)
                  setCurrentStep(step);
              }}
              disabled={step !== 'upload' && !processedData}
              className={`px-6 py-2 rounded-lg font-semibold transition-all ${
                currentStep === step
                  ? 'bg-accent-teal text-dark-bg'
                  : 'bg-dark-card border border-dark-border text-text-muted'
              } disabled:opacity-50 disabled:cursor-not-allowed`}
            >
              {['📤 Upload', '📈 Analysis', '📄 Report'][idx]}
            </button>
          ))}
        </div>
      </div>

      {/* Content */}
      <div className="max-w-6xl mx-auto px-4 pb-16">
        {currentStep === 'upload' && <UploadSection onFileUpload={handleFileUpload} isLoading={isLoading} errors={validationErrors} rawData={rawData} />}

        {currentStep === 'analysis' && processedData && statistics && (
          <AnalysisSection
            data={processedData}
            stats={statistics}
            filteredData={filteredData}
            filterStatus={filterStatus}
            onFilterChange={setFilterStatus}
          />
        )}

        {currentStep === 'report' && processedData && statistics && (
          <ReportSection data={processedData} stats={statistics} />
        )}
      </div>
    </div>
  );
}

function UploadSection({
  onFileUpload,
  isLoading,
  errors,
  rawData,
}: {
  onFileUpload: (e: React.ChangeEvent<HTMLInputElement>) => void;
  isLoading: boolean;
  errors: string[];
  rawData: any[] | null;
}) {
  return (
    <div className="space-y-6">
      <GlassCard
        title="📥 Upload & Validate Data"
        subtitle="Upload an Excel file with student marks"
        icon="📥"
      >
        <div className="grid md:grid-cols-2 gap-6">
          <div>
            <p className="text-text-muted mb-4">
              Upload an Excel file (.xlsx) with the following format:
            </p>
            <ul className="space-y-2 text-sm text-text-muted mb-6">
              <li>
                <strong>Column 1:</strong> Student_Name
              </li>
              <li>
                <strong>Column 2:</strong> Roll_No
              </li>
              <li>
                <strong>Columns 3+:</strong> Subject marks (0-100)
              </li>
            </ul>
            <p className="text-sm text-accent-teal mb-4">
              Example: Math, English, Science, History, Computer
            </p>
          </div>

          <div className="flex flex-col gap-4 justify-start">
            <Button
              onClick={() => downloadSampleExcel()}
              icon="📥"
              variant="secondary"
            >
              Download Sample Format
            </Button>

            <label className="cursor-pointer">
              <input
                type="file"
                accept=".xlsx"
                onChange={onFileUpload}
                disabled={isLoading}
                className="hidden"
              />
              <div className="glass-card border-2 border-dashed border-dark-border p-6 text-center hover:border-accent-teal transition-colors">
                <div className="text-4xl mb-2">📁</div>
                <p className="font-semibold">
                  {isLoading ? 'Processing...' : 'Click to upload Excel file'}
                </p>
              </div>
            </label>
          </div>
        </div>
      </GlassCard>

      {errors.length > 0 && (
        <GlassCard title="⚠️ Validation Errors">
          <div className="space-y-2">
            {errors.map((error, idx) => (
              <div key={idx} className="text-red-400 text-sm">
                • {error}
              </div>
            ))}
          </div>
        </GlassCard>
      )}

      {rawData && (
        <GlassCard title="✅ Data Preview" subtitle="Loaded from file">
          <div className="overflow-x-auto text-xs">
            <DataTable
              data={rawData.slice(0, 5)}
              columns={Object.keys(rawData[0])}
            />
          </div>
          {rawData.length > 5 && (
            <p className="text-text-muted text-sm mt-2">
              Showing 5 of {rawData.length} records
            </p>
          )}
        </GlassCard>
      )}
    </div>
  );
}

function AnalysisSection({
  data,
  stats,
  filteredData,
  filterStatus,
  onFilterChange,
}: {
  data: ProcessedStudent[];
  stats: Statistics;
  filteredData: ProcessedStudent[] | null;
  filterStatus: 'All' | 'PASS' | 'FAIL';
  onFilterChange: (status: 'All' | 'PASS' | 'FAIL') => void;
}) {
  const toppers = getToppers(data, 10);
  const weakSubjects = getWeakSubjects(data);
  const strongSubjects = getStrongSubjects(data);

  return (
    <div className="space-y-6">
      {/* Statistics */}
      <GlassCard title="✨ Overall Statistics" icon="✨">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <MetricCard label="Class Average" value={stats['Class Average'].toFixed(2)} />
          <MetricCard label="Class GPA" value={stats['Class GPA'].toFixed(2)} />
          <MetricCard label="Highest Score" value={stats['Highest Score'].toFixed(2)} />
          <MetricCard label="Lowest Score" value={stats['Lowest Score'].toFixed(2)} />
        </div>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mt-4">
          <MetricCard label="Pass Rate" value={`${stats['Pass %'].toFixed(1)}%`} />
          <MetricCard label="Total Students" value={stats['Total Students']} />
          <MetricCard label="Pass Count" value={stats['Pass Count']} />
        </div>
      </GlassCard>

      {/* Tabs */}
      <Tabs
        tabs={[
          {
            label: '🏅 Top Performers',
            content: (
              <GlassCard>
                <DataTable
                  data={toppers}
                  columns={[
                    'Student_Name',
                    'Roll_No',
                    'Average',
                    'Grade',
                    'GPA',
                    'Status',
                  ]}
                />
              </GlassCard>
            ),
          },
          {
            label: '📚 Subject Analysis',
            content: (
              <div className="grid md:grid-cols-2 gap-6">
                <GlassCard title="Strong Subjects" icon="📈">
                  <DataTable
                    data={Object.entries(strongSubjects)
                      .slice(0, 5)
                      .map(([subject, avg]) => ({
                        Subject: subject,
                        'Average Marks': avg.toFixed(2),
                      }))}
                    columns={['Subject', 'Average Marks']}
                  />
                </GlassCard>
                <GlassCard title="Weak Subjects" icon="📉">
                  <DataTable
                    data={Object.entries(weakSubjects)
                      .slice(0, 5)
                      .map(([subject, avg]) => ({
                        Subject: subject,
                        'Average Marks': avg.toFixed(2),
                      }))}
                    columns={['Subject', 'Average Marks']}
                  />
                </GlassCard>
              </div>
            ),
          },
          {
            label: '📊 Charts',
            content: (
              <div className="grid md:grid-cols-2 gap-6">
                <GlassCard>
                  <GradeDistributionChart data={data} />
                </GlassCard>
                <GlassCard>
                  <PassFailChart data={data} />
                </GlassCard>
                <GlassCard>
                  <AverageDistributionChart data={data} />
                </GlassCard>
                <GlassCard>
                  <SubjectPerformanceChart data={data} />
                </GlassCard>
              </div>
            ),
          },
          {
            label: '📋 Student Data',
            content: (
              <GlassCard>
                <div className="mb-4">
                  <select
                    value={filterStatus}
                    onChange={(e) =>
                      onFilterChange(e.target.value as 'All' | 'PASS' | 'FAIL')
                    }
                    className="bg-dark-card border border-dark-border text-white px-4 py-2 rounded-lg"
                  >
                    <option value="All">All</option>
                    <option value="PASS">PASS</option>
                    <option value="FAIL">FAIL</option>
                  </select>
                </div>
                {filteredData && (
                  <DataTable
                    data={filteredData}
                    columns={['Student_Name', 'Roll_No', 'Average', 'Grade', 'Status']}
                  />
                )}
              </GlassCard>
            ),
          },
        ]}
      />
    </div>
  );
}

function ReportSection({
  data,
  stats,
}: {
  data: ProcessedStudent[];
  stats: Statistics;
}) {
  const handleDownloadCSV = async () => {
    const csv = await generateCSV(data);
    downloadCSV(csv, 'exam_results.csv');
  };

  const handleDownloadPDF = async () => {
    const reportElement = document.getElementById('pdf-report');
    if (reportElement) {
      await generatePDFReport(reportElement, 'exam_report.pdf');
    }
  };

  return (
    <div className="space-y-6">
      <GlassCard
        title="📄 Generate Reports"
        subtitle="Export data in multiple formats"
        icon="📄"
      >
        <div className="flex gap-4 flex-wrap">
          <Button onClick={handleDownloadCSV} icon="📥">
            Download CSV
          </Button>
          <Button onClick={handleDownloadPDF} icon="📥">
            Download PDF
          </Button>
        </div>
      </GlassCard>

      <div id="pdf-report" className="space-y-6 p-6 bg-dark-bg">
        <GlassCard title="📊 Exam Analysis Report" icon="📄">
          <p className="text-text-muted mb-4">
            Generated on {new Date().toLocaleDateString()}
          </p>

          <h3 className="subheader-style">Overall Statistics</h3>
          <div className="grid md:grid-cols-4 gap-4 mb-6">
            <MetricCard label="Total Students" value={stats['Total Students']} />
            <MetricCard label="Class Average" value={stats['Class Average'].toFixed(2)} />
            <MetricCard label="Pass Rate" value={`${stats['Pass %'].toFixed(1)}%`} />
            <MetricCard label="Class GPA" value={stats['Class GPA'].toFixed(2)} />
          </div>

          <h3 className="subheader-style">Top 5 Performers</h3>
          <DataTable
            data={getToppers(data, 5)}
            columns={['Student_Name', 'Roll_No', 'Average', 'Grade', 'GPA']}
          />

          <h3 className="subheader-style mt-6">Subject Performance</h3>
          <DataTable
            data={Object.entries(getStrongSubjects(data))
              .slice(0, 5)
              .map(([subject, avg]) => ({
                Subject: subject,
                'Average Marks': avg.toFixed(2),
              }))}
            columns={['Subject', 'Average Marks']}
          />
        </GlassCard>
      </div>
    </div>
  );
}
