import { spring } from "remotion";

type SpringCfg = Parameters<typeof spring>[0]["config"];

/** spring que dispara no segundo absoluto `at` (base do edit-plan). */
export const springAt = (t: number, at: number, fps: number, config: SpringCfg = { damping: 14, mass: 0.7 }) =>
  t < at ? 0 : spring({ frame: (t - at) * fps, fps, config });

/** Valor que pula de keyframe em keyframe com spring (cada mudança "rola" com leve overshoot). */
export const keyframed = (
  t: number,
  fps: number,
  frames: { at: number; v: number }[],
  config: SpringCfg = { damping: 13, mass: 0.8, stiffness: 120 },
) => {
  let v = frames[0].v;
  for (let i = 1; i < frames.length; i++) v += (frames[i].v - frames[i - 1].v) * springAt(t, frames[i].at, fps, config);
  return v;
};

/** Mergulho rápido de "toque" (escala) ao redor de `at`: 1 → 0.9 → 1. */
export const tapScale = (t: number, at: number | undefined, fps: number) => {
  if (at === undefined || t < at - 0.12) return 1;
  if (t < at) return 1 - ((t - (at - 0.12)) / 0.12) * 0.1;
  return 0.9 + 0.1 * springAt(t, at, fps, { damping: 8, mass: 0.5, stiffness: 260 });
};

/** Anel de "toque" que expande e some depois de `at` (sem mouse, só o feedback do dedo). */
export const ripple = (t: number, at: number | undefined) => {
  if (at === undefined || t < at || t > at + 0.5) return "none";
  const p = (t - at) / 0.5;
  return `0 0 0 ${p * 22}px rgba(49,44,40,${0.28 * (1 - p)})`;
};

/** Flutuação ociosa pra nada ficar 100% parado. */
export const idleFloat = (t: number, seed = 0) => ({
  y: Math.sin(t * 1.9 + seed) * 7,
  rot: Math.sin(t * 1.3 + seed * 2) * 0.7,
});
