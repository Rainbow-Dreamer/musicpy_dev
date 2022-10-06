let c1 = chord Cmaj7 (duration 1/2; interval 1/8) {% (1/8, 1/8)}
let c3 = chord (F5, A5, C6, E6) (duration 1/2; interval 1/8) {% (1/2, 1/8) - database.octave}
let e1 = c1 | c3

let n1 = note C5
let n2 = note A#6 {% (1,50)}
let n3 = note C5 (channel 3; volume 20)
let n4 = note C5 (channel 3) {+2}

let e2 = c1 + 2
let e3 = c1.reverse()

let s1 = scale (C5 self_defined_scale; interval [1,2,1,1,2,1,2])
let s2 = scale (C5 major)

let e1 = piece {(c1, 1, start_time 0); (c3, 47, start_time 2); (bpm 150); (name example_song)}
let e5 = piece {tracks: (c1, c3); instruments: (1, 47); channels: (0, 1); bpm: 150; name: example_song}

define piece example_song
name: example song
bpm: 150
track:
c1, instrument 1, start_time 0, channel 0, track_name piano
c3, instrument 47, start_time 1, channel 1, track_name harp
end

define piece e3
name: example song
bpm: 150
tracks: c1, c3
instruments: 1, 47
start_times: 0, 2
channels: 0, 1
track_names: piano, harp
end
# write the piece instance example_song to a MIDI file
# play example_song, name='temp.mid'

use musicpy.sampler

define sampler current
num: 3
name: example song
bpm: 150
channels:
channel 1, name piano, sound "Arachno.sf2"
channel 2, name harp, sound "Arachno.sf2"
end
