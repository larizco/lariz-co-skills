import { Img, staticFile, useVideoConfig } from "remotion";
import { BRAND } from "../brand";
import { ripple, springAt, tapScale } from "../motion";
import { useClipTime } from "../time";
import type { PlanEvent } from "../types";
import { ACCENT_FONT, COLORS, DISPLAY_FONT, UI_FONT } from "../ui";
import { Confetti } from "./Confetti";
import { Panel, pulse } from "./Panel";

/**
 * Chamada final: card da marca (logo + nome + frase) → botão tocado → carregando → pronto + confete →
 * etiqueta "link na bio" (ou o texto do CTA) pulando. Textos padrão vêm de BRAND.cta.
 */
export type CTAProps = {
  tapAt: number;
  doneAt: number;
  bioAt: number;
  confettiAt?: number;
  title?: string;
  subtitle?: string;
  button?: string;
  buttonDone?: string;
  loading?: string;
  bioText?: string;
};

export const CTA = ({ ev }: { ev: PlanEvent<CTAProps> }) => {
  const t = useClipTime();
  const { fps } = useVideoConfig();
  const p = ev.props;
  const prog = Math.min(1, Math.max(0, (t - p.tapAt) / Math.max(0.01, p.doneAt - p.tapAt)));
  const ready = t >= p.doneAt;
  const bio = springAt(t, p.bioAt, fps, { damping: 7, mass: 0.5, stiffness: 220 });
  const bounce = t > p.bioAt + 0.5 ? Math.abs(Math.sin((t - p.bioAt) * 5)) * 16 : 0;
  const label = ready ? p.buttonDone ?? BRAND.cta.buttonDone : t >= p.tapAt ? `${p.loading ?? "carregando"}... ${Math.round(prog * 100)}%` : p.button ?? BRAND.cta.button;
  return (
    <Panel ev={ev} seed={12} pad="40px 36px">
      <div style={{ position: "relative" }}>
        <Confetti t={t - (p.confettiAt ?? p.doneAt)} n={24} />
        <div style={{ display: "flex", alignItems: "center", gap: 24 }}>
          {BRAND.logo ? (
            <Img
              src={staticFile(BRAND.logo)}
              style={{ width: 150, height: 150, objectFit: "contain", borderRadius: 38, flexShrink: 0, transform: `rotate(${Math.sin(t * 2) * 4}deg) scale(${1 + pulse(t, p.doneAt, 0.4) * 0.12})` }}
            />
          ) : null}
          <div>
            <div style={{ fontFamily: DISPLAY_FONT, fontSize: 66, color: COLORS.ink, lineHeight: 1 }}>{p.title ?? BRAND.name}</div>
            {p.subtitle ? <div style={{ fontFamily: UI_FONT, fontSize: 24, color: COLORS.muted, marginTop: 10 }}>{p.subtitle}</div> : null}
          </div>
        </div>
        <div
          style={{
            position: "relative",
            marginTop: 34,
            height: 88,
            borderRadius: 44,
            overflow: "hidden",
            background: ready ? COLORS.success : COLORS.ink,
            color: "#fff",
            fontFamily: UI_FONT,
            fontWeight: 800,
            fontSize: 32,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            transform: `scale(${tapScale(t, p.tapAt, fps) + pulse(t, p.doneAt) * 0.06})`,
            boxShadow: ripple(t, p.tapAt),
          }}
        >
          {t >= p.tapAt && !ready ? <div style={{ position: "absolute", left: 0, top: 0, bottom: 0, width: `${prog * 100}%`, background: "rgba(255,255,255,0.25)" }} /> : null}
          <span style={{ position: "relative" }}>{label}</span>
        </div>
      </div>
      {bio > 0 ? (
        <div style={{ marginTop: 30, textAlign: "center", transform: `translateY(${-bounce}px) scale(${bio}) rotate(${(1 - bio) * -20 - 3}deg)` }}>
          <span style={{ display: "inline-block", fontFamily: ACCENT_FONT, fontSize: 60, whiteSpace: "nowrap", color: COLORS.ink, background: COLORS.soft[0], borderRadius: 26, padding: "4px 30px 14px", border: "4px solid #fff" }}>
            {p.bioText ?? `🔗 ${BRAND.cta.text}`}
          </span>
        </div>
      ) : null}
    </Panel>
  );
};
