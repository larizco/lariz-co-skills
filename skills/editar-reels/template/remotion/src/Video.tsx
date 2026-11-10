import type { ComponentType } from "react";
import { AbsoluteFill, Audio, OffthreadVideo, useVideoConfig } from "remotion";
import { VERTICAL } from "./vertical";
import { BigNumber } from "./components/BigNumber";
import { Caption } from "./components/Caption";
import { ChatBubbles } from "./components/ChatBubbles";
import { CoverTitle } from "./components/CoverTitle";
import { CTA } from "./components/CTA";
import { HookTitle } from "./components/HookTitle";
import { Keyword } from "./components/Keyword";
import { ListCard } from "./components/ListCard";
import { NameTag } from "./components/NameTag";
import { Notification } from "./components/Notification";
import { Recap } from "./components/Recap";
import { Sticker } from "./components/Sticker";
import { videoFile, VideoProvider, useClipTime } from "./time";
import type { EventType, PlanEvent, VideoData } from "./types";

export type EditProps = {
  slug: string;
  /** trecho em segundos do vídeo final (0 = trim.start); null = vídeo inteiro */
  range: [number, number] | null;
  showGuides: boolean;
  planFile?: string;
  data?: VideoData;
};

// ordem de empilhamento: primeiro = mais embaixo. Componente novo? registre aqui.
const LAYERS: Partial<Record<EventType, ComponentType<{ ev: PlanEvent<any> }>>> = {
  ListCard,
  ChatBubbles,
  BigNumber,
  Notification,
  Recap,
  CTA,
  Sticker,
  HookTitle,
  CoverTitle,
  NameTag,
  Caption,
  Keyword,
};
const ORDER = Object.keys(LAYERS) as EventType[];

export const Edit = ({ range, showGuides, data }: EditProps) => {
  const { fps } = useVideoConfig();
  if (!data) return null;
  const { plan } = data;
  const startSec = plan.trim.start + (range?.[0] ?? 0);
  const trimBefore = Math.round(startSec * fps);

  return (
    <VideoProvider value={{ ...data, slug: plan.slug, startSec }}>
      <AbsoluteFill style={{ background: "#000", overflow: "hidden" }}>
        <OffthreadVideo src={videoFile(plan.slug, plan.media.video)} muted trimBefore={trimBefore} />
        <Overlays events={plan.events} />
        {showGuides ? <SafeZoneGuides /> : null}
      </AbsoluteFill>
      <Audio src={videoFile(plan.slug, plan.media.audio)} trimBefore={trimBefore} />
    </VideoProvider>
  );
};

// componentes que se posicionam sozinhos (não passam pelo remapeamento de card no vertical)
const FREE_LAYOUT = new Set(["HookTitle", "CoverTitle", "NameTag", "Caption", "Keyword", "Sticker"]);

const Overlays = ({ events }: { events: PlanEvent[] }) => {
  const t = useClipTime();
  const { width, height } = useVideoConfig();
  const vertical = height > width;
  const visible = events
    .filter((ev) => LAYERS[ev.type] && t >= ev.start && t < ev.end)
    .sort((a, b) => ORDER.indexOf(a.type) - ORDER.indexOf(b.type));
  return (
    <>
      {visible.map((ev) => {
        const C = LAYERS[ev.type]!;
        if (vertical && !FREE_LAYOUT.has(ev.type)) {
          // os cards são desenhados na coluna direita do 1920x1080 (centro ~1590,540);
          // no vertical eles vão pro espaço livre (layout.x/y/scale por evento)
          const s = ev.layout?.scale ?? VERTICAL.cardScale;
          const x = ev.layout?.x ?? 540;
          const y = ev.layout?.y ?? VERTICAL.cardY;
          return (
            <div key={ev.id} style={{ position: "absolute", left: 0, top: 0, width: 1920, height: 1080, transformOrigin: "1590px 540px", transform: `translate(${x - 1590}px, ${y - 540}px) scale(${s})` }}>
              <C ev={ev} />
            </div>
          );
        }
        return <C key={ev.id} ev={ev} />;
      })}
    </>
  );
};

// guias das zonas que a interface do Reels/TikTok/YouTube cobre (só nos trechos de validação)
const SafeZoneGuides = () => {
  const zone = { position: "absolute" as const, background: "rgba(255,0,80,0.22)", border: "2px dashed rgba(255,0,80,0.8)" };
  const { width, height } = useVideoConfig();
  if (height > width)
    return (
      <AbsoluteFill style={{ pointerEvents: "none" }}>
        <div style={{ ...zone, top: 0, left: 0, right: 0, height: VERTICAL.safeTop }} />
        <div style={{ ...zone, top: VERTICAL.safeBottom, left: 0, right: 0, bottom: 0 }} />
      </AbsoluteFill>
    );
  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      <div style={{ ...zone, top: 0, left: 0, right: 0, height: 120 }} />
      <div style={{ ...zone, bottom: 0, left: 0, right: 0, height: 120 }} />
    </AbsoluteFill>
  );
};
