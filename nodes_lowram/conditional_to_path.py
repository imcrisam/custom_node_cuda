import torch
import os
import folder_paths
 


class SaveCondToPath:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "conditioning": ("CONDITIONING",),
                "path": ("STRING", {"default": "output/my_cond.pt"}),
            }
        }
 
    RETURN_TYPES = ()
    FUNCTION = "save"
    CATEGORY = "conditioning/path"
    OUTPUT_NODE = True
 
    def save(self, conditioning, path):
        full_path = os.path.join(folder_paths.base_path, path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        torch.save(conditioning, full_path)
        print(f"[SaveCondToPath] saved to {full_path}")
        return ()
 
 
class LoadCondFromPath:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "path": ("STRING", {"default": "output/my_cond.pt"}),
            }
        }
 
    RETURN_TYPES = ("CONDITIONING",)
    FUNCTION = "load"
    CATEGORY = "conditioning/path"
 
    def load(self, path):
        full_path = os.path.join(folder_paths.base_path, path)
        conditioning = torch.load(full_path, map_location="cpu")
        print(f"[LoadCondFromPath] loaded from {full_path}")
        return (conditioning,)