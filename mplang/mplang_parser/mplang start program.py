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
import pygame.midi
import time

abs_path = os.path.dirname(sys.executable)
os.chdir(abs_path)
sys.path.append('.')

with open('musicpy/__init__.py', encoding='utf-8') as f:
    exec(f.read())

with open('mplang.py', encoding='utf-8') as f:
    exec(f.read())
