"""
ComfyUI KDP Tools - Custom Nodes
Replica del pipeline XnConvert para preparación de imágenes KDP (Amazon)

Nodos incluidos:
  1. KDP Emboss
  2. KDP Replace Color
  3. KDP Enhance Detail
  4. KDP Change Color Depth
  5. KDP Canvas Resize (KDP Presets)
  6. KDP Save as PDF
"""

import torch
import numpy as np
from PIL import Image, ImageFilter, ImageOps
import os
import folder_paths


# ─────────────────────────────────────────────
#  Utilidades internas
# ─────────────────────────────────────────────

def tensor2pil(image: torch.Tensor) -> Image.Image:
    """Convierte tensor ComfyUI [B,H,W,C] float32 → PIL RGB."""
    arr = image.cpu().numpy().squeeze()          # H,W,C
    arr = np.clip(arr * 255.0, 0, 255).astype(np.uint8)
    return Image.fromarray(arr).convert("RGB")


def pil2tensor(image: Image.Image) -> torch.Tensor:
    """Convierte PIL → tensor ComfyUI [1,H,W,C] float32."""
    arr = np.array(image.convert("RGB")).astype(np.float32) / 255.0
    return torch.from_numpy(arr).unsqueeze(0)


def hex_to_rgb(hex_color: str) -> tuple:
    h = hex_color.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


# ─────────────────────────────────────────────
#  Nodo 1 – KDP Emboss
#  Equivalente a <Emboss/> en XnConvert
# ─────────────────────────────────────────────

class KDP_Emboss:
    CATEGORY = "KDP Tools"
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "apply"

    MODES = [
        "Coloring page (edge detect)",
        "Emboss clásico",
        "Emboss + invertir",
    ]

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "mode": (cls.MODES,),
                "strength": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.1,
                    "max": 3.0,
                    "step": 0.1,
                    "display": "slider"
                }),
            }
        }

    def apply(self, image, mode, strength):
        pil = tensor2pil(image)

        if mode == "Coloring page (edge detect)":
            # Escala de grises → detección de bordes → invertir → líneas negras sobre blanco
            gray = pil.convert("L")
            edges = gray.filter(ImageFilter.FIND_EDGES)
            if strength != 1.0:
                edges = edges.filter(
                    ImageFilter.UnsharpMask(radius=1, percent=int(200 * strength), threshold=1)
                )
            result = ImageOps.invert(edges).convert("RGB")

        elif mode == "Emboss + invertir":
            embossed = pil.filter(ImageFilter.EMBOSS)
            if strength != 1.0:
                embossed = Image.blend(pil, embossed, alpha=min(strength, 1.0))
            result = ImageOps.invert(embossed)

        else:  # Emboss clásico
            embossed = pil.filter(ImageFilter.EMBOSS)
            if strength != 1.0:
                embossed = Image.blend(pil, embossed, alpha=min(strength, 1.0))
            result = embossed

        return (pil2tensor(result),)


# ─────────────────────────────────────────────
#  Nodo 2 – KDP Replace Color
#  Equivalente a <Replace_color src="#7e7e80" dst="#ffffff" tolerance="30"/>
# ─────────────────────────────────────────────

class KDP_ReplaceColor:
    CATEGORY = "KDP Tools"
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "apply"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "src_color": ("STRING", {"default": "#7e7e80"}),
                "dst_color": ("STRING", {"default": "#ffffff"}),
                "tolerance": ("INT", {
                    "default": 30,
                    "min": 0,
                    "max": 255,
                    "step": 1,
                    "display": "slider"
                }),
            }
        }

    def apply(self, image, src_color, dst_color, tolerance):
        pil = tensor2pil(image)
        arr = np.array(pil, dtype=np.float32)           # H,W,3

        src = np.array(hex_to_rgb(src_color), dtype=np.float32)
        dst = np.array(hex_to_rgb(dst_color), dtype=np.float32)

        # Máscara: píxeles cuya distancia max-channel ≤ tolerance
        diff = np.abs(arr - src)
        mask = np.all(diff <= tolerance, axis=2)         # H,W bool

        arr[mask] = dst
        result = Image.fromarray(arr.astype(np.uint8))
        return (pil2tensor(result),)


# ─────────────────────────────────────────────
#  Nodo 3 – KDP Enhance Detail
#  Equivalente a <Enhance_detail/>
# ─────────────────────────────────────────────

class KDP_EnhanceDetail:
    CATEGORY = "KDP Tools"
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "apply"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "radius": ("FLOAT", {
                    "default": 2.0,
                    "min": 0.5,
                    "max": 8.0,
                    "step": 0.5,
                    "display": "slider"
                }),
                "percent": ("INT", {
                    "default": 150,
                    "min": 50,
                    "max": 500,
                    "step": 10,
                    "display": "slider"
                }),
                "threshold": ("INT", {
                    "default": 3,
                    "min": 0,
                    "max": 10,
                    "step": 1
                }),
            }
        }

    def apply(self, image, radius, percent, threshold):
        pil = tensor2pil(image)
        enhanced = pil.filter(
            ImageFilter.UnsharpMask(
                radius=radius,
                percent=percent,
                threshold=threshold
            )
        )
        return (pil2tensor(enhanced),)


