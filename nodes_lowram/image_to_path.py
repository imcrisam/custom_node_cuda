from datetime import datetime

import torch
import os
import numpy as np
import folder_paths
from PIL import Image
from .vhs_compat import path_widget, strip_path


SUPPORTED_FORMATS = ["png", "jpg", "webp", "bmp", "tiff"]


class SaveImageToPath:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "path": ("STRING", {**path_widget(SUPPORTED_FORMATS), "default": "output/my_image.png"}),
                "format": (SUPPORTED_FORMATS, {"default": "png"}),
                "quality": ("INT", {"default": 95, "min": 1, "max": 100, "step": 1}),
                "overwrite": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ()
    FUNCTION = "save"
    CATEGORY = "image/path"
    OUTPUT_NODE = True

    def save(self, image, path, format, quality, overwrite):
        base, _ = os.path.splitext(strip_path(path))
        full_path = os.path.join(folder_paths.base_path, f"{base}.{format}")
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        if not overwrite:
            base_path = full_path[: -len(format) - 1]
            ts = datetime.now().strftime("%m%d%H%M%S")
            full_path = f"{base_path}_{ts}.{format}"

        frame = image[0]
        img_np = (frame.numpy() * 255).clip(0, 255).astype(np.uint8)
        pil_img = Image.fromarray(img_np)

        save_kwargs = {}
        if format == "jpg":
            pil_img = pil_img.convert("RGB")
            save_kwargs["quality"] = quality
        elif format == "webp":
            save_kwargs["quality"] = quality
        elif format == "png":
            save_kwargs["compress_level"] = max(0, min(9, 9 - round(quality / 11)))

        pil_img.save(full_path, format=format.upper(), **save_kwargs)
        print(f"[SaveImageToPath] saved to {full_path}")
        return ()


class LoadImageFromPath:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "path": ("STRING", {**path_widget(SUPPORTED_FORMATS), "default": "output/my_image.png"}),
            }
        }

    RETURN_TYPES = ("IMAGE", "MASK")
    FUNCTION = "load"
    CATEGORY = "image/path"

    def load(self, path):
        full_path = os.path.join(folder_paths.base_path, strip_path(path))
        pil_img = Image.open(full_path)

        # Imagen → tensor (1, H, W, C) float32 en [0, 1]
        img_np = np.array(pil_img.convert("RGBA")).astype(np.float32) / 255.0
        image = torch.from_numpy(img_np[:, :, :3]).unsqueeze(0)  # RGB
        mask = torch.from_numpy(img_np[:, :, 3]).unsqueeze(0)    # Alpha como máscara

        print(f"[LoadImageFromPath] loaded from {full_path}")
        return (image, mask)