"""
ComfyUI Custom Node Package: latent_to_cuda
Author: imcrisam
"""

from image.kdp_nodes import KDP_CanvasResize, KDP_ChangeColorDepth, KDP_Emboss, KDP_EnhanceDetail, KDP_ReplaceColor, KDP_SaveAsPDF

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
    "KDP_Emboss":           KDP_Emboss,
    "KDP_ReplaceColor":     KDP_ReplaceColor,
    "KDP_EnhanceDetail":    KDP_EnhanceDetail,
    "KDP_ChangeColorDepth": KDP_ChangeColorDepth,
    "KDP_CanvasResize":     KDP_CanvasResize,
    "KDP_SaveAsPDF":        KDP_SaveAsPDF,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "latent_to_cuda": "Latent to CUDA",
    "SaveLatentToPath": "Save Latent to Path",
    "LoadLatentFromPath": "Load Latent from Path",
    "SaveCondToPath": "Save Conditioning to Path",
    "LoadCondFromPath": "Load Conditioning from Path",
    "SaveAudioToPath": "Save Audio to Path",
    "LoadAudioFromPath": "Load Audio from Path",
    "KDP_Emboss":           "KDP ① Emboss",
    "KDP_ReplaceColor":     "KDP ② Replace Color",
    "KDP_EnhanceDetail":    "KDP ③ Enhance Detail",
    "KDP_ChangeColorDepth": "KDP ④ Change Color Depth",
    "KDP_CanvasResize":     "KDP ⑤ Canvas Resize",
    "KDP_SaveAsPDF":        "KDP ⑥ Save as PDF",
}

print("🔥 custom_node_cuda IMPORTED")

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]

