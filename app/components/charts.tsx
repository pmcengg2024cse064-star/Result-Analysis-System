'use client';

import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Bar, Pie, Line, Radar } from 'react-chartjs-2';
import { ProcessedStudent, Statistics } from '@/lib/data-processor';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

const chartOptions = {
  responsive: true,
  maintainAspectRatio: true,
  plugins: {
    legend: {
      labels: {
        color: '#e6eef8',
      },
    },
  },
  scales: {
    y: {
      ticks: { color: '#e6eef8' },
      grid: { color: 'rgba(255,255,255,0.1)' },
    },
    x: {
      ticks: { color: '#e6eef8' },
      grid: { color: 'rgba(255,255,255,0.1)' },
    },
  },
};

export function GradeDistributionChart({ data }: { data: ProcessedStudent[] }) {
  const grades = ['A+', 'A', 'B+', 'B', 'C+', 'C', 'F'];
  const counts = grades.map(
    (grade) => data.filter((s) => s.Grade === grade).length
  );

  const chartData = {
    labels: grades,
    datasets: [
      {
        label: 'Number of Students',
        data: counts,
        backgroundColor: [
          '#10b981',
          '#34d399',
          '#6ee7b7',
          '#a7f3d0',
          '#fbbf24',
          '#f97316',
          '#ef4444',
        ],
        borderColor: '#e6eef8',
      },
    ],
  };

  return <Bar data={chartData} options={chartOptions} />;
}

export function PassFailChart({ data }: { data: ProcessedStudent[] }) {
  const passCount = data.filter((s) => s.Status === 'PASS').length;
  const failCount = data.filter((s) => s.Status === 'FAIL').length;

  const chartData = {
    labels: ['PASS', 'FAIL'],
    datasets: [
      {
        data: [passCount, failCount],
        backgroundColor: ['#10b981', '#ef4444'],
        borderColor: '#e6eef8',
      },
    ],
  };

  return (
    <div className="flex justify-center">
      <Pie data={chartData} options={chartOptions} />
    </div>
  );
}

export function AverageDistributionChart({ data }: { data: ProcessedStudent[] }) {
  const averages = data.map((s) => s.Average);
  const min = Math.floor(Math.min(...averages) / 10) * 10;
  const max = Math.ceil(Math.max(...averages) / 10) * 10;

  const bins = [];
  for (let i = min; i <= max; i += 10) {
    bins.push(`${i}-${i + 10}`);
  }

  const counts = bins.map((bin) => {
    const [start, end] = bin.split('-').map(Number);
    return averages.filter((avg) => avg >= start && avg < end).length;
  });

  const chartData = {
    labels: bins,
    datasets: [
      {
        label: 'Frequency',
        data: counts,
        backgroundColor: '#60a5fa',
        borderColor: '#e6eef8',
      },
    ],
  };

  return <Bar data={chartData} options={chartOptions} />;
}

export function SubjectPerformanceChart({ data }: { data: ProcessedStudent[] }) {
  const subjectCols = Object.keys(data[0]).filter(
    (key) =>
      !['Student_Name', 'Roll_No', 'Average', 'Grade', 'GPA', 'Status'].includes(
        key
      )
  );

  const subjectAvgs = subjectCols.map((subject) => {
    const marks = data.map((s) => parseFloat(String(s[subject])) || 0);
    return (marks.reduce((a, b) => a + b, 0) / marks.length).toFixed(2);
  });

  const chartData = {
    labels: subjectCols,
    datasets: [
      {
        label: 'Average Marks',
        data: subjectAvgs,
        backgroundColor: '#2dd4bf',
        borderColor: '#e6eef8',
      },
    ],
  };

  return <Bar data={chartData} options={chartOptions} />;
}

export function GPADistributionChart({ data }: { data: ProcessedStudent[] }) {
  const gpaValues = [4.0, 3.5, 3.0, 2.5, 2.0, 1.5, 0.0];
  const counts = gpaValues.map(
    (gpa) => data.filter((s) => s.GPA === gpa).length
  );

  const chartData = {
    labels: gpaValues.map((g) => g.toFixed(1)),
    datasets: [
      {
        label: 'Number of Students',
        data: counts,
        backgroundColor: '#6366f1',
        borderColor: '#e6eef8',
      },
    ],
  };

  return <Bar data={chartData} options={chartOptions} />;
}
