#!/usr/bin/env python3
"""
generate_music.py
Simple CLI to generate music WAVs from text prompts using MusicGen (Audiocraft).
"""

import os
import argparse
import torch
import soundfile as sf
from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write

def get_model(model_name: str, device: str):
    """
    Load a pretrained MusicGen model from Audiocraft.
    model_name examples: "musicgen-small", "musicgen-medium", "musicgen-large"
    """
    print(f"Loading model {model_name} on {device} ...")
    model = MusicGen.get_pretrained(model_name)

def generate_from_prompt(model, prompt: str, out_path: str, duration: float = 10.0, cfg_coef: float = 1.0, melody_path: str = None, device: str="cpu"):
    """
    Generate audio using the model from a text prompt.
    - duration: seconds of output audio
    - cfg_coef: classifier-free guidance coefficient (higher -> more adherence to prompt; typical 1.0-3.0)
    - melody_path: optional path to WAV/MP3 to condition on an existing melody
    """
    print("Generating:", prompt)
    model.set_generation_params(duration=duration, cfg_coef=cfg_coef)

    # If you want to condition on a melody file, pass it as the second argument in a list
    # The MusicGen API accepts generate([prompt], [optional_audio])
    if melody_path:
        print("Using melody conditioning file:", melody_path)
        wav = model.generate([prompt], melody_wavs=[melody_path])
        audio = wav[0]
    else:
        wav = model.generate([prompt])
        audio = wav[0]

    # audio is a numpy array: shape (channels, samples) or (samples,)
    # write a wav file at 44100 Hz (or model's sample rate)
    sr = 32000  # MusicGen uses 32kHz typically
    print(f"Saving to {out_path} (sr={sr}) ...")
    # convert to float32 and write
    audio_write(out_path, audio, sr, strategy="loudness")
    print("Done.")

def main():
    parser = argparse.ArgumentParser(description="Generate music from text prompts using MusicGen / Audiocraft.")
    parser.add_argument("--prompt", "-p", type=str, required=True, help="Text prompt describing the music.")
    parser.add_argument("--model", "-m", default="musicgen-small", choices=["musicgen-small", "musicgen-medium", "musicgen-large"], help="Which pretrained MusicGen model to use.")
    parser.add_argument("--out", "-o", default="output.wav", help="Output WAV filename.")
    parser.add_argument("--duration", "-d", type=float, default=10.0, help="Duration of output in seconds (e.g. 10.0).")
    parser.add_argument("--cfg", type=float, default=1.0, help="Guidance strength (cfg coef). Typical 0.5-3.0.")
    parser.add_argument("--melody", type=str, default=None, help="Optional path to WAV/MP3 to use as melody conditioning.")
    args = parser.parse_args()

    # device selection
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print("Using device:", device)

    model = get_model(args.model, device=device)
    generate_from_prompt(model, args.prompt, args.out, duration=args.duration, cfg_coef=args.cfg, melody_path=args.melody, device=device)

if __name__ == "__main__":
    main()
# example 1: quick test (10s)
python generate_music.py -p "A chill lo-fi beat with mellow piano and vinyl crackle, slow tempo, relaxed vibe" -o chill_lofi.wav

# example 2: longer, stronger guidance (20s)
python generate_music.py -p "Uplifting orchestral cinematic piece with strings, brass, swelling choir and steady drums" -o epic_orchestra.wav --duration 20 --cfg 1.5

# example 3: melody conditioning (supply a short wav melody)
python generate_music.py -p "Full band arrangement around the melody" -o arranged.wav --melody seed_melody.wav  
#example 4:
