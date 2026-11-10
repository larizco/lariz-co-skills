import { useVideoConfig } from "remotion";
import { ripple, springAt } from "../motion";
import { useClipTime } from "../time";
import type { PlanEvent } from "../types";
import { ACCENT_FONT, COLORS, DISPLAY_FONT, UI_FONT } from "../ui";
import { Check, Panel, pulse } from "./Panel";

/** Fecho "nesse vídeo:" — itens ganham check um a um, na palavra. `teaser` = chamada pra parte 2 (opcional). */
export type RecapProps = { title: string; items: { text: string; at: number }[]; teaser?: { text: string; at: number }; bg?: string };

export const Recap = ({ ev }: { ev: PlanEvent<RecapProps> }) => {
  const t = useClipTime();
  const { fps } = useVideoConfig();
  const p = ev.props;
  const tz = p.teaser ? springAt(t, p.teaser.at, fps, { damping: 7, mass: 0.5, stiffness: 220 }) : 0;
  return (
    <Panel ev={ev} seed={11} bg={p.bg ?? COLORS.soft[0]}>
      <div style={{ fontFamily: DISPLAY_FONT, fontSize: 48, color: COLORS.ink, marginBottom: 20 }}>{p.title}</div>
      {p.items.map((it, i) => {
        const done = t >= it.at;
        const pop = springAt(t, it.at, fps, { damping: 7, mass: 0.4, stiffness: 260 });
        return (
          <div key={i} style={{ display: "flex", alignItems: "center", gap: 16, background: done ? COLORS.paper : "rgba(255,255,255,0.5)", borderRadius: 22, padding: "16px 20px", marginBottom: 12, transform: `scale(${1 + pulse(t, it.at) * 0.05})`, boxShadow: ripple(t, it.at) }}>
            <Check done={done} pop={pop} size={36} />
            <span style={{ fontFamily: UI_FONT, fontWeight: 700, fontSize: 26, color: COLORS.ink }}>{it.text}</span>
          </div>
        );
      })}
      {tz > 0 && p.teaser ? (
        <div style={{ marginTop: 10, textAlign: "center", fontFamily: ACCENT_FONT, fontSize: 56, color: COLORS.accent, transform: `rotate(-4deg) scale(${tz})` }}>{p.teaser.text}</div>
      ) : null}
    </Panel>
  );
};
