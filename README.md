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
**Configurações → Capacidades → Skills**. Use no **Claude Code** (aba Code do app desktop): as skills precisam rodar
programas no seu computador (ver Requisitos).

## Requisitos
As duas skills precisam do **Claude Code** (terminal ou aba Code do app desktop), porque rodam programas no seu
computador. **Você não precisa instalar nada antes:** na primeira vez, o Claude confere o que já existe e instala
o que faltar pra você, explicando cada coisa e pedindo seu OK antes de baixar. Se o computador pedir senha de
administrador, é você quem digita.

- **Carrosséis:** Python, Pillow e um navegador Chrome, Edge ou Chromium (leve; o Edge já vem no Windows).
- **Reels:** além disso Node, ffmpeg, uv, Remotion e WhisperX. São ~3–4 GB na primeira vez (inclui o modelo de
  transcrição) e ~6 GB livres em disco.

## Ferramentas usadas
Essas skills se apoiam em ferramentas de terceiros, cada uma com a sua licença:

| ferramenta | pra que serve aqui | licença |
|---|---|---|
| [Remotion](https://www.remotion.dev) | monta e renderiza o vídeo em código (cards animados, legendas) | **source-available, com regras próprias** (ver abaixo) |
| [WhisperX](https://github.com/m-bain/whisperX) | transcreve a fala com o tempo de cada palavra (base das legendas) | BSD-2-Clause |
| [FFmpeg](https://ffmpeg.org) | corta, converte e extrai o áudio dos vídeos | LGPL/GPL |
| [Node.js](https://nodejs.org) | roda o Remotion | MIT |
| [Python](https://www.python.org) + [uv](https://docs.astral.sh/uv/) | scripts de marca, áudio e slides; instala o WhisperX isolado | PSF / MIT-Apache |
| [Pillow](https://python-pillow.org) | otimiza imagens do editor de revisão dos carrosséis | MIT-CMU |
| Chrome / Edge / Chromium | transforma os slides HTML em PNG | — |
| [Google Fonts](https://fonts.google.com) | fontes da sua marca, quando você não tem as suas | licenças abertas (OFL/Apache) |

### ⚠️ Licença do Remotion (importante pra uso comercial)
O Remotion é gratuito pra **pessoas físicas** (inclusive uso comercial), **empresas com até 3 pessoas** e
**organizações sem fins lucrativos**. **Empresas com 4 pessoas ou mais precisam de uma licença paga do Remotion**
(a skill de reels escreve código Remotion pra você). Agência que entrega só o MP4 pro cliente conta só a própria
equipe. Confira as regras atuais em [remotion.dev/license](https://www.remotion.dev/license) antes de usar numa empresa.
A licença das skills lariz.co (abaixo) não inclui nem substitui a licença do Remotion.

---
Skill criada por **Lariz · lariz.co**. Uso pessoal — não redistribua nem revenda (ver [LICENSE.md](LICENSE.md)).
