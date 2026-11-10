# Marca: achar a que existe ou criar uma (passo compartilhado reels + carrosséis)

A marca mora em `<projeto>/marca/` e serve pras DUAS skills (`lariz-co:editar-reels` e `lariz-co:carrosseis`).
Se a pessoa já fez esse passo numa delas, **não refaça**: mostre o resumo (`marca/board.png`) e pergunte se segue igual.

```
<projeto>/marca/
  marca.md          voz, público, palavras, regras de design (o "manual" — leia antes de criar)
  tokens.json       cores, fontes, logo, @, CTA (os scripts leem daqui)
  tokens.css        gerado (marca.py css)
  board.html/.png   prancha de aprovação (marca.py board)
  fontes/           .woff2/.otf/.ttf
  elementos/        SVG/PNG reutilizáveis + README.md (índice)
  referencias/      prints de posts que ela curte, posts antigos, inspirações
```

## A. Ela TEM identidade visual
1. Peça a pasta: "me mostra onde está sua identidade visual (logo, manual, fontes, cores, elementos)".
   Se houver uma ferramenta de escolher pasta (ex.: `request_directory` no app do Claude), use; senão peça pra
   **arrastar a pasta pro chat** ou colar o caminho. Pode ser também um link do Drive/Canva/Figma se houver conector.
2. Leia tudo o que tiver: manual em PDF, imagens de posts, logo, arquivos de fonte. Olhe as imagens de verdade.
3. Copie (não mova) pra `marca/`: logo → `marca/logo.png|svg`, fontes → `marca/fontes/`, elementos → `marca/elementos/`,
   posts/inspirações → `marca/referencias/`. Fonte comercial que ela não tem o arquivo? Peça o arquivo ou proponha a
   alternativa mais parecida do Google Fonts (e diga que é substituta).
4. Rode `python <skill>/scripts/marca.py init <projeto> --nome "<marca>"` e preencha `tokens.json` com o que achou
   (papéis das cores abaixo). Fontes do Google: `marca.py fonte <projeto> "Família" --papel display|body|script --pesos 400,700`.
   Fonte própria: ponha o arquivo em `marca/fontes/` e registre em `tokens.json` (`{"family","files":[{"file","weight"}],"fallback"}`).
5. Pergunte só o que o material NÃO responde (tom de voz, público, palavras proibidas, CTA, @).
6. Escreva `marca/marca.md`, rode `marca.py board <projeto>` e mande o `board.png`. ⏸ **Aprovação 1: marca.**

## B. Ela NÃO TEM identidade visual — entrevista curta (no máximo 2 rodadas de perguntas)
Pergunte em blocos, com opções prontas (use a ferramenta de perguntas com botões se existir). Nunca uma pergunta por mensagem.

**Rodada 1 — quem é**
- Nome da marca/perfil e @. O que vende/ensina, em uma frase.
- Pra quem fala (quem é a pessoa do outro lado, o que ela sente, o que ela quer).
- 3 palavras pra como a marca deve SOAR (ex.: acolhedora, divertida, direta, sofisticada, irreverente, didática).
- Palavras/expressões que ela usa muito e que ela odeia (ex.: odeia "coach", "hack", "você precisa").
- Perfis/marcas que ela acha bonitos (pode mandar prints → `marca/referencias/`).

**Rodada 2 — preferências visuais** (rápida)
- O que ela ama e o que ela odeia visualmente (cores, estilos, "nada de rosa", "nada muito sério"…).
- Emojis: muito / pouco / nunca. Minúsculas nos títulos? Usa gírias?
- CTA padrão (ex.: "link na bio", "comenta QUERO", "salva esse post") e o texto do botão.

### As 3 propostas: 3 CAMINHOS DIFERENTES, não 3 variações
O erro mais comum é entregar 3 opções quase iguais (mesma vibe, paletas vizinhas, fontes parecidas). Isso não serve:
ela precisa de **3 direções criativas que ela consiga distinguir de longe**, todas ainda fiéis às referências e ao
público dela. Antes de mostrar, monte esta tabela pra você mesma e refaça se alguma linha repetir:

