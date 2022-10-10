# sd-multi - run multiple forks of Stable Diffusion

**[Screenshots 👇](https://github.com/arktronic/sd-multi#fork-options)**

## Purpose

I've noticed that some forks of Stable Diffusion, while very active, often break. This repo adds a little bit of stability and predictability, while at the same time allowing the freedom to (relatively easily) play around with different forks and their features.

Docker is used to provide some isolation between various forks' dependencies beyond what Anaconda can do. It also consolidates input and output locations.

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

All the resources (models and weights) are in `~/sd-multi/res/` and all the output files generated by Stable Diffusion are in `~/sd-multi/output/`.

### Fork options

---

#### ⭐ [AUTOMATIC1111](https://github.com/AUTOMATIC1111/stable-diffusion-webui/)
```bash
docker compose --profile automatic1111 up --build
```
![image](https://user-images.githubusercontent.com/344911/194965615-a45a6d8b-3fed-473e-ae3a-44886f0be7a9.png)

---

#### ⭐ [hlky (sd-webui)](https://github.com/sd-webui/stable-diffusion-webui/), gradio mode
```bash
docker compose --profile hlky up --build
```
![image](https://user-images.githubusercontent.com/344911/194965931-46949452-0103-48f1-bb7a-a149338ed97c.png)

---

#### ⭐ [hlky (sd-webui)](https://github.com/sd-webui/stable-diffusion-webui/), streamlit mode
```bash
docker compose build hlky \
 && docker compose run --service-ports --rm hlky bash -c 'python -m streamlit run scripts/webui_streamlit.py'
```
![image](https://user-images.githubusercontent.com/344911/194966164-eb4dc5a4-4ad5-43f1-8d7d-254dbacf4f57.png)

---

#### ⭐ [lstein (InvokeAI)](https://github.com/invoke-ai/InvokeAI/), web mode
```bash
docker compose --profile lstein up --build
```
![image](https://user-images.githubusercontent.com/344911/194965220-d1225e16-9ad0-4093-89e1-f1b60a726719.png)

---

#### ⭐ [lstein (InvokeAI)](https://github.com/invoke-ai/InvokeAI/), CLI mode
```bash
docker compose build lstein \
 && docker compose run --service-ports --rm lstein python scripts/invoke.py
```
![image](https://user-images.githubusercontent.com/344911/194965397-36635481-ae00-4b1b-a38f-9f2dae34a84a.png)

---

#### ⭐ [osi1880vr (deforum-sd-ui)](https://github.com/osi1880vr/deforum-sd-ui/)
```bash
docker compose --profile osi1880vr up --build
```
![image](https://user-images.githubusercontent.com/344911/194966751-77ecd5a3-1bc3-40a1-8fc9-9ffd12e5c99a.png)
