#!/bin/bash

set -e
cd -- "$( dirname -- "${BASH_SOURCE[0]}" )"

DOWNLOAD=0
while getopts ":d" o; do
  case "${o}" in
    d)
      DOWNLOAD=1
      ;;
  esac
done

[ $DOWNLOAD -eq 0 ] && echo 'NOTE: You can specify "-d" to download applicable missing/corrupted files.'

ERR=0

mkdir -p ./res/checkpoints
[ ! -f "./res/checkpoints/sd-v1-4.ckpt" ] && ln -sf ../sd-v1-4.ckpt ./res/checkpoints/sd-v1-4.ckpt
[ ! -f "./res/checkpoints/v1-5-pruned-emaonly.ckpt" ] && ln -sf ../v1-5-pruned-emaonly.ckpt ./res/checkpoints/v1-5-pruned-emaonly.ckpt

# SD models cannot be downloaded directly
function verify_file_huggingface {
  echo "***** Checking res/$1..."
  if [ -f "res/$1" ]; then
    echo "$2  res/$1" | sha256sum -c --quiet &>/dev/null || {
      echo "WARNING: res/$1 appears to be corrupted!"
      echo "Please download it again from $3"
      ERR=1
    }
  else
    echo "WARNING: res/$1 is missing!"
    echo "Please download it from $3"
    echo "(You will need to register for a free account and agree to terms of use)"
    ERR=1
fi
}

# The other files are all verified and downloaded in a similar way:
function verify_file {
  echo "***** Checking $1..."
  if [ -f "res/$1" ]; then
    echo "$2  res/$1" | sha256sum -c --quiet &>/dev/null || {
      echo "WARNING: res/$1 appears to be corrupted!"
      [ $DOWNLOAD -eq 0 ] && ERR=1
      [ $DOWNLOAD -eq 1 ] && {
        echo "Deleting and re-downloading..."
        rm -f "res/$1"
      } || true
    }
  else
    [ $DOWNLOAD -eq 0 ] && {
      echo "WARNING: res/$1 is missing!"
      ERR=1
    } || true
  fi

  [ $DOWNLOAD -eq 1 ] && [ ! -f "res/$1" ] && {
    echo "Downloading $1 from $3..."
    wget "$3" -O "res/$1" -q || {
      echo "WARNING: failed to download file!"
      ERR=1
    }
  } || true
}

verify_file GFPGANv1.3.pth c953a88f2727c85c3d9ae72e2bd4846bbaf59fe6972ad94130e23e7017524a70 "https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.3.pth"
verify_file GFPGANv1.4.pth e2cd4703ab14f4d01fd1383a8a8b266f9a5833dacee8e6a79d3bf21a1b6be5ad "https://github.com/TencentARC/GFPGAN/releases/download/v1.3.4/GFPGANv1.4.pth"
verify_file BSRGAN.pth 5d505a0766160921e0388d76e1ddf08cb114303990f9080432bf2b1c988b1c54 "https://github.com/cszn/KAIR/releases/download/v1.0/BSRGAN.pth"
verify_file ESRGAN.pth 65fece06e1ccb48853242aa972bdf00ad07a7dd8938d2dcbdf4221b59f6372ce "https://github.com/cszn/KAIR/releases/download/v1.0/ESRGAN.pth"
verify_file RealESRGAN_x4plus.pth 4fa0d38905f75ac06eb49a7951b426670021be3018265fd191d2125df9d682f1 "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth"
verify_file RealESRGAN_x4plus_anime_6B.pth f872d837d3c90ed2e05227bed711af5671a6fd1c9f7d7e91c911a61f155e99da "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.2.4/RealESRGAN_x4plus_anime_6B.pth"
verify_file LDSR.yaml 9d6ad53c5dafeb07200fb712db14b813b527edd262bc80ea136777bdb41be2ba "https://heibox.uni-heidelberg.de/f/31a76b13ea27482981b4/?dl=1"
verify_file LDSR.ckpt c209caecac2f97b4bb8f4d726b70ac2ac9b35904b7fc99801e1f5e61f9210c13 "https://heibox.uni-heidelberg.de/f/578df07c8fc04ffbadf3/?dl=1"
verify_file detection_Resnet50_Final.pth 6d1de9c2944f2ccddca5f5e010ea5ae64a39845a86311af6fdf30841b0a5a16d "https://github.com/xinntao/facexlib/releases/download/v0.1.0/detection_Resnet50_Final.pth"
verify_file parsing_parsenet.pth 3d558d8d0e42c20224f13cf5a29c79eba2d59913419f945545d8cf7b72920de2 "https://github.com/xinntao/facexlib/releases/download/v0.2.2/parsing_parsenet.pth"
verify_file SwinIR_4x.pth 99adfa91350a84c99e946c1eb3d8fce34bc28f57d807b09dc8fe40a316328c0a "https://github.com/JingyunLiang/SwinIR/releases/download/v0.0/003_realSR_BSRGAN_DFOWMFC_s64w8_SwinIR-L_x4_GAN.pth"
verify_file dpt_large-midas-2f21e586.pt 2f21e586477d90cb9624c7eef5df7891edca49a1c4795ee2cb631fd4daa6ca69 "https://github.com/intel-isl/DPT/releases/download/1_0/dpt_large-midas-2f21e586.pt"
verify_file AdaBins_nyu.pt 3c917d1b86d058918d4055e70b2cdb9696ec4967bb2d8f05c0051263c1ac9641 "https://cloudflare-ipfs.com/ipfs/Qmd2mMnDLWePKmgfS8m6ntAg4nhV5VkUyAydYBp8cWWeB7/AdaBins_nyu.pt"
verify_file codeformer.pth 1009e537e0c2a07d4cabce6355f53cb66767cd4b4297ec7a4a64ca4b8a5684b7 "https://github.com/sczhou/CodeFormer/releases/download/v0.1.0/codeformer.pth"
#verify_file sd-v1-4.ckpt fe4efff1e174c627256e44ec2991ba279b3816e364b49f9be2abc0b3ff3f8556 "https://www.googleapis.com/storage/v1/b/aai-blog-files/o/sd-v1-4.ckpt?alt=media"

verify_file_huggingface sd-v1-4.ckpt fe4efff1e174c627256e44ec2991ba279b3816e364b49f9be2abc0b3ff3f8556 "https://huggingface.co/CompVis/stable-diffusion-v-1-4-original"
verify_file_huggingface v1-5-pruned-emaonly.ckpt cc6cb27103417325ff94f52b7a5d2dde45a7515b25c255d8e396c90014281516 "https://huggingface.co/runwayml/stable-diffusion-v1-5"

echo ""
if [ $ERR -eq 0 ]; then
  echo "Everything seems to be in order!"
else
  echo "Issues were found. Please address them, or SD may not work correctly."
fi
