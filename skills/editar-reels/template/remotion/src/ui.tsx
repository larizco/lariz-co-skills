import type { CSSProperties } from "react";
import { BRAND } from "./brand";

/** Atalhos pros tokens da marca (src/brand.ts é gerado a partir de <projeto>/marca/tokens.json). */
export const COLORS = BRAND.colors;
export const DISPLAY_FONT = BRAND.fonts.display;
export const ACCENT_FONT = BRAND.fonts.script;
export const UI_FONT = BRAND.fonts.body;

export const softShadow = "0 8px 24px rgba(0,0,0,0.12)";

export const paperCard = (bg: string = COLORS.paper): CSSProperties => ({
  background: bg,
  borderRadius: 20,
  border: `1px solid ${COLORS.border}`,
});

/** cor suave n (gira na lista de cores suaves da marca) */
export const soft = (n: number) => COLORS.soft[((n % COLORS.soft.length) + COLORS.soft.length) % COLORS.soft.length];
