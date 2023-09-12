import os, sys
import argparse
import pyutau

import utils

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ust_template', type = str, default = 'templates/utau_template.ust')
    parser.add_argument('--word_table', type = str, default = None)
    # parser.add_argument('--voice_bank', type = str, default = 'jklex')
    parser.add_argument('--start_pitch', type = str, default = 'F#2')
    parser.add_argument('--end_pitch', type = str, default = 'C6')
    parser.add_argument('--pitch_step', type = int, default = 1)
    args = parser.parse_args()

    temp_ust = pyutau.UtauPlugin(args.ust_template)
    #print(temp_ust.__str__())

    rest = temp_ust.notes[0]
    note = temp_ust.notes[1]
    temp_ust.notes = []

    f = open(args.word_table)
    words = f.readlines();
    f.close()

    out_dir = './out/'
    out_label = 'default'
    cnt = 0

    for line in words:
        if line[0] == '[':
            out_label = line.replace('\n', '').replace('[', '').replace(']', '')
            if (not os.path.exists(out_dir + out_label)):
                os.makedirs(out_dir + out_label)
            cnt = 0
            continue
        print(out_label, cnt, line.replace('\n', ''))
        lyrics = line.replace('\n', '').split(' ')
        for pitch_num in range(utils.NoteName2PitchNum(args.start_pitch), 1 + utils.NoteName2PitchNum(args.end_pitch), args.pitch_step):
            temp_ust.notes = []
            rest.set_note_num(pitch_num)
            note.set_note_num(pitch_num)
            for i in range(len(lyrics)):
                note.set_lyric(lyrics[i].replace('_', ' '))
                note.note_type = '{:04d}'.format(2 * i + 1)
                rest.note_type = '{:04d}'.format(2 * i)
                temp_ust.insert_note(2 * i, rest.copy())
                temp_ust.insert_note(2 * i + 1, note.copy())
            rest.note_type = '{:04d}'.format(2 * len(lyrics))
            temp_ust.insert_note(2 * len(lyrics), rest)
            
            ust_name = f'{out_label}{cnt}_{utils.PitchNum2NoteName(pitch_num)}'
            temp_ust.write(f'{out_dir}{out_label}/{ust_name}.ust', True)
            #print(f'Written ust: {out_dir}{out_label}/{ust_name}.ust\n')
        cnt += 1

if __name__ == '__main__':
    main()
