"""
ComfyUI Custom Node: latent_to_cuda
Author: imcrisam
Category: toCuda/latents
"""

import torch


class latent_to_cuda:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "latent": ("LATENT",),
                "to_cuda": ("BOOLEAN", {"default": True}),
            },
        }

    RETURN_TYPES = ("LATENT",)
    RETURN_NAMES = ("passthrough",)
    FUNCTION = "main"
    CATEGORY = "toCuda/latents"

    def main(self, latent, to_cuda):
        device = "cuda" if to_cuda else "cpu"

        # Clonar para no modificar el original
        latent = latent.copy()

        # Mover el tensor
        if "samples" in latent:
            latent["samples"] = latent["samples"].to(device)

        return (latent,)


NODE_CLASS_MAPPINGS = {
    "latent_to_cuda": latent_to_cuda,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "latent_to_cuda": "Latent to CUDA",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
