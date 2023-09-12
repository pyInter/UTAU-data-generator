import os
import argparse

import yaml, ruamel.yaml
import copy

import utils

yml = ruamel.yaml.YAML()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ustx_template', type = str, default = 'templates/openutau_template.ustx')
    parser.add_argument('--word_table', type = str, default = None)
    # parser.add_argument('--voice_bank', type = str, default = 'jklex')
    parser.add_argument('--start_pitch', type = str, default = 'F#2')
    parser.add_argument('--end_pitch', type = str, default = 'C6')
    parser.add_argument('--pitch_step', type = int, default = 1)
    args = parser.parse_args()

    with open(args.word_table) as f:
        words = f.readlines();

    out_dir = './out/'
    label = 'default'
    cnt = 0
    track = 0

    with open(args.ustx_template, encoding = 'utf-8') as f:
        ustx_data = yaml.load(f.read(), Loader = yaml.FullLoader)
    one_track = copy.deepcopy(ustx_data['tracks'][0])
    one_part = copy.deepcopy(ustx_data['voice_parts'][0])
    one_note = copy.deepcopy(one_part['notes'][0])

    ustx_data['tracks'] = []
    ustx_data['voice_parts'] = []

    for line in words:
        if line[0] == '[':
            new_label = line.replace('\n', '').replace('[', '').replace(']', '')
            #if (not os.path.exists(out_dir + label)):
            #    os.makedirs(out_dir + label)
            if (track > 0):
                with open(f'{out_dir}{label}.ustx', 'w+', encoding = 'utf-8') as f:
                    yml.dump(ustx_data, f)
                    print(f'Written ustx: {out_dir}{label}.ustx\n')
            cnt = 0
            track = 0
            ustx_data['tracks'] = []
            ustx_data['voice_parts'] = []
            label = new_label
            continue
        print(label, cnt, line.replace('\n', ''))
        lyrics = [lyric.replace('_', ' ') for lyric in line.replace('\n', '').split(' ')]
        new_part = one_part
        new_part['notes'] = [copy.deepcopy(one_note) for _ in range(len(lyrics))]
        for pitch_num in range(utils.NoteName2PitchNum(args.start_pitch), 1 + utils.NoteName2PitchNum(args.end_pitch), args.pitch_step):
            new_part['name'] = f'{label}{cnt}_{utils.PitchNum2NoteName(pitch_num)}'
            new_part['track_no'] = track
            for i in range(len(lyrics)):
                new_part['notes'][i]['position'] = one_note['position'] + i * (one_note['position'] + one_note['duration'])
                new_part['notes'][i]['tone'] = pitch_num
                new_part['notes'][i]['lyric'] = lyrics[i]
            ustx_data['tracks'].append(copy.deepcopy(one_track))
            ustx_data['voice_parts'].append(copy.deepcopy(new_part))
            track += 1
        cnt += 1

    if (track > 0):
        with open(f'{out_dir}{label}.ustx', 'w+', encoding = 'utf-8') as f:
            yml.dump(ustx_data, f)

if __name__ == '__main__':
    main()
