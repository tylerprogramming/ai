# Text to Video (diffusers)

Generates a short video from a text prompt ("a cat surfing a wave") with the open ModelScope text-to-video model `ali-vilab/text-to-video-ms-1.7b` via Hugging Face diffusers, and saves it as `vid1.mp4`. Despite the folder name, this example doesn't use AutoGen.

## Run it

Needs an NVIDIA GPU. Install PyTorch for your CUDA version from https://pytorch.org, then:

```bash
pip install -r requirements.txt
python main.py
```

The first run downloads the model (several GB) from Hugging Face.

> **Note:** Updated for diffusers 0.41. `TextToVideoSDPipeline` is now a deprecated pipeline in diffusers (it still works but gets no more fixes), and `pipe.enable_vae_slicing()` became `pipe.vae.enable_slicing()`.
