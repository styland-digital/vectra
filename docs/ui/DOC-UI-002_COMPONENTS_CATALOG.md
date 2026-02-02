# VECTRA - CATALOGUE COMPOSANTS UI (SUITE)
## Component Library Reference - Part 2
### Version 1.0 | 14 Janvier 2026

---

## 4. COMPOSANTS DE DONNÉES (SUITE)

### 4.1 DataTable (Complet)

```tsx
// components/ui/data-table.tsx
'use client';

import * as React from 'react';
import {
  ColumnDef,
  ColumnFiltersState,
  SortingState,
  VisibilityState,
  flexRender,
  getCoreRowModel,
  getFilteredRowModel,
  getPaginationRowModel,
  getSortedRowModel,
  useReactTable,
} from '@tanstack/react-table';
import { ArrowUpDown, ChevronDown, Search, SlidersHorizontal } from 'lucide-react';

import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import {
  DropdownMenu,
  DropdownMenuCheckboxItem,
  DropdownMenuContent,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';

interface DataTableProps<TData, TValue> {
  columns: ColumnDef<TData, TValue>[];
  data: TData[];
  searchKey?: string;
  searchPlaceholder?: string;
  pageSize?: number;
  showColumnToggle?: boolean;
  showPagination?: boolean;
  onRowClick?: (row: TData) => void;
  emptyState?: React.ReactNode;
  loading?: boolean;
}

export function DataTable<TData, TValue>({
  columns,
  data,
  searchKey,
  searchPlaceholder = 'Search...',
  pageSize = 10,
  showColumnToggle = true,
  showPagination = true,
  onRowClick,
  emptyState,
  loading = false,
}: DataTableProps<TData, TValue>) {
  const [sorting, setSorting] = React.useState<SortingState>([]);
  const [columnFilters, setColumnFilters] = React.useState<ColumnFiltersState>([]);
  const [columnVisibility, setColumnVisibility] = React.useState<VisibilityState>({});
  const [rowSelection, setRowSelection] = React.useState({});

  const table = useReactTable({
    data,
    columns,
    onSortingChange: setSorting,
    onColumnFiltersChange: setColumnFilters,
    getCoreRowModel: getCoreRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    onColumnVisibilityChange: setColumnVisibility,
    onRowSelectionChange: setRowSelection,
    state: {
      sorting,
      columnFilters,
      columnVisibility,
      rowSelection,
    },
    initialState: {
      pagination: { pageSize },
    },
  });

  return (
    <div className="space-y-4">
      {/* Toolbar */}
      <div className="flex items-center justify-between gap-4">
        {/* Search */}
        {searchKey && (
          <div className="relative w-64">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-text-muted" />
            <Input
              placeholder={searchPlaceholder}
              value={(table.getColumn(searchKey)?.getFilterValue() as string) ?? ''}
              onChange={(e) =>
                table.getColumn(searchKey)?.setFilterValue(e.target.value)
              }
              className="pl-9"
            />
          </div>
        )}
        
        {/* Column Toggle */}
        {showColumnToggle && (
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="secondary" size="sm">
                <SlidersHorizontal className="h-4 w-4 mr-2" />
                Columns
                <ChevronDown className="h-4 w-4 ml-2" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" className="w-48">
              {table
                .getAllColumns()
                .filter((column) => column.getCanHide())
                .map((column) => (
                  <DropdownMenuCheckboxItem
                    key={column.id}
                    className="capitalize"
                    checked={column.getIsVisible()}
                    onCheckedChange={(value) => column.toggleVisibility(!!value)}
                  >
                    {column.id}
                  </DropdownMenuCheckboxItem>
                ))}
            </DropdownMenuContent>
          </DropdownMenu>
        )}
      </div>

      {/* Table */}
      <div className="rounded-lg border border-border-primary overflow-hidden">
        <table className="w-full">
          <thead className="bg-surface-secondary">
            {table.getHeaderGroups().map((headerGroup) => (
              <tr key={headerGroup.id}>
                {headerGroup.headers.map((header) => (
                  <th
                    key={header.id}
                    className="px-4 py-3 text-left text-xs font-medium text-text-secondary uppercase tracking-wider"
                  >
                    {header.isPlaceholder ? null : (
                      <div
                        className={cn(
                          'flex items-center gap-2',
                          header.column.getCanSort() &&
                            'cursor-pointer select-none hover:text-text-primary'
                        )}
                        onClick={header.column.getToggleSortingHandler()}
                      >
                        {flexRender(
                          header.column.columnDef.header,
                          header.getContext()
                        )}
                        {header.column.getCanSort() && (
                          <ArrowUpDown className="h-3.5 w-3.5" />
                        )}
                      </div>
                    )}
                  </th>
                ))}
              </tr>
            ))}
          </thead>
          <tbody className="divide-y divide-border-secondary">
            {loading ? (
              // Loading skeleton
              Array.from({ length: pageSize }).map((_, i) => (
                <tr key={i}>
                  {columns.map((_, j) => (
                    <td key={j} className="px-4 py-4">
                      <div className="h-4 bg-surface-secondary rounded animate-pulse" />
                    </td>
                  ))}
                </tr>
              ))
            ) : table.getRowModel().rows?.length ? (
              table.getRowModel().rows.map((row) => (
                <tr
                  key={row.id}
                  className={cn(
                    'transition-colors',
                    onRowClick && 'cursor-pointer hover:bg-surface-hover',
                    row.getIsSelected() && 'bg-primary-50 dark:bg-primary-950/20'
                  )}
                  onClick={() => onRowClick?.(row.original)}
                >
                  {row.getVisibleCells().map((cell) => (
                    <td
                      key={cell.id}
                      className="px-4 py-4 text-sm text-text-primary"
                    >
                      {flexRender(cell.column.columnDef.cell, cell.getContext())}
                    </td>
                  ))}
                </tr>
              ))
            ) : (
              <tr>
                <td
                  colSpan={columns.length}
                  className="h-48 text-center text-text-secondary"
                >
                  {emptyState || 'No results.'}
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      {showPagination && (
        <div className="flex items-center justify-between">
          <p className="text-sm text-text-secondary">
            Showing{' '}
            {table.getState().pagination.pageIndex * pageSize + 1}-
            {Math.min(
              (table.getState().pagination.pageIndex + 1) * pageSize,
              table.getFilteredRowModel().rows.length
            )}{' '}
            of {table.getFilteredRowModel().rows.length} results
          </p>
          <div className="flex items-center gap-2">
            <Button
              variant="secondary"
              size="sm"
              onClick={() => table.previousPage()}
              disabled={!table.getCanPreviousPage()}
            >
              Previous
            </Button>
            <Button
              variant="secondary"
              size="sm"
              onClick={() => table.nextPage()}
              disabled={!table.getCanNextPage()}
            >
              Next
            </Button>
          </div>
        </div>
      )}
    </div>
  );
}

// Column helper for sortable header
export function SortableHeader({ column, title }: { column: any; title: string }) {
  return (
    <Button
      variant="ghost"
      size="sm"
      className="-ml-3 h-8"
      onClick={() => column.toggleSorting(column.getIsSorted() === 'asc')}
    >
      {title}
      <ArrowUpDown className="ml-2 h-3.5 w-3.5" />
    </Button>
  );
}
```

