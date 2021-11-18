# mplang

### This is the official documentation of `mplang`, the inner language of musicpy.

## Contents

- [Introduction](#Introduction)
- [Suggested file naming](#Suggested file naming)
- [Usage of mplang interpreter executable](#Usage of mplang interpreter executable)

## Introduction

`mplang` is an inner language of musicpy which could be interpreted to python code, and then be executed with musicpy package. It has a totally independent syntax to represent data structures of musicpy and other functionality. The interpreter of mplang is a standalone executable, which could provide interactive shell and parsing whole mplang file, so you can use mplang without python installed. You can still write python code and execute in mplang using some special syntax which I will talk about in the syntax section.

## Suggested file naming

The suggested file extension of mplang is `.mp`

## Usage of mplang interpreter executable

You could download `mplang.exe` from the [release page](https://github.com/Rainbow-Dreamer/musicpy_dev/releases/latest).

The mplang interpreter has an interactive shell when you open it, and it could execute `.mp` files with arguments, and there are some optional flags.

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

## The syntax of mplang

### Construct basic musicpy data structures

Use `let` keyword with predefined tokens to construct basic musicpy data structures such as note, chord, scale, piece and drum. Normal variable assignment also must start with `let` keyword.

Here is a list of predefined tokens for constructing musicpy data structures:

```
note, chord, scale, piece, drum
```

There are different syntax for each basic musicpy data structures.

#### note

To construct note instances, the syntax is `let variable_name = note note_name`

For example, `let n1 = note C5`

If you want to set other attributes of the note instance, 

```
let n1 = note C5
let n2 = note C5 (channel 3)
let n3 = note C5 (channel 3; volume 20)

let c1 = chord Cmaj7
let c2 = chord (F5, A5, C6, E6)

let result = c1 | c2

let s1 = scale (C5 major)
let s2 = scale (C5 major; interval=[1,2,1,1,2,1,2])

let e1 = piece {(c1, 1, start_time=0); (c3, 47, start_time=2); (bpm 150); (name example_song)}
let e2 = piece {tracks: (c1, c2); instruments: (1, 47); channels: (0, 1); bpm: 150; name: example_song}
```

#### variable assignment in mplang must using `let` keyword, or switch to python mode to write straight python assignment
```
let c1 = C('Cmaj7')
let c2 = chord('C5, F5, G5, C6')
let result = c1 | c2
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

#### (the order of the keywords in the definition body of piece could be changed)

### Using functions

#### Using functions in mplang is like using python functions without the parenthesis
```
write result, name='test.mid'
play result
```

If you want to include the parenthesis, make sure there are no spaces in the line, then it will work as straight python code.

```
write(result,name='test.mid')
play(result)
```

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

#### (there could be empty lines inside the definition body)

#### using the sampler module
```
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

#### write python code inside mplang (could be multi-line)
```
python:
# some python code
end
```

#### write one line of python code inside mplang
```
python # python code
```

#### import python modules

Normal import statement in python will work, and an additional syntax `use module` which is equivalent to `from module import *`

```
import module
use module
```

