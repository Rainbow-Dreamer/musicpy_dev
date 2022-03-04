import musicpy as mp
'''
Introduction:
This is a small script of a music theory function implemented using musicpy,
this function converts a piece of music as if it is played on a 88-key piano
but the piano keys are reversed (the lowest key become the highest key, and so on),
just enjoy this little fun function~

Usage:
# firstly read a MIDI file as a piece instance,
# and then apply merge function to it in order to get a chord instance
bpm, test_piece, start_time = mp.read(file_path).merge()

# convert to a new chord instance with reversed piano keys applied
test_piece_new = reverse_piano_keys(test_piece)

# play the converted piece and enjoy
mp.play(test_piece_new, bpm=bpm, start_time=start_time)
'''


def reverse_piano_keys(obj):
    temp = mp.copy(obj)
    for i, each in enumerate(temp.notes):
        if type(each) == mp.note:
            reverse_note = mp.degree_to_note(87 - (each.degree - 21) + 21)
            reverse_note.channel = each.channel
            reverse_note.duration = each.duration
            reverse_note.volume = each.volume
            temp.notes[i] = reverse_note
    return temp
