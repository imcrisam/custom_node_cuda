import torch
import torchaudio
import os
import folder_paths

from .vhs_compat import path_widget, strip_path

class SaveAudioToPath:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "audio": ("AUDIO",),
                "path": ("STRING", {**path_widget(["wav"]), "default": "output/my_audio.wav"}),
            }
        }

    RETURN_TYPES = ()
    FUNCTION = "save"
    CATEGORY = "audio/path"
    OUTPUT_NODE = True

    def save(self, audio, path):
        full_path = os.path.join(folder_paths.base_path, strip_path(path))
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        waveform = audio["waveform"]
        sample_rate = audio["sample_rate"]
        torchaudio.save(full_path, waveform[0], sample_rate, format="wav", backend="soundfile")
        print(f"[SaveAudioToPath] saved to {full_path}")
        return ()


class LoadAudioFromPath:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "path": ("STRING", {**path_widget(["wav"]), "default": "output/my_audio.wav"}),
            }
        }

    RETURN_TYPES = ("AUDIO",)
    FUNCTION = "load"
    CATEGORY = "audio/path"

    def load(self, path):
        full_path = os.path.join(folder_paths.base_path, strip_path(path))
        waveform, sample_rate = torchaudio.load(full_path, backend="soundfile")
        audio = {"waveform": waveform.unsqueeze(0), "sample_rate": sample_rate}
        print(f"[LoadAudioFromPath] loaded from {full_path}")
        return (audio,)