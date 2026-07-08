import type { ReactNode } from 'react';

type ModalProps = {
  open: boolean;
  children: ReactNode;
};

export function Modal({ open, children }: ModalProps) {
  if (!open) return null;

  return (
    <div className="fixed inset-0 grid place-items-center bg-slate-950/40 p-4">
      <div className="w-full max-w-lg rounded-md bg-white p-4 shadow-lg">{children}</div>
    </div>
  );
}
