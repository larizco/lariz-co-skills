import { useVideoConfig } from "remotion";
import { useEventClock } from "../time";
import { VERTICAL } from "../vertical";
import type { PlanEvent } from "../types";
import { BRAND } from "../brand";
import { UI_FONT } from "../ui";

// Palavra em destaque nunca entra misturada aqui — isso é o componente Keyword, sozinho na tela.
export type CaptionProps = { text: string };

export const Caption = ({ ev }: { ev: PlanEvent<CaptionProps> }) => {
  const { enter, exit } = useEventClock(ev);
  const { text } = ev.props;
  const vis = Math.min(enter(0, { damping: 16, mass: 0.6 }), exit(0.2));
  const dy = (1 - vis) * 22;
  const { width, height } = useVideoConfig();
  const v = height > width;

  return (
    <div
      style={{
        position: "absolute",
        left: v ? 80 : 260,
        right: v ? 80 : 260,
        bottom: v ? VERTICAL.captionBottom : 160,
        textAlign: "center",
        opacity: vis,
        transform: `translateY(${dy}px)`,
      }}
    >
      <span
        style={{
          fontFamily: UI_FONT,
          fontWeight: BRAND.caption.weight,
          fontSize: v ? 60 : 52,
          lineHeight: 1.22,
          color: BRAND.caption.color,
          textShadow: "0 2px 12px rgba(0,0,0,0.5), 0 1px 3px rgba(0,0,0,0.75)",
        }}
      >
        {text}
      </span>
    </div>
  );
};
