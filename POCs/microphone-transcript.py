#!/usr/bin/env python3

"""Simple microphone-to-transcript POC with helpful CLI and error handling.

Usage:
  ./microphone-transcript.py            # record from default input device and transcribe
  ./microphone-transcript.py --file f.wav  # transcribe existing WAV file
  ./microphone-transcript.py --list-devices  # list available audio devices

Notes:
- If running inside a container you may not have access to a host microphone; use --file to transcribe an existing file instead.
- Ensure PortAudio/dev headers are installed (see project README).
"""

import argparse
import sys
import sounddevice as sd
from scipy.io.wavfile import write
import whisper

# Audio defaults
SAMPLE_RATE = 16000
DURATION = 5  # seconds
OUTPUT_FILE = "speech.wav"


def list_devices():
    print("Available audio devices:\n")
    for i, dev in enumerate(sd.query_devices()):
        print(f"{i}: {dev['name']} (max input channels: {dev['max_input_channels']})")


def record_to_file(duration, samplerate, outfile):
    print(f"Recording {duration}s at {samplerate}Hz...")
    try:
        audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
        sd.wait()
    except sd.PortAudioError as e:
        print("Error: could not access audio input device.")
        print("Details:", e)
        print("\nTips:")
        print(" - Run with --list-devices to see available devices and their indices.")
        print(" - Run with --file <path> to transcribe an existing WAV file instead of recording.")
        sys.exit(2)

    write(outfile, samplerate, audio)
    print("Recording saved to:", outfile)
    return outfile


def transcribe_file(filepath):
    print("Loading Whisper model (this may take a moment)...")
    model = whisper.load_model("base")
    print("Transcribing...")
    result = model.transcribe(filepath)
    print("Transcribed text:")
    print(result.get("text", ""))


def main():
    parser = argparse.ArgumentParser(description="Record audio and transcribe using Whisper")
    parser.add_argument("--file", "-f", help="Path to WAV file to transcribe (skip recording)")
    parser.add_argument("--duration", "-d", type=int, default=DURATION, help="Recording duration in seconds")
    parser.add_argument("--rate", type=int, default=SAMPLE_RATE, help="Sample rate for recording")
    parser.add_argument("--out", default=OUTPUT_FILE, help="Output WAV filename for recording")
    parser.add_argument("--list-devices", action="store_true", help="List available audio devices")

    args = parser.parse_args()

    if args.list_devices:
        list_devices()
        return

    if args.file:
        filepath = args.file
    else:
        filepath = record_to_file(args.duration, args.rate, args.out)

    transcribe_file(filepath)


if __name__ == "__main__":
    main()
