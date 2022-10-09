# sd-multi - run multiple forks of Stable Diffusion

## Purpose

I've noticed that some forks of Stable Diffusion, while very active, often break. This repo adds a little bit of stability and predictability, while at the same time allowing the freedom to (relatively easily) play around with different forks and their features.

## Usage

For a detailed description of how to get this working in Windows using WSL2 and native Docker (not Docker Desktop), see [my blog post](https://trycatch.dev/2022/10/01/stable-diffusion-on-wsl2-with-docker/).

### Prerequisites

- A modern Nvidia GPU
- Windows 10/11 with [WSL2](https://learn.microsoft.com/en-us/windows/wsl/install) or native Linux
- [Docker CE](https://docs.docker.com/engine/install/) installed
- [Docker Compose plugin](https://docs.docker.com/compose/install/) installed
- [Nvidia Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#docker) installed
- Git and wget installed in WSL2/Linux
- The file `sd-v1-4.ckpt` from [HuggingFace](https://huggingface.co/CompVis/stable-diffusion-v-1-4-original) (free registration required)

### Steps

1. Clone this repo to, say, your home directory, and then `cd` into it:
```bash
cd ~
git clone https://github.com/arktronic/sd-multi.git
cd sd-multi
```

2. Place the `sd-v1-4.ckpt` file you downloaded earlier into `~/sd-multi/res/`
3. Run `./verify-resources.sh -d` to verify and download any missing models or weights
    - If you encounter any issues, please make sure they are resolved before continuing to the next step
4. Launch one of the supported forks! (see the fork options below)

### Fork options

⭐ [AUTOMATIC1111](https://github.com/AUTOMATIC1111/stable-diffusion-webui/)
```bash
docker compose --profile automatic1111 up --build
```

⭐ [hlky (sd-webui)](https://github.com/sd-webui/stable-diffusion-webui/), gradio mode
```bash
docker compose --profile hlky up --build
```

⭐ [hlky (sd-webui)](https://github.com/sd-webui/stable-diffusion-webui/), streamlit mode
```bash
docker compose build sd-hlky \
 && docker compose run --service-ports --rm sd-hlky bash -c 'python -m streamlit run scripts/webui_streamlit.py'
```

⭐ [lstein (InvokeAI)](https://github.com/invoke-ai/InvokeAI/), CLI mode
```bash
docker compose build sd-lstein \
 && docker compose run --service-ports --rm sd-lstein
```

⭐ [lstein (InvokeAI)](https://github.com/invoke-ai/InvokeAI/), web mode
```bash
docker compose build sd-lstein \
 && docker compose run --service-ports --rm sd-lstein python scripts/dream.py --web --host 0.0.0.0
```