### 4.2 Stats Card

```tsx
// components/features/analytics/stats-card.tsx
import * as React from 'react';
import { TrendingUp, TrendingDown, Minus } from 'lucide-react';
import { cn } from '@/lib/utils';
import { Card } from '@/components/ui/card';

interface StatsCardProps {
  title: string;
  value: string | number;
  change?: {
    value: string;
    type: 'positive' | 'negative' | 'neutral';
  };
  trend?: number[]; // For sparkline
  icon?: React.ElementType;
  description?: string;
  loading?: boolean;
}

export function StatsCard({
  title,
  value,
  change,
  trend,
  icon: Icon,
  description,
  loading = false,
}: StatsCardProps) {
  if (loading) {
    return (
      <Card className="p-6">
        <div className="space-y-3">
          <div className="h-4 w-24 bg-surface-secondary rounded animate-pulse" />
          <div className="h-8 w-32 bg-surface-secondary rounded animate-pulse" />
          <div className="h-3 w-20 bg-surface-secondary rounded animate-pulse" />
        </div>
      </Card>
    );
  }

  return (
    <Card className="p-6 hover:border-border-hover transition-colors">
      <div className="flex items-start justify-between">
        <div className="space-y-2">
          {/* Title */}
          <p className="text-sm font-medium text-text-secondary">{title}</p>
          
          {/* Value */}
          <p className="text-3xl font-semibold text-text-primary tracking-tight">
            {typeof value === 'number' ? value.toLocaleString() : value}
          </p>
          
          {/* Change indicator */}
          {change && (
            <div
              className={cn(
                'flex items-center gap-1 text-sm font-medium',
                change.type === 'positive' && 'text-success-500',
                change.type === 'negative' && 'text-error-500',
                change.type === 'neutral' && 'text-text-secondary'
              )}
            >
              {change.type === 'positive' && <TrendingUp className="h-4 w-4" />}
              {change.type === 'negative' && <TrendingDown className="h-4 w-4" />}
              {change.type === 'neutral' && <Minus className="h-4 w-4" />}
              <span>{change.value}</span>
              <span className="text-text-muted font-normal">vs last period</span>
            </div>
          )}
          
          {/* Description */}
          {description && (
            <p className="text-xs text-text-muted">{description}</p>
          )}
        </div>
        
        {/* Icon */}
        {Icon && (
          <div className="p-3 rounded-lg bg-primary-100 dark:bg-primary-900/20">
            <Icon className="h-5 w-5 text-primary-500" />
          </div>
        )}
      </div>
      
      {/* Sparkline trend */}
      {trend && trend.length > 0 && (
        <div className="mt-4 h-12">
          <Sparkline data={trend} />
        </div>
      )}
    </Card>
  );
}

// Simple Sparkline component
function Sparkline({ data }: { data: number[] }) {
  const max = Math.max(...data);
  const min = Math.min(...data);
  const range = max - min || 1;
  
  const points = data
    .map((value, i) => {
      const x = (i / (data.length - 1)) * 100;
      const y = 100 - ((value - min) / range) * 100;
      return `${x},${y}`;
    })
    .join(' ');

  return (
    <svg
      viewBox="0 0 100 100"
      preserveAspectRatio="none"
      className="w-full h-full"
    >
      <polyline
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
        points={points}
        className="text-primary-500"
      />
    </svg>
  );
}
```

