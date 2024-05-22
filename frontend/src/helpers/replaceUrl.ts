import placeholderImg from "@images/placeholder.png";

export function replaceUrl(url: string): string {
  if (url !== null && url !== undefined) {
    return `${import.meta.env.VITE_API_URL}${url}`;
  } else {
    return placeholderImg;
  }
}
