import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Card } from '../components/Card';
import { reportesApi } from '../services/reportesApi';
import type { ReporteResumen } from '../types/reporte.types';
import { formatMoney } from '../utils/formatMoney';
import { currentPeriod } from '../utils/currentPeriod';

// Importamos las imágenes desde la carpeta assets (donde deben estar ahora)
import imgEmpleados from '../assets/empleado-del-mes.png';
import imgAsistencia from '../assets/ausencia.png';
import imgBonos from '../assets/bonos-del-gobierno.png';
import imgSueldos from '../assets/nomina-de-sueldos.png';
import imgBoletas from '../assets/factura.png';
import imgReportes from '../assets/informe.png';

const accesos = [
  { to: '/empleados', label: 'Empleados', img: imgEmpleados },
  { to: '/asistencia', label: 'Asistencia', img: imgAsistencia },
  { to: '/bonos-descuentos', label: 'Bonos y descuentos', img: imgBonos },
  { to: '/sueldos', label: 'Sueldos', img: imgSueldos },
  { to: '/boletas', label: 'Boletas', img: imgBoletas },
  { to: '/reportes', label: 'Reportes', img: imgReportes },
];

export function Dashboard() {
  const [resumen, setResumen] = useState<ReporteResumen | null>(null);
  const [error, setError] = useState('');

  useEffect(() => {
    let activo = true;
    reportesApi
      .resumen(currentPeriod())
      .then((response) => {
        if (activo) setResumen(response.data);
      })
      .catch(() => {
        if (activo) setError('No se pudo cargar el resumen del periodo.');
      });

    return () => {
      activo = false;
    };
  }, []);

  return (
    <div className="space-y-5">
      <header>
        <h2 className="text-2xl font-semibold text-slate-900">
          Menu principal
        </h2>
        <p className="text-sm text-slate-500">
          Resumen general del sistema y accesos rapidos.
        </p>
      </header>

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
            {resumen?.total_empleados ?? 0}
          </p>
        </Card>
        <Card>
          <p className="text-sm text-slate-500">Pagos</p>
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

      <div className="grid gap-4 md:grid-cols-3">
        {accesos.map((item) => (
          <Link
            className="flex items-center gap-3 rounded-md border border-slate-200 bg-white p-4 font-semibold text-slate-800 shadow-sm transition-colors hover:border-blue-300 hover:text-blue-700"
            key={item.to}
            to={item.to}
          >
            <img
              src={item.img}
              alt={item.label}
              className="h-10 w-10 object-contain"
            />
            <span>{item.label}</span>
          </Link>
        ))}
      </div>
    </div>
  );
}