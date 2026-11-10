export type EventType = string;

export type PlanEvent<P = Record<string, unknown>> = {
  id: string;
  type: EventType;
  start: number;
  end: number;
  props: P;
  why?: string;
  /** só no vertical: escala e centro (px do quadro 1080x1920) do card */
  layout?: { scale?: number; x?: number; y?: number };
};

export type EditPlan = {
  slug: string;
  title: string;
  format: "horizontal" | "vertical";
  trim: { start: number; end: number };
  media: { video: string; audio: string };
  events: PlanEvent[];
};

export type TranscriptWord = { word: string; start: number; end: number; score: number };
export type TranscriptLine = { text: string; start: number; end: number };
export type Transcript = { lines: TranscriptLine[]; words: TranscriptWord[] };

export type VideoData = { plan: EditPlan; transcript: Transcript };
