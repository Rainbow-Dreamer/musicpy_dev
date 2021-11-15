# musicpy_dev
This is a repository holding musicpy develop thoughts and some other related stuffs.

### Date: 2021-11-15
I do want to implement an inner language of musicpy that uses a totally independent syntax to represent data structures of musicpy and other functionality these days.

There are already some drafts about the syntax design. I will start working on implementing the interpreter to convert this inner language of musicpy to actual python code that uses musicpy could execute soon.

You can see the draft of the design of this inner language [here](https://github.com/Rainbow-Dreamer/musicpy_dev/blob/main/musicpy%20mp%20language.md).

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
write example_song name='test.mid'
```
