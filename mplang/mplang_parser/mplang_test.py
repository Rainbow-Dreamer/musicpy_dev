import sys
import os

sys.path.append(r'G:\university\MyAI project\py files\musicpy')
sys.path.append(
    r'G:\university\MyAI project\py files\other py files\sf2_loader')
import mplang

mplang.parse(file='examples.mp', debug=1)
#mplang.interactive_parse()
