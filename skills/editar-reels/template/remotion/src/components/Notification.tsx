import { Img, interpolate, staticFile, useVideoConfig } from "remotion";
import { BRAND } from "../brand";
import { springAt } from "../motion";
import { useClipTime } from "../time";
import type { PlanEvent } from "../types";
import { COLORS, UI_FONT } from "../ui";
import { Panel } from "./Panel";

/**
 * Pilha de notificações de celular caindo (`at`); a mais nova entra em cima. `shakeAt` = a pilha treme
 * (sobrecarga, "tudo ao mesmo tempo"). Ícone = emoji do item ou logo da marca.
 */
export type NotificationProps = {
  items: { app?: string; title: string; text: string; at: number; emoji?: string; time?: string }[];
  shakeAt?: number;
};

export const Notification = ({ ev }: { ev: PlanEvent<NotificationProps> }) => {
  const t = useClipTime();
  const { fps } = useVideoConfig();
  const p = ev.props;
  const shake =
    p.shakeAt !== undefined && t > p.shakeAt && t < p.shakeAt + 0.6 ? Math.sin((t - p.shakeAt) * 60) * 8 * (1 - (t - p.shakeAt) / 0.6) : 0;
  const shown = p.items.filter((it) => t >= it.at);
  return (
    <Panel ev={ev} seed={7} bare>
      <div style={{ display: "flex", flexDirection: "column", gap: 14, transform: `translateX(${shake}px)` }}>
        {[...shown].reverse().map((it, i) => {
          const inn = springAt(t, it.at, fps, { damping: 12, mass: 0.6, stiffness: 200 });
          return (
            <div
              key={`${it.at}-${it.title}`}
              style={{
                display: "flex",
                gap: 18,
                alignItems: "center",
                background: "rgba(255,255,255,0.96)",
                borderRadius: 34,
                padding: "20px 24px",
                border: `1px solid ${COLORS.border}`,
                transform: `translateY(${(1 - inn) * -120}px) scale(${interpolate(inn, [0, 1], [0.85, 1]) - i * 0.02})`,
                opacity: Math.min(1, inn * 1.6),
              }}
            >
              <div
                style={{
                  width: 76,
                  height: 76,
                  borderRadius: 20,
                  background: COLORS.soft[0],
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  fontSize: 42,
                  flexShrink: 0,
                  overflow: "hidden",
                }}
              >
                {it.emoji ?? (BRAND.logo ? <Img src={staticFile(BRAND.logo)} style={{ width: "100%", height: "100%", objectFit: "cover" }} /> : "🔔")}
              </div>
              <div style={{ flex: 1, minWidth: 0, fontFamily: UI_FONT, color: COLORS.ink }}>
                <div style={{ display: "flex", justifyContent: "space-between", fontSize: 20, color: COLORS.muted }}>
                  <span>{it.app ?? BRAND.name}</span>
                  <span>{it.time ?? "agora"}</span>
                </div>
                <div style={{ fontWeight: 800, fontSize: 26, marginTop: 2 }}>{it.title}</div>
                <div style={{ fontSize: 24, lineHeight: 1.25 }}>{it.text}</div>
              </div>
            </div>
          );
        })}
      </div>
    </Panel>
  );
};
