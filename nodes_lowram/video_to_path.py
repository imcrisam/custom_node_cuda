import torch
import os
import numpy as np
import folder_paths
import cv2
from .vhs_compat import path_widget, strip_path


SUPPORTED_FORMATS = ["mp4", "avi", "webm", "mov"]

FOURCC_MAP = {
    "mp4":  cv2.VideoWriter_fourcc(*"mp4v"),
    "avi":  cv2.VideoWriter_fourcc(*"XVID"),
    "webm": cv2.VideoWriter_fourcc(*"VP80"),
    "mov":  cv2.VideoWriter_fourcc(*"mp4v"),
}


class SaveVideoToPath:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),  # (frames, H, W, C) float32 [0,1]
                "path": ("STRING", {**path_widget(SUPPORTED_FORMATS), "default": "output/my_video.mp4"}),
                "format": (SUPPORTED_FORMATS, {"default": "mp4"}),
                "fps": ("FLOAT", {"default": 24.0, "min": 1.0, "max": 120.0, "step": 0.1}),
                "overwrite": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("saved_path",)
    FUNCTION = "save"
    CATEGORY = "video/path"
    OUTPUT_NODE = True

    def save(self, images, path, format, fps, overwrite):
        try:
            base, _ = os.path.splitext(strip_path(path))
            full_path = os.path.join(folder_paths.base_path, f"{base}.{format}")
            os.makedirs(os.path.dirname(full_path), exist_ok=True)

            if not overwrite and os.path.exists(full_path):
                from datetime import datetime
                ts = datetime.now().strftime("%m%d%H%M%S")
                full_path = os.path.join(folder_paths.base_path, f"{base}_{ts}.{format}")

            frames_np = (images.numpy() * 255).clip(0, 255).astype(np.uint8)
            _, H, W, _ = frames_np.shape

            fourcc = FOURCC_MAP[format]
            writer = cv2.VideoWriter(full_path, fourcc, fps, (W, H))
            if not writer.isOpened():
                raise RuntimeError(f"VideoWriter could not open: {full_path}")

            for frame in frames_np:
                writer.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

            writer.release()
            print(f"[SaveVideoToPath] saved {len(frames_np)} frames to {full_path}")
            return (full_path,)
        except Exception as e:
            error_msg = f"ERROR: {str(e)}"
            print(f"[SaveVideoToPath] {error_msg}")
            return (error_msg,)


class LoadVideoFromPath:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "path": ("STRING", {**path_widget(SUPPORTED_FORMATS), "default": "output/my_video.mp4"}),
                "max_frames": ("INT", {"default": 0, "min": 0, "max": 10000, "step": 1,
                                       "tooltip": "0 = cargar todos los frames"}),
            }
        }

    RETURN_TYPES = ("IMAGE", "FLOAT", "INT", "STRING")
    RETURN_NAMES = ("images", "fps", "frame_count", "loaded_path")
    FUNCTION = "load"
    CATEGORY = "video/path"

    def load(self, path, max_frames):
        try:
            full_path = os.path.join(folder_paths.base_path, strip_path(path))
            cap = cv2.VideoCapture(full_path)
            if not cap.isOpened():
                raise RuntimeError(f"No se pudo abrir el video: {full_path}")

            fps = cap.get(cv2.CAP_PROP_FPS)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            limit = total_frames if max_frames == 0 else min(max_frames, total_frames)

            frames = []
            for _ in range(limit):
                ret, frame = cap.read()
                if not ret:
                    break
                frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            cap.release()

            if not frames:
                raise RuntimeError("El video no contiene frames legibles")

            frames_np = np.stack(frames).astype(np.float32) / 255.0
            images = torch.from_numpy(frames_np)  # (frames, H, W, C)

            print(f"[LoadVideoFromPath] loaded {len(frames)} frames @ {fps}fps from {full_path}")
            return (images, fps, len(frames), full_path)
        except Exception as e:
            error_msg = f"ERROR: {str(e)}"
            print(f"[LoadVideoFromPath] {error_msg}")
            raise ValueError(error_msg)