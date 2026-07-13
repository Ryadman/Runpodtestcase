Gradio will print a local URL in the terminal (something like `http://127.0.0.1:7860`) - open that address in your browser, type a prompt, and the generated image will appear a little while later.

## A few decisions worth explaining

- The model is cached on a network volume rather than installed into the Docker image - keeps builds fast and avoids re-downloading ~24GB on every cold start.
- Ran into "no kernel image available" errors on newer GPUs with the original base image, so it's now running CUDA 12.8 / PyTorch 2.8, which covers a much wider range of GPU generations.
- Inference runs at 25 steps instead of the default 50 - a reasonable speed/quality trade-off for something meant to feel responsive in a live demo.
- The UI polls RunPod's `/run` + `/status` endpoints instead of `/runsync`, since generation takes longer than runsync's ~90 second window.

