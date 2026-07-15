import { FormEvent, useEffect, useMemo, useState } from 'react';
import { Button } from '../components/Button';
import { Card } from '../components/Card';
import { Table } from '../components/Table';
import { conceptosApi } from '../services/conceptosApi';
import { empleadosApi } from '../services/empleadosApi';
import type { ConceptoPago, TipoConcepto } from '../types/concepto.types';
import type { Empleado } from '../types/empleado.types';
import { formatMoney } from '../utils/formatMoney';

export function BonosDescuentos() {
  const [empleados, setEmpleados] = useState<Empleado[]>([]);
  const [conceptos, setConceptos] = useState<ConceptoPago[]>([]);
  const [empleadoId, setEmpleadoId] = useState<number | undefined>();
  const [periodo, setPeriodo] = useState('2026-06');
  const [tipo, setTipo] = useState<TipoConcepto>('BONO');
  const [concepto, setConcepto] = useState('Bono por puntualidad');
  const [monto, setMonto] = useState('150');
  const [mensaje, setMensaje] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    empleadosApi.listar().then((response) => {
      setEmpleados(response.data);
      setEmpleadoId((current) => current ?? response.data[0]?.id);
    });
  }, []);

  useEffect(() => {
    if (!empleadoId) return;
    conceptosApi
      .listar({ empleado_id: empleadoId, periodo })
      .then((response) => setConceptos(response.data))
      .catch(() => setError('No se pudieron cargar los conceptos.'));
  }, [empleadoId, periodo]);

  const resumen = useMemo(
    () => ({
      bonos: conceptos.filter((item) => item.tipo === 'BONO').reduce((total, item) => total + item.monto, 0),
      descuentos: conceptos.filter((item) => item.tipo === 'DESCUENTO').reduce((total, item) => total + item.monto, 0),
    }),
    [conceptos],
  );

  async function registrarConcepto(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!empleadoId) return;
    setMensaje('');
    setError('');

    try {
      const response = await conceptosApi.registrar({
        empleado_id: empleadoId,
        tipo,
        concepto,
        monto: Number(monto),
        periodo,
      });
      setConceptos((current) => [response.data, ...current]);
      setMensaje('Concepto registrado correctamente.');
      setConcepto(tipo === 'BONO' ? 'Bono por puntualidad' : 'Descuento por tardanza');
      setMonto(tipo === 'BONO' ? '150' : '30');
    } catch {
      setError('No se pudo registrar el concepto.');
    }
  }

  return (
    <div className="space-y-5">
      <header>
        <h2 className="text-2xl font-semibold text-slate-900">Bonos y descuentos</h2>
        <p className="text-sm text-slate-500">Conceptos adicionales por empleado y periodo.</p>
      </header>

      <div className="grid gap-4 lg:grid-cols-[1fr_320px]">
        <Card>
          <form className="grid gap-4 md:grid-cols-2" onSubmit={registrarConcepto}>
            <label className="block">
              <span className="mb-1 block text-sm font-medium text-slate-700">Empleado</span>
              <select
                className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm outline-none focus:border-blue-500"
                value={empleadoId ?? ''}
                onChange={(event) => setEmpleadoId(Number(event.target.value))}
              >
                {empleados.map((empleado) => (
                  <option key={empleado.id} value={empleado.id}>
                    {empleado.codigo} - {empleado.nombres} {empleado.apellidos}
                  </option>
                ))}
              </select>
            </label>

            <label className="block">
              <span className="mb-1 block text-sm font-medium text-slate-700">Periodo</span>
              <input
                className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm outline-none focus:border-blue-500"
                type="month"
                value={periodo}
                onChange={(event) => setPeriodo(event.target.value)}
              />
            </label>

            <label className="block">
              <span className="mb-1 block text-sm font-medium text-slate-700">Tipo</span>
              <select
                className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm outline-none focus:border-blue-500"
                value={tipo}
                onChange={(event) => setTipo(event.target.value as TipoConcepto)}
              >
                <option value="BONO">Bono</option>
                <option value="DESCUENTO">Descuento</option>
              </select>
            </label>

            <label className="block">
              <span className="mb-1 block text-sm font-medium text-slate-700">Monto</span>
              <input
                className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm outline-none focus:border-blue-500"
                min="1"
                type="number"
                value={monto}
                onChange={(event) => setMonto(event.target.value)}
              />
            </label>

            <label className="block md:col-span-2">
              <span className="mb-1 block text-sm font-medium text-slate-700">Concepto</span>
              <input
                className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm outline-none focus:border-blue-500"
                value={concepto}
                onChange={(event) => setConcepto(event.target.value)}
              />
            </label>

            <div className="md:col-span-2">
              <Button className="w-full" type="submit">
                Registrar
              </Button>
            </div>
          </form>

          {mensaje && <p className="mt-4 rounded-md bg-emerald-50 px-3 py-2 text-sm text-emerald-700">{mensaje}</p>}
          {error && <p className="mt-4 rounded-md bg-rose-50 px-3 py-2 text-sm text-rose-700">{error}</p>}
        </Card>

        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-1">
          <Card>
            <p className="text-sm text-slate-500">Bonos</p>
            <p className="mt-2 text-2xl font-bold text-emerald-700">{formatMoney(resumen.bonos)}</p>
          </Card>
          <Card>
            <p className="text-sm text-slate-500">Descuentos</p>
            <p className="mt-2 text-2xl font-bold text-rose-700">{formatMoney(resumen.descuentos)}</p>
          </Card>
        </div>
      </div>

      <Card>
        <div className="mb-4 flex items-center justify-between">
          <h3 className="text-lg font-semibold">Conceptos registrados</h3>
          <span className="text-sm text-slate-500">{conceptos.length} registros</span>
        </div>
        <div className="overflow-x-auto">
          <Table>
            <thead className="bg-slate-100 text-left text-xs uppercase text-slate-500">
              <tr>
                <th className="px-3 py-2">Tipo</th>
                <th className="px-3 py-2">Concepto</th>
                <th className="px-3 py-2">Periodo</th>
                <th className="px-3 py-2">Monto</th>
              </tr>
            </thead>
            <tbody>
              {conceptos.map((item) => (
                <tr className="border-t border-slate-100" key={item.id}>
                  <td className="px-3 py-3">{item.tipo === 'BONO' ? 'Bono' : 'Descuento'}</td>
                  <td className="px-3 py-3 font-medium">{item.concepto}</td>
                  <td className="px-3 py-3">{item.periodo}</td>
                  <td className="px-3 py-3">{formatMoney(item.monto)}</td>
                </tr>
              ))}
            </tbody>
          </Table>
        </div>
      </Card>
    </div>
  );
}