| eixo | proposta A | proposta B | proposta C |
|---|---|---|---|
| conceito (nome curto + metáfora) | ex.: "caderno de ateliê" | ex.: "revista de domingo" | ex.: "pôster de feira" |
| família estética | ex.: colagem/scrapbook | ex.: editorial/serifado | ex.: gráfico bold / retrô / minimal escuro |
| temperatura da paleta | quente e clara | neutra com 1 acento forte | saturada ou escura |
| categoria da fonte display | serifada suave | serifada de revista / condensada | grotesca pesada / display expressiva |
| fundo dominante | papel claro | off-white limpo | cor chapada forte |
| elemento assinatura | ex.: fita adesiva + rabisco | ex.: fio fino + numeração | ex.: forma geométrica + adesivo |

Regras:
- **Cada eixo diferente entre as 3.** Se duas usam serifada, ou duas têm paleta clara-quente, troque uma.
- **Âncora nas referências:** cada proposta pega UMA coisa diferente das referências dela (uma pega a cor, outra o
  tipo de letra, outra o clima/composição) e diz qual. Uma das 3 pode ser a mais "segura"; pelo menos uma deve ser
  ousada (algo que ela não pensaria sozinha, mas que ainda faz sentido pro público).
- **Mostre aplicado, não só amostras:** pra cada proposta, renderize uma **mini capa de carrossel** (1080×1350, com o
  nome da marca e um gancho de exemplo) + as cores + as fontes. Uma imagem com as 3 lado a lado, cada uma com o nome
  do conceito em cima e uma frase de "por que combina com você".
- Dica de pares de fonte bem distintos (Google Fonts): Fraunces + DM Sans + Caveat (aconchego), Playfair Display / DM
  Serif Display + Lato (editorial), Archivo Black / Anton + Inter (bold), Instrument Serif + Geist (clean chique),
  Gloock + Outfit (retrô), Bricolage Grotesque + Manrope (moderno), Syne + Space Grotesk (experimental), Abril
  Fatface + Work Sans (revista), Shrikhand + Nunito (divertido). Fuja dos mesmos 2–3 pares sempre.
- Ela pode **misturar** ("a cor da A com a fonte da C"): faça a mistura e mostre de novo.

Depois da escolha: `marca.py init` → `fonte` (×3) → preencher `tokens.json` → `marca.md` → `board`. ⏸ **Aprovação 1: marca.**

## Papéis das cores (tokens.json → colors)
| papel | uso |
|---|---|
| `ink` | texto principal e fundo de contraste (escuro) |
| `paper` | fundo claro / cards |
| `accent` | cor de destaque: palavra-chave, botão, marca-texto, balão "eu" |
| `accent2` | segunda cor de destaque: estrelinhas, post-it, carimbo |
| `soft` | 2–4 cores suaves pra fundos e cards (alternar) |
| `muted` / `border` / `success` | texto secundário / bordas finas / "feito" (check) |
Contraste: `ink` sobre `paper`/`soft` precisa ser bem legível; texto branco só sobre `ink` ou `accent` escuro o bastante.

## O que vai no marca.md (curto, 1 tela)
Quem é · pra quem fala · tom de voz (3 palavras + 3 exemplos de frases no jeito dela + 3 do que NÃO falar) ·
palavras proibidas · uso de emoji/minúsculas · estética (o que define o estilo, 4–6 bullets) · regras de fonte
(display só em título grande; manuscrita só em comentário curto) · CTA padrão · elementos disponíveis (link pro índice).
Cada feedback que ela der depois ("amei", "não gosto de X") vira uma linha em **"Aprendizados"** no fim do marca.md,
com data. Esses aprendizados valem mais que qualquer regra genérica das skills.
