Deploys FLUX.1-dev as a RunPod Serverless endpoint, with a Gradio chat-style UI in front of it.

## Files
- `handler.py` - RunPod serverless worker, loads FLUX.1-dev and generates images
- `Dockerfile` - container definition
- `requirements.txt` - worker dependencies
- `app.py` - Gradio chat UI, calls the deployed endpoint
- `ui-requirements.txt` - UI dependencies

## Deploy the worker
1. Push this repo to GitHub.
2. RunPod console -> Serverless -> New Endpoint -> Deploy from a GitHub repository.
3. Select this repo, branch `main`.
4. Attach a network volume (for model caching) and set environment variables:
   - `HF_TOKEN` - your Hugging Face access token (FLUX.1-dev is gated, accept the license first)
   - `MODEL_CACHE_DIR` = `/runpod-volume/model-cache`
5. Choose a GPU with enough VRAM (48GB recommended).
6. Deploy.

## Run the UI locally
