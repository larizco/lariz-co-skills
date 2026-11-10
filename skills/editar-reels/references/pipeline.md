# Pipeline Python (`R/pipeline`) e armadilhas

| script | faz |
|---|---|
| `prepare.py <slug> --video <mp4> [--grade] [--end s]` | modo simples (áudio do próprio vídeo): `video.mp4` sem áudio + `audio.wav` |
| `resync.py <slug> --video <cortado.mp4> --raw-audio <mic.m4a> [--grade]` | casa cada trecho do vídeo cortado com a gravação longa do microfone → `resync.json` + `video.mp4` |
| `cuts.py <cortado.mp4> --resync <resync.json>` | detecta os cortes pela imagem → lista pro `--cuts` |
| `rebuild_audio.py <slug> --video <cortado.mp4> --raw-audio <mic> --cuts <lista> [--replace t:"arquivo"]` | monta o `audio.wav` final corte a corte |
| `diag_sync.py <cortado.mp4> <audio.wav>` | mede atraso áudio×câmera em janelas de 1 s (tem que dar ±5 ms) |
| `transcribe.py <slug> --lang pt --prompt "..."` | WhisperX → `transcript.json` (palavra a palavra) |
| `captions.py` | `build(words, start, end, keywords)` → eventos `Caption`/`Keyword` |
| `sheet.py <mp4> <png> --times ...` | prancha de frames pra revisar (leia a imagem) |
| `finalize.py <render.mp4> <saída.mp4>` | converte pro padrão Instagram/YouTube (obrigatório no final) |

## Microfone gravado à parte (vídeo já cortado + gravação longa)
```bash
cd R/pipeline
PY resync.py <slug> --video "<cortado.mp4>" --raw-audio "<mic.m4a>"
PY cuts.py "<cortado.mp4>" --resync ../remotion/public/videos/<slug>/resync.json
PY rebuild_audio.py <slug> --video "<cortado.mp4>" --raw-audio "<mic.m4a>" --cuts <lista do cuts.py>
PY diag_sync.py "<cortado.mp4>" ../remotion/public/videos/<slug>/audio.wav
```
- O `<cortado.mp4>` é o vídeo COM o áudio da câmera (é ele que serve de referência). O `video.mp4` gerado sai sem áudio.
- O `audio.wav` do `resync.py` tem defeitos conhecidos (emendas até 1 s fora, atraso acumulando): **sempre sobrescreva
  com o `rebuild_audio.py`**.
- `cuts.py`: cortes com `?` são cluster (pessoa se mexendo muito) → use a fronteira do `resync.json` mais próxima.
  Cortes com `+` vieram do áudio e podem ser falsos: ouça trechos curtos (< 1 s).
- `diag_sync.py`: sequência fora de ±5 ms = corte faltando ou offset errado. Janela com `sim` < 0,8 em cima de um corte
  quase sempre é sílaba duplicada (começou a palavra, cortou, regravou): confira o `tail` desse corte no `rebuild.json`.
- Frase regravada depois: `--replace <início do clip>:"<arquivo>"`.

## Armadilhas
- **Corrigiu o áudio depois de cronometrar o plano?** Os tempos da fala mudam: rode `transcribe.py` de novo e ajuste
  os tempos das cenas no `build.py`.
- Whisper "estica" palavra numa pausa e a legenda parece travada: o `captions.py` já corta; não aumente `MAX_DUR`.
- Passe `--prompt` com nomes próprios e termos do tema (nome da marca, produto) pro Whisper escrever certo. Revise a
  transcrição e corrija palavras erradas no `transcript.json` antes de gerar legendas.
- Render de ~4 min leva ~20–30 min, `finalize.py` mais ~15: rode em background e não faça polling.
- **Não encadeie `render ... | tail && finalize`**: o `tail` esconde a falha e o `finalize` reempacota o mp4 ANTIGO.
  Apague o `out/<slug>-full.mp4` antes e rode sem pipe.
- Não use o Remotion Studio pra ela revisar (trava com cliques rápidos): render + `sheet.py`.
- Revise com `sheet.py` **antes** de mostrar. Procure: card cobrindo rosto/texto, card parado com espaço vazio, texto
  quebrando linha (use `whiteSpace: "nowrap"`), sticker cortado pela borda, card sumindo cedo depois do payoff.
- Windows: antivírus segura arquivos recém-escritos (o `common.py` já tenta de novo). ffmpeg instalado pelo winget e
  fora do PATH é achado sozinho.
