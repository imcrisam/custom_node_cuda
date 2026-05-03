import torch
import os
import folder_paths
from .vhs_compat import path_widget, strip_path


class SaveLatentToPath:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "latent": ("LATENT",),
                "path": ("STRING", {**path_widget(["pt"]), "default": "output/my_latent.pt"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("saved_path",)
    FUNCTION = "save"
    CATEGORY = "latent/path"
    OUTPUT_NODE = True

    def save(self, latent, path):
        try:
            full_path = os.path.join(folder_paths.base_path, strip_path(path))
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            torch.save(latent["samples"], full_path)
            print(f"[SaveLatentToPath] saved to {full_path}")
            return (full_path,)
        except Exception as e:
            error_msg = f"ERROR: {str(e)}"
            print(f"[SaveLatentToPath] {error_msg}")
            return (error_msg,)


class LoadLatentFromPath:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "path": ("STRING", {**path_widget(["pt"]), "default": "output/my_latent.pt"}),
                "weights_only": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("LATENT", "STRING")
    RETURN_NAMES = ("latent", "loaded_path")
    FUNCTION = "load"
    CATEGORY = "latent/path"

    def load(self, path, weights_only):
        try:
            full_path = os.path.join(folder_paths.base_path, strip_path(path))
            samples = torch.load(full_path, map_location="cpu", weights_only=weights_only)
            print(f"[LoadLatentFromPath] loaded from {full_path}")
            return ({"samples": samples}, full_path)
        except Exception as e:
            error_msg = f"ERROR: {str(e)}"
            print(f"[LoadLatentFromPath] {error_msg}")
            raise ValueError(error_msg)