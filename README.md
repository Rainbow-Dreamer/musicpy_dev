# musicpy_dev
This is a repository holding musicpy develop thoughts and some other related stuffs.



### Date: 2022-06-05

Now mplang executable is recompiled to be using musicpy and sf2_loader as dynamic libraries, which means it depends on the musicpy and sf2_loader files that put with it, if you change some parameters inside the packages, you can use mplang with the updated versions. This change avoids any further recompilations of mplang executable when musicpy and sf2_loader are updated. If you want to use mplang with the latest version of musicpy and sf2_loader, just download the latest version and replace the files inside `mplang/mplang_parser/packages` folder. Now the mplang executable is located in `mplang/mplang_parser` folder instead of releases.



### Date: 2022-02-06

Because musicpy and sf2_loader are updated very frequently, so each time they update, the mplang executable is not up-to-date, I personally don't have that much time to compile for a new executable each time I update musicpy or sf2_loader, so you can try to compile a mplang executable by yourself. Here are the steps.

Firstly, be sure to install python >= 3.7.

Then, for python libraries you need to pip install: pyinstaller, musicpy, sf2_loader, if you are already installed musicpy and sf2_loader, please upgrade to the newest version by `pip install --upgrade musicpy sf2_loader`.

Then, download this repository by clicking [here](https://github.com/Rainbow-Dreamer/musicpy_dev/archive/refs/heads/main.zip).

Then, go to the directory `mplang/mplang_parser`.

Open the python file `extra-hooks/hook-sf2_loader.py` in a text editor or IDE, change the python installation path header for the sf2_loader data file path to match your personal python installation path.

Then, open the terminal, copy and paste what is in the text file `pyinstaller mplang.txt` to the terminal, and run to compile the mplang executable. The result executable will be in the `dist` folder.

The mplang executable at the release page will not be updated from now on.



### Date: 2021-11-19

The mplang official documentation is ready, you can look at it [here](https://github.com/Rainbow-Dreamer/musicpy_dev/blob/main/mplang/mplang%20official%20documentation.md).

I just wrote a little music theory function `reverse_piano_keys` using musicpy which converts a piece of music as if it is played on a 88-key piano but the piano keys are reversed (the lowest key become the highest key, and so on), which is actually pretty funny, and somewhat interesting (especially when you hear the result).

The script could be found [here](https://github.com/Rainbow-Dreamer/musicpy_dev/blob/main/reverse_piano_keys/reverse_piano_keys.py), the usage is in the script file.

There are also some examples of original MIDI files and converted MIDI files included at the same folder where the script is in, you can download them and listen, the link is [here](https://github.com/Rainbow-Dreamer/musicpy_dev/tree/main/reverse_piano_keys/examples).

This function is just for fun and not for serious music theory experiment.



### Date: 2021-11-18

Trying to compile the mplang interpreter into a standalone executable.

You could download `mplang.exe` from the release page.

This is the first version of the standalone mplang interpreter, you can use it without python installed, it has an interactive shell when you open it, and it could execute `.mp` files with arguments, and there are some optional flags.

For example, run `mplang` in shell will enter the interactive shell, run `mplang filename` will execute a text file written in mplang.

Optional flags:

`-t`: the filename will be execute as text straightly to the interpreter

`-w`: after interpretation and execution, the interpreter will wait until user press enter to close, this is very useful if you have any play functions in the file, if you do not include this flag, it is very possible that the sound won't come out

Examples of the usage of mplang interpreter executable:
```
mplang "examples.mp"
mplang -t "play C('Cmaj7')"
mplang -w "examples.mp"
```

The mplang official documentation will come out soon.



### Date: 2021-11-17

Adding the interactive parsing functionality to the interpreter. Now you can use mplang interactively using the interpreter.



### Date: 2021-11-16

I have already finished the implementation of some of the most basic syntax parsing functionality of the interpreter for this inner language.

By the way, I think this inner language of musicpy should be called `mplang`.

Well, as the implementation of the syntax abstraction in the interpreter, there will be some special syntax restriction in some specific cases, but not that much. The syntax of mplang will look very different from python, and I have decided to make a special syntax that allows users to write straight python codes inside mplang, which I will talk about in the wiki when the design of this inner language is finished.

Currently, the interpreter already supports parsing a whole text file and a string written in mplang.

If you want to take a look at the interpreter, you can see current progress [here](https://github.com/Rainbow-Dreamer/musicpy_dev/blob/main/mplang/mplang_parser/mplang.py).



### Date: 2021-11-15

I do want to implement an inner language of musicpy that uses a totally independent syntax to represent data structures of musicpy and other functionality these days.

There are already some drafts about the syntax design. I will start working on implementing the interpreter to convert this inner language of musicpy to actual python code that could be executed soon.

You can see the draft of the design of this inner language [here](https://github.com/Rainbow-Dreamer/musicpy_dev/blob/main/mplang/musicpy%20inner%20language%20mplang.md).

For example, a construction of a piece instance in this inner language will be like:
```
let c1 = chord Cmaj7
let c3 = chord (F5, A5, C6, E6)

define piece example_song
name: example song
bpm: 150
track:
c1, instrument 1, start_time 0, channel 0, track_name piano
c3, instrument 47, start_time 2, channel 1, track_name harp
end

# write the piece instance example_song to a MIDI file
write example_song, name='test.mid'
```
