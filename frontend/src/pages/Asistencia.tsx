import type { InputHTMLAttributes } from 'react';
import { useEffect, useMemo, useState } from 'react';
import { Button } from '../components/Button';
import { Input } from '../components/Input';
import { asistenciaApi } from '../services/asistenciaApi';
import { empleadosApi } from '../services/empleadosApi';
import type { Asistencia as AsistenciaRegistro, EstadoAsistencia } from '../types/asistencia.types';
import type { Empleado } from '../types/empleado.types';

type AsistenciaTab = 'registrar' | 'resumen' | 'configuracion';

const tabs: Array<{ id: AsistenciaTab; label: string }> = [
  { id: 'registrar', label: 'Registrar asistencia' },
  { id: 'resumen', label: 'Resumen del dia' },
  { id: 'configuracion', label: 'Configuracion' },
];

const estadoStyles: Record<EstadoAsistencia, string> = {
  ASISTIO: 'border-emerald-200 bg-emerald-50 text-emerald-800',
  TARDE: 'border-amber-200 bg-amber-50 text-amber-800',
  FALTO: 'border-rose-200 bg-rose-50 text-rose-800',
};

export function Asistencia() {
  const [activeTab, setActiveTab] = useState<AsistenciaTab>('registrar');
  const [periodo, setPeriodo] = useState('2026-01');
  const [empleados, setEmpleados] = useState<Empleado[]>([]);
  const [selectedEmpleadoId, setSelectedEmpleadoId] = useState<number | undefined>();
  const [selectedDate, setSelectedDate] = useState('2026-01-01');
  const [registros, setRegistros] = useState<AsistenciaRegistro[]>([]);
  const [minutosTardanza, setMinutosTardanza] = useState('23');
  const [loading, setLoading] = useState(false);

  const empleadoSeleccionado = empleados.find((empleado) => empleado.id === selectedEmpleadoId) ?? empleados[0];
  const dias = useMemo(() => crearDiasDelPeriodo(periodo), [periodo]);

  useEffect(() => {
    async function cargarEmpleados() {
      setLoading(true);
      try {
        const response = await empleadosApi.listarActivos(periodo);
        setEmpleados(response.data);
        setSelectedEmpleadoId((current) => current ?? response.data[0]?.id);
      } finally {
        setLoading(false);
      }
    }

    void cargarEmpleados();
  }, [periodo]);

  useEffect(() => {
    async function cargarAsistencias() {
      if (!empleadoSeleccionado) {
        setRegistros([]);
        return;
      }

      const response = await asistenciaApi.listar({ empleado_id: empleadoSeleccionado.id, periodo });
      setRegistros(response.data);
    }

    void cargarAsistencias();
  }, [empleadoSeleccionado, periodo]);

  async function actualizarEstado(estado: EstadoAsistencia) {
    if (!empleadoSeleccionado || !selectedDate) return;

    const comentario = estado === 'TARDE' ? `${minutosTardanza || 0} min` : undefined;
    const minutos = estado === 'TARDE' ? Number(minutosTardanza || 0) : undefined;

    const response = await asistenciaApi.registrar({
      empleado_id: empleadoSeleccionado.id,
      fecha: selectedDate,
      estado,
      minutos_tardanza: minutos,
      comentario,
    });

    setRegistros((current) => [
      ...current.filter((registro) => !(registro.empleado_id === empleadoSeleccionado.id && registro.fecha === selectedDate)),
      response.data,
    ]);
  }

  async function limpiarFecha() {
    if (!empleadoSeleccionado || !selectedDate) return;

    await asistenciaApi.eliminar({ empleado_id: empleadoSeleccionado.id, fecha: selectedDate });
    setRegistros((current) =>
      current.filter((registro) => !(registro.empleado_id === empleadoSeleccionado.id && registro.fecha === selectedDate)),
    );
  }

  return (
    <div className="space-y-5">
      <header>
        <h2 className="text-2xl font-semibold text-slate-900">Control de asistencias</h2>
        <p className="text-sm text-slate-500">Registro por periodo, empleado y calendario.</p>
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

      {activeTab === 'registrar' && (
        <section className="space-y-4">
          <div className="rounded-md border border-slate-200 bg-white p-4">
            <label className="block max-w-xs">
              <span className="mb-1 block text-sm font-semibold text-slate-700">Periodo</span>
              <Input
                type="month"
                value={periodo}
                onChange={(event) => {
                  setPeriodo(event.target.value);
                  setSelectedDate(`${event.target.value}-01`);
                  setSelectedEmpleadoId(undefined);
                }}
              />
            </label>

            <div className="mt-4 flex gap-2 overflow-x-auto pb-1">
              {empleados.map((empleado) => (
                <button
                  key={empleado.id}
                  type="button"
                  className={`min-w-fit rounded-md border px-4 py-2 text-sm font-semibold ${
                    empleado.id === empleadoSeleccionado?.id
                      ? 'border-blue-600 bg-blue-50 text-blue-700'
                      : 'border-slate-200 bg-white text-slate-700'
                  }`}
                  onClick={() => setSelectedEmpleadoId(empleado.id)}
                >
                  {empleado.nombres} {empleado.apellidos}
                </button>
              ))}
            </div>
            {loading && <p className="mt-3 text-sm text-slate-500">Cargando empleados activos...</p>}
          </div>

          {empleadoSeleccionado ? (
            <>
              <div className="grid gap-4 xl:grid-cols-[1fr_220px]">
                <Calendario
                  dias={dias}
                  periodo={periodo}
                  registros={registros}
                  selectedDate={selectedDate}
                  onSelectDate={setSelectedDate}
                />

                <div className="space-y-3 rounded-md border border-slate-200 bg-white p-4">
                  <Button className="w-full bg-emerald-600 hover:bg-emerald-700" type="button" onClick={() => actualizarEstado('ASISTIO')}>
                    Asistencia
                  </Button>
                  <div className="space-y-2">
                    <Button className="w-full bg-amber-500 hover:bg-amber-600" type="button" onClick={() => actualizarEstado('TARDE')}>
                      Tardanza
                    </Button>
                    <Input
                      className="w-full"
                      type="number"
                      value={minutosTardanza}
                      onChange={(event) => setMinutosTardanza(event.target.value)}
                      placeholder="Minutos tarde"
                    />
                  </div>
                  <Button className="w-full bg-rose-600 hover:bg-rose-700" type="button" onClick={() => actualizarEstado('FALTO')}>
                    Falta
                  </Button>
                  <Button className="w-full bg-slate-600 hover:bg-slate-700" type="button" onClick={limpiarFecha}>
                    Limpiar fecha
                  </Button>
                </div>
              </div>

              <div className="grid gap-4 lg:grid-cols-2">
                <ReglasEmpresa />
                <PerfilEmpleado empleado={empleadoSeleccionado} />
              </div>
            </>
          ) : (
            <p className="rounded-md border border-slate-200 bg-white p-4 text-sm text-slate-500">
              No hay empleados activos para este periodo.
            </p>
          )}
        </section>
      )}

      {activeTab === 'resumen' && (
        <section className="rounded-md border border-slate-200 bg-white p-4">
          <h3 className="text-lg font-semibold">Resumen del dia</h3>
          <p className="mt-1 text-sm text-slate-500">Aqui se mostrara el resumen diario de asistencias.</p>
        </section>
      )}

      {activeTab === 'configuracion' && (
        <section className="rounded-md border border-slate-200 bg-white p-4">
          <h3 className="text-lg font-semibold">Configuracion de reglas</h3>
          <div className="mt-4 grid gap-4 md:grid-cols-3">
            <Field label="Hora de ingreso" defaultValue="08:00" type="time" />
            <Field label="Hora de salida" defaultValue="17:00" type="time" />
            <Field label="Tardanzas permitidas" defaultValue="3" type="number" />
          </div>
        </section>
      )}
    </div>
  );
}

