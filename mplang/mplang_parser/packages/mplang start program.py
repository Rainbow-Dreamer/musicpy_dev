import os
import sys
import traceback
import chunk
import midiutil
import mido
import fractions
import pygame
from pydub import AudioSegment
from pydub.generators import Sine, Triangle, Sawtooth, Square, WhiteNoise, Pulse
import py

abs_path = os.path.dirname(sys.executable)
sys.path.append('packages')
os.chdir(abs_path)

with open('packages/musicpy/__init__.py', encoding='utf-8') as f:
    exec(f.read())

with open('mplang.py', encoding='utf-8') as f:
    exec(f.read())