### 4.3 Chart Card

```tsx
// components/features/analytics/chart-card.tsx
'use client';

import * as React from 'react';
import {
  LineChart,
  Line,
  AreaChart,
  Area,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from 'recharts';
import { Card, CardHeader, CardContent } from '@/components/ui/card';
import { cn } from '@/lib/utils';

interface ChartCardProps {
  title: string;
  description?: string;
  data: any[];
  type?: 'line' | 'area' | 'bar';
  dataKey: string;
  xAxisKey?: string;
  color?: string;
  showGrid?: boolean;
  showLegend?: boolean;
  height?: number;
  className?: string;
}

export function ChartCard({
  title,
  description,
  data,
  type = 'line',
  dataKey,
  xAxisKey = 'name',
  color = 'var(--color-primary-500)',
  showGrid = true,
  showLegend = false,
  height = 300,
  className,
}: ChartCardProps) {
  const ChartComponent = {
    line: LineChart,
    area: AreaChart,
    bar: BarChart,
  }[type];

  const DataComponent = {
    line: Line,
    area: Area,
    bar: Bar,
  }[type];

  return (
    <Card className={cn('overflow-hidden', className)}>
      <CardHeader className="pb-2">
        <h3 className="text-lg font-medium text-text-primary">{title}</h3>
        {description && (
          <p className="text-sm text-text-secondary">{description}</p>
        )}
      </CardHeader>
      <CardContent className="pt-0">
        <ResponsiveContainer width="100%" height={height}>
          <ChartComponent data={data}>
            {showGrid && (
              <CartesianGrid
                strokeDasharray="3 3"
                stroke="var(--border-secondary)"
                vertical={false}
              />
            )}
            <XAxis
              dataKey={xAxisKey}
              axisLine={false}
              tickLine={false}
              tick={{ fill: 'var(--text-secondary)', fontSize: 12 }}
              dy={10}
            />
            <YAxis
              axisLine={false}
              tickLine={false}
              tick={{ fill: 'var(--text-secondary)', fontSize: 12 }}
              dx={-10}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: 'var(--surface-primary)',
                border: '1px solid var(--border-primary)',
                borderRadius: '8px',
                boxShadow: 'var(--shadow-lg)',
              }}
              labelStyle={{ color: 'var(--text-primary)' }}
            />
            {showLegend && <Legend />}
            {type === 'line' && (
              <Line
                type="monotone"
                dataKey={dataKey}
                stroke={color}
                strokeWidth={2}
                dot={false}
                activeDot={{ r: 4, fill: color }}
              />
            )}
            {type === 'area' && (
              <Area
                type="monotone"
                dataKey={dataKey}
                stroke={color}
                strokeWidth={2}
                fill={color}
                fillOpacity={0.1}
              />
            )}
            {type === 'bar' && (
              <Bar
                dataKey={dataKey}
                fill={color}
                radius={[4, 4, 0, 0]}
              />
            )}
          </ChartComponent>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}
```

---

## 5. COMPOSANTS SPÉCIFIQUES VECTRA

### 5.1 BANT Score Display

