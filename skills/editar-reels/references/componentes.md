# Componentes e plano de edição (`R/remotion`)

## O plano
`public/videos/<slug>/edit-plan.json`: `{slug, title, format: "vertical"|"horizontal", trim:{start,end}, media:{video,audio}, events:[...]}`.
Cada evento: `{id, type, start, end, props, layout?, why?}`. Tempos em **segundos do vídeo final** (base do
`transcript.json`), inclusive dentro das props. **Não escreva o plano à mão**: copie
`public/videos/_exemplo/build.py` pra pasta do vídeo, troque as cenas e rode — ele gera legendas e palavras-chave com
`pipeline/captions.py` e grava o JSON inteiro (idempotente). Depois registre o slug em `VIDEOS` no `src/Root.tsx`.

Cores e fontes vêm de `src/brand.ts` (gerado por `marca.py ts` a partir de `marca/tokens.json`). Não chumbe hex nos
componentes: use `COLORS.ink/paper/accent/accent2/soft[n]/muted/border/success` e `DISPLAY_FONT/UI_FONT/ACCENT_FONT` de `src/ui.tsx`.

## Prontos
| type | props | quando usar |
|---|---|---|
| `HookTitle` | `lines:[{text,at}]`, `size?` | gancho: título gigante, cada linha pula na palavra. Combine com um card do lado (`layout:{x≈800,y≈560,scale}`) |
| `NameTag` | `lines:["eu sou","a Ana"]`, `x?`,`y?`,`size?`, `arrow?:{start,ctrl,tip}` | apresentação com seta desenhada até a cabeça. Ajuste posições num still por vídeo |
| `Caption` | `text` | legenda (gerada pelo `captions.build`, não à mão) |
| `Keyword` | `text` | palavra sozinha, gigante, fonte display, ≥ 1,1 s (gerada pelo `captions.build` via `KEYWORDS`) |
| `ListCard` | `title`, `items:[{text,at,doneAt?,strikeAt?,emoji?}]`, `stamp?:{text,at}`, `numbered?`, `bg?` | passos, dicas, erros (riscados), checklist (checks) |
| `ChatBubbles` | `header?`, `messages:[{from:"me"|"them",text,at}]` | pergunta de seguidor, objeção e resposta, depoimento |
| `Notification` | `items:[{title,text,at,emoji?,app?,time?}]`, `shakeAt?` | caos/sobrecarga, lembrete, "alguém te mandou…" |
| `BigNumber` | `label`, `steps:[{at,v}]`, `prefix?`,`suffix?`,`max?`,`caption?`,`decimals?` | dado, resultado, antes/depois |
| `Sticker` | `src?` (ex.: `marca/elementos/seta.svg`) ou `emoji?`, `x`,`y`,`size?`,`rot?` | reforço solto na palavra (px do quadro) |
| `Recap` | `title`, `items:[{text,at}]`, `teaser?:{text,at}`, `bg?` | fecho "nesse vídeo:" |
| `CTA` | `tapAt`,`doneAt`,`bioAt`, `confettiAt?`, `title?`,`subtitle?`,`button?`,`buttonDone?`,`loading?`,`bioText?` | chamada final (logo + botão tocado + "link na bio" pulando); textos padrão em `BRAND.cta` |
| `CoverTitle` | `lines`, `y`, `size`, `highlight?`, `rot?` | só na capa (`cover.json`) |

Ordem de empilhamento = ordem em `LAYERS` (`src/Video.tsx`); `Caption`/`Keyword` por último (por cima de tudo).

## Vertical
Cards são desenhados na coluna direita do 1920×1080 e remapeados pro vertical com `layout:{x,y,scale}` por evento
(centro em px do 1080×1920). Escolha o maior tamanho que caiba no espaço livre sem cobrir o rosto (meça com
`sheet.py`). Componentes "livres" (`HookTitle`, `NameTag`, `Caption`, `Keyword`, `Sticker`, `CoverTitle`) se
posicionam sozinhos. Constantes em `src/vertical.ts` (`safeTop`, `safeBottom`, `cardY`, `captionBottom`).

## Criando um componente novo (o normal é criar 1–3 por vídeo, específicos do tema)
Quando o que ela fala pede uma tela própria (o app/produto dela, um antes/depois, um calendário, um carrinho de
compras, uma planilha virando algo bonito…):
1. Arquivo em `src/components/<Nome>.tsx`, exporte `<Nome>Props` e `<Nome> = ({ev}) => ...`.
2. Embrulhe em `Panel` (`bare` se o filho desenha o próprio fundo; `clip={false}` se tiver carimbo saindo da borda).
3. Tudo que muda é função do tempo: `const t = useClipTime()` + `springAt(t, at, fps)`, `keyframed(t, fps, [{at,v}])`
   (valores que rolam com overshoot), `tapScale`/`ripple` (toque sem mouse), `pulse`, `typed` + `Caret` (digitação),
   `Check`, `Confetti`, `idleFloat`.
4. **Mostre a interação**, não o estado final: algo sendo tocado, digitado, preenchido, concluído, trocando de tela.
5. Se for tela de um produto/app real dela, recrie a partir de prints que ela mandar (nunca invente uma tela diferente).
6. Registre em `LAYERS`, rode `npx tsc --noEmit -p .` e confira um still (`npx remotion still <slug> out/x.png --frame=N`).
7. Se ficou bom e é reaproveitável, anote em `R/historico.md` (pra usar nos próximos vídeos).
