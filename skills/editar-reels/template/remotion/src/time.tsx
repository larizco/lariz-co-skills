import { createContext, useContext } from "react";
import { interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import type { PlanEvent, VideoData } from "./types";

type VideoCtx = VideoData & { slug: string; startSec: number };

const Ctx = createContext<VideoCtx | null>(null);
export const VideoProvider = Ctx.Provider;

export const useVideo = (): VideoCtx => {
  const ctx = useContext(Ctx);
  if (!ctx) throw new Error("useVideo fora do VideoProvider");
  return ctx;
};

export const videoFile = (slug: string, file: string) => staticFile(`videos/${slug}/${file}`);

/** Tempo atual na base do vídeo (mesma do edit-plan.json / transcript.json). */
export const useClipTime = (): number => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return useVideo().startSec + frame / fps;
};

/** Tempo e helpers relativos a um evento do plano. */
export const useEventClock = (ev: Pick<PlanEvent, "start" | "end">) => {
  const t = useClipTime();
  const { fps } = useVideoConfig();
  const local = t - ev.start;
  const remaining = ev.end - t;
  return {
    t,
    local,
    remaining,
    fps,
    /** spring que começa `delay` segundos depois do início do evento */
    enter: (delay = 0, config: Parameters<typeof spring>[0]["config"] = { damping: 14, mass: 0.7 }) =>
      spring({ frame: (local - delay) * fps, fps, config }),
    /** 1 → 0 nos últimos `dur` segundos do evento */
    exit: (dur = 0.25) => interpolate(remaining, [0, dur], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
  };
};

export const clamp01 = (v: number) => Math.min(1, Math.max(0, v));
