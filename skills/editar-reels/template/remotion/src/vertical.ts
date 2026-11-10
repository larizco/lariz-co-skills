/**
 * Layout do formato vertical (1080x1920). Ajuste POR PESSOA no primeiro vídeo (meça num still com sheet.py):
 * os cards vão no espaço livre do quadro (em geral acima da cabeça) e a legenda no peito.
 */
export const VERTICAL = {
  safeTop: 250, // UI do Reels/TikTok em cima
  safeBottom: 1520, // UI do Reels/TikTok embaixo
  cardY: 560, // centro dos cards (entre o topo seguro e o topo da cabeça)
  cardScale: 0.8,
  captionBottom: 560, // distância da base até a legenda/palavra-chave
};
