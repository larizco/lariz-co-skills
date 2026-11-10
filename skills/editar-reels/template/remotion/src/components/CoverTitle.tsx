import type { PlanEvent } from "../types";
import { COLORS, DISPLAY_FONT } from "../ui";

/**
 * Título estático de CAPA (thumbnail): enorme, branco, centralizado em `y`. A linha `highlight` vai numa
 * etiqueta na cor de destaque da marca. Usado nos planos `cover.json` (still), não no vídeo.
 */
export type CoverTitleProps = { lines: string[]; y: number; size: number; highlight?: number; rot?: number };

export const CoverTitle = ({ ev }: { ev: PlanEvent<CoverTitleProps> }) => {
  const { lines, y, size, highlight, rot = -3 } = ev.props;
  return (
    <div style={{ position: "absolute", left: 0, right: 0, top: y, transform: `translateY(-50%) rotate(${rot}deg)`, textAlign: "center" }}>
      {lines.map((l, i) =>
        i === highlight ? (
          <div key={i} style={{ marginTop: size * 0.12 }}>
            <span
              style={{
                display: "inline-block",
                fontFamily: DISPLAY_FONT,
                fontSize: size,
                lineHeight: 1.05,
                color: COLORS.ink,
                background: COLORS.soft[0],
                border: "8px solid #fff",
                borderRadius: size * 0.3,
                padding: `0 ${size * 0.3}px ${size * 0.08}px`,
                boxShadow: "0 18px 40px rgba(0,0,0,0.35)",
                whiteSpace: "nowrap",
              }}
            >
              {l}
            </span>
          </div>
        ) : (
          <div
            key={i}
            style={{
              fontFamily: DISPLAY_FONT,
              fontSize: size,
              lineHeight: 1.0,
              color: "#fff",
              whiteSpace: "nowrap",
              textShadow: "0 6px 26px rgba(0,0,0,0.55), 0 2px 10px rgba(0,0,0,0.65)",
            }}
          >
            {l}
          </div>
        ),
      )}
    </div>
  );
};
