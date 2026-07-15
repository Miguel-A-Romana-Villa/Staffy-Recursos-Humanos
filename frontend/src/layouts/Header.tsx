export function Header() {
  return (
    <header className="border-b border-slate-200 bg-white px-4 py-3 md:px-6">
      <div className="flex items-center justify-between gap-4">
        <p className="text-sm font-medium text-slate-500">Sistema de Gestion de Recursos Humanos</p>
        <div className="grid h-9 w-9 place-items-center rounded-full bg-blue-600 text-sm font-bold text-white">AM</div>
      </div>
    </header>
  );
}