function Calendario({
  dias,
  periodo,
  registros,
  selectedDate,
  onSelectDate,
}: {
  dias: number[];
  periodo: string;
  registros: AsistenciaRegistro[];
  selectedDate: string;
  onSelectDate: (date: string) => void;
}) {
  const diasSemana = ['Domingo', 'Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado'];

  return (
    <div className="overflow-hidden rounded-md border border-slate-200 bg-white">
      <div className="grid grid-cols-7 border-b border-slate-200 bg-slate-50 text-xs font-bold uppercase text-slate-600">
        {diasSemana.map((dia) => (
          <div key={dia} className="px-2 py-3 text-center">
            {dia}
          </div>
        ))}
      </div>
      <div className="grid grid-cols-7">
        {dias.map((dia) => {
          const fecha = `${periodo}-${String(dia).padStart(2, '0')}`;
          const registro = registros.find((item) => item.fecha === fecha);
          const estadoClass = registro ? estadoStyles[registro.estado] : 'border-slate-100 bg-white';

          return (
            <button
              key={fecha}
              type="button"
              className={`min-h-20 border p-2 text-left text-sm ${estadoClass} ${
                selectedDate === fecha ? 'ring-2 ring-blue-500 ring-inset' : ''
              }`}
              onClick={() => onSelectDate(fecha)}
            >
              <span className="font-semibold">{dia}</span>
              {registro && (
                <span className="mt-2 block text-xs font-semibold">
                  {registro.estado}
                  {registro.comentario ? ` - ${registro.comentario}` : ''}
                </span>
              )}
            </button>
          );
        })}
      </div>
    </div>
  );
}

function ReglasEmpresa() {
  return (
    <section className="rounded-md border border-slate-200 bg-white p-4">
      <h3 className="mb-3 text-sm font-bold uppercase">Reglas establecidas por la empresa</h3>
      <p className="text-sm">Hora de ingreso: 8:00 am</p>
      <p className="text-sm">Hora de salida: 17:00 pm</p>
      <p className="text-sm">Tardanzas permitidas: 3</p>
    </section>
  );
}

function PerfilEmpleado({ empleado }: { empleado: Empleado }) {
  return (
    <section className="rounded-md border border-slate-200 bg-white p-4">
      <div className="flex gap-4">
        <div className="grid h-24 w-24 place-items-center rounded-md border border-slate-300 bg-slate-50 text-center text-xs font-semibold text-slate-500">
          Foto empleado
        </div>
        <div className="space-y-1 text-sm">
          <p>
            <strong>Nombre:</strong> {empleado.nombres} {empleado.apellidos}
          </p>
          <p>
            <strong>Cargo:</strong> {empleado.cargo}
          </p>
          <p>
            <strong>Numero:</strong> {empleado.telefono ?? 'Sin telefono'}
          </p>
          <p>
            <strong>Correo:</strong> {empleado.correo ?? 'Sin correo'}
          </p>
          <p>
            <strong>Fecha de inicio:</strong> {empleado.fecha_inicio ?? 'Sin fecha'}
          </p>
          <p>
            <strong>Fecha de cese:</strong> {empleado.fecha_cese ?? 'Sin cese'}
          </p>
        </div>
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

function crearDiasDelPeriodo(periodo: string) {
  const [anio, mes] = periodo.split('-').map(Number);
  const totalDias = new Date(anio, mes, 0).getDate();
  return Array.from({ length: totalDias }, (_, index) => index + 1);
}
