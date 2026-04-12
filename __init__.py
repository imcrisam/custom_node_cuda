"""
ComfyUI Custom Node Package: latent_to_cuda
Author: imcrisam
"""

from nodes_lowram.conditional_to_path import LoadCondFromPath, SaveCondToPath
from nodes_lowram.latent_to_path import LoadLatentFromPath, SaveLatentToPath

from .nodes_lowram.to_cuda import latent_to_cuda

NODE_CLASS_MAPPINGS = {
    "latent_to_cuda": latent_to_cuda,
        "SaveLatentToPath": SaveLatentToPath,
    "LoadLatentFromPath": LoadLatentFromPath,
    "SaveCondToPath": SaveCondToPath,
    "LoadCondFromPath": LoadCondFromPath,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "latent_to_cuda": "Latent to CUDA",
        "SaveLatentToPath": "Save Latent to Path",
    "LoadLatentFromPath": "Load Latent from Path",
    "SaveCondToPath": "Save Conditioning to Path",
    "LoadCondFromPath": "Load Conditioning from Path",
}

print("🔥 custom_node_cuda IMPORTED")

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
