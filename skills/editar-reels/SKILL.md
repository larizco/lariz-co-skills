---
name: editar-reels
description: Edita vídeos talking-head (pessoa falando pra câmera) em reels/vídeos dinâmicos com legendas curtas, palavras-chave gigantes, títulos de gancho e cards animados que ilustram a fala, na marca de quem estiver usando — importa ou monta a identidade visual, cria elementos reutilizáveis, copia o vídeo pro projeto e aprova em etapas. Usa Remotion + WhisperX. Use quando mandarem um vídeo pra editar, pedirem um reel/TikTok/Short/vídeo pro YouTube, legendas animadas, "deixa esse vídeo mais dinâmico" ou mencionarem Remotion — mesmo sem falar "skill". Skill criada por Lariz (lariz.co).
---

# Editar reels · lariz.co

> Skill criada por **Lariz · lariz.co**. Uso pessoal — não redistribua nem revenda (ver `LICENSE.md`).

Transforma um vídeo da pessoa falando num vídeo com camada criativa. A essência (não negociável, vale pra qualquer marca):
- **Movimento o tempo todo**: nenhum card parado; tudo entra com soco/zoom e overshoot, flutua de leve e reage
  **na palavra exata** que ela fala (item caindo, check, número rolando, texto digitando, toque com anel).
- **Gancho nos primeiros ~1,5 s**: título gigante em 2–3 linhas que pulam a cada palavra + um card que já "vive" a frase.
- **Legenda curta** (≤ 4 palavras / 1,6 s, coluna estreita) e **palavra-chave sozinha, gigante** (nunca misturada na legenda).
- **Cards grandes** que mostram o que ela diz, trocando junto com a fala; payoff fica ≥ 3 s na tela.
- **Fecho**: recap com checks + CTA animado.
O que muda é a marca: cores, fontes, elementos, tom e CTA são os DELA.

Caminhos: `SKILL` = pasta desta skill; `<projeto>` = pasta de trabalho dela; `R = <projeto>/reels`.
Use caminhos absolutos nos comandos. Python do pipeline: `R/pipeline/.venv/Scripts/python.exe` (Windows) ou
`R/pipeline/.venv/bin/python` (Mac/Linux) — abaixo chamado de `PY`.

## Regra de ouro: aprovar em etapas ⏸
Pare em cada ⏸, mostre (imagem, tabela ou mp4) e espere o OK. Feedback dela ("amei", "não gosto de X") vira linha em
`marca/marca.md` → "Aprendizados" e vale pros próximos vídeos.

## Fluxo

### Antes de tudo: conferir e instalar as ferramentas ⏸
**Se a pessoa ainda não tiver as ferramentas, você instala** (com o OK dela), antes de qualquer outro passo. Ela não
precisa saber programar nem abrir nada: você roda os comandos e explica cada um em português simples.
Esta skill precisa rodar comandos no computador dela (Claude Code no terminal ou na aba Code do app desktop). No chat
do claude.ai sem acesso ao computador ela não funciona: diga isso e sugira o Claude Code.

1. **Confira o que já existe** (rápido, sem instalar nada): `python --version` (ou `python3`), `node --version`,
   `ffmpeg -version`, `uv --version`. Mostre pra ela uma lista curta: ✅ já tem / ⬇️ falta.
2. **Instale só o que faltar**, dizendo o que é, pra que serve e quanto baixa, e peça OK uma vez pra lista toda:
   | falta | pra que serve | Windows | Mac (precisa do Homebrew: brew.sh) |
   |---|---|---|---|
   | Python 3.10+ | scripts de marca e de áudio | `winget install Python.Python.3.12` | `brew install python` |
   | Node 18+ | rodar o Remotion (monta o vídeo) | `winget install OpenJS.NodeJS.LTS` | `brew install node` |
   | ffmpeg | cortar, converter e extrair áudio | `winget install Gyan.FFmpeg` | `brew install ffmpeg` |
   | uv | instala o Python 3.11 e o WhisperX isolados | `winget install astral-sh.uv` | `brew install uv` |
   Se `winget`/`brew` pedir senha de administrador, peça pra ELA digitar (você nunca digita senha). Sem Homebrew no Mac,
   mostre o comando de instalação de brew.sh e peça pra ela rodar. Depois de instalar pelo winget, o terminal atual
   pode não enxergar o programa: abra uma sessão nova ou use o caminho completo. Confira de novo no fim (passo 1).