# ─────────────────────────────────────────────
#  Nodo 4 – KDP Change Color Depth
#  Equivalente a <Change_color_depth method="0" dither="5" ncompo="-1"/>
# ─────────────────────────────────────────────

class KDP_ChangeColorDepth:
    CATEGORY = "KDP Tools"
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "apply"

    MODES = ["Grayscale", "Black & White (1-bit)", "RGB (sin cambio)"]
    DITHER_MODES = ["Ninguno", "Floyd-Steinberg"]

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "mode": (cls.MODES,),
                "dither": (cls.DITHER_MODES,),
            }
        }

    def apply(self, image, mode, dither):
        pil = tensor2pil(image)
        dither_val = (
            Image.Dither.FLOYDSTEINBERG
            if dither == "Floyd-Steinberg"
            else Image.Dither.NONE
        )

        if mode == "Grayscale":
            result = pil.convert("L").convert("RGB")

        elif mode == "Black & White (1-bit)":
            gray = pil.convert("L")
            bw = gray.convert("1", dither=dither_val)
            result = bw.convert("RGB")

        else:  # RGB sin cambio
            result = pil

        return (pil2tensor(result),)


# ─────────────────────────────────────────────
#  Nodo 5 – KDP Canvas Resize
#  Equivalente a <Canvas_resize width3="8.5" height3="11" unit="2"/>
#  + <Set_DPI x="600" y="600"/>
# ─────────────────────────────────────────────

class KDP_CanvasResize:
    CATEGORY = "KDP Tools"
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "apply"

    # Presets KDP comunes (ancho_px, alto_px) a 600 DPI
    PRESETS = {
        "8.5 x 11\"  @ 600 DPI  (Letter / US Trade)": (5100, 6600),
        "6 x 9\"     @ 300 DPI  (Novela estándar)":   (1800, 2700),
        "5.5 x 8.5\" @ 300 DPI  (Digest)":            (1650, 2550),
        "5 x 8\"     @ 300 DPI  (Pocket)":             (1500, 2400),
        "8 x 10\"    @ 300 DPI  (Cuadrado grande)":    (2400, 3000),
        "Personalizado":                                None,
    }

    POSITIONS = ["Centro", "Arriba-izquierda", "Arriba-derecha",
                 "Abajo-izquierda", "Abajo-derecha"]

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "preset": (list(cls.PRESETS.keys()),),
                "bg_color": ("STRING", {"default": "#ffffff"}),
                "position": (cls.POSITIONS,),
                "scale_to_fit": ("BOOLEAN", {"default": True}),
            },
            "optional": {
                "custom_width_px":  ("INT", {"default": 5100, "min": 100, "max": 14400}),
                "custom_height_px": ("INT", {"default": 6600, "min": 100, "max": 14400}),
            }
        }

    def apply(self, image, preset, bg_color, position,
              scale_to_fit, custom_width_px=5100, custom_height_px=6600):

        pil = tensor2pil(image)

        # Resolución destino
        if preset == "Personalizado":
            tw, th = custom_width_px, custom_height_px
        else:
            tw, th = self.PRESETS[preset]

        bg = Image.new("RGB", (tw, th), hex_to_rgb(bg_color))
        sw, sh = pil.size

        if scale_to_fit:
            scale = min(tw / sw, th / sh)
            sw = int(sw * scale)
            sh = int(sh * scale)
            pil = pil.resize((sw, sh), Image.LANCZOS)

        offsets = {
            "Centro":           ((tw - sw) // 2,   (th - sh) // 2),
            "Arriba-izquierda": (0,                 0),
            "Arriba-derecha":   (tw - sw,           0),
            "Abajo-izquierda":  (0,                 th - sh),
            "Abajo-derecha":    (tw - sw,           th - sh),
        }
        px, py = offsets[position]
        bg.paste(pil, (px, py))

        return (pil2tensor(bg),)


# ─────────────────────────────────────────────
#  Nodo 6 – KDP Save as PDF
#  Equivalente a <Output format="PDF"> con compress=0 y quality=99
# ─────────────────────────────────────────────

class KDP_SaveAsPDF:
    CATEGORY = "KDP Tools"
    RETURN_TYPES = ()
    OUTPUT_NODE = True
    FUNCTION = "apply"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "filename_prefix": ("STRING", {"default": "kdp_output"}),
                "dpi": ("INT", {
                    "default": 600,
                    "min": 72,
                    "max": 1200,
                    "step": 1
                }),
                "quality": ("INT", {
                    "default": 99,
                    "min": 1,
                    "max": 100,
                    "step": 1
                }),
                "overwrite": ("BOOLEAN", {"default": True}),
            }
        }

    def apply(self, image, filename_prefix, dpi, quality, overwrite):
        output_dir = folder_paths.get_output_directory()
        pil = tensor2pil(image)

        # Resolver nombre de archivo (sin colisión si overwrite=False)
        base_name = filename_prefix.strip() or "kdp_output"
        pdf_path = os.path.join(output_dir, f"{base_name}.pdf")

        if not overwrite:
            counter = 1
            while os.path.exists(pdf_path):
                pdf_path = os.path.join(output_dir, f"{base_name}_{counter:04d}.pdf")
                counter += 1

        pil.save(
            pdf_path,
            format="PDF",
            resolution=dpi,
            quality=quality,
            save_all=False,
        )

        print(f"[KDP Tools] PDF guardado en: {pdf_path}")
        return {}

