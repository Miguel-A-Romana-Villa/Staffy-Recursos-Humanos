import { useEffect, useState } from 'react';
import { Download } from 'lucide-react';
import { Button } from '../components/Button';
import { Card } from '../components/Card';
import { Input } from '../components/Input';
import { Table } from '../components/Table';
import { reportesApi } from '../services/reportesApi';
import type { ReporteGeneral } from '../types/reporte.types';
import { currentPeriod } from '../utils/currentPeriod';
import { formatMoney } from '../utils/formatMoney';

export function Reportes() {
  const [periodo, setPeriodo] = useState(currentPeriod);
  const [reporte, setReporte] = useState<ReporteGeneral | null>(null);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState('');
  const [descargando, setDescargando] = useState(false);

  useEffect(() => {
    let activo = true;
    setCargando(true);
    setError('');
    setReporte(null);

    reportesApi
      .general(periodo)
      .then((response) => {
        if (activo) setReporte(response.data);
      })
      .catch(() => {
        if (activo) setError('No se pudieron cargar los reportes.');
      })
      .finally(() => {
        if (activo) setCargando(false);
      });

    return () => {
      activo = false;
    };
  }, [periodo]);

  async function descargarReporte() {
    setDescargando(true);
    setError('');

    try {
      const response = await reportesApi.descargarPdf(periodo);
      const url = URL.createObjectURL(response.data);
      const enlace = document.createElement('a');
      enlace.href = url;
      enlace.download = `reporte-staffy-${periodo}.pdf`;
      document.body.appendChild(enlace);
      enlace.click();
      enlace.remove();
      URL.revokeObjectURL(url);
    } catch {
      setError('No se pudo generar el reporte PDF.');
    } finally {
      setDescargando(false);
    }
  }

  const pagos = reporte?.pagos ?? [];
  const asistencias = reporte?.asistencias ?? [];

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <h2 className="text-2xl font-semibold">Reportes</h2>
          <p className="mt-1 text-sm text-slate-500">
            Resumen de empleados, asistencias y pagos del periodo seleccionado.
          </p>
        </div>
        <div className="flex flex-wrap items-end gap-3">
          <label>
            <span className="mb-1 block text-sm font-medium text-slate-700">
              Periodo
            </span>
            <Input
              aria-label="Periodo del reporte"
              type="month"
              value={periodo}
              onChange={(event) => {
                if (event.target.value) setPeriodo(event.target.value);
              }}
            />
          </label>
          <Button
            className="inline-flex items-center gap-2 disabled:cursor-not-allowed disabled:bg-blue-300"
            disabled={descargando || cargando || !reporte}
            type="button"
            onClick={descargarReporte}
          >
            <Download size={17} />
            {descargando ? 'Generando...' : 'Descargar PDF'}
          </Button>
        </div>
      </div>

      {cargando && (
        <p className="text-sm text-slate-500" role="status">
          Cargando reporte...
        </p>
      )}
      {error && (
        <p
          className="rounded-md bg-red-50 px-3 py-2 text-sm text-red-700"
          role="alert"
        >
          {error}
        </p>
      )}

      <div className="grid gap-4 md:grid-cols-4">
        <Card>
          <p className="text-sm text-slate-500">Empleados activos</p>
          <p className="mt-2 text-2xl font-bold">
            {reporte?.resumen.total_empleados ?? '—'}
          </p>
        </Card>
        <Card>
          <p className="text-sm text-slate-500">Pagos calculados</p>
          <p className="mt-2 text-2xl font-bold">
            {reporte ? formatMoney(reporte.resumen.total_pagos) : '—'}
          </p>
        </Card>
        <Card>
          <p className="text-sm text-slate-500">Tardanzas</p>
          <p className="mt-2 text-2xl font-bold">
            {reporte?.resumen.total_tardanzas ?? '—'}
          </p>
        </Card>
        <Card>
          <p className="text-sm text-slate-500">Faltas</p>
          <p className="mt-2 text-2xl font-bold">
            {reporte?.resumen.total_faltas ?? '—'}
          </p>
        </Card>
      </div>

      <Card>
        <h3 className="mb-4 text-lg font-semibold">Pagos del periodo</h3>
        <div className="overflow-x-auto">
          <Table>
            <thead className="bg-slate-100 text-left text-xs uppercase text-slate-500">
              <tr>
                <th className="px-3 py-2">Periodo</th>
                <th className="px-3 py-2">Boletas</th>
                <th className="px-3 py-2">Total pagado</th>
              </tr>
            </thead>
            <tbody>
              {pagos.map((pago) => (
                <tr className="border-t border-slate-100" key={pago.periodo}>
                  <td className="px-3 py-3">{pago.periodo}</td>
                  <td className="px-3 py-3">{pago.cantidad_boletas}</td>
                  <td className="px-3 py-3 font-semibold">
                    {formatMoney(pago.total_pagado)}
                  </td>
                </tr>
              ))}
              {!cargando && pagos.length === 0 && (
                <tr>
                  <td className="px-3 py-4 text-sm text-slate-500" colSpan={3}>
                    No hay pagos registrados en este periodo.
                  </td>
                </tr>
              )}
            </tbody>
          </Table>
        </div>
      </Card>

      <Card>
        <h3 className="mb-4 text-lg font-semibold">Asistencias por empleado</h3>
        <div className="overflow-x-auto">
          <Table>
            <thead className="bg-slate-100 text-left text-xs uppercase text-slate-500">
              <tr>
                <th className="px-3 py-2">Empleado</th>
                <th className="px-3 py-2">Asistio</th>
                <th className="px-3 py-2">Tarde</th>
                <th className="px-3 py-2">Falto</th>
              </tr>
            </thead>
            <tbody>
              {asistencias.map((asistencia) => (
                <tr
                  className="border-t border-slate-100"
                  key={asistencia.empleado_codigo}
                >
                  <td className="px-3 py-3">
                    <p className="font-medium">{asistencia.empleado_nombre}</p>
                    <p className="text-xs text-slate-500">
                      {asistencia.empleado_codigo}
                    </p>
                  </td>
                  <td className="px-3 py-3">{asistencia.asistio}</td>
                  <td className="px-3 py-3">{asistencia.tarde}</td>
                  <td className="px-3 py-3">{asistencia.falto}</td>
                </tr>
              ))}
              {!cargando && asistencias.length === 0 && (
                <tr>
                  <td className="px-3 py-4 text-sm text-slate-500" colSpan={4}>
                    No hay empleados activos en este periodo.
                  </td>
                </tr>
              )}
            </tbody>
          </Table>
        </div>
      </Card>
    </div>
  );
}
