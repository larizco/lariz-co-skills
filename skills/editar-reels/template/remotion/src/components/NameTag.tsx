import { interpolate, useVideoConfig } from "remotion";
import { useEventClock } from "../time";
import type { PlanEvent } from "../types";
import { ACCENT_FONT } from "../ui";

/**
 * Apresentação "eu sou a <nome>": nome em fonte manuscrita branca + seta à mão apontando pra cabeça da pessoa.
 * A seta é SVG (traço se desenhando). Tudo em px do quadro (1920x1080 ou 1080x1920): ajuste `x/y` do texto e
 * `arrow` (start/ctrl/tip) por vídeo e confira num still — a ponta tem que mirar a cabeça.
 */
type Pt = { x: number; y: number };
export type NameTagProps = { lines: string[]; x?: number; y?: number; size?: number; arrow?: { start: Pt; ctrl: Pt; tip: Pt } };

const DEFAULT_ARROW = { start: { x: 470, y: 222 }, ctrl: { x: 575, y: 120 }, tip: { x: 668, y: 238 } };

export const NameTag = ({ ev }: { ev: PlanEvent<NameTagProps> }) => {
  const { local, enter, exit } = useEventClock(ev);
  const { lines, x = 80, y = 150, size = 132 } = ev.props;
  const { start: START, ctrl: CTRL, tip: TIP } = ev.props.arrow ?? DEFAULT_ARROW;
  const ARC = `M ${START.x} ${START.y} Q ${CTRL.x} ${CTRL.y} ${TIP.x} ${TIP.y}`;
  const { width, height } = useVideoConfig();
  const out = exit(0.2);
  const pop = enter(0, { damping: 10, mass: 0.5, stiffness: 220 });

  // "escrita à mão": cada linha se revela da esquerda pra direita
  const reveal = (i: number) => interpolate(local, [i * 0.16, i * 0.16 + 0.3], [0, 100], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  // seta se desenha depois do texto
  const draw = interpolate(local, [0.28, 0.58], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const head = interpolate(local, [0.55, 0.68], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  // ponta "cutuca" de leve na direção dela depois de desenhada
  const nudge = local > 0.68 ? Math.sin((local - 0.68) * 14) * 5 * Math.exp(-(local - 0.68) * 3) : 0;

  const ang = Math.atan2(TIP.y - CTRL.y, TIP.x - CTRL.x);
  const wing = (d: number) => `${TIP.x - 34 * Math.cos(ang + d)} ${TIP.y - 34 * Math.sin(ang + d)}`;
  const shadow = "drop-shadow(0 2px 0 rgba(0,0,0,0.75)) drop-shadow(0 4px 12px rgba(0,0,0,0.35))";

  return (
    <div style={{ position: "absolute", inset: 0, opacity: out }}>
      <div
        style={{
          position: "absolute",
          left: x,
          top: y,
          transform: `rotate(-6deg) scale(${interpolate(pop, [0, 1], [0.7, 1])})`,
          transformOrigin: "left center",
        }}
      >
        {lines.map((line, i) => (
          <div
            key={i}
            style={{
              fontFamily: ACCENT_FONT,
              fontSize: size,
              lineHeight: 1.0,
              color: "#fff",
              marginLeft: i * 30,
              clipPath: `inset(-20% ${100 - reveal(i)}% -30% -5%)`,
              filter: shadow,
            }}
          >
            {line}
          </div>
        ))}
      </div>
      <svg
        width={width}
        height={height}
        style={{ position: "absolute", inset: 0, filter: shadow, transform: `translate(${nudge * Math.cos(ang)}px, ${nudge * Math.sin(ang)}px)` }}
      >
        <path
          d={ARC}
          fill="none"
          stroke="#fff"
          strokeWidth={8}
          strokeLinecap="round"
          pathLength={1}
          strokeDasharray={1}
          strokeDashoffset={1 - draw}
        />
        {head > 0 ? (
          <path
            d={`M ${wing(0.5)} L ${TIP.x} ${TIP.y} L ${wing(-0.5)}`}
            fill="none"
            stroke="#fff"
            strokeWidth={8}
            strokeLinecap="round"
            strokeLinejoin="round"
            style={{ transformOrigin: `${TIP.x}px ${TIP.y}px`, transform: `scale(${head})` }}
          />
        ) : null}
      </svg>
    </div>
  );
};
