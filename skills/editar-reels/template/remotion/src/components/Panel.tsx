import type { CSSProperties, ReactNode } from "react";
import { interpolate } from "remotion";
import { idleFloat } from "../motion";
import { useEventClock } from "../time";
import type { PlanEvent } from "../types";
import { COLORS, softShadow } from "../ui";

/**
 * Moldura padrão dos componentes ao lado dela: coluna direita, centralizada na vertical, entra com soco de zoom +
 * giro (overshoot), flutua de leve enquanto está na tela e sai encolhendo/girando. Todo componente novo usa isto.
 */
export const PANEL_LEFT = 1290;
export const PANEL_W = 600;

export const Panel = ({
  ev,
  children,
  bg = COLORS.paper,
  seed = 0,
  pad = "34px 34px",
  style,
  bare = false,
  clip = true,
}: {
  ev: PlanEvent<any>;
  children: ReactNode;
  bg?: string;
  seed?: number;
  pad?: string;
  style?: CSSProperties;
  bare?: boolean; // sem o cartão branco (o filho desenha o próprio fundo)
  clip?: boolean; // false = carimbos/stickers podem sair pra fora do card
}) => {
  const { t, enter, exit } = useEventClock(ev);
  const vis = enter(0, { damping: 9, mass: 0.6, stiffness: 200 });
  const out = exit(0.3);
  const fl = idleFloat(t, seed);
  const dir = seed % 2 ? 1 : -1;
  return (
    <div
      style={{
        position: "absolute",
        left: PANEL_LEFT,
        top: 540,
        width: PANEL_W,
        opacity: Math.min(1, vis * 1.5, out * 1.5),
        transform: `translate(${(1 - vis) * 140}px, calc(-50% + ${fl.y + (1 - out) * 40}px)) rotate(${fl.rot + (1 - vis) * 9 * dir + (1 - out) * -8 * dir}deg) scale(${interpolate(vis, [0, 1], [0.5, 1]) * interpolate(out, [0, 1], [0.7, 1])})`,
        ...style,
      }}
    >
      {bare ? (
        children
      ) : (
        <div style={{ background: bg, borderRadius: 44, padding: pad, boxShadow: "0 30px 70px rgba(0,0,0,0.35), " + softShadow, position: "relative", overflow: clip ? "hidden" : "visible" }}>
          {children}
        </div>
      )}
    </div>
  );
};

/** quanto um "toque" pulsa (0..1..0) logo depois de `at` — pra fazer o card inteiro reagir. */
export const pulse = (t: number, at: number | undefined, dur = 0.3) => {
  if (at === undefined) return 0;
  const d = t - at;
  return d > 0 && d < dur ? Math.sin((d / dur) * Math.PI) : 0;
};

/** texto sendo digitado entre `from` e `to` (com cursor piscando). */
export const typed = (text: string, t: number, from: number, to: number) => {
  if (t < from) return "";
  const n = Math.round(Math.min(1, (t - from) / Math.max(0.01, to - from)) * text.length);
  return text.slice(0, n);
};
export const Caret = ({ t, show = true }: { t: number; show?: boolean }) =>
  show && Math.floor(t * 2.4) % 2 === 0 ? <span style={{ display: "inline-block", width: 3, height: "1em", background: "currentColor", marginLeft: 2, verticalAlign: "-0.12em" }} /> : null;

export const Check = ({ done, pop, size = 36 }: { done: boolean; pop: number; size?: number }) => (
  <div
    style={{
      width: size,
      height: size,
      borderRadius: size / 2,
      flexShrink: 0,
      boxSizing: "border-box",
      border: `3px solid ${done ? COLORS.success : "rgba(0,0,0,0.25)"}`,
      background: done ? COLORS.success : "transparent",
      color: "#fff",
      fontWeight: 800,
      fontSize: size * 0.55,
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      transform: `scale(${done ? 0.6 + Math.min(1.2, pop) * 0.4 : 1})`,
    }}
  >
    {done ? "✓" : ""}
  </div>
);