```tsx
// components/features/leads/bant-score-display.tsx
import * as React from 'react';
import { cn } from '@/lib/utils';
import { Tooltip, TooltipContent, TooltipTrigger } from '@/components/ui/tooltip';

interface BANTBreakdown {
  budget: number;
  authority: number;
  need: number;
  timeline: number;
}

interface BANTScoreDisplayProps {
  score: number;
  breakdown?: BANTBreakdown;
  size?: 'sm' | 'md' | 'lg';
  showBreakdown?: boolean;
}

export function BANTScoreDisplay({
  score,
  breakdown,
  size = 'md',
  showBreakdown = true,
}: BANTScoreDisplayProps) {
  const getScoreStatus = (score: number) => {
    if (score >= 70) return { label: 'Qualified', color: 'success' };
    if (score >= 50) return { label: 'Review', color: 'warning' };
    return { label: 'Not Qualified', color: 'error' };
  };

  const status = getScoreStatus(score);
  
  const sizeClasses = {
    sm: 'w-10 h-10 text-sm',
    md: 'w-14 h-14 text-xl',
    lg: 'w-20 h-20 text-3xl',
  };
  
  const colorClasses = {
    success: 'bg-success-100 text-success-700 dark:bg-success-900/30 dark:text-success-400',
    warning: 'bg-warning-100 text-warning-700 dark:bg-warning-900/30 dark:text-warning-400',
    error: 'bg-error-100 text-error-700 dark:bg-error-900/30 dark:text-error-400',
  };

  const criteriaLabels = [
    { key: 'budget', label: 'Budget', icon: '💰' },
    { key: 'authority', label: 'Authority', icon: '👤' },
    { key: 'need', label: 'Need', icon: '🎯' },
    { key: 'timeline', label: 'Timeline', icon: '⏰' },
  ];

  return (
    <div className="space-y-4">
      {/* Main Score Circle */}
      <div className="flex items-center gap-4">
        <Tooltip>
          <TooltipTrigger>
            <div
              className={cn(
                'rounded-full flex items-center justify-center font-bold',
                sizeClasses[size],
                colorClasses[status.color as keyof typeof colorClasses]
              )}
            >
              {score}
            </div>
          </TooltipTrigger>
          <TooltipContent>
            <p>BANT Score: {score}/100</p>
            <p className="text-xs text-text-muted">{status.label}</p>
          </TooltipContent>
        </Tooltip>
        
        <div>
          <p className="font-medium text-text-primary">{status.label}</p>
          <p className="text-sm text-text-secondary">BANT Score</p>
        </div>
      </div>

      {/* Breakdown bars */}
      {showBreakdown && breakdown && (
        <div className="grid grid-cols-2 gap-3">
          {criteriaLabels.map(({ key, label, icon }) => {
            const value = breakdown[key as keyof BANTBreakdown];
            const percentage = (value / 25) * 100;
            
            return (
              <div key={key} className="space-y-1.5">
                <div className="flex items-center justify-between text-xs">
                  <span className="flex items-center gap-1 text-text-secondary">
                    <span>{icon}</span>
                    {label}
                  </span>
                  <span className="font-medium text-text-primary">
                    {value}/25
                  </span>
                </div>
                <div className="h-1.5 rounded-full bg-surface-secondary overflow-hidden">
                  <div
                    className={cn(
                      'h-full rounded-full transition-all duration-500',
                      percentage >= 60 && 'bg-success-500',
                      percentage >= 40 && percentage < 60 && 'bg-warning-500',
                      percentage < 40 && 'bg-error-500'
                    )}
                    style={{ width: `${percentage}%` }}
                  />
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
```

### 5.2 Campaign Card

