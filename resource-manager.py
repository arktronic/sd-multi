from huggingface_hub.hf_api import HfFolder
import argparse
import hashlib
import huggingface_hub
import os
import pathlib
import progressbar
import shutil
import urllib.request

DIR_PREFIX = "/res/"
progbar = None
do_normal_downloads = False
do_hf_downloads = False
issues_found = False
files_normal = (
  ["c953a88f2727c85c3d9ae72e2bd4846bbaf59fe6972ad94130e23e7017524a70", "GFPGANv1.3.pth", "https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.3.pth"],
  ["e2cd4703ab14f4d01fd1383a8a8b266f9a5833dacee8e6a79d3bf21a1b6be5ad", "GFPGANv1.4.pth", "https://github.com/TencentARC/GFPGAN/releases/download/v1.3.4/GFPGANv1.4.pth"],
  ["5d505a0766160921e0388d76e1ddf08cb114303990f9080432bf2b1c988b1c54", "BSRGAN.pth", "https://github.com/cszn/KAIR/releases/download/v1.0/BSRGAN.pth"],
  ["65fece06e1ccb48853242aa972bdf00ad07a7dd8938d2dcbdf4221b59f6372ce", "ESRGAN.pth", "https://github.com/cszn/KAIR/releases/download/v1.0/ESRGAN.pth"],
  ["4fa0d38905f75ac06eb49a7951b426670021be3018265fd191d2125df9d682f1", "RealESRGAN_x4plus.pth", "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth"],
  ["f872d837d3c90ed2e05227bed711af5671a6fd1c9f7d7e91c911a61f155e99da", "RealESRGAN_x4plus_anime_6B.pth", "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.2.4/RealESRGAN_x4plus_anime_6B.pth"],
  ["9d6ad53c5dafeb07200fb712db14b813b527edd262bc80ea136777bdb41be2ba", "LDSR.yaml", "https://heibox.uni-heidelberg.de/f/31a76b13ea27482981b4/?dl=1"],
  ["c209caecac2f97b4bb8f4d726b70ac2ac9b35904b7fc99801e1f5e61f9210c13", "LDSR.ckpt", "https://heibox.uni-heidelberg.de/f/578df07c8fc04ffbadf3/?dl=1"],
  ["6d1de9c2944f2ccddca5f5e010ea5ae64a39845a86311af6fdf30841b0a5a16d", "detection_Resnet50_Final.pth", "https://github.com/xinntao/facexlib/releases/download/v0.1.0/detection_Resnet50_Final.pth"],
  ["3d558d8d0e42c20224f13cf5a29c79eba2d59913419f945545d8cf7b72920de2", "parsing_parsenet.pth", "https://github.com/xinntao/facexlib/releases/download/v0.2.2/parsing_parsenet.pth"],
  ["99adfa91350a84c99e946c1eb3d8fce34bc28f57d807b09dc8fe40a316328c0a", "SwinIR_4x.pth", "https://github.com/JingyunLiang/SwinIR/releases/download/v0.0/003_realSR_BSRGAN_DFOWMFC_s64w8_SwinIR-L_x4_GAN.pth"],
  ["2f21e586477d90cb9624c7eef5df7891edca49a1c4795ee2cb631fd4daa6ca69", "dpt_large-midas-2f21e586.pt", "https://github.com/intel-isl/DPT/releases/download/1_0/dpt_large-midas-2f21e586.pt"],
  ["3c917d1b86d058918d4055e70b2cdb9696ec4967bb2d8f05c0051263c1ac9641", "AdaBins_nyu.pt", "https://cloudflare-ipfs.com/ipfs/Qmd2mMnDLWePKmgfS8m6ntAg4nhV5VkUyAydYBp8cWWeB7/AdaBins_nyu.pt"],
  ["1009e537e0c2a07d4cabce6355f53cb66767cd4b4297ec7a4a64ca4b8a5684b7", "codeformer.pth", "https://github.com/sczhou/CodeFormer/releases/download/v0.1.0/codeformer.pth"],
  ["c6a580b13a5bc05a5e16e4dbb80608ff2ec251a162311590c1f34c013d7f3dab", "vae-ft-mse-840000-ema-pruned.ckpt", "https://huggingface.co/stabilityai/sd-vae-ft-mse-original/resolve/main/vae-ft-mse-840000-ema-pruned.ckpt"],
  ["ad2a33c361c1f593c4a1fb32ea81afce2b5bb7d1983c6b94793a26a3b54b08a0", "v2-1_768-ema-pruned.ckpt", "https://huggingface.co/stabilityai/stable-diffusion-2-1/resolve/main/v2-1_768-ema-pruned.ckpt"],
  ["72b092aadfe146f5d3f395a720c0aa3b2354b2095e3f10dc18f0e9716d286dcb", "v2-1_768-ema-pruned.yaml", "https://raw.githubusercontent.com/Stability-AI/stablediffusion/ca86da3a30c4e080d4db8c25fca73de843663cb4/configs/stable-diffusion/v2-inference-v.yaml"],
)
files_hf = (
  ["fe4efff1e174c627256e44ec2991ba279b3816e364b49f9be2abc0b3ff3f8556", "sd-v1-4.ckpt", "https://huggingface.co/CompVis/stable-diffusion-v-1-4-original", {"repo_id":"CompVis/stable-diffusion-v-1-4-original","filename":"sd-v1-4.ckpt"}],
  ["cc6cb27103417325ff94f52b7a5d2dde45a7515b25c255d8e396c90014281516", "v1-5-pruned-emaonly.ckpt", "https://huggingface.co/runwayml/stable-diffusion-v1-5", {"repo_id":"runwayml/stable-diffusion-v1-5","filename":"v1-5-pruned-emaonly.ckpt"}],
  ["c6bbc15e3224e6973459ba78de4998b80b50112b0ae5b5c67113d56b4e366b19", "sd-v1-5-inpainting.ckpt", "https://huggingface.co/runwayml/stable-diffusion-inpainting", {"repo_id":"runwayml/stable-diffusion-inpainting","filename":"sd-v1-5-inpainting.ckpt"}],
)

