# Elementos da marca (criar uma vez, reutilizar sempre)

Se a pessoa não tem elementos prontos, crie um kit inicial em **código** (SVG ou HTML/CSS) com as cores da marca e
guarde em `<projeto>/marca/elementos/`. Os mesmos arquivos servem pros carrosséis (`<img class="el" src="img/elementos/x.svg">`)
e pros vídeos (`Sticker` com `src: "marca/elementos/x.svg"`, depois de `marca.py ts`).

## Kit inicial (8–12 peças, escolha pelas respostas da entrevista)
Escolha pela estética aprovada; não faça tudo. Sugestões:
- **setas à mão** (curva, em loop, reta com ponta torta) — apontar pra algo
- **rabisco/sublinhado** e **círculo à mão** — destacar palavra
- **estrela de 4 pontas** / brilhinho — acabamento
- **selo/carimbo** redondo com texto em volta (ex.: "aprovado", "novo", o @)
- **etiqueta** (tag com furinho), **fita adesiva** (washi tape), **post-it**
- **balão de fala** vazio, **coração**, **flor/forma orgânica**, **moldura polaroid**
- **ícone de pasta**, **cursor de mão**, **janelinha de app** (estética "interface")
- **fundo**: papel quadriculado/pautado, pontinhos, grade rabiscada (como SVG em `pattern` ou PNG 1080×1350 transparente)

## Regras pra desenhar em SVG
- `viewBox` quadrado ou proporcional à peça, sem `width/height` fixos (escala livre). Fundo transparente.
- Cores **literais da marca** (hex do tokens.json) — o SVG fica autossuficiente. Gere uma variação clara/escura quando
  fizer sentido (`seta-curva-ink.svg`, `seta-curva-branca.svg`).
- Traço "à mão": `stroke-linecap="round"`, `stroke-linejoin="round"`, path com leve irregularidade (curvas Q/C
  imperfeitas), espessura proporcional (≈ 2–4% do viewBox). Nada de sombra nem gradiente pesado.
- Texto dentro de SVG só se for parte do desenho (carimbo); converta pra path se usar fonte que pode não existir no render.
- Nome em kebab-case descritivo: `seta-curva.svg`, `estrela-4-pontas.svg`, `selo-redondo-arroba.svg`.

## Índice obrigatório
Cada peça nova ganha uma linha em `marca/elementos/README.md`: `arquivo` — o que é — quando usar (ex.: "apontar
pra palavra-chave; no máx. 1 por slide"). Antes de criar algo, **leia o índice e reaproveite**. Ao terminar um
carrossel/vídeo, se criou peça nova que ficou boa, salve-a aqui (não deixe só dentro do projeto do post).

## Aprovação
Depois de criar o kit, rode `marca.py board <projeto>` (a prancha mostra os elementos) e mande o `board.png`.
⏸ **Aprovação 2: elementos.** Corrija o que ela pedir antes de usar em conteúdo.

## Elementos HTML/CSS (já prontos no base.css do carrossel)
Interface de celular como cenário costuma ser o ponto mais elogiado: notificação (`.notif`), Notas (`.notes`),
Lembretes (`.rem`), chat (`.chat`), campo de mensagem (`.imsg-input`), busca (`.search`), navegador (`.browser`),
barra de emojis (`.emojibar`), card de meta com barra (`.goal`). Crie mais no mesmo espírito quando o tema pedir
(convite de calendário, tela de bloqueio, widget, Wallet, câmera/polaroid) e adicione a classe nova no `base.css`
do carrossel + uma linha no índice de elementos.