```tsx
// components/features/campaigns/campaign-card.tsx
import * as React from 'react';
import Link from 'next/link';
import { formatDistanceToNow } from 'date-fns';
import { 
  MoreHorizontal, 
  Play, 
  Pause, 
  Users, 
  Mail, 
  Calendar,
  TrendingUp 
} from 'lucide-react';
import { cn } from '@/lib/utils';
import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';

interface Campaign {
  id: string;
  name: string;
  status: 'draft' | 'active' | 'paused' | 'completed';
  target_criteria: {
    job_titles: string[];
    industries: string[];
  };
  stats: {
    leads_found: number;
    leads_qualified: number;
    emails_sent: number;
    meetings_booked: number;
  };
  created_at: string;
  updated_at: string;
}

interface CampaignCardProps {
  campaign: Campaign;
  onStatusChange?: (campaignId: string, status: 'active' | 'paused') => void;
}

const statusConfig = {
  draft: { label: 'Draft', variant: 'default' as const },
  active: { label: 'Active', variant: 'success' as const },
  paused: { label: 'Paused', variant: 'warning' as const },
  completed: { label: 'Completed', variant: 'primary' as const },
};

export function CampaignCard({ campaign, onStatusChange }: CampaignCardProps) {
  const status = statusConfig[campaign.status];
  const conversionRate = campaign.stats.leads_found > 0
    ? ((campaign.stats.meetings_booked / campaign.stats.leads_found) * 100).toFixed(1)
    : '0';

  return (
    <Card className="group hover:border-border-hover transition-all duration-200">
      <div className="p-6">
        {/* Header */}
        <div className="flex items-start justify-between mb-4">
          <div className="space-y-1">
            <Link 
              href={`/campaigns/${campaign.id}`}
              className="font-semibold text-text-primary hover:text-primary-500 transition-colors"
            >
              {campaign.name}
            </Link>
            <p className="text-sm text-text-secondary">
              {campaign.target_criteria.job_titles.slice(0, 2).join(', ')}
              {campaign.target_criteria.job_titles.length > 2 && ' +more'}
            </p>
          </div>
          
          <div className="flex items-center gap-2">
            <Badge variant={status.variant}>{status.label}</Badge>
            
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" size="icon-sm">
                  <MoreHorizontal className="h-4 w-4" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end">
                {campaign.status === 'active' && (
                  <DropdownMenuItem onClick={() => onStatusChange?.(campaign.id, 'paused')}>
                    <Pause className="h-4 w-4 mr-2" />
                    Pause Campaign
                  </DropdownMenuItem>
                )}
                {campaign.status === 'paused' && (
                  <DropdownMenuItem onClick={() => onStatusChange?.(campaign.id, 'active')}>
                    <Play className="h-4 w-4 mr-2" />
                    Resume Campaign
                  </DropdownMenuItem>
                )}
                <DropdownMenuItem>Edit</DropdownMenuItem>
                <DropdownMenuItem>Duplicate</DropdownMenuItem>
                <DropdownMenuItem className="text-error-500">Delete</DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-4 gap-4 mb-4">
          <div className="text-center p-3 rounded-lg bg-surface-secondary">
            <Users className="h-4 w-4 mx-auto mb-1 text-text-muted" />
            <p className="text-lg font-semibold text-text-primary">
              {campaign.stats.leads_found}
            </p>
            <p className="text-xs text-text-secondary">Leads</p>
          </div>
          <div className="text-center p-3 rounded-lg bg-surface-secondary">
            <TrendingUp className="h-4 w-4 mx-auto mb-1 text-text-muted" />
            <p className="text-lg font-semibold text-text-primary">
              {campaign.stats.leads_qualified}
            </p>
            <p className="text-xs text-text-secondary">Qualified</p>
          </div>
          <div className="text-center p-3 rounded-lg bg-surface-secondary">
            <Mail className="h-4 w-4 mx-auto mb-1 text-text-muted" />
            <p className="text-lg font-semibold text-text-primary">
              {campaign.stats.emails_sent}
            </p>
            <p className="text-xs text-text-secondary">Sent</p>
          </div>
          <div className="text-center p-3 rounded-lg bg-surface-secondary">
            <Calendar className="h-4 w-4 mx-auto mb-1 text-text-muted" />
            <p className="text-lg font-semibold text-text-primary">
              {campaign.stats.meetings_booked}
            </p>
            <p className="text-xs text-text-secondary">Meetings</p>
          </div>
        </div>

        {/* Footer */}
        <div className="flex items-center justify-between pt-4 border-t border-border-secondary">
          <p className="text-xs text-text-muted">
            Updated {formatDistanceToNow(new Date(campaign.updated_at), { addSuffix: true })}
          </p>
          <div className="flex items-center gap-1 text-xs">
            <span className="text-text-secondary">Conversion:</span>
            <span className={cn(
              'font-medium',
              parseFloat(conversionRate) >= 2 && 'text-success-500',
              parseFloat(conversionRate) < 2 && parseFloat(conversionRate) >= 1 && 'text-warning-500',
              parseFloat(conversionRate) < 1 && 'text-error-500'
            )}>
              {conversionRate}%
            </span>
          </div>
        </div>
      </div>
    </Card>
  );
}
```

### 5.3 Email Preview Card

