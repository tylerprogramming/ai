import torch
import cv2
from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler
from diffusers.utils import export_to_video

# pipe = DiffusionPipeline.from_pretrained("damo-vilab/text-to-video-ms-1.7b", torch_dtype=torch.float16, variant="fp16")
# pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
# pipe.enable_model_cpu_offload()

# prompt = "Spiderman is surfing"
# video_frames = pipe(prompt, num_inference_steps=25).frames
# video_path = export_to_video(video_frames)

pipe = DiffusionPipeline.from_pretrained("ali-vilab/text-to-video-ms-1.7b", torch_dtype=torch.float16)
pipe.enable_model_cpu_offload()

# memory optimization
pipe.unet.enable_forward_chunking(chunk_size=1, dim=1)
pipe.enable_vae_slicing()

# prompt = "spiderman surfing a wave"
# video_frames = pipe(prompt, num_frames=24).frames[0]

prompt = "a cat surfing a wave"
video_frames = pipe(prompt, num_frames=100).frames[0]

video_path = export_to_video(video_frames, fps=30, output_video_path="vid1.mp4")


# UPSCALE THIS AS WELL