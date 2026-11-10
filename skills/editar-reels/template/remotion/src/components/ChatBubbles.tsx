import { interpolate, useVideoConfig } from "remotion";
import { springAt } from "../motion";
import { useClipTime } from "../time";
import type { PlanEvent } from "../types";
import { COLORS, UI_FONT } from "../ui";
import { Panel } from "./Panel";

/**
 * Conversa de celular: mensagens chegando (`at`), com "digitando" (3 pontinhos) antes das de `from: "them"`.
 * Bom pra pergunta de seguidor, depoimento, objeção ("mas eu não tenho tempo...") e resposta.
 */
export type ChatBubblesProps = {
  header?: string;
  messages: { from: "me" | "them"; text: string; at: number }[];
};

const Dots = ({ t }: { t: number }) => (
  <div style={{ display: "flex", gap: 8, padding: "18px 22px" }}>
    {[0, 1, 2].map((k) => (
      <div key={k} style={{ width: 12, height: 12, borderRadius: 6, background: COLORS.muted, opacity: 0.4 + 0.6 * Math.abs(Math.sin(t * 6 + k)) }} />
    ))}
  </div>
);

export const ChatBubbles = ({ ev }: { ev: PlanEvent<ChatBubblesProps> }) => {
  const t = useClipTime();
  const { fps } = useVideoConfig();
  const p = ev.props;
  return (
    <Panel ev={ev} seed={5} pad="26px 26px 30px">
      {p.header ? (
        <div style={{ textAlign: "center", fontFamily: UI_FONT, fontWeight: 700, fontSize: 24, color: COLORS.muted, marginBottom: 16 }}>{p.header}</div>
      ) : null}
      <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
        {p.messages.map((m, i) => {
          const me = m.from === "me";
          const typing = !me && t >= m.at - 0.8 && t < m.at;
          if (typing)
            return (
              <div key={i} style={{ alignSelf: "flex-start", background: COLORS.soft[0], borderRadius: 26 }}>
                <Dots t={t} />
              </div>
            );
          const inn = springAt(t, m.at, fps, { damping: 11, mass: 0.5, stiffness: 220 });
          if (inn <= 0) return null;
          return (
            <div
              key={i}
              style={{
                alignSelf: me ? "flex-end" : "flex-start",
                maxWidth: "82%",
                background: me ? COLORS.accent : COLORS.soft[0],
                color: me ? "#fff" : COLORS.ink,
                fontFamily: UI_FONT,
                fontWeight: 600,
                fontSize: 28,
                lineHeight: 1.25,
                padding: "16px 22px",
                borderRadius: me ? "26px 26px 8px 26px" : "26px 26px 26px 8px",
                transformOrigin: me ? "right bottom" : "left bottom",
                transform: `scale(${interpolate(inn, [0, 1], [0.5, 1])})`,
                opacity: Math.min(1, inn * 1.5),
              }}
            >
              {m.text}
            </div>
          );
        })}
      </div>
    </Panel>
  );
};
