'use client';

import React, { ReactNode } from 'react';

interface GlassCardProps {
  children: ReactNode;
  title?: string;
  subtitle?: string;
  icon?: string;
}

export function GlassCard({ children, title, subtitle, icon }: GlassCardProps) {
  return (
    <div className="glass-card slide-up">
      {title && (
        <div className="tab-header mb-4">
          <h3 className="text-lg font-bold text-accent-teal">
            {icon} {title}
          </h3>
        </div>
      )}
      {subtitle && (
        <div className="text-text-muted text-sm mb-4">{subtitle}</div>
      )}
      {children}
    </div>
  );
}

interface MetricCardProps {
  label: string;
  value: string | number;
}

export function MetricCard({ label, value }: MetricCardProps) {
  return (
    <div className="metric-card">
      <div className="text-text-muted text-sm">{label}</div>
      <div className="text-2xl font-bold text-accent-teal">{value}</div>
    </div>
  );
}

interface TabsProps {
  tabs: { label: string; content: ReactNode }[];
}

export function Tabs({ tabs }: TabsProps) {
  const [activeTab, setActiveTab] = React.useState(0);

  return (
    <div>
      <div className="flex gap-2 mb-6 border-b border-dark-border overflow-x-auto">
        {tabs.map((tab, index) => (
          <button
            key={index}
            onClick={() => setActiveTab(index)}
            className={`px-4 py-2 whitespace-nowrap transition-all ${
              activeTab === index
                ? 'text-accent-teal border-b-2 border-accent-teal'
                : 'text-text-muted hover:text-white'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>
      <div>{tabs[activeTab].content}</div>
    </div>
  );
}

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary';
  icon?: string;
}

export function Button({
  children,
  variant = 'primary',
  icon,
  className = '',
  ...props
}: ButtonProps) {
  const baseStyles =
    'px-4 py-2 rounded-lg font-semibold transition-all inline-flex items-center gap-2';
  const variantStyles =
    variant === 'primary'
      ? 'btn-primary'
      : 'bg-dark-card border border-dark-border text-white hover:bg-dark-border';

  return (
    <button className={`${baseStyles} ${variantStyles} ${className}`} {...props}>
      {icon && <span>{icon}</span>}
      {children}
    </button>
  );
}

interface DataTableProps {
  data: any[];
  columns: string[];
}

export function DataTable({ data, columns }: DataTableProps) {
  return (
    <div className="overflow-x-auto rounded-lg">
      <table className="w-full text-sm">
        <thead>
          <tr className="bg-dark-card border-b border-dark-border">
            {columns.map((col) => (
              <th
                key={col}
                className="px-4 py-3 text-left text-accent-teal font-semibold"
              >
                {col}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, idx) => (
            <tr
              key={idx}
              className="border-b border-dark-border hover:bg-dark-card transition-colors"
            >
              {columns.map((col) => (
                <td key={col} className="px-4 py-3 text-text-muted">
                  {row[col]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