```tsx
// components/features/emails/email-preview-card.tsx
'use client';

import * as React from 'react';
import { formatDistanceToNow } from 'date-fns';
import { Check, X, Pencil, RefreshCw, User, Building2 } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { cn } from '@/lib/utils';
import { Card, CardHeader, CardContent, CardFooter } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';

interface Email {
  id: string;
  recipient: {
    name: string;
    email: string;
    company: string;
    job_title: string;
  };
  subject: string;
  body: string;
  status: 'pending' | 'approved' | 'rejected' | 'sent';
  bant_score: number;
  generated_at: string;
}

interface EmailPreviewCardProps {
  email: Email;
  onApprove?: (id: string) => void;
  onReject?: (id: string) => void;
  onEdit?: (id: string) => void;
  onRegenerate?: (id: string) => void;
}

export function EmailPreviewCard({
  email,
  onApprove,
  onReject,
  onEdit,
  onRegenerate,
}: EmailPreviewCardProps) {
  const [isExpanded, setIsExpanded] = React.useState(false);
  const [isActioning, setIsActioning] = React.useState(false);

  const handleApprove = async () => {
    setIsActioning(true);
    await onApprove?.(email.id);
    setIsActioning(false);
  };

  const handleReject = async () => {
    setIsActioning(true);
    await onReject?.(email.id);
    setIsActioning(false);
  };

  const statusColors = {
    pending: 'warning',
    approved: 'success',
    rejected: 'error',
    sent: 'primary',
  } as const;

  return (
    <motion.div
      layout
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -10 }}
    >
      <Card className={cn(
        'transition-all duration-200',
        email.status === 'pending' && 'border-warning-500/50'
      )}>
        {/* Header */}
        <CardHeader className="pb-3">
          <div className="flex items-start justify-between">
            <div className="flex items-center gap-3">
              <Avatar className="h-10 w-10">
                <AvatarFallback className="bg-primary-100 text-primary-700">
                  {email.recipient.name.split(' ').map(n => n[0]).join('')}
                </AvatarFallback>
              </Avatar>
              <div>
                <p className="font-medium text-text-primary">
                  {email.recipient.name}
                </p>
                <div className="flex items-center gap-2 text-sm text-text-secondary">
                  <span>{email.recipient.email}</span>
                </div>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <Badge variant={statusColors[email.status]}>
                {email.status}
              </Badge>
              <div className="text-xs px-2 py-1 rounded bg-surface-secondary">
                Score: {email.bant_score}
              </div>
            </div>
          </div>
        </CardHeader>

        {/* Content */}
        <CardContent className="space-y-4">
          {/* Recipient info */}
          <div className="flex items-center gap-4 text-sm text-text-secondary">
            <span className="flex items-center gap-1">
              <Building2 className="h-3.5 w-3.5" />
              {email.recipient.company}
            </span>
            <span className="flex items-center gap-1">
              <User className="h-3.5 w-3.5" />
              {email.recipient.job_title}
            </span>
          </div>

          {/* Subject */}
          <div className="space-y-1">
            <p className="text-xs font-medium text-text-secondary uppercase tracking-wider">
              Subject
            </p>
            <p className="text-sm text-text-primary font-medium">
              {email.subject}
            </p>
          </div>

          {/* Body */}
          <div className="space-y-1">
            <p className="text-xs font-medium text-text-secondary uppercase tracking-wider">
              Preview
            </p>
            <div
              className={cn(
                'p-4 rounded-lg bg-surface-secondary text-sm text-text-primary',
                'whitespace-pre-wrap',
                !isExpanded && 'line-clamp-4'
              )}
            >
              {email.body}
            </div>
            {email.body.length > 200 && (
              <button
                onClick={() => setIsExpanded(!isExpanded)}
                className="text-xs text-primary-500 hover:text-primary-600"
              >
                {isExpanded ? 'Show less' : 'Show more'}
              </button>
            )}
          </div>
        </CardContent>

        {/* Actions */}
        {email.status === 'pending' && (
          <CardFooter className="pt-0 flex items-center justify-between">
            <p className="text-xs text-text-muted">
              Generated {formatDistanceToNow(new Date(email.generated_at), { addSuffix: true })}
            </p>
            <div className="flex items-center gap-2">
              <Button
                variant="ghost"
                size="sm"
                onClick={handleReject}
                disabled={isActioning}
              >
                <X className="h-4 w-4 mr-1" />
                Reject
              </Button>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => onRegenerate?.(email.id)}
                disabled={isActioning}
              >
                <RefreshCw className="h-4 w-4 mr-1" />
                Regenerate
              </Button>
              <Button
                variant="secondary"
                size="sm"
                onClick={() => onEdit?.(email.id)}
                disabled={isActioning}
              >
                <Pencil className="h-4 w-4 mr-1" />
                Edit
              </Button>
              <Button
                variant="primary"
                size="sm"
                onClick={handleApprove}
                disabled={isActioning}
                loading={isActioning}
              >
                <Check className="h-4 w-4 mr-1" />
                Approve
              </Button>
            </div>
          </CardFooter>
        )}
      </Card>
    </motion.div>
  );
}
```

### 5.4 Lead Detail Panel