def report_progress(chunk_num, chunk_size, file_size):
  global progbar
  if progbar is None:
    widgets = [progressbar.Bar(), " ", progressbar.Percentage(), " ", progressbar.FileTransferSpeed(), " ", progressbar.AnimatedMarker()]
    progbar = progressbar.ProgressBar(widgets = widgets, maxval = file_size)
  try:
    progbar.update(chunk_num * chunk_size)
  except KeyboardInterrupt:
    os._exit(1)
  except:
    pass # Ignore progress bar errors

def save_hf_token(token):
  HfFolder.save_token(token)

def download_hf(file, url, hfargs):
  global issues_found
  try:
    filename = DIR_PREFIX + file
    dl_path = huggingface_hub.hf_hub_download(use_auth_token=True, **hfargs)
    print("Copying " + file + " to destination...")
    shutil.copy(dl_path, filename, follow_symlinks=True)
  except KeyboardInterrupt:
    os._exit(1)
  except Exception as e:
    issues_found = True
    print("Error downloading " + file + ": " + getattr(e, 'message', repr(e)))
    print("Please ensure the provided Hugging Face token is valid.")
    print("You must also agree to " + file + " terms of use at " + url + " to enable this download.")

def download_normal(file, url):
  global issues_found, progbar
  try:
    print("Downloading " + file + "...")
    filename = DIR_PREFIX + file
    pathlib.Path(filename).unlink(missing_ok=True)
    urllib.request.urlretrieve(url, filename, reporthook=report_progress)
  except KeyboardInterrupt:
    os._exit(1)
  except Exception as e:
    issues_found = True
    print("Error downloading " + file + ":" + getattr(e, 'message', repr(e)))
  finally:
    urllib.request.urlcleanup()
    if progbar is not None:
      progbar.finish()
      progbar = None

def verify_hash(hash, file):
  try:
    filename = DIR_PREFIX + file
    if not pathlib.Path(filename).exists():
      return None
    with open(filename, "rb") as f:
      bytes = f.read()
      calculated = hashlib.sha256(bytes).hexdigest()
      return (hash.lower() == calculated.lower())
  except KeyboardInterrupt:
    os._exit(1)
  except:
    return False

def process_normal_files():
  global issues_found, files_normal, do_normal_downloads
  for obj in files_normal:
    hash, filename, url = obj
    print("Checking " + filename + "...", end=" ")
    res = verify_hash(hash, filename)
    if res is None:
      print("Missing")
      if do_normal_downloads:
        download_normal(filename, url)
      else:
        issues_found = True
    elif res==False:
      print("Corrupted")
      if do_normal_downloads:
        download_normal(filename, url)
      else:
        issues_found = True
    else: # True
      print("OK")

