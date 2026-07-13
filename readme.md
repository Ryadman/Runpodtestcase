# FLUX.1-dev on RunPod Serverless

**Stack:** RunPod Serverless · Diffusers (FLUX.1-dev) · Gradio · Docker

This project deploys FLUX.1-dev on a RunPod Serverless GPU endpoint and puts a chat-style Gradio UI in front of it, so you can type a prompt and watch the image get generated.

## What's in here
- `handler.py` - the RunPod worker. Loads FLUX.1-dev and turns prompts into images.
- `Dockerfile` - defines the container the worker runs in.
- `requirements.txt` - worker dependencies.
- `app.py` - the Gradio UI, talks to the deployed endpoint.
- `ui-requirements.txt` - dependencies for the UI.

## Getting the worker running
1. Push this repo to GitHub.
2. In the RunPod console: Serverless -> New Endpoint -> Deploy from a GitHub repository.
3. Point it at this repo, branch `main`.
4. Attach a network volume (so the model gets cached instead of re-downloaded every time) and set two environment variables:
   - `HF_TOKEN` - your Hugging Face token. FLUX.1-dev is gated, so you'll need to accept the license on the model page first.
   - `MODEL_CACHE_DIR` = `/runpod-volume/model-cache`
5. Pick a GPU with enough VRAM - 48GB worked well in testing.
6. Deploy, and give the first request a few minutes since it has to pull the model down.

## Running the UI on local machine
