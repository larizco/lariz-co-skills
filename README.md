# lariz.co · skills para Claude

Duas skills que usam a **mesma marca** (a pasta `marca/` do seu projeto):

| skill | faz |
|---|---|
| `lariz-co:carrosseis` | carrosséis curtos e criativos (5–7 slides, gancho forte), PNG 2160×2700, editor visual de revisão |
| `lariz-co:editar-reels` | vídeos talking-head dinâmicos: legendas curtas, palavras-chave gigantes, gancho, cards animados (Remotion) |

As duas seguem o mesmo caminho, sempre aprovando com você em etapas: **marca** (importa a sua ou monta com você) →
**elementos** reutilizáveis (SVG/CSS) → **conteúdo/vídeo** → **roteiro** → **design/edição** → **entrega**.

## Instalar no Claude Code
Dentro do Claude Code, rode:
```
/plugin marketplace add larizco/lariz-co-skills
/plugin install lariz-co@lariz-co
```
Reinicie a sessão e peça: *"faz um carrossel sobre…"* ou *"edita esse vídeo pra reels"*.
Para receber versões novas: `/plugin marketplace update lariz-co`.

## Instalar no app do Claude (claude.ai / desktop)
Baixe o `.zip` da skill na página de [Releases](https://github.com/larizco/lariz-co-skills/releases) e envie em
**Configurações → Capacidades → Skills** (o de carrosséis funciona no app; o de reels precisa do Claude Code, ver abaixo).

## Requisitos
- **Carrosséis:** Python 3.10+ com Pillow, e Chrome, Edge ou Chromium.
- **Reels:** precisa do **Claude Code** (terminal ou aba Code do app desktop), porque roda programas no seu computador.
  Na primeira vez o Claude confere o que falta (Node, ffmpeg, Python/uv, Remotion, WhisperX) e instala pra você,
  pedindo OK antes de cada download (~3–4 GB no total, só uma vez). Não funciona no chat do claude.ai.

---
Skill criada por **Lariz · lariz.co**. Uso pessoal — não redistribua nem revenda (ver [LICENSE.md](LICENSE.md)).