def process_hf_files():
  global issues_found, files_hf, do_hf_downloads
  for obj in files_hf:
    hash, filename, url, hf_args = obj
    print("Checking " + filename + "...", end=" ")
    res = verify_hash(hash, filename)
    if res is None:
      print("Missing")
      if do_hf_downloads:
        download_hf(filename, url, hf_args)
      else:
        issues_found = True
        print("Please provide a valid Hugging Face token to download " + filename + " - see https://huggingface.co/settings/tokens")
        print("You must also agree to " + filename + " terms of use at " + url + " to enable this download.")
    elif res==False:
      print("Corrupted")
      if do_hf_downloads:
        download_hf(filename, url, hf_args)
      else:
        issues_found = True
        print("Please provide a valid Hugging Face token to download " + filename + " - see https://huggingface.co/settings/tokens")
        print("You must also agree to " + filename + " terms of use at " + url + " to enable this download.")
    else: # True
      print("OK")

def process_supplemental():
  pathlib.Path("/res/checkpoints").mkdir(parents=True, exist_ok=True)
  pathlib.Path("/res/controlnet").mkdir(parents=True, exist_ok=True)
  os.system("chmod -R go+rw /res")
  if pathlib.Path("/res/sd-v1-4.ckpt").exists() and not pathlib.Path("/res/checkpoints/sd-v1-4.ckpt").exists():
    os.system("ln -sf ../sd-v1-4.ckpt /res/checkpoints/sd-v1-4.ckpt")
  if pathlib.Path("/res/v1-5-pruned-emaonly.ckpt").exists() and not pathlib.Path("/res/checkpoints/v1-5-pruned-emaonly.ckpt").exists():
    os.system("ln -sf ../v1-5-pruned-emaonly.ckpt /res/checkpoints/v1-5-pruned-emaonly.ckpt")
  if pathlib.Path("/res/vae-ft-mse-840000-ema-pruned.ckpt").exists() and not pathlib.Path("/res/checkpoints/v1-5-pruned-emaonly.vae.pt").exists():
    os.system("ln -sf ../vae-ft-mse-840000-ema-pruned.ckpt /res/checkpoints/v1-5-pruned-emaonly.vae.pt")
  if pathlib.Path("/res/v2-1_768-ema-pruned.ckpt").exists() and not pathlib.Path("/res/checkpoints/v2-1_768-ema-pruned.ckpt").exists():
    os.system("ln -sf ../v2-1_768-ema-pruned.ckpt /res/checkpoints/v2-1_768-ema-pruned.ckpt")
  if pathlib.Path("/res/v2-1_768-ema-pruned.yaml").exists() and not pathlib.Path("/res/checkpoints/v2-1_768-ema-pruned.yaml").exists():
    os.system("ln -sf ../v2-1_768-ema-pruned.yaml /res/checkpoints/v2-1_768-ema-pruned.yaml")

  if not pathlib.Path("/res/target-model.ckpt").exists():
    if pathlib.Path("/res/v1-5-pruned-emaonly.ckpt").exists():
      print("Selecting SD v1.5 as the default model (target-model.ckpt)")
      os.system("ln -sf ./v1-5-pruned-emaonly.ckpt /res/target-model.ckpt")
    elif pathlib.Path("/res/sd-v1-4.ckpt").exists():
      print("Selecting SD v1.4 as the default model (target-model.ckpt)")
      os.system("ln -sf ./sd-v1-4.ckpt /res/target-model.ckpt")
    else:
      print("Warning: no default SD model exists. You need at least one in order to generate images.")

if __name__ == "__main__":
  parser = argparse.ArgumentParser("Verify and optionally download resource files")
  parser.add_argument("-d", "--download", action="store_true", help="Download missing or corrupted files in addition to verifying")
  parser.add_argument("-t", "--token", nargs=1, default="", help="Hugging Face token for downloading weights")
  args = parser.parse_args()
  do_normal_downloads = args.download
  if args.token != "":
    do_hf_downloads = True
    save_hf_token(args.token[0])

  print("\n*** Stable Diffusion Resource Manager ***\n")

  if not do_hf_downloads and len(os.environ.get("HUGGINGFACE_TOKEN", "").strip()) > 0:
    print("(Using HUGGINGFACE_TOKEN environment variable)")
    do_hf_downloads = True
    save_hf_token(os.environ.get("HUGGINGFACE_TOKEN", "").strip())

  if not do_normal_downloads:
    print("Note: you can specify \"-d\" to download missing files and \"-t your_hf_token\" to include Hugging Face downloads.\n")
  elif not do_hf_downloads:
    print("Note: you can specify \"-t your_hf_token\" in addition to \"-d\" to include Hugging Face downloads.\n")

  process_normal_files()
  process_hf_files()
  process_supplemental()
  if issues_found:
    print("\nIssues were found. Please address them, or SD might not work correctly.")
  else:
    print("\nEverything seems to be in order!")
