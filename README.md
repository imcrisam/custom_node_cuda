# ComfyUI Latent to CUDA

A simple ComfyUI custom node that allows you to move latents between CPU and CUDA devices.

## Author

imcrisam

## Installation

1. Navigate to your ComfyUI `custom_nodes` directory
2. Clone or copy this repository:
   ```bash
   git clone https://github.com/imcrisam/comfyui-latent-to-cuda.git
   ```
3. Restart ComfyUI

## Usage

This node provides a simple interface to move latent tensors between CPU and CUDA:

- **latent**: Input latent tensor (LATENT type)
- **to_cuda**: Boolean toggle (default: True)
  - When True: Moves latent to CUDA
  - When False: Moves latent to CPU

The node outputs the modified latent tensor while preserving the original structure.

## Node Location

You can find this node in the `RES4LYF/latents` category in ComfyUI.

## Features

- Safe tensor movement without modifying the original latent
- Automatic device detection
- Compatible with standard ComfyUI latent workflows
- Simple boolean toggle for device selection

## Requirements

- ComfyUI
- PyTorch
- CUDA-compatible GPU (for CUDA operations)

## License

MIT License
