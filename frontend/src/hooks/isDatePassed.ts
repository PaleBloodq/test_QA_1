export function isDatePassed(targetDateISO: string) {
  const targetDate = new Date(targetDateISO);
  const currentDate = new Date();

  return currentDate >= targetDate;
}
