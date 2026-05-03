import torch
import os
import scipy.io.wavfile as wavfile
import numpy as np
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

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("saved_path",)
    FUNCTION = "save"
    CATEGORY = "audio/path"
    OUTPUT_NODE = True

    def save(self, audio, path):
        try:
            full_path = os.path.join(folder_paths.base_path, strip_path(path))
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            waveform = audio["waveform"][0]  # (channels, samples)
            sample_rate = audio["sample_rate"]
            audio_np = waveform.numpy().T.astype(np.float32)  # (samples, channels)
            wavfile.write(full_path, sample_rate, audio_np)
            print(f"[SaveAudioToPath] saved to {full_path}")
            return (full_path,)
        except Exception as e:
            error_msg = f"ERROR: {str(e)}"
            print(f"[SaveAudioToPath] {error_msg}")
            return (error_msg,)


class LoadAudioFromPath:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "path": ("STRING", {**path_widget(["wav"]), "default": "output/my_audio.wav"}),
            }
        }

    RETURN_TYPES = ("AUDIO", "STRING")
    RETURN_NAMES = ("audio", "loaded_path")
    FUNCTION = "load"
    CATEGORY = "audio/path"

    def load(self, path):
        try:
            full_path = os.path.join(folder_paths.base_path, strip_path(path))
            sample_rate, audio_np = wavfile.read(full_path)
            audio_np = audio_np.astype(np.float32)

            if audio_np.ndim == 1:
                audio_np = audio_np[:, np.newaxis]  # mono: (S,) → (S, 1)

            waveform = torch.from_numpy(audio_np.T)  # (channels, samples)
            audio = {"waveform": waveform.unsqueeze(0), "sample_rate": sample_rate}
            print(f"[LoadAudioFromPath] loaded from {full_path}")
            return (audio, full_path)
        except Exception as e:
            error_msg = f"ERROR: {str(e)}"
            print(f"[LoadAudioFromPath] {error_msg}")
            raise ValueError(error_msg)