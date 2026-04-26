"""
ComfyUI Custom Node Package: latent_to_cuda
Author: imcrisam
"""

from .nodes_lowram.image_to_path import LoadImageFromPath, SaveImageToPath

from .image.nodes import CanvasResize, ChangeColorDepth, Emboss, EnhanceDetail, ReplaceColor, SaveAsPDF

from .nodes_lowram.conditional_to_path import LoadCondFromPath, SaveCondToPath
from .nodes_lowram.latent_to_path import LoadLatentFromPath, SaveLatentToPath
from .nodes_lowram.audio_to_path import SaveAudioToPath, LoadAudioFromPath
from .nodes_lowram.to_cuda import latent_to_cuda


NODE_CLASS_MAPPINGS = {
    "latent_to_cuda": latent_to_cuda,
    "SaveLatentToPath": SaveLatentToPath,
    "LoadLatentFromPath": LoadLatentFromPath,
    "SaveCondToPath": SaveCondToPath,
    "LoadCondFromPath": LoadCondFromPath,
    "SaveAudioToPath": SaveAudioToPath,
    "LoadAudioFromPath": LoadAudioFromPath,
    "Emboss":           Emboss,
    "ReplaceColor":     ReplaceColor,
    "EnhanceDetail":    EnhanceDetail,
    "ChangeColorDepth": ChangeColorDepth,
    "CanvasResize":     CanvasResize,
    "SaveAsPDF":        SaveAsPDF,
    "SaveImageToPath": SaveImageToPath,
    "LoadImageFromPath": LoadImageFromPath,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "latent_to_cuda": "Latent to CUDA",
    "SaveLatentToPath": "Save Latent to Path",
    "LoadLatentFromPath": "Load Latent from Path",
    "SaveCondToPath": "Save Conditioning to Path",
    "LoadCondFromPath": "Load Conditioning from Path",
    "SaveAudioToPath": "Save Audio to Path",
    "LoadAudioFromPath": "Load Audio from Path",
    "Emboss":           "Emboss",
    "ReplaceColor":     "Replace Color",
    "EnhanceDetail":    "Enhance Detail",
    "ChangeColorDepth": "Change Color Depth",
    "CanvasResize":     "Canvas Resize",
    "SaveAsPDF":        "Save as PDF",
    "SaveImageToPath": "Save Image to Path",
    "LoadImageFromPath": "Load Image from Path",
}

print("🔥 custom_node_cuda IMPORTED")

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]

