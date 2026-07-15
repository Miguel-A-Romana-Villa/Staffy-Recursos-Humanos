import type { FormEvent, InputHTMLAttributes } from 'react';
import { useEffect, useMemo, useState } from 'react';
import { Button } from '../components/Button';
import { Input } from '../components/Input';
import { empleadosApi } from '../services/empleadosApi';
import type { Empleado, EmpleadoForm } from '../types/empleado.types';
import { formatMoney } from '../utils/formatMoney';

type EmpleadosTab = 'registrar' | 'buscar' | 'lista';

const tabs: Array<{ id: EmpleadosTab; label: string }> = [
  { id: 'registrar', label: 'Registrar' },
  { id: 'buscar', label: 'Buscar' },
  { id: 'lista', label: 'Lista de empleados' },
];

const initialForm: EmpleadoForm = {
  codigo: '',
  dni: '',
  correo: '',
  telefono: '',
  nombres: '',
  apellidos: '',
  cargo: '',
  sueldo_base: 0,
  tipo: 'tiempo_completo',
  horas_trabajadas: undefined,
  tarifa_por_hora: undefined,
  hijos: 0,
  fecha_nacimiento: '',
  fecha_inicio: new Date().toISOString().slice(0, 10),
  fecha_cese: '',
  regimen_pensionario: 'AFP',
  foto_url: '',
  activo: true,
};

export function Empleados() {
  const [activeTab, setActiveTab] = useState<EmpleadosTab>('registrar');
  const [empleados, setEmpleados] = useState<Empleado[]>([]);
  const [search, setSearch] = useState('');
  const [form, setForm] = useState<EmpleadoForm>(initialForm);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  async function cargarEmpleados(searchTerm = search) {
    setLoading(true);
    try {
      const response = await empleadosApi.listar(searchTerm || undefined);
      setEmpleados(response.data);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void cargarEmpleados('');
  }, []);

  const empleadoEncontrado = useMemo(() => empleados[0], [empleados]);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setMessage('');
    const payload = {
      ...form,
      sueldo_base: Number(form.sueldo_base),
      horas_trabajadas: form.tipo === 'medio_tiempo' ? Number(form.horas_trabajadas || 0) : undefined,
      tarifa_por_hora: form.tipo === 'medio_tiempo' ? Number(form.tarifa_por_hora || 0) : undefined,
      hijos: Number(form.hijos),
      fecha_cese: form.fecha_cese || undefined,
    };

    await empleadosApi.crear(payload);
    setForm(initialForm);
    setMessage('Empleado registrado correctamente.');
    await cargarEmpleados('');
  }

  async function handleSearch(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    await cargarEmpleados(search);
  }

  return (
    <div className="space-y-5">
      <header>
        <h2 className="text-2xl font-semibold text-slate-900">Control empleados</h2>
        <p className="text-sm text-slate-500">Registro, busqueda y listado del personal.</p>
      </header>

      <div className="flex gap-2 overflow-x-auto rounded-md border border-slate-200 bg-white p-1">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            className={`min-w-fit rounded px-4 py-2 text-sm font-semibold ${
              activeTab === tab.id ? 'bg-blue-600 text-white' : 'text-slate-700 hover:bg-slate-100'
            }`}
            type="button"
            onClick={() => setActiveTab(tab.id)}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {message && <p className="rounded-md bg-emerald-50 px-4 py-3 text-sm text-emerald-700">{message}</p>}
      {loading && <p className="text-sm text-slate-500">Cargando empleados...</p>}

      {activeTab === 'registrar' && <RegistrarEmpleado form={form} setForm={setForm} onSubmit={handleSubmit} />}
      {activeTab === 'buscar' && (
        <BuscarEmpleado empleado={empleadoEncontrado} search={search} onSearchChange={setSearch} onSearch={handleSearch} />
      )}
      {activeTab === 'lista' && <ListaEmpleados empleados={empleados} />}
    </div>
  );
}

