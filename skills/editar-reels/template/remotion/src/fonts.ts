import { loadFont } from "@remotion/fonts";
import { staticFile } from "remotion";
import { BRAND } from "./brand";

// os arquivos ficam em public/marca/fontes/ (copiados pelo `marca.py ts`)
export const fontsReady = Promise.all(
  BRAND.fontFiles.map((f) => loadFont({ family: f.family, url: staticFile(`marca/fontes/${f.file}`), weight: f.weight })),
);
