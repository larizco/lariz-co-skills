import { COLORS } from "../ui";

/** Explosão de confete (t = segundos desde o disparo; some em 1,4 s). Cores da marca. */
export const Confetti = ({ t, n = 18 }: { t: number; n?: number }) => {
  if (t < 0 || t > 1.4) return null;
  const cols = [COLORS.accent, COLORS.accent2, ...COLORS.soft, COLORS.success];
  return (
    <>
      {Array.from({ length: n }).map((_, k) => {
        const a = (k / n) * Math.PI * 2 + k;
        const sp = 220 + (k % 5) * 40;
        const x = Math.cos(a) * sp * t;
        const y = Math.sin(a) * sp * t + 260 * t * t;
        return (
          <div
            key={k}
            style={{
              position: "absolute",
              left: "50%",
              top: "40%",
              width: 12,
              height: 7,
              background: cols[k % cols.length],
              borderRadius: 2,
              transform: `translate(${x}px, ${y}px) rotate(${t * 600 + k * 40}deg)`,
              opacity: 1 - t / 1.4,
            }}
          />
        );
      })}
    </>
  );
};
