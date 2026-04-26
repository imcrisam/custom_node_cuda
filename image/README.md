# ComfyUI KDP Tools

Pack de **6 nodos personalizados** que replican el pipeline del script XnConvert `ImgToKdp` directamente en ComfyUI.

## Correspondencia con el script original

| # | XnConvert | Nodo ComfyUI |
|---|-----------|--------------|
| 1 | `<Emboss/>` | **KDP ① Emboss** |
| 2 | `<Replace_color src="#7e7e80" dst="#ffffff" tolerance="30"/>` | **KDP ② Replace Color** |
| 3 | `<Enhance_detail/>` | **KDP ③ Enhance Detail** |
| 4 | `<Change_color_depth method="0" dither="5"/>` | **KDP ④ Change Color Depth** |
| 5 | `<Set_DPI x="600"/> + <Canvas_resize width3="8.5" height3="11"/>` | **KDP ⑤ Canvas Resize** |
| 6 | `<Output format="PDF" quality="99"/>` | **KDP ⑥ Save as PDF** |

---

## Instalación

### Opción A — Manual
1. Copia la carpeta `comfyui-kdp-tools/` dentro de:
   ```
   ComfyUI/custom_nodes/
   ```
2. Reinicia ComfyUI.
3. Los nodos aparecen en la categoría **KDP Tools**.

### Opción B — ComfyUI Manager
1. Abre el Manager → *Install via Git URL*
2. Pega la URL del repositorio (si lo subes a GitHub).

---

## Importar el workflow

1. En ComfyUI ve a **Load** → selecciona `workflow_kdp.json`
2. El pipeline completo se carga listo para usar.
3. Solo conecta tu imagen en el nodo **LoadImage**.

---

## Notas sobre DPI

ComfyUI trabaja en píxeles, no en DPI. La equivalencia usada es:

| Tamaño (pulgadas) | DPI | Píxeles |
|---|---|---|
| 8.5 × 11 | 600 | 5100 × 6600 |
| 6 × 9 | 300 | 1800 × 2700 |
| 5.5 × 8.5 | 300 | 1650 × 2550 |

El nodo **KDP ⑤ Canvas Resize** incluye estos presets. El DPI real se escribe en los metadatos del PDF por el nodo **KDP ⑥ Save as PDF**.

---

## Requisitos

- ComfyUI (cualquier versión reciente)
- Python ≥ 3.8
- Pillow (`pip install Pillow`) — normalmente ya incluido en ComfyUI