```tsx
// components/features/leads/lead-detail-panel.tsx
'use client';

import * as React from 'react';
import { formatDistanceToNow } from 'date-fns';
import { 
  X, 
  Mail, 
  Phone, 
  Building2, 
  MapPin,
  Linkedin,
  ExternalLink,
  Calendar,
  MessageSquare,
  Clock
} from 'lucide-react';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { BANTScoreDisplay } from './bant-score-display';
import { ScrollArea } from '@/components/ui/scroll-area';

interface Lead {
  id: string;
  first_name: string;
  last_name: string;
  email: string;
  phone?: string;
  company_name: string;
  job_title: string;
  company_size?: string;
  industry?: string;
  location?: string;
  linkedin_url?: string;
  website?: string;
  bant_score: number;
  bant_breakdown: {
    budget: number;
    authority: number;
    need: number;
    timeline: number;
  };
  status: string;
  intent?: string;
  interactions: Array<{
    id: string;
    type: string;
    description: string;
    created_at: string;
  }>;
  created_at: string;
}

interface LeadDetailPanelProps {
  lead: Lead;
  onClose: () => void;
  onSendEmail?: () => void;
  onScheduleMeeting?: () => void;
}

export function LeadDetailPanel({
  lead,
  onClose,
  onSendEmail,
  onScheduleMeeting,
}: LeadDetailPanelProps) {
  return (
    <div className="fixed inset-y-0 right-0 w-full max-w-lg bg-surface-primary border-l border-border-primary shadow-xl z-50">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-border-secondary">
        <div>
          <h2 className="text-lg font-semibold text-text-primary">
            {lead.first_name} {lead.last_name}
          </h2>
          <p className="text-sm text-text-secondary">{lead.job_title}</p>
        </div>
        <Button variant="ghost" size="icon" onClick={onClose}>
          <X className="h-5 w-5" />
        </Button>
      </div>

      <ScrollArea className="h-[calc(100vh-64px)]">
        <div className="p-4 space-y-6">
          {/* Quick Actions */}
          <div className="flex items-center gap-2">
            <Button variant="primary" className="flex-1" onClick={onSendEmail}>
              <Mail className="h-4 w-4 mr-2" />
              Send Email
            </Button>
            <Button variant="secondary" className="flex-1" onClick={onScheduleMeeting}>
              <Calendar className="h-4 w-4 mr-2" />
              Schedule
            </Button>
          </div>

          {/* Status & Score */}
          <div className="flex items-center justify-between p-4 rounded-lg bg-surface-secondary">
            <div>
              <p className="text-xs text-text-secondary mb-1">Status</p>
              <Badge variant="primary">{lead.status}</Badge>
            </div>
            <BANTScoreDisplay
              score={lead.bant_score}
              breakdown={lead.bant_breakdown}
              size="sm"
              showBreakdown={false}
            />
          </div>

          {/* Tabs */}
          <Tabs defaultValue="details" className="w-full">
            <TabsList className="w-full">
              <TabsTrigger value="details" className="flex-1">Details</TabsTrigger>
              <TabsTrigger value="score" className="flex-1">BANT Score</TabsTrigger>
              <TabsTrigger value="activity" className="flex-1">Activity</TabsTrigger>
            </TabsList>

            {/* Details Tab */}
            <TabsContent value="details" className="space-y-4 pt-4">
              {/* Contact Info */}
              <div className="space-y-3">
                <h3 className="text-sm font-medium text-text-primary">Contact</h3>
                <div className="space-y-2">
                  <a
                    href={`mailto:${lead.email}`}
                    className="flex items-center gap-3 p-2 rounded-lg hover:bg-surface-hover transition-colors"
                  >
                    <Mail className="h-4 w-4 text-text-muted" />
                    <span className="text-sm text-text-primary">{lead.email}</span>
                  </a>
                  {lead.phone && (
                    <a
                      href={`tel:${lead.phone}`}
                      className="flex items-center gap-3 p-2 rounded-lg hover:bg-surface-hover transition-colors"
                    >
                      <Phone className="h-4 w-4 text-text-muted" />
                      <span className="text-sm text-text-primary">{lead.phone}</span>
                    </a>
                  )}
                  {lead.linkedin_url && (
                    <a
                      href={lead.linkedin_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex items-center gap-3 p-2 rounded-lg hover:bg-surface-hover transition-colors"
                    >
                      <Linkedin className="h-4 w-4 text-text-muted" />
                      <span className="text-sm text-text-primary">LinkedIn Profile</span>
                      <ExternalLink className="h-3 w-3 text-text-muted ml-auto" />
                    </a>
                  )}
                </div>
              </div>

              {/* Company Info */}
              <div className="space-y-3">
                <h3 className="text-sm font-medium text-text-primary">Company</h3>
                <div className="space-y-2">
                  <div className="flex items-center gap-3 p-2">
                    <Building2 className="h-4 w-4 text-text-muted" />
                    <span className="text-sm text-text-primary">{lead.company_name}</span>
                  </div>
                  {lead.industry && (
                    <div className="flex items-center gap-3 p-2">
                      <span className="text-xs text-text-secondary w-4">🏭</span>
                      <span className="text-sm text-text-primary">{lead.industry}</span>
                    </div>
                  )}
                  {lead.company_size && (
                    <div className="flex items-center gap-3 p-2">
                      <span className="text-xs text-text-secondary w-4">👥</span>
                      <span className="text-sm text-text-primary">{lead.company_size} employees</span>
                    </div>
                  )}
                  {lead.location && (
                    <div className="flex items-center gap-3 p-2">
                      <MapPin className="h-4 w-4 text-text-muted" />
                      <span className="text-sm text-text-primary">{lead.location}</span>
                    </div>
                  )}
                </div>
              </div>
            </TabsContent>

            {/* BANT Score Tab */}
            <TabsContent value="score" className="pt-4">
              <BANTScoreDisplay
                score={lead.bant_score}
                breakdown={lead.bant_breakdown}
                size="lg"
                showBreakdown={true}
              />
            </TabsContent>

            {/* Activity Tab */}
            <TabsContent value="activity" className="pt-4">
              <div className="space-y-4">
                {lead.interactions.length > 0 ? (
                  lead.interactions.map((interaction, index) => (
                    <div
                      key={interaction.id}
                      className="relative pl-6 pb-4 border-l border-border-secondary last:pb-0"
                    >
                      <div className="absolute left-0 top-0 -translate-x-1/2 w-3 h-3 rounded-full bg-primary-500" />
                      <div className="space-y-1">
                        <p className="text-sm text-text-primary">
                          {interaction.description}
                        </p>
                        <p className="text-xs text-text-muted flex items-center gap-1">
                          <Clock className="h-3 w-3" />
                          {formatDistanceToNow(new Date(interaction.created_at), { addSuffix: true })}
                        </p>
                      </div>
                    </div>
                  ))
                ) : (
                  <div className="text-center py-8 text-text-secondary">
                    <MessageSquare className="h-8 w-8 mx-auto mb-2 text-text-muted" />
                    <p className="text-sm">No activity yet</p>
                  </div>
                )}
              </div>
            </TabsContent>
          </Tabs>
        </div>
      </ScrollArea>
    </div>
  );
}
```

