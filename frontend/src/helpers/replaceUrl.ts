import placeholderImg from "@images/placeholder.png";

export function replaceUrl(url: string): string {
  if (url !== null) {
    return `https://chatlabs.site/aokibot/backend/${url}`;
  } else {
    return placeholderImg;
  }
}