function RegistrarEmpleado({
  form,
  setForm,
  onSubmit,
}: {
  form: EmpleadoForm;
  setForm: (form: EmpleadoForm) => void;
  onSubmit: (event: FormEvent<HTMLFormElement>) => void;
}) {
  function updateField<K extends keyof EmpleadoForm>(field: K, value: EmpleadoForm[K]) {
    setForm({ ...form, [field]: value });
  }

  return (
    <section className="rounded-md border border-slate-200 bg-white">
      <h3 className="border-b border-slate-200 bg-blue-50 px-4 py-3 text-center text-sm font-bold uppercase">
        Registrar empleado
      </h3>
      <form className="grid gap-4 p-4 md:grid-cols-2" onSubmit={onSubmit}>
        <Field label="Codigo" value={form.codigo} onChange={(event) => updateField('codigo', event.target.value)} />
        <Field label="DNI" value={form.dni} onChange={(event) => updateField('dni', event.target.value)} required />
        <Field label="Nombre" value={form.nombres} onChange={(event) => updateField('nombres', event.target.value)} required />
        <Field label="Apellidos" value={form.apellidos} onChange={(event) => updateField('apellidos', event.target.value)} required />
        <Field label="Correo" value={form.correo} onChange={(event) => updateField('correo', event.target.value)} type="email" />
        <Field label="Numero de telefono" value={form.telefono} onChange={(event) => updateField('telefono', event.target.value)} />
        <Field label="Sueldo" value={form.sueldo_base} onChange={(event) => updateField('sueldo_base', Number(event.target.value))} type="number" required />
        <label className="block">
          <span className="mb-1 block text-sm font-medium text-slate-700">Tipo de contrato</span>
          <select
            className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm outline-none focus:border-blue-500"
            value={form.tipo}
            onChange={(event) => updateField('tipo', event.target.value as EmpleadoForm['tipo'])}
          >
            <option value="tiempo_completo">Tiempo completo</option>
            <option value="medio_tiempo">Medio tiempo</option>
          </select>
        </label>
        {form.tipo === 'medio_tiempo' && (
          <>
            <Field
              label="Horas trabajadas"
              value={form.horas_trabajadas ?? ''}
              onChange={(event) => updateField('horas_trabajadas', Number(event.target.value))}
              type="number"
              required
            />
            <Field
              label="Tarifa por hora"
              value={form.tarifa_por_hora ?? ''}
              onChange={(event) => updateField('tarifa_por_hora', Number(event.target.value))}
              type="number"
              required
            />
          </>
        )}
        <Field label="Hijos" value={form.hijos} onChange={(event) => updateField('hijos', Number(event.target.value))} type="number" />
        <Field label="Fecha de nacimiento" value={form.fecha_nacimiento} onChange={(event) => updateField('fecha_nacimiento', event.target.value)} type="date" />
        <Field label="Cargo" value={form.cargo} onChange={(event) => updateField('cargo', event.target.value)} required />
        <label className="block">
          <span className="mb-1 block text-sm font-medium text-slate-700">Regimen pensionario</span>
          <select
            className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm outline-none focus:border-blue-500"
            value={form.regimen_pensionario}
            onChange={(event) => updateField('regimen_pensionario', event.target.value as EmpleadoForm['regimen_pensionario'])}
          >
            <option value="AFP">AFP</option>
            <option value="ONP">ONP</option>
            <option value="SIN_REGIMEN">Sin regimen</option>
          </select>
        </label>
        <Field label="Fecha de inicio" value={form.fecha_inicio} onChange={(event) => updateField('fecha_inicio', event.target.value)} type="date" />
        <Field label="Fecha de cese / renuncia" value={form.fecha_cese} onChange={(event) => updateField('fecha_cese', event.target.value)} type="date" />
        <div className="md:col-span-2">
          <Button className="w-full" type="submit">
            Registrar
          </Button>
        </div>
      </form>
    </section>
  );
}

function BuscarEmpleado({
  empleado,
  search,
  onSearchChange,
  onSearch,
}: {
  empleado?: Empleado;
  search: string;
  onSearchChange: (value: string) => void;
  onSearch: (event: FormEvent<HTMLFormElement>) => void;
}) {
  return (
    <section className="space-y-4">
      <form className="rounded-md border border-slate-200 bg-white p-4" onSubmit={onSearch}>
        <h3 className="mb-3 text-sm font-bold uppercase">Buscar empleado</h3>
        <div className="flex flex-col gap-2 sm:flex-row">
          <Input
            className="w-full"
            value={search}
            onChange={(event) => onSearchChange(event.target.value)}
            placeholder="Ingresar nombre, apellido o DNI"
          />
          <Button type="submit">Buscar</Button>
        </div>
      </form>

      {empleado ? <FichaEmpleado empleado={empleado} /> : <p className="text-sm text-slate-500">No hay resultados.</p>}
    </section>
  );
}

