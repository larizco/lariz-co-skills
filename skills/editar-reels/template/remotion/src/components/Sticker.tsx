import { Img, staticFile, useVideoConfig } from "remotion";
import { idleFloat, springAt } from "../motion";
import { useEventClock } from "../time";
import type { PlanEvent } from "../types";

/**
 * Elemento solto da marca (SVG/PNG de public/marca/elementos/ ou emoji) que entra com soco, flutua e sai.
 * Posição em px do quadro (x, y = centro). Use pra reforçar uma palavra: seta, coração, selo, rabisco, estrela.
 */
export type StickerProps = { src?: string; emoji?: string; x: number; y: number; size?: number; rot?: number };

export const Sticker = ({ ev }: { ev: PlanEvent<StickerProps> }) => {
  const { t, local, fps, exit } = useEventClock(ev);
  const { width } = useVideoConfig();
  const p = ev.props;
  const size = p.size ?? Math.round(width * 0.14);
  const inn = springAt(local, 0, fps, { damping: 8, mass: 0.5, stiffness: 240 });
  const out = exit(0.25);
  const fl = idleFloat(t, p.x);
  return (
    <div
      style={{
        position: "absolute",
        left: p.x - size / 2,
        top: p.y - size / 2,
        width: size,
        height: size,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        opacity: Math.min(1, inn * 1.5, out * 1.5),
        transform: `translateY(${fl.y}px) rotate(${(p.rot ?? -8) + fl.rot * 3 + (1 - inn) * -30}deg) scale(${inn * out})`,
      }}
    >
      {p.src ? (
        <Img src={staticFile(p.src)} style={{ width: "100%", height: "100%", objectFit: "contain" }} />
      ) : (
        <span style={{ fontSize: size * 0.85, lineHeight: 1 }}>{p.emoji ?? "✨"}</span>
      )}
    </div>
  );
};
