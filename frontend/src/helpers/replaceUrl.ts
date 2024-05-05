import placeholderImg from "@images/placeholder.png";

export function replaceUrl(url: string): string {
  if (url !== null && url !== undefined) {
    return `https://chatlabs.site/aokibot/backend/${url}`;
  } else {
    return placeholderImg;
  }
}
