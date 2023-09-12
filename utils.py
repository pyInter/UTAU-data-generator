
NoteNames = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

def PitchNum2NoteName(pitch_num):
    return NoteNames[pitch_num % 12] + str(int(pitch_num / 12 - 1))

def NoteName2PitchNum(note_name):
    note = note_name[:-1]
    octave = int(note_name[-1])
    pitch_num = NoteNames.index(note)
    return pitch_num + (octave + 1) * 12
