import torch
import os
import folder_paths
 
 
class SaveLatentToPath:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "latent": ("LATENT",),
                "path": ("STRING", {"default": "output/my_latent.pt"}),
            }
        }
 
    RETURN_TYPES = ()
    FUNCTION = "save"
    CATEGORY = "latent/path"
    OUTPUT_NODE = True
 
    def save(self, latent, path):
        full_path = os.path.join(folder_paths.base_path, path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        torch.save(latent["samples"], full_path)
        print(f"[SaveLatentToPath] saved to {full_path}")
        return ()
 
 
class LoadLatentFromPath:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "path": ("STRING", {"default": "output/my_latent.pt"}),
            }
        }
 
    RETURN_TYPES = ("LATENT",)
    FUNCTION = "load"
    CATEGORY = "latent/path"
 
    def load(self, path):
        full_path = os.path.join(folder_paths.base_path, path)
        samples = torch.load(full_path, map_location="cpu")
        print(f"[LoadLatentFromPath] loaded from {full_path}")
        return ({"samples": samples},)
 
