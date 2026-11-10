import { useVideoConfig } from "remotion";
import { keyframed, springAt } from "../motion";
import { useClipTime } from "../time";
import type { PlanEvent } from "../types";
import { COLORS, DISPLAY_FONT, UI_FONT } from "../ui";
import { Panel, pulse } from "./Panel";

/**
 * Número que ROLA até o valor (contador com overshoot) + barra enchendo opcional. Pra dado, resultado,
 * antes/depois, "em 30 dias", "3x mais". `steps` = keyframes [{at, v}] (o primeiro costuma ser {at: start, v: 0}).
 */
export type BigNumberProps = {
  label: string;
  steps: { at: number; v: number }[];
  prefix?: string;
  suffix?: string;
  max?: number;
  caption?: string;
  decimals?: number;
};

export const BigNumber = ({ ev }: { ev: PlanEvent<BigNumberProps> }) => {
  const t = useClipTime();
  const { fps } = useVideoConfig();
  const p = ev.props;
  const v = keyframed(t, fps, p.steps);
  const last = p.steps[p.steps.length - 1];
  const cap = p.caption ? springAt(t, last.at + 0.3, fps) : 0;
  return (
    <Panel ev={ev} seed={9} bg={COLORS.soft[1 % COLORS.soft.length]}>
      <div style={{ fontFamily: UI_FONT, fontWeight: 700, fontSize: 28, color: COLORS.muted }}>{p.label}</div>
      <div
        style={{
          fontFamily: DISPLAY_FONT,
          fontSize: 150,
          lineHeight: 1.05,
          color: COLORS.ink,
          transform: `scale(${1 + pulse(t, last.at, 0.4) * 0.08})`,
          transformOrigin: "left center",
          whiteSpace: "nowrap",
        }}
      >
        {p.prefix ?? ""}
        {v.toFixed(p.decimals ?? 0)}
        {p.suffix ?? ""}
      </div>
      {p.max ? (
        <div style={{ height: 22, borderRadius: 11, background: "rgba(0,0,0,0.08)", overflow: "hidden", marginTop: 8 }}>
          <div style={{ height: "100%", width: `${Math.max(0, Math.min(1, v / p.max)) * 100}%`, background: COLORS.accent, borderRadius: 11 }} />
        </div>
      ) : null}
      {cap > 0 ? (
        <div style={{ marginTop: 18, fontFamily: UI_FONT, fontWeight: 700, fontSize: 28, color: COLORS.ink, opacity: cap, transform: `translateY(${(1 - cap) * 20}px)` }}>
          {p.caption}
        </div>
      ) : null}
    </Panel>
  );
};
