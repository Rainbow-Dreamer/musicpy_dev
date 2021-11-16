# musicpy_dev
This is a repository holding musicpy develop thoughts and some other related stuffs.

### Date: 2021-11-16
I have already finished writing some of the most basic syntax parsing functionality of the interpreter for this inner language.

By the way, I think this inner language of musicpy should be called `mplang`.

Well, as the implementation of the syntax abstraction in the interpreter, there will be some special syntax restriction in some specific cases, but not that much. The syntax of mplang will look very different from python, and I have decided to make a special syntax that allows users to write straight python codes inside mplang, which I will talk about in the wiki when the design of this inner language is finished.

If you want to take a look at the interpreter, you can see current progress [here](https://github.com/Rainbow-Dreamer/musicpy_dev/blob/main/mplang/mplang_parser/mplang_parser.py).

### Date: 2021-11-15
I do want to implement an inner language of musicpy that uses a totally independent syntax to represent data structures of musicpy and other functionality these days.

There are already some drafts about the syntax design. I will start working on implementing the interpreter to convert this inner language of musicpy to actual python code that uses musicpy could execute soon.

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
