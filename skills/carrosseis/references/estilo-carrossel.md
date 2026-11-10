# Estilo dos carrosséis (a essência lariz.co, adaptada à marca de cada pessoa)

**Olhe `marca/referencias/` e `marca/board.png` antes de desenhar.** Se a estética dela for diferente da colagem
(ex.: editorial clean), mantenha os princípios (gancho, 1 ideia, hierarquia, peças de interface, palavra forte) e
adapte a decoração: menos objetos, mais respiro, mas sempre com UMA peça visual que conta a ideia.

## Princípios
- **Colagem com intenção**: fundo + 2–4 peças por slide (print/foto, elemento da marca, peça de interface, emoji),
  levemente inclinadas (−6° a +6°), **sobrepostas** (flor na quina do card, selo no canto, fita sobre a foto).
  Nada de peças soltas com espaço igual ao redor.
- **Interface de celular como cenário**: notificação na capa, Notas pra "lista que nunca funciona", chat pra pergunta
  de seguidor, busca com o título digitado, Lembretes no CTA. São os elementos mais elogiados — crie novos quando o
  tema pedir.
- **Prints/fotos grandes, inclinados e cortados pela borda** (sensação de "continua", puxa o swipe). Recorte
  componentes em vez de tela inteira. Recrie em HTML quando for grande (fica mais nítido que print).
- **Cada elemento tem relação com o texto do slide.** Enfeite sem motivo sai.
- **Sem sombra** (chapado; borda fina se precisar separar do fundo). Sem glassmorphism, gradiente em texto, borda
  lateral colorida.

## Tipografia
- Texto em peso normal com **UMA palavra forte** (`.light` + `.kw`, ou `.selx`/`.mark`/`.hl` na palavra-herói).
- **Display** só nos títulos grandes (capa e no máximo 1 título de destaque no miolo). **Manuscrita** só em
  comentário curto, muitas vezes com seta apontando. Não misture display e texto na mesma linha.
- Título de capa 110–150px (quebra em 2–3 linhas; reserve altura ≈ 3 × tamanho). Título de miolo 60–80px. Corpo ≥ 36px.
  Precisou de texto pequeno pra caber? Tem coisa demais: divida.

## Composição (1080×1350)
- Margem de segurança ~70px; texto nunca encosta na borda.
- **Assimetria**: título fora do centro, peças nos cantos, diagonais. Respiro de ~35–45%.
- **Fundos SEMPRE revezam** (regra padrão; só não vale se ela pedir explicitamente fundo contínuo/igual em todos):
  - use **pelo menos 3 fundos diferentes** no carrossel e **nunca o mesmo em dois slides vizinhos**;
  - nenhum fundo aparece em mais da metade dos slides;
  - misture tipos: um com textura (`.bg-grid`, `.bg-dots`, `.bg-lined`), um de cor suave (`.bg-soft1/2/3`,
    `.bg-sky`, `.bg-glow`, `.bg-split`) e um claro/limpo (`.bg-paper`) ou foto; varie a intensidade (um mais clarinho
    pra momento calmo, um mais vivo pro momento "uau");
  - fundo escuro (`.bg-ink`) ou `.bg-accent` dá contraste ótimo, mas no máx. 1 slide (gancho, virada ou CTA);
  - em fundo de cor sólida, ponha uma camada de textura por cima (`.fx-grid`, `.fx-dots`, `.fx-stars`, um elemento
    de fundo da marca) em vez de deixar vazio. Opacidade de textura é ajuste da camada, nunca do slide inteiro.
  - Na proposta (tabela slide a slide) a coluna **fundo** já mostra o revezamento; confira antes de mandar.
  - Fundo contínuo (pedido dela): um fundo grande que atravessa os slides (ex.: faixa/ilustração que continua no
    próximo, `background-position` deslocado 1080px por slide) — também é um bom recurso quando ela pedir.
- **Variedade**: cada slide com layout e 1–2 elementos diferentes dos vizinhos; o mesmo elemento decorativo no máx.
  2× por carrossel. Mão-cursor só quando "clica" em algo.

## Capas (sempre diferentes — consulte `carrosseis/_historico.md`)
Ideias: notificação inclinada + título; texto "selecionado" com menu copiar/recortar; barra de busca com o título
digitado; pasta com coisas saindo; carta/envelope abrindo; post-it/polaroid num mural; balão de chat com a pergunta;
título gigante com palavra em marca-texto + 2–3 objetos grandes; print gigante cortado + título por cima; foto dela
(slide transparente) com título enorme. **Logo pequeno ou ausente na capa.** Sem ideia? Gere 3 variantes só do título
(palavra gigante / texto selecionado / empilhado) e deixe ela escolher.

## Receitas do base.css
Fundos `.bg-*` (paper, grid, lined, dots, soft1-3, sky(.vivid), glow, split(.v), ink, accent) + texturas `.fx-grid` `.fx-dots` `.fx-stars` · destaque `.hl` `.mark(.alt)` `.selx` · `.ticket` (etiqueta serrilhada) · `.bubble(.dark/.left)` ·
`.star` · `.postit` · `.polaroid` · `.tagchip` · `.sticker-outline` · `.swipe` · `.emo` (emoji grande) ·
interface: `.notif` `.notes` `.rem` `.chat.them/.me` `.imsg-input` `.search` `.emojibar` `.browser` `.goal` ·
`.print` (print/foto arredondado) · `.el` (elemento SVG/PNG de `img/elementos/`).
Elementos da marca no slide: `<img class="el" src="img/elementos/seta-curva.svg" style="left:..;top:..;width:..;transform:rotate(..)">`.
Nunca use `url(img/...)` em `style=""` inline (o editor quebra): crie uma classe no `<style>` do slide.
