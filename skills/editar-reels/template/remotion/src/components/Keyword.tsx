import { interpolate, useVideoConfig } from "remotion";
import { VERTICAL } from "../vertical";
import { useEventClock } from "../time";
import type { PlanEvent } from "../types";
import { BRAND } from "../brand";
import { DISPLAY_FONT } from "../ui";

/** Palavra-chave sozinha na tela, sem se misturar com a legenda normal (fonte de display da marca, grande). */
export type KeywordProps = { text: string };

export const Keyword = ({ ev }: { ev: PlanEvent<KeywordProps> }) => {
  const { enter, exit } = useEventClock(ev);
  const { text } = ev.props;
  const vis = Math.min(enter(0, { damping: 9, mass: 0.6, stiffness: 220 }), exit(0.2));
  const scale = interpolate(vis, [0, 1], [1.5, 1]);
  const { width, height } = useVideoConfig();
  const v = height > width;

  return (
    <div style={{ position: "absolute", left: 0, right: 0, bottom: v ? VERTICAL.captionBottom - 10 : 150, textAlign: "center", opacity: vis }}>
      <span
        style={{
          fontFamily: DISPLAY_FONT,
          fontSize: v ? 104 : 88,
          color: BRAND.caption.keywordColor,
          textShadow: "0 3px 16px rgba(0,0,0,0.6), 0 1px 4px rgba(0,0,0,0.85)",
          display: "inline-block",
          transform: `scale(${scale})`,
        }}
      >
        {text}
      </span>
    </div>
  );
};
