import { FormEvent, useEffect, useState } from 'react';
import { Button } from '../components/Button';
import { Card } from '../components/Card';
import { Table } from '../components/Table';
import { boletasApi } from '../services/boletasApi';
import type { Boleta } from '../types/boleta.types';
import { formatMoney } from '../utils/formatMoney';

export function Boletas() {
  const [boletas, setBoletas] = useState<Boleta[]>([]);
  const [empleadoCodigo, setEmpleadoCodigo] = useState('EMP001');
  const [periodo, setPeriodo] = useState('Junio 2026');
  const [bonos, setBonos] = useState('150');
  const [descuentos, setDescuentos] = useState('30');
  const [mensaje, setMensaje] = useState('');
  const [error, setError] = useState('');

  async function cargarBoletas() {
    const response = await boletasApi.listar();
    setBoletas(response.data);
  }

  useEffect(() => {
    cargarBoletas().catch(() => setError('No se pudieron cargar las boletas.'));
  }, []);

  async function generarBoleta(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setMensaje('');
    setError('');

    try {
      const response = await boletasApi.generar({
        empleado_codigo: empleadoCodigo,
        periodo,
        bonos: Number(bonos),
        descuentos: Number(descuentos),
      });

      setBoletas((current) => [response.data, ...current]);
      setMensaje('Boleta generada correctamente.');
    } catch {
      setError('No se pudo generar la boleta. Verifica el codigo del empleado.');
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-semibold">Boletas</h2>
        <p className="mt-1 text-sm text-slate-500">
          Genera boletas por empleado y periodo con sueldo base, bonos, descuentos y sueldo neto.
        </p>
      </div>

      <Card>
        <form className="grid gap-4 md:grid-cols-5" onSubmit={generarBoleta}>
          <label className="space-y-1 text-sm font-medium text-slate-700">
            Codigo
            <input
              className="w-full rounded-md border border-slate-300 px-3 py-2"
              value={empleadoCodigo}
              onChange={(event) => setEmpleadoCodigo(event.target.value)}
            />
          </label>
          <label className="space-y-1 text-sm font-medium text-slate-700">
            Periodo
            <input
              className="w-full rounded-md border border-slate-300 px-3 py-2"
              value={periodo}
              onChange={(event) => setPeriodo(event.target.value)}
            />
          </label>
          <label className="space-y-1 text-sm font-medium text-slate-700">
            Bonos
            <input
              className="w-full rounded-md border border-slate-300 px-3 py-2"
              min="0"
              type="number"
              value={bonos}
              onChange={(event) => setBonos(event.target.value)}
            />
          </label>
          <label className="space-y-1 text-sm font-medium text-slate-700">
            Descuentos
            <input
              className="w-full rounded-md border border-slate-300 px-3 py-2"
              min="0"
              type="number"
              value={descuentos}
              onChange={(event) => setDescuentos(event.target.value)}
            />
          </label>
          <div className="flex items-end">
            <Button className="w-full" type="submit">
              Generar
            </Button>
          </div>
        </form>

        {mensaje && <p className="mt-4 rounded-md bg-green-50 px-3 py-2 text-sm text-green-700">{mensaje}</p>}
        {error && <p className="mt-4 rounded-md bg-red-50 px-3 py-2 text-sm text-red-700">{error}</p>}
      </Card>

      <Card>
        <div className="mb-4 flex items-center justify-between">
          <h3 className="text-lg font-semibold">Boletas generadas</h3>
          <span className="text-sm text-slate-500">{boletas.length} registros</span>
        </div>
        <div className="overflow-x-auto">
          <Table>
            <thead className="bg-slate-100 text-left text-xs uppercase text-slate-500">
              <tr>
                <th className="px-3 py-2">Empleado</th>
                <th className="px-3 py-2">Periodo</th>
                <th className="px-3 py-2">Sueldo base</th>
                <th className="px-3 py-2">Bonos</th>
                <th className="px-3 py-2">Descuentos</th>
                <th className="px-3 py-2">Neto</th>
              </tr>
            </thead>
            <tbody>
              {boletas.map((boleta) => (
                <tr className="border-t border-slate-100" key={boleta.id}>
                  <td className="px-3 py-3">
                    <p className="font-medium text-slate-900">{boleta.empleado_nombre}</p>
                    <p className="text-xs text-slate-500">{boleta.empleado_codigo}</p>
                  </td>
                  <td className="px-3 py-3">{boleta.periodo}</td>
                  <td className="px-3 py-3">{formatMoney(boleta.sueldo_base)}</td>
                  <td className="px-3 py-3">{formatMoney(boleta.bonos)}</td>
                  <td className="px-3 py-3">{formatMoney(boleta.descuentos)}</td>
                  <td className="px-3 py-3 font-semibold text-blue-700">{formatMoney(boleta.sueldo_neto)}</td>
                </tr>
              ))}
            </tbody>
          </Table>
        </div>
      </Card>
    </div>
  );
}
