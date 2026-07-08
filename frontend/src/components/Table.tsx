import type { TableHTMLAttributes } from 'react';

type TableProps = TableHTMLAttributes<HTMLTableElement>;

export function Table({ className = '', ...props }: TableProps) {
  return <table className={`w-full border-collapse text-sm ${className}`} {...props} />;
}