---

## 6. PATTERNS DE COMPOSITION

### 6.1 Page Template

```tsx
// Pattern for consistent page structure
function PageTemplate({
  title,
  description,
  breadcrumbs,
  actions,
  children,
}) {
  return (
    <div className="min-h-screen bg-bg-primary">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <PageHeader
          title={title}
          description={description}
          breadcrumbs={breadcrumbs}
          actions={actions}
        />
        <main>{children}</main>
      </div>
    </div>
  );
}

// Usage
function CampaignsPage() {
  return (
    <PageTemplate
      title="Campaigns"
      description="Manage your prospecting campaigns"
      breadcrumbs={[
        { label: 'Dashboard', href: '/dashboard' },
        { label: 'Campaigns' },
      ]}
      actions={
        <Button>
          <Plus className="h-4 w-4 mr-2" />
          New Campaign
        </Button>
      }
    >
      <CampaignsList />
    </PageTemplate>
  );
}
```

### 6.2 List + Detail Pattern

```tsx
// Master-detail layout for leads, campaigns, etc.
function ListDetailLayout({
  items,
  selectedId,
  onSelect,
  renderItem,
  renderDetail,
}) {
  const selectedItem = items.find((item) => item.id === selectedId);

  return (
    <div className="flex h-[calc(100vh-200px)]">
      {/* List */}
      <div className="w-96 border-r border-border-primary overflow-auto">
        {items.map((item) => (
          <div
            key={item.id}
            onClick={() => onSelect(item.id)}
            className={cn(
              'cursor-pointer transition-colors',
              item.id === selectedId && 'bg-surface-hover'
            )}
          >
            {renderItem(item)}
          </div>
        ))}
      </div>

      {/* Detail */}
      <div className="flex-1 overflow-auto">
        {selectedItem ? (
          renderDetail(selectedItem)
        ) : (
          <EmptyState
            icon={MousePointer}
            title="Select an item"
            description="Choose an item from the list to view details"
          />
        )}
      </div>
    </div>
  );
}
```

### 6.3 Wizard Pattern

```tsx
// Multi-step form pattern
function WizardPattern({
  steps,
  currentStep,
  onNext,
  onBack,
  onComplete,
  children,
}) {
  const progress = ((currentStep + 1) / steps.length) * 100;

  return (
    <div className="max-w-2xl mx-auto">
      {/* Progress */}
      <div className="mb-8">
        <div className="flex justify-between mb-2">
          {steps.map((step, index) => (
            <div
              key={index}
              className={cn(
                'flex items-center gap-2',
                index <= currentStep ? 'text-primary-500' : 'text-text-muted'
              )}
            >
              <div
                className={cn(
                  'w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium',
                  index < currentStep && 'bg-primary-500 text-white',
                  index === currentStep && 'bg-primary-100 text-primary-700 dark:bg-primary-900 dark:text-primary-300',
                  index > currentStep && 'bg-surface-secondary text-text-muted'
                )}
              >
                {index < currentStep ? <Check className="h-4 w-4" /> : index + 1}
              </div>
              <span className="hidden sm:inline text-sm font-medium">
                {step.title}
              </span>
            </div>
          ))}
        </div>
        <div className="h-1 bg-surface-secondary rounded-full">
          <div
            className="h-full bg-primary-500 rounded-full transition-all duration-300"
            style={{ width: `${progress}%` }}
          />
        </div>
      </div>

      {/* Content */}
      <Card className="p-6">
        <h2 className="text-xl font-semibold text-text-primary mb-2">
          {steps[currentStep].title}
        </h2>
        <p className="text-text-secondary mb-6">
          {steps[currentStep].description}
        </p>
        
        {children}

        {/* Actions */}
        <div className="flex justify-between mt-8 pt-6 border-t border-border-secondary">
          <Button
            variant="ghost"
            onClick={onBack}
            disabled={currentStep === 0}
          >
            Back
          </Button>
          {currentStep === steps.length - 1 ? (
            <Button onClick={onComplete}>
              Complete
            </Button>
          ) : (
            <Button onClick={onNext}>
              Continue
            </Button>
          )}
        </div>
      </Card>
    </div>
  );
}
```

---

**- FIN DU DOCUMENT -**

*Catalogue Composants UI Vectra v1.0*
*14 Janvier 2026*
