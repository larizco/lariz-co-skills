import { interpolate, useVideoConfig } from "remotion";
import { springAt } from "../motion";
import { useEventClock } from "../time";
import type { PlanEvent } from "../types";
import { DISPLAY_FONT } from "../ui";

/**
 * Título gigante do gancho (fonte display da marca, branco), cada linha pula quando a pessoa fala a palavra (`at`).
 * Combine com qualquer card no lado oposto (no vertical: título à esquerda e card à direita, acima da cabeça,
 * com `layout: {x, y, scale}` no evento do card).
 */
export type HookTitleProps = { lines: { text: string; at: number }[]; size?: number };

export const HookTitle = ({ ev }: { ev: PlanEvent<HookTitleProps> }) => {
  const { t, fps, local, exit } = useEventClock(ev);
  const { width, height } = useVideoConfig();
  const v = height > width;
  const out = exit(0.3);
  const size = ev.props.size ?? (v ? 90 : 150);
  return (
    <div style={{ position: "absolute", left: v ? 46 : 70, top: v ? 300 : "50%", transform: `translate(${-(1 - out) * 120}px, ${v ? 0 : "-50%"})`, opacity: out }}>
      {ev.props.lines.map((line, i) => {
        const inn = springAt(local, i * 0.08, fps, { damping: 10, mass: 0.6, stiffness: 200 });
        const d = t - line.at;
        const hit = d > 0 && d < 0.45 ? Math.sin((d / 0.45) * Math.PI) : 0;
        return (
          <div
            key={i}
            style={{
              fontFamily: DISPLAY_FONT,
              fontSize: size,
              lineHeight: 1.0,
              color: "#fff",
              whiteSpace: "nowrap",
              textShadow: "0 4px 20px rgba(0,0,0,0.5), 0 2px 10px rgba(0,0,0,0.6)",
              opacity: Math.min(1, inn * 1.5),
              transform: `translateY(${(1 - inn) * 80}px) scale(${interpolate(inn, [0, 1], [0.6, 1]) + hit * 0.09}) rotate(${hit * (i % 2 ? 2 : -2)}deg)`,
              transformOrigin: "left center",
            }}
          >
            {line.text}
          </div>
        );
      })}
    </div>
  );
};
