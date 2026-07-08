export function formatDate(value: string | Date) {
  return new Intl.DateTimeFormat('es-PE').format(new Date(value));
}
