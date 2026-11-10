import { interpolate, useVideoConfig } from "remotion";
import { ripple, springAt } from "../motion";
import { useClipTime } from "../time";
import type { PlanEvent } from "../types";
import { ACCENT_FONT, COLORS, DISPLAY_FONT, UI_FONT } from "../ui";
import { Check, Panel, pulse } from "./Panel";

/**
 * Lista viva: título + itens que CAEM um a um (`at`), e opcionalmente ganham check (`doneAt`) ou risco (`strikeAt`).
 * `stamp` = carimbo manuscrito que entra no fim. Serve pra passos, dicas, erros comuns, "o que eu uso", checklist.
 */
export type ListCardProps = {
  title: string;
  items: { text: string; at: number; doneAt?: number; strikeAt?: number; emoji?: string }[];
  stamp?: { text: string; at: number };
  bg?: string;
  numbered?: boolean;
};

export const ListCard = ({ ev }: { ev: PlanEvent<ListCardProps> }) => {
  const t = useClipTime();
  const { fps } = useVideoConfig();
  const p = ev.props;
  const st = p.stamp ? springAt(t, p.stamp.at, fps, { damping: 7, mass: 0.5, stiffness: 240 }) : 0;
  return (
    <Panel ev={ev} seed={3} bg={p.bg ?? COLORS.paper} clip={false}>
      <div style={{ fontFamily: DISPLAY_FONT, fontSize: 50, color: COLORS.ink, marginBottom: 22, lineHeight: 1.05 }}>{p.title}</div>
      {p.items.map((it, i) => {
        const inn = springAt(t, it.at, fps, { damping: 10, mass: 0.6, stiffness: 200 });
        if (inn <= 0) return null;
        const done = it.doneAt !== undefined && t >= it.doneAt;
        const pop = it.doneAt !== undefined ? springAt(t, it.doneAt, fps, { damping: 7, mass: 0.4, stiffness: 260 }) : 0;
        const strike =
          it.strikeAt !== undefined ? interpolate(t, [it.strikeAt, it.strikeAt + 0.35], [0, 100], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }) : 0;
        return (
          <div
            key={i}
            style={{
              display: "flex",
              alignItems: "center",
              gap: 16,
              background: COLORS.soft[i % COLORS.soft.length],
              borderRadius: 22,
              padding: "16px 20px",
              marginBottom: 12,
              opacity: Math.min(1, inn * 1.4),
              transform: `translateY(${(1 - inn) * -60}px) scale(${interpolate(inn, [0, 1], [0.7, 1]) + pulse(t, it.doneAt) * 0.05})`,
              boxShadow: ripple(t, it.doneAt),
            }}
          >
            {it.doneAt !== undefined ? (
              <Check done={done} pop={pop} size={36} />
            ) : p.numbered ? (
              <b style={{ fontFamily: DISPLAY_FONT, fontSize: 34, color: COLORS.accent, width: 36 }}>{i + 1}</b>
            ) : null}
            {it.emoji ? <span style={{ fontSize: 34 }}>{it.emoji}</span> : null}
            <span style={{ position: "relative", fontFamily: UI_FONT, fontWeight: 700, fontSize: 28, color: done ? COLORS.muted : COLORS.ink }}>
              {it.text}
              {strike > 0 ? <span style={{ position: "absolute", left: 0, top: "52%", height: 4, width: `${strike}%`, background: COLORS.accent, borderRadius: 2 }} /> : null}
            </span>
          </div>
        );
      })}
      {st > 0 && p.stamp ? (
        <div style={{ position: "absolute", right: -30, bottom: -36, transform: `rotate(-8deg) scale(${st})` }}>
          <span
            style={{
              display: "inline-block",
              fontFamily: ACCENT_FONT,
              fontSize: 48,
              color: COLORS.ink,
              background: COLORS.accent2,
              padding: "2px 26px 10px",
              borderRadius: 20,
              border: "4px solid #fff",
              whiteSpace: "nowrap",
            }}
          >
            {p.stamp.text}
          </span>
        </div>
      ) : null}
    </Panel>
  );
};
