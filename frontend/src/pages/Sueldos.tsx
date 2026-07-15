import { FormEvent, useEffect, useState } from 'react';
import { Button } from '../components/Button';
import { Card } from '../components/Card';
import { Table } from '../components/Table';
import { empleadosApi } from '../services/empleadosApi';
import { sueldosApi } from '../services/sueldosApi';
import type { Empleado } from '../types/empleado.types';
import type { SueldoCalculo } from '../types/sueldo.types';
import { formatMoney } from '../utils/formatMoney';

export function Sueldos() {
  const [empleados, setEmpleados] = useState<Empleado[]>([]);
  const [empleadoCodigo, setEmpleadoCodigo] = useState('');
  const [periodo, setPeriodo] = useState('2026-06');
  const [bonos, setBonos] = useState('0');
  const [descuentos, setDescuentos] = useState('0');
  const [resultado, setResultado] = useState<SueldoCalculo | null>(null);
  const [error, setError] = useState('');

  useEffect(() => {
    empleadosApi.listar().then((response) => {
      setEmpleados(response.data);
      setEmpleadoCodigo((current) => current || response.data[0]?.codigo || '');
    });
  }, []);

  async function calcularSueldo(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError('');
    try {
      const response = await sueldosApi.calcular({
        empleado_codigo: empleadoCodigo,
        periodo,
        bonos: Number(bonos),
        descuentos: Number(descuentos),
      });
      setResultado(response.data);
    } catch {
      setError('No se pudo calcular el sueldo.');
    }
  }

  return (
    <div className="space-y-5">
      <header>
        <h2 className="text-2xl font-semibold text-slate-900">Calculo de sueldo</h2>
        <p className="text-sm text-slate-500">Sueldo base, conceptos del periodo y neto calculado.</p>
      </header>

      <Card>
        <form className="grid gap-4 md:grid-cols-5" onSubmit={calcularSueldo}>
          <label className="block md:col-span-2">
            <span className="mb-1 block text-sm font-medium text-slate-700">Empleado</span>
            <select
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm outline-none focus:border-blue-500"
              value={empleadoCodigo}
              onChange={(event) => setEmpleadoCodigo(event.target.value)}
            >
              {empleados.map((empleado) => (
                <option key={empleado.id} value={empleado.codigo}>
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
            <span className="mb-1 block text-sm font-medium text-slate-700">Bono extra</span>
            <input
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm outline-none focus:border-blue-500"
              min="0"
              type="number"
              value={bonos}
              onChange={(event) => setBonos(event.target.value)}
            />
          </label>
          <label className="block">
            <span className="mb-1 block text-sm font-medium text-slate-700">Descuento extra</span>
            <input
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm outline-none focus:border-blue-500"
              min="0"
              type="number"
              value={descuentos}
              onChange={(event) => setDescuentos(event.target.value)}
            />
          </label>
          <div className="md:col-span-5">
            <Button className="w-full" type="submit">
              Calcular
            </Button>
          </div>
        </form>
        {error && <p className="mt-4 rounded-md bg-rose-50 px-3 py-2 text-sm text-rose-700">{error}</p>}
      </Card>

      {resultado && (
        <>
          <div className="grid gap-4 md:grid-cols-4">
            <Card>
              <p className="text-sm text-slate-500">Sueldo base</p>
              <p className="mt-2 text-2xl font-bold">{formatMoney(resultado.sueldo_base)}</p>
            </Card>
            <Card>
              <p className="text-sm text-slate-500">Bonos</p>
              <p className="mt-2 text-2xl font-bold text-emerald-700">{formatMoney(resultado.bonos)}</p>
            </Card>
            <Card>
              <p className="text-sm text-slate-500">Descuentos</p>
              <p className="mt-2 text-2xl font-bold text-rose-700">{formatMoney(resultado.descuentos)}</p>
            </Card>
            <Card>
              <p className="text-sm text-slate-500">Neto</p>
              <p className="mt-2 text-2xl font-bold text-blue-700">{formatMoney(resultado.sueldo_neto)}</p>
            </Card>
          </div>

          <Card>
            <div className="mb-4">
              <h3 className="text-lg font-semibold">{resultado.empleado_nombre}</h3>
              <p className="text-sm text-slate-500">
                {resultado.empleado_codigo} · {resultado.cargo} · {resultado.periodo}
              </p>
            </div>
            <div className="overflow-x-auto">
              <Table>
                <thead className="bg-slate-100 text-left text-xs uppercase text-slate-500">
                  <tr>
                    <th className="px-3 py-2">Tipo</th>
                    <th className="px-3 py-2">Concepto</th>
                    <th className="px-3 py-2">Monto</th>
                  </tr>
                </thead>
                <tbody>
                  {resultado.conceptos.map((item, index) => (
                    <tr className="border-t border-slate-100" key={`${item.tipo}-${item.concepto}-${index}`}>
                      <td className="px-3 py-3">{item.tipo === 'BONO' ? 'Bono' : 'Descuento'}</td>
                      <td className="px-3 py-3">{item.concepto}</td>
                      <td className="px-3 py-3">{formatMoney(item.monto)}</td>
                    </tr>
                  ))}
                </tbody>
              </Table>
            </div>
          </Card>
        </>
      )}
    </div>
  );
}
