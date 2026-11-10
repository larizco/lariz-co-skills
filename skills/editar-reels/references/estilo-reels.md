# A fórmula dos reels lariz.co

Público de celular pula rápido. Cada segundo precisa de algo novo na tela, ligado ao que a pessoa está dizendo.

## Gancho (0 – ~7 s)
- **O melhor momento acontece no primeiro 1,5 s.** Título gigante (fonte display da marca, branco, 2–3 linhas
  empilhadas) + um card que já "vive" a frase de abertura (notificações caindo, lista sendo riscada, número rolando,
  a tela do produto dela sendo usada). Nunca imagem parada.
- Cada linha do título dá um pulo quando ela fala a palavra. O título pode cobrir o corpo, **nunca o rosto**.
- Sem legenda durante o gancho (o título já é o texto).
- Se ela se apresenta ("eu sou a Ana"), use `NameTag`: nome em manuscrita perto da cabeça + seta que se desenha.
  O nome nunca vira legenda comum.

## Ritmo
- **Movimento o tempo todo**: nada fica parado no mesmo estado. Tudo flutua de leve (`idleFloat`).
- **Mostre a interação**: botão sendo tocado (afunda e solta um anel, sem mouse), item caindo, check, risco, barra
  enchendo, contador rolando, texto sendo digitado, mensagem chegando com "digitando…".
- **Cada mudança cai na palavra exata** (use os tempos do `transcript.json`).
- **Troca de card junto com a fala**: quando um card termina de se montar, corte pro próximo que mostra o resultado.
  Bloco de fala longo = fases dentro do mesmo card, não um card parado.
- **Tempo pra ler**: payoff (resultado, lista completa) fica ≥ 3 s antes de trocar. Palavra-chave ≥ 1,1 s.

## Texto na tela
- **Legenda**: fonte de texto da marca, peso forte, branca com sombra, coluna estreita e centralizada, ≤ 4 palavras
  ou 1,6 s cada (o `captions.py` já faz). No vertical fica no peito.
- **Palavra-chave sozinha**: fonte display, grande, entra com soco. Nunca dentro da legenda. 1 a cada ~10–20 s, nas
  palavras que carregam a ideia (escolha na tabela do roteiro).

## Cards
- Grandes ("a tela é pequena"), mais altos que largos, entrada de soco/zoom com overshoot (nunca fade educado),
  moldura `Panel`. Horizontal: ao lado dela. Vertical: no espaço livre do quadro (em geral acima da cabeça).
- Carimbos/etiquetas manuscritas podem sair pra fora da borda do card, mas nunca cobrem texto.
- Elementos da marca (`marca/elementos/`) entram como `Sticker` pra reforçar momentos (seta pra palavra, estrela no
  resultado, coração no depoimento).
- Na dúvida, maior e mais centralizado.

## Fecho
Recap com checks ("nesse vídeo:") + CTA animado (botão tocado → carregando → pronto + confete → "link na bio" pulando,
ou o CTA que ela escolheu). Teaser de parte 2 opcional no recap.

## Vertical (1080×1920)
- Peça pra ela gravar deixando espaço livre acima da cabeça (os cards vão lá). Se o vídeo não tem esse espaço, combine
  outra área (lateral, metade de cima com ela menor) e anote no `R/historico.md`.
- A UI do Reels cobre ~250 px no topo e ~400 px embaixo: nada essencial ali (os trechos de validação mostram essas
  zonas em vermelho).

## Vídeos curtos a partir de um longo
Se ela cortar vários reels de um vídeo longo da mesma gravação, reaproveite as cenas do longo: copie os eventos e
some o deslocamento de tempo entre os dois cortes (compare onde a mesma frase cai no `transcript.json` de cada um).
O que é novo no curto (gancho, CTA) usa os mesmos componentes com tempos novos.