3. Os pacotes pesados do projeto (Remotion e WhisperX, ~2,5 GB) ficam pro passo 2, depois da marca aprovada.
4. **Licença do Remotion** (avise uma vez, em uma linha): é grátis pra pessoa física, empresa com até 3 pessoas e
   ONG; empresa com 4+ pessoas precisa da licença paga do Remotion (remotion.dev/license). Se ela disser que é
   empresa maior, mostre o link e siga só depois que ela confirmar que vai cuidar disso.

### 0. Projeto
Pergunte onde fica o projeto (ferramenta de escolher pasta se existir; senão caminho/arrastar a pasta). Se já existe
`<projeto>/marca/tokens.json`, leia `marca/marca.md` + `marca/elementos/README.md`, mostre `marca/board.png` e pergunte
se segue igual. Se já existe `R/`, leia `R/historico.md` (vídeos anteriores, medidas do layout vertical).

### 1. Marca ⏸ e elementos ⏸
Pergunte primeiro: **"você já tem identidade visual?"** Siga `references/marca-setup.md` (A = importar a pasta dela;
B = entrevista + 3 opções). Depois, se ela não tem elementos, crie o kit em SVG (`references/elementos.md`).
Script: `python SKILL/scripts/marca.py init|fonte|board <projeto>`. A pasta `marca/` é a mesma da skill de carrosséis.

### 2. Montar o projeto de vídeo (só na primeira vez) ⏸
`python SKILL/scripts/setup_reels.py <projeto>` copia o template pra `R/`, gera `src/brand.ts` e mostra o que falta
(`--check` só mostra). Se ainda faltar algum programa do sistema, volte em "Antes de tudo". Instale **só o que faltar**,
dizendo o que é e quanto baixa, com OK antes:
1. (programas do sistema: já conferidos em "Antes de tudo")
2. **Pacotes do projeto** (uma vez por projeto): `cd R/remotion && npm install` (~300 MB) e
   `cd R/pipeline && uv venv --python 3.11 .venv && uv pip install --python <PY> --extra-index-url https://download.pytorch.org/whl/cpu --index-strategy unsafe-best-match -r requirements.txt`
   (WhisperX + torch CPU, ~2 GB; o modelo do Whisper, ~1,5 GB, baixa sozinho na 1ª transcrição). Rode em background.
3. `setup_reels.py <projeto> --check` tem que dar tudo `ok`. Mudou a marca depois? `marca.py ts <projeto>` de novo.
Requisitos de máquina: ~6 GB livres em disco; render de um reel de 1 min leva ~5–10 min num notebook comum.

### 3. Receber o vídeo
Peça pra ela **selecionar o vídeo** (arrastar o arquivo pro chat ou colar o caminho). Pergunte junto (uma mensagem só):
- **formato**: vertical 1080×1920 (Reels/TikTok/Shorts) ou horizontal 1920×1080 (YouTube);
- o áudio é **do próprio vídeo** ou ela gravou num **microfone à parte** (aí peça esse arquivo também);
- o vídeo já está **cortado** (sem erros/pausas) ou é bruto (se bruto, sugira cortar no CapCut/editor antes — esta
  skill não faz o corte de erros);
- **tema** em uma frase, **objetivo** (alcance, salvar, vender, seguir), **CTA** (link na bio, comentar palavra…),
  se tem **produto/app/tela** pra mostrar (peça prints) e se quer a apresentação "eu sou a <nome>".
Crie um slug kebab-case sem acento e **copie** o vídeo pra `R/remotion/public/videos/<slug>/original.<ext>` (copiar, não
recortar: o original fica onde estava, a não ser que ela peça pra mover). Confira com `ffprobe` duração, resolução e fps.
Proporção diferente do formato? Pergunte como enquadrar antes de seguir. Marca d'água no fim? Corte com `--end`.

