export function isDatePassed(targetDateISO) {
  const targetDate = new Date(targetDateISO);
  const currentDate = new Date();

  return currentDate >= targetDate;
}
