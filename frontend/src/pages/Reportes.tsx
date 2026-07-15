import { useEffect, useState } from 'react';
import { Download } from 'lucide-react';
import { Button } from '../components/Button';
import { Card } from '../components/Card';
import { Table } from '../components/Table';
import { reportesApi } from '../services/reportesApi';
import type {
  ReporteAsistenciaEmpleado,
  ReportePagoPeriodo,
  ReporteResumen,
} from '../types/reporte.types';
import { formatMoney } from '../utils/formatMoney';

export function Reportes() {
  const [resumen, setResumen] = useState<ReporteResumen | null>(null);
  const [pagos, setPagos] = useState<ReportePagoPeriodo[]>([]);
  const [asistencias, setAsistencias] = useState<ReporteAsistenciaEmpleado[]>(
    [],
  );
  const [error, setError] = useState('');
  const [descargando, setDescargando] = useState(false);

  useEffect(() => {
    Promise.all([
      reportesApi.resumen(),
      reportesApi.pagos(),
      reportesApi.asistencias(),
    ])
      .then(([resumenResponse, pagosResponse, asistenciasResponse]) => {
        setResumen(resumenResponse.data);
        setPagos(pagosResponse.data);
        setAsistencias(asistenciasResponse.data);
      })
      .catch(() => setError('No se pudieron cargar los reportes.'));
  }, []);

  async function descargarReporte() {
    setDescargando(true);
    setError('');

    try {
      const response = await reportesApi.descargarPdf();
      const url = URL.createObjectURL(response.data);
      const enlace = document.createElement('a');
      enlace.href = url;
      enlace.download = `reporte-staffy-${new Date().toISOString().slice(0, 10)}.pdf`;
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

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-semibold">Reportes</h2>
          <p className="mt-1 text-sm text-slate-500">
            Resumen de empleados, asistencias y pagos calculados por periodo.
          </p>
        </div>
        <Button
          className="inline-flex items-center gap-2 disabled:cursor-not-allowed disabled:bg-blue-300"
          disabled={descargando}
          type="button"
          onClick={descargarReporte}
        >
          <Download size={17} />
          {descargando ? 'Generando...' : 'Descargar PDF'}
        </Button>
      </div>

      {error && (
        <p className="rounded-md bg-red-50 px-3 py-2 text-sm text-red-700">
          {error}
        </p>
      )}

      <div className="grid gap-4 md:grid-cols-4">
        <Card>
          <p className="text-sm text-slate-500">Empleados activos</p>
          <p className="mt-2 text-2xl font-bold">
            {resumen?.total_empleados ?? 0}
          </p>
        </Card>
        <Card>
          <p className="text-sm text-slate-500">Pagos calculados</p>
          <p className="mt-2 text-2xl font-bold">
            {formatMoney(resumen?.total_pagos ?? 0)}
          </p>
        </Card>
        <Card>
          <p className="text-sm text-slate-500">Tardanzas</p>
          <p className="mt-2 text-2xl font-bold">
            {resumen?.total_tardanzas ?? 0}
          </p>
        </Card>
        <Card>
          <p className="text-sm text-slate-500">Faltas</p>
          <p className="mt-2 text-2xl font-bold">
            {resumen?.total_faltas ?? 0}
          </p>
        </Card>
      </div>

      <Card>
        <h3 className="mb-4 text-lg font-semibold">Pagos por periodo</h3>
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
            </tbody>
          </Table>
        </div>
      </Card>
    </div>
  );
}
