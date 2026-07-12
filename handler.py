import base64
import io
import torch
from diffusers import FluxPipeline
import runpod

pipe = FluxPipeline.from_pretrained(
    "black-forest-labs/FLUX.1-dev",
    torch_dtype=torch.bfloat16,
)
pipe.to("cuda")


def handler(job):
    job_input = job["input"]
    prompt = job_input.get("prompt")

    image = pipe(prompt=prompt).images[0]

    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    image_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return {"image_base64": image_base64}


runpod.serverless.start({"handler": handler})