function FichaEmpleado({ empleado }: { empleado: Empleado }) {
  return (
    <article className="rounded-md border border-slate-200 bg-white p-4">
      <div className="mb-4 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div className="flex items-center gap-4">
          <div className="grid h-24 w-24 place-items-center rounded-md border border-slate-300 bg-slate-50 text-center text-xs font-semibold text-slate-500">
            Foto del empleado
          </div>
          <div>
            <h3 className="text-xl font-semibold">
              {empleado.nombres} {empleado.apellidos}
            </h3>
            <p className="text-sm text-slate-500">{empleado.cargo}</p>
          </div>
        </div>
        <Button type="button">Editar</Button>
      </div>

      <dl className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
        <Info label="Codigo" value={empleado.codigo} />
        <Info label="DNI" value={empleado.dni} />
        <Info label="Correo" value={empleado.correo ?? 'Sin correo'} />
        <Info label="Telefono" value={empleado.telefono ?? 'Sin telefono'} />
        <Info label="Sueldo base" value={formatMoney(empleado.sueldo_base)} />
        <Info label="Tipo" value={empleado.tipo === 'medio_tiempo' ? 'Medio tiempo' : 'Tiempo completo'} />
        <Info label="Hijos" value={String(empleado.hijos)} />
        <Info label="Fecha de nacimiento" value={empleado.fecha_nacimiento ?? 'Sin fecha'} />
        <Info label="Fecha de inicio" value={empleado.fecha_inicio ?? 'Sin fecha'} />
        <Info label="Fecha de cese" value={empleado.fecha_cese ?? 'Sin cese'} />
        <Info label="Regimen pensionario" value={empleado.regimen_pensionario} />
        <Info label="Estado" value={empleado.activo ? 'Activo' : 'Inactivo'} />
      </dl>
    </article>
  );
}

function ListaEmpleados({ empleados }: { empleados: Empleado[] }) {
  return (
    <section className="overflow-hidden rounded-md border border-slate-200 bg-white">
      <h3 className="border-b border-slate-200 px-4 py-3 text-sm font-bold uppercase">Lista de empleados</h3>
      <div className="overflow-x-auto">
        <table className="w-full min-w-[640px] text-left text-sm">
          <thead className="bg-slate-50 text-xs uppercase text-slate-500">
            <tr>
              <th className="px-4 py-3">ID</th>
              <th className="px-4 py-3">Nombre completo</th>
              <th className="px-4 py-3">DNI</th>
              <th className="px-4 py-3">Cargo</th>
              <th className="px-4 py-3">Tipo</th>
              <th className="px-4 py-3">Estado</th>
            </tr>
          </thead>
          <tbody>
            {empleados.map((empleado) => (
              <tr key={empleado.id} className="border-t border-slate-100">
                <td className="px-4 py-3">{empleado.id}</td>
                <td className="px-4 py-3 font-medium">
                  {empleado.nombres} {empleado.apellidos}
                </td>
                <td className="px-4 py-3">{empleado.dni}</td>
                <td className="px-4 py-3">{empleado.cargo}</td>
                <td className="px-4 py-3">{empleado.tipo === 'medio_tiempo' ? 'Medio tiempo' : 'Tiempo completo'}</td>
                <td className="px-4 py-3">{empleado.activo ? 'Activo' : 'Inactivo'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}

function Field({ label, ...props }: { label: string } & InputHTMLAttributes<HTMLInputElement>) {
  return (
    <label className="block">
      <span className="mb-1 block text-sm font-medium text-slate-700">{label}</span>
      <Input className="w-full" {...props} />
    </label>
  );
}

function Info({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-md border border-slate-200 p-3">
      <dt className="text-xs font-medium uppercase text-slate-500">{label}</dt>
      <dd className="mt-1 text-sm font-semibold text-slate-900">{value}</dd>
    </div>
  );
}