### 4. Áudio e transcrição
- **Áudio do próprio vídeo:** `cd R/pipeline && PY prepare.py <slug> --video <original> [--end s]`.
- **Microfone à parte:** fluxo de sincronia em `references/pipeline.md` (`resync.py` → `cuts.py` → `rebuild_audio.py` →
  `diag_sync.py`, lag ±5 ms).
- Correção de cor é opcional (`--grade`): mostre um frame antes/depois e pergunte.
- `PY transcribe.py <slug> --lang pt --prompt "<nome da marca, termos do tema>"` → `transcript.json` palavra a palavra.

### 5. Roteiro visual em tabela ⏸
Leia a transcrição inteira, divida em blocos de assunto e proponha uma **tabela com o tempo real**
(tempo · frase · o que aparece na tela · componente · por quê) + o **gancho** (título em 2–3 linhas e o card que vive a
frase) + **palavras-chave** + fecho (recap/CTA, teaser de parte 2?). Pergunte o que for decisão dela. Pare pra aprovar.

### 6. Trecho de validação ⏸
Monte o plano (`references/componentes.md`: `edit-plan.json` + script de cenas `build.py` com legendas automáticas).
Registre o vídeo e 1–2 trechos em `VIDEOS` no `R/remotion/src/Root.tsx` (`gancho` 0–~9 s + um trecho de 15–30 s).
**No vertical, este é o momento de medir o layout dela** (onde fica a cabeça, espaço livre): ajuste `src/vertical.ts`
e `layout` dos cards, e anote as medidas em `R/historico.md`. Diga isso a ela explicitamente.
```bash
cd R/remotion && npx tsc --noEmit -p . && npx remotion render <slug>-gancho out/<slug>-gancho.mp4 --log=error
```
Revise os frames você mesma (`PY R/pipeline/sheet.py <mp4> <png> --times ...` + ler a imagem) e mande o mp4.

### 7. Vídeo inteiro ⏸
Escreva todas as cenas, renderize, faça pranchas, corrija, e só então mostre. Render longo em background, sem polling,
sem `| tail` (esconde falha), apagando o mp4 antigo antes:
```bash
npx remotion render <slug> out/<slug>-full.mp4 --log=error
cd R/pipeline && PY finalize.py ../remotion/out/<slug>-full.mp4 ../prontos/<slug>.mp4
```
**Entrega sempre em `R/prontos/<slug>.mp4`** (o `finalize.py` é obrigatório: corrige cor/compatibilidade pro Instagram/YouTube).

### 8. Capa ⏸ (sempre junto com o vídeo)
Mesmo formato do vídeo, em `R/prontos/capas/capa-<slug>.jpg`. Plano à parte `public/videos/<slug>/cover.json` com o card
mais colorido no estado final + `CoverTitle` gigante (nunca no rosto) + frame dela sorrindo:
`npx remotion still <slug> out/capa.png --frame=<f> --props '{"slug":"<slug>","range":null,"showGuides":false,"planFile":"cover.json"}'`.
Vertical: tudo dentro do recorte 3:4 do grid (y 240–1680). Horizontal: 1280×720 JPG < 2 MB.
Registre o vídeo em `R/historico.md` (data, slug, componentes usados, medidas, feedback).

## Referências
- `references/estilo-reels.md` — a fórmula em detalhe (gancho, ritmo, legendas, cards, vertical).
- `references/componentes.md` — componentes prontos, props, como montar o plano e criar componente novo.
- `references/pipeline.md` — scripts Python, sincronia com microfone externo, armadilhas.
- `references/marca-setup.md`, `references/elementos.md` — marca e elementos (iguais aos da skill de carrosséis).

## Como falar com ela
Português informal e direto (ou o idioma dela). Planos em tabela com tempo real, uma linha de porquê por escolha, e
diga o que não foi verificado. Na dúvida de tamanho: maior e mais centralizado — vídeo de celular pede "mais", não "menos".
