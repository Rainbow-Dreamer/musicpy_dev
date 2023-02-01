# mplang

### This is the official documentation of `mplang`, the inner language of musicpy.



## Contents

- [Introduction](#Introduction)
- [Suggested file naming](#Suggested-file-naming)
- [Usage of mplang interpreter executable](#Usage-of-mplang-interpreter-executable)
- [The syntax of mplang](#The-syntax-of-mplang)
  - [Construct musicpy data structures using `let` keyword](#Construct-musicpy-data-structures-using-let-keyword)
    - [note](#note)
    - [chord](#chord)
    - [scale](#scale)
    - [piece](#piece)
    - [drum](#drum)
  - [Write python code inside mplang](#Write-python-code-inside-mplang)
    - [write one line of python code inside mplang](#write-one-line-of-python-code-inside-mplang)
	- [write multi-line python code inside mplang](#write-multi-line-python-code-inside-mplang)
  - [Variable assignments](#Variable-assignments)
  - [Construct musicpy data structures using `define` keyword](#Construct-musicpy-data-structures-using-define-keyword)
    - [piece](#piece-1)
    - [drum](#drum-1)
    - [daw](#daw)
  - [Using functions](#Using-functions)
  - [Import python modules](#Import-python-modules)
  - [Comments in mplang](#Comments-in-mplang)
- [TODO](#TODO)



## Introduction

`mplang` is an inner language of musicpy which could be interpreted to python code, and then be executed with musicpy package. It has a totally independent syntax to represent data structures of musicpy and other functionality. The interpreter of mplang is a standalone executable, which could provide interactive shell and parsing whole mplang file, so you can use mplang without python installed. You can still write python code and execute in mplang using some special syntax which I will talk about in the syntax section.



## Suggested file naming

The suggested file extension of mplang is `.mp`



## Usage of mplang interpreter executable

You could download `mplang.exe` from the downloaded folder `musicpy_dev\mplang\mplang_parser`.

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

### Construct musicpy data structures using `let` keyword

Use `let` keyword with predefined tokens to construct musicpy data structures such as note, chord, scale, piece and drum. Normal variable assignment also must start with `let` keyword.

Here is a list of predefined tokens for constructing musicpy data structures:

```
note, chord, scale, piece, drum
```

There are different syntax for each basic musicpy data structures.

### note

To construct a note, the syntax is

```
let variable_name = note note_name
```

For example,

```
let n1 = note C5
```

If you want to set other attributes of the note, use a pair of parenthesis after it, and put the attribute assignment inside the parenthesis separated by `;`, the syntax of attribute assignment is

```
attribute_name attribute_value
```

For example,

```
let n1 = note C5 (channel 3; volume 20)
```

If you want to add some other operations or functions after the note, use a pair of curly brackets after it, and put what you want to add inside the curly brackets. For example,

```
let n1 = note C5 (channel 3; volume 20) {+ 2}
```

### chord

There are 2 ways to construct a chord, one is to write a chord type, the another one is to write a collection of notes.

To construct a chord using a chord type, the syntax is

```
let variable_name = chord chord_type
```

For example,

```
let c1 = chord Cmaj7
let c2 = chord C7, b9
```

To construct a chord using a collection of notes, the syntax is

```
let variable_name = chord (n1, n2, n3, ...)
```

For example,

```
let c1 = chord (F5, A5, C6, E6)
```

The advanced syntax to specify each note's duration and interval is supported, for example,

```
let c1 = chord (F5[.8;.8], A5[.16;.16], C6[.8;.8], E6[.16;.16])
```

To set other attributes and add some other operations or functions after the chord, the syntax could refer to note. For example,

```
let c1 = chord Cmaj7 (duration 1/8; interval 1/8) {+ 2}
let c1 = chord (F5, A5, C6, E6) (duration 1/8; interval 1/8) {+ 2}
```

### scale

To construct a scale, the syntax is `let variable_name = scale (start_note mode)`, the parenthesis is required. If you want to add other attributes, use `;` to separate attribute assignments, for example

```
let s1 = scale (C5 major)

let s1 = scale (C5 custom_mode; interval [1,2,1,1,2,1,2])
```

### piece

There are 2 ways to construct a piece in musicpy, which are using `piece` constructor and `build` function.

This corresponds to 2 ways of writing a piece in mplang.

If you want to set each attribute when constructing a piece, the syntax is

```
let variable_name = piece {attribute_name1: attribute_value1; attribute_name2: attribute_value2; ...}
```

For example,

```
let e1 = piece {tracks: (c1, c2); instruments: (1, 47); channels: (0, 1); bpm: 150; name: example_song}
```

If you want to use tracks to construct a piece, the syntax is

```
let variable_name = piece {(track1_attribute_name1 track1_attribute_value1, track1_attribute_name2 track1_attribute_value2, ...); (track2_attribute_name1 track2_attribute_value1, track2_attribute_name2 track2_attribute_value2, ...); ...; (other_attribute_name other_attribute_value)}
```

For example,

```
let e1 = piece {(c1, 1, start_time 0); (c2, 47, start_time 2); (bpm 150); (name example_song)}
```

### drum

To construct a drum beat, the syntax is

```
let variable_name = drum (pattern)
```

To add other attributes and other operations and functions after it, you can refer to note.

For example,

```
let d1 = drum (K, H, S, H, r:2)
```



### Write python code inside mplang

You can write python code inside mplang, for one line and multi lines of python code, there are different syntax.

### write one line of python code inside mplang

You can start with `python` with a space and then write python code.

```
python some python code
```

### write multi-line python code inside mplang

You can use `python:` at one line and then write python code under it, enclosing with `end`.

```
python:
some python code
end
```



### Variable assignments

Variable assignment in mplang requires `let` keyword, or you can switch to python mode to write straight python assignment. For example,

```
let result = c1 | c2
```



### Construct musicpy data structures using `define` keyword

You can also use `define` keyword to construct musicpy data structures, which provides a more readable syntax, but this currently only works for a few musicpy data structures, which are piece, drum and daw.

The general form of this syntax is

```
define type variable_name
attribute_name1: attribute_value1
attribute_name2: attribute_value2
...
end
```

The syntax using `define` keyword slightly varies for different types, but in general they follow this form.

The order of the keywords in the definition body of piece could be changed.

There could be empty lines inside the definition body.

### piece

In this example, a piece instance will be assigned to the variable `e3`, the piece instance will have a name `example song`, bpm 150, and the tracks specified inside the definition body.

```
define piece e3
name: example song
bpm: 150
track:
c1, instrument 1, start_time 0, channel 0, track_name piano
c3, instrument 47, start_time 2, channel 1, track_name harp
end
```

Alternatively, you can specify tracks information separately by attributes.

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

### drum

```
define drum d1
pattern:
K, H, S, H, r:2,
K, K, S, H, r:2,
K, H[l:.16; i:.], K[l:.16; i:.], S, H,
K, H, S, H
end
```

### daw
Note that for channels, you must start with `channel number` to construct each channel of the daw, the index is 1-based.
```
define daw current
num: 3
name: example song
bpm: 150
channels:
channel 1, name piano, sound "celeste.sf2"
channel 2, name harp, sound "celeste.sf2"
end
```



### Using functions

Using functions in mplang is like using python functions without the parenthesis.

```
write result, name='test.mid'
play result
```

If you want to include the parenthesis, make sure there are no spaces in the line, then it will work as straight python code.

```
write(result,name='test.mid')
play(result)
```



### Import python modules

Normal import statement in python will work, and an additional syntax `use module` which is equivalent to `from module import *`

```
import module
use module
```



### Comments in mplang

The comments in mplang is the same as python, using `#` at the start for comments. For multi-line comments you will need to create a python block and then write multi-line comments there using python syntax.



## TODO

Currently the design of mplang is at its early stage, the syntax is very simple, and the functionality it supports natively is restricted. The data structures and other advanced music theory functions needs to has their own mplang representation.

* Add construct syntax of other musicpy data structures using `let` keyword including track, tempo, pitch_bend, pan, volume, rest, and mdi, effect, effect_chain, pitch, sound from daw module. For the daw class, I think its construction will be supported only using `define` keyword, like some data structures only support constructing using `let` keyword.

* Add construct syntax of other musicpy data structures using `define` keyword including track, mdi, effect, effect_chain.

* Make multiple chords concatenation while each chord is in construct syntax possible, for example,

  ```
  let c1 = chord Cmaj7 | chord Dmaj7 | chord Emaj7 | chord (F5, A5, C6, E6) | chord Cmaj9
  ```

  at least `|`, `+`, `&` separators should be supported, and nested parenthesis should be supported. For example,

  ```
  let c1 = ((chord Cmaj7 | chord Dmaj7) {% 2}) | chord Emaj7 | chord (F5, A5, C6, E6) | chord Cmaj9
  ```
