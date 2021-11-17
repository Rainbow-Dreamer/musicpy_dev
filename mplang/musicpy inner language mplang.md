### this is a representation of musicpy inner language `mplang` which could be converted to python code, and then execute with musicpy package, with suggested file extension `.mp`

#### some examples of constructing notes, chords and scales

```
let c1 = chord Cmaj7
let c2 = chord [C5, F5, G5, C6]
let c3 = chord (F5, A5, C6, E6)
let a1 = chord {c, f, g, c}
let a2 = note C5
let a2 = note C5 (channel 3)
let a3 = scale (C5 major)
let e1 = piece {(c1, 1, start_time=0); (c3, 47, start_time=2); (bpm 150); (name example_song)}
let e5 = piece {tracks: (c1, c2); instruments: (1, 47); channels: (0, 1); bpm: 150; name: example_song}
let s1 = scale (C5 major; interval=[1,2,1,1,2,1,2])
let result = c1 | c2
write result
play result
```



### syntax for constructing a piece instance
#### in this example, a piece instance will be assigned to the variable `e3`, the piece instance will have a name `example_song`, bpm 150, and the tracks specified inside the definition body

```
define piece e3
name: example song
bpm: 150
track:
c1, instrument 1, start_time 0, channel 0, track_name piano
c3, instrument 47, start_time 2, channel 1, track_name harp
end
```



#### or specify tracks information separately
```
define piece e3
name: example song
bpm: 150
tracks: c1, c3
instruments: 1, 47
start_times: 0, 2
channels: 0, 1
track_names: piano, harp
end
```



### the order of the keywords in the definition body of piece could be changed

#### get the first track of the piece instance e3
```
let t1 = e3[1]
```

#### get the attributes of the track instance
```
let t1_channel = t1.channel
```

#### use functions of the chord instance
```
let e5 = c1 + 2
let e5 = c1.reverse()
```

#### define drum beats
```
# this syntax must be in one line
let d1 = drum 0,1,2,1,{2}

# this syntax supports multiple lines
define drum d1
mapping: ... (if use default mappings then you do not need to write this)
pattern:
0, 1, 2, 1, {2},
0, 0, 2, 1, {2},
0, 1[.16;.], 0[.16;.], 2, 1,
0, 1, 2, 1
end
```

#### there could be empty lines inside the definition body



#### using the sampler module

```
use musicpy.sampler
define sampler current
num: 3
name: example song
bpm: 150
channels:
channel 1, name piano, sound "celeste.sf2"
channel 2, name harp, sound "celeste.sf2"
end

current.export(e3)
```

### write python code inside mplang (could be multi-line)
```
python:
# some python code
end
```

### write one line of python code inside mplang
```
python # python code
```
