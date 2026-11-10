# lariz.co · skills para Claude

Carrosséis criativos e reels dinâmicos **na sua marca**, com o Claude te guiando passo a passo e você aprovando
cada etapa. Não precisa saber programar.

| skill | faz |
|---|---|
| `/lariz-co:init` | **comece por aqui**: define sua identidade visual, escolhe/cria sua pasta de conteúdo, confere as ferramentas e te leva pro carrossel ou pro reels |
| `/lariz-co:carrosseis` | carrosséis curtos e criativos (5–7 slides, gancho forte), PNG em alta, editor visual de revisão |
| `/lariz-co:editar-reels` | vídeos falando pra câmera viram reels dinâmicos: legendas curtas, palavras-chave gigantes, gancho, cards animados |

## 1. Instalar (uma vez)
Abra o **Claude Code** (aba **Code** do app Claude no computador, ou `claude` no terminal) e cole esta mensagem:
```
Instala pra mim o plugin da lariz.co rodando no terminal:
claude plugin marketplace add larizco/lariz-co-skills
claude plugin install lariz-co@lariz-co
Depois me avisa se deu certo.
```
(Ou, no terminal, digite `/plugin marketplace add larizco/lariz-co-skills` e `/plugin install lariz-co@lariz-co`.)

## 2. Começar
Abra uma **conversa nova** e digite:
```
/lariz-co:init
```
O guia te pergunta da sua identidade visual (ou cria uma com você), onde guardar seu conteúdo, instala o que
faltar no computador e te leva pro que você quer fazer. Da próxima vez, abra o Claude na sua pasta de conteúdo e
peça com suas palavras: *"faz um carrossel sobre…"*, *"edita meu vídeo novo pra reels"*.

Versões novas: peça pro Claude *"atualiza o plugin da lariz.co"* (ele roda `claude plugin marketplace update lariz-co` e
`claude plugin update lariz-co@lariz-co`) e abra uma conversa nova.

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
| [gdown](https://github.com/wkentaro/gdown) | baixa vídeos de um link compartilhado do Google Drive | MIT |
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
