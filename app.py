import os
import time
import base64
import io

import gradio as gr
import requests
from PIL import Image

RUNPOD_ENDPOINT_ID = os.environ.get("RUNPOD_ENDPOINT_ID")
RUNPOD_API_KEY = os.environ.get("RUNPOD_API_KEY")

RUN_URL = f"https://api.runpod.ai/v2/{RUNPOD_ENDPOINT_ID}/run"
STATUS_URL = f"https://api.runpod.ai/v2/{RUNPOD_ENDPOINT_ID}/status"

HEADERS = {
    "Authorization": f"Bearer {RUNPOD_API_KEY}",
    "Content-Type": "application/json",
}


def generate(prompt, history):
    payload = {"input": {"prompt": prompt}}
    response = requests.post(RUN_URL, headers=HEADERS, json=payload, timeout=30)
    response.raise_for_status()
    job_id = response.json()["id"]

    elapsed = 0
    for _ in range(60):
        status_response = requests.get(f"{STATUS_URL}/{job_id}", headers=HEADERS, timeout=30)
        status_response.raise_for_status()
        data = status_response.json()
        status = data.get("status")

        if status == "COMPLETED":
            output = data.get("output", {})
            if "error" in output:
                return f"⚠️ Error: {output['error']}"
            image_b64 = output.get("image_base64")
            if not image_b64:
                return "⚠️ No image in the response."
            image = Image.open(io.BytesIO(base64.b64decode(image_b64)))
            temp_path = f"generated_{int(time.time())}.png"
            image.save(temp_path)
            return gr.Image(temp_path)

        if status == "FAILED":
            return f"⚠️ Job failed: {data}"

        time.sleep(5)
        elapsed += 5

    return "⏱️ Timed out waiting for the result."


THEME = gr.themes.Soft(
    primary_hue="violet",
    secondary_hue="indigo",
)

CUSTOM_CSS = """
#component-0 { max-width: 900px; margin: auto; }
.gradio-container { font-family: 'Inter', sans-serif; }
"""

with gr.Blocks(theme=THEME, css=CUSTOM_CSS, title="FLUX.1-dev Image Generator") as demo:
    gr.Markdown(
        """
        # 🎨 FLUX.1-dev Image Generator
        Type a prompt, hit enter, and watch the image get generated live —
        powered by **FLUX.1-dev** running on a **RunPod Serverless GPU endpoint**.

        *Generation typically takes 1–4 minutes depending on GPU availability.*
        """
    )

    chat = gr.ChatInterface(
        fn=generate,
        examples=[
            "a cozy cabin in the mountains at sunset, cinematic lighting",
            "a robot painting a landscape, oil painting style",
            "a neon-lit cyberpunk street market at night, rain reflections",
        ],
        fill_height=True,
    )

    gr.Markdown(
        "<center><sub>Built for the RunPod Technical Support Analyst case study</sub></center>"
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)