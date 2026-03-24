"""
ComfyUI Custom Node Package: latent_to_cuda
Author: imcrisam
"""

from .nodes import latent_to_cuda

NODE_CLASS_MAPPINGS = {
    "latent_to_cuda": latent_to_cuda,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "latent_to_cuda": "Latent to CUDA",
}

print("🔥 custom_node_cuda IMPORTED")

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
