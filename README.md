# musicpy_dev
This is a repository holding musicpy develop thoughts and some other related stuffs.

### Date: 2021-11-19
The official mplang documentation is already, you can look at it [here](https://github.com/Rainbow-Dreamer/musicpy_dev/blob/main/mplang/mplang%20official%20documentation.md)

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

The official mplang documentation will come out soon.

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
