import { Composition, Folder, staticFile, type CalculateMetadataFunction } from "remotion";
import "./fonts";
import { Edit, type EditProps } from "./Video";
import type { EditPlan, Transcript, VideoData } from "./types";

const FPS = 30;

/**
 * Uma entrada por vídeo em public/videos/<slug>. `trechos` = janelas de validação (segundos do vídeo final),
 * renderizadas com as guias de zona segura. Ex.:
 *   { slug: "meu-primeiro-reel", trechos: [{ id: "gancho", range: [0, 9] }, { id: "meio", range: [20, 40] }] },
 */
const VIDEOS: { slug: string; trechos: { id: string; range: [number, number] }[] }[] = [];

const loadJson = async <T,>(slug: string, file: string): Promise<T> => {
  const res = await fetch(staticFile(`videos/${slug}/${file}`));
  if (!res.ok) throw new Error(`Não achei videos/${slug}/${file}`);
  return res.json() as Promise<T>;
};

const calculateMetadata: CalculateMetadataFunction<EditProps> = async ({ props }) => {
  const plan = await loadJson<EditPlan>(props.slug, props.planFile ?? "edit-plan.json");
  const transcript = await loadJson<Transcript>(props.slug, "transcript.json");
  const data: VideoData = { plan, transcript };
  const seconds = props.range ? props.range[1] - props.range[0] : plan.trim.end - plan.trim.start;
  const dims = plan.format === "vertical" ? { width: 1080, height: 1920 } : { width: 1920, height: 1080 };
  return { durationInFrames: Math.max(1, Math.round(seconds * FPS)), props: { ...props, data }, ...dims };
};

export const Root = () => (
  <>
    {VIDEOS.map(({ slug, trechos }) => (
      <Folder key={slug} name={slug}>
        <Composition
          id={slug}
          component={Edit}
          width={1080}
          height={1920}
          fps={FPS}
          durationInFrames={FPS}
          calculateMetadata={calculateMetadata}
          defaultProps={{ slug, range: null, showGuides: false } satisfies EditProps}
        />
        {trechos.map(({ id, range }) => (
          <Composition
            key={id}
            id={`${slug}-${id}`}
            component={Edit}
            width={1080}
            height={1920}
            fps={FPS}
            durationInFrames={FPS}
            calculateMetadata={calculateMetadata}
            defaultProps={{ slug, range, showGuides: true } satisfies EditProps}
          />
        ))}
      </Folder>
    ))}
  </>
);
