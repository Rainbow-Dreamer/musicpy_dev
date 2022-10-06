piece_attributes = piece.__init__.__code__.co_varnames
piece_attributes_str = ['name', 'track_names']
track_attributes = track.__init__.__code__.co_varnames
track_attributes_str = ['track_name', 'name']
scale_attributes_str = ['start', 'mode', 'name']
sampler_attributes = ['name', 'num', 'bpm']
drum_attributes_str = ['name']
define_state = False
define_variable = None
define_body = []
python_state = False
special_argv = ['-t', '-w']


def find_parenthesis(lines, left='(', right=')'):
    result = []
    current_pair = []
    find_left = False
    omit_left = False
    for i in range(len(lines)):
        current = lines[i]
        if current == left:
            if not find_left:
                current_pair.append(i)
                find_left = True
            else:
                omit_left = True
        elif current == right and find_left:
            if not omit_left:
                current_pair.append(i)
                result.append(current_pair)
                current_pair = []
                find_left = False
            else:
                omit_left = False
    return result


def get_part_in_parenthesis(lines, inds, ind):
    current_ind = inds[ind]
    return lines[current_ind[0] + 1:current_ind[1]]


def parse_set_attribute(lines, str_attributes=None, split_symbol=';'):
    current_attributes = [
        r.strip().split(' ', 1) for r in lines.split(split_symbol)
    ]
    if str_attributes:
        for each in current_attributes:
            if each[0] in str_attributes:
                each[1] = f'"{each[1]}"'
    result = ','.join(['='.join(i) for i in current_attributes])
    return result


def parser(text=None, file=None):
    if file:
        with open(file, encoding='utf-8') as f:
            text = f.read()
    lines = text.split('\n')
    i = 0
    while i < len(lines):
        current = lines[i]
        current_split = current.split(' ', 1)
        current_split_length = len(current_split)
        if current_split_length == 2:
            start_token, remain_part = current_split
            if start_token == 'let':
                make_token_parser(lines, i, remain_part)
            elif start_token == 'define':
                define_token_parser(lines, i, remain_part)
            else:
                special_token_parser(start_token, lines, i, remain_part)
        elif current_split_length == 1:
            single_token_parser(lines, i, current_split)
        i += 1
    return '\n'.join(lines)


def make_token_parser(lines=None, i=None, remain_part=None, current=None):
    if '=' in remain_part:
        variable_name, definition_part = remain_part.split('=', 1)
    else:
        variable_name, definition_part = remain_part.split(' ', 1)
    variable_name = variable_name.strip()
    definition_part = definition_part.lstrip()
    current_definition_split = definition_part.split(' ', 1)
    if len(current_definition_split) == 1:
        if current is not None:
            return remain_part
        else:
            lines[i] = remain_part
    elif len(current_definition_split) == 2:
        data_type_token, current_data = current_definition_split
        current_data = current_data.strip()
        if data_type_token == 'chord':
            result = make_chord_parser(lines, variable_name, current_data, i,
                                       current)
        elif data_type_token == 'note':
            result = make_note_parser(lines, variable_name, current_data, i,
                                      current)
        elif data_type_token == 'scale':
            result = make_scale_parser(lines, variable_name, current_data, i,
                                       current)
        elif data_type_token == 'piece':
            result = make_piece_parser(lines, variable_name, current_data, i,
                                       current)
        elif data_type_token == 'drum':
            result = make_drum_parser(lines, variable_name, current_data, i,
                                      current)
        else:
            if current is not None:
                return remain_part
            else:
                lines[i] = remain_part
        if current is not None:
            return result


def define_token_parser(lines=None, i=None, remain_part=None, current=None):
    global define_state
    global define_variable
    type_name, variable_name = remain_part.split(' ', 1)
    if type_name == 'piece':
        if current:
            define_state = 'piece'
            define_variable = variable_name
        else:
            define_piece_parser(lines, i, variable_name)
    elif type_name == 'drum':
        if current:
            define_state = 'drum'
            define_variable = variable_name
        else:
            define_drum_parser(lines, i, variable_name)
    elif type_name == 'sampler':
        if current:
            define_state = 'sampler'
            define_variable = variable_name
        else:
            define_sampler_parser(lines, i, variable_name)
    if current:
        return ''


def single_token_parser(lines=None, i=None, current_split=None, current=None):
    if current_split[0] == 'python:':
        if not current:
            python_code_parser(lines, i)
        else:
            global python_state
            python_state = True
            return ''
    else:
        if current:
            return current


def special_token_parser(start_token,
                         lines=None,
                         i=None,
                         remain_part=None,
                         current=None):
    if start_token != '#':
        if start_token == 'use':
            result = f'from {remain_part} import *'
        elif start_token == 'import':
            result = f'import {remain_part}'
        elif start_token == 'python':
            result = remain_part
        else:
            result = f'{start_token}({remain_part})'
        if current:
            return result
        else:
            lines[i] = result
    else:
        if current:
            return current


def python_code_parser(lines, i, current=None):
    ind = len(lines)
    for j in range(i, ind):
        if lines[j].strip() == 'end':
            ind = j
            break
    if current:
        result = '\n'.join(lines[i:ind])
        return result
    else:
        result = '\n'.join(lines[i + 1:ind])
        lines[i] = result
        del lines[i + 1:ind + 1]


def make_chord_parser(lines=None,
                      variable_name=None,
                      current_data=None,
                      i=None,
                      current=None):
    config_part, other_part = '', ''
    config_inds = find_parenthesis(current_data)
    other_inds = find_parenthesis(current_data, '{', '}')
    start_ind = len(current_data)
    chord_mode = 0
    if config_inds:
        has_config = True
        current_config_ind = 0
        first_config_ind = config_inds[0][0]
        if first_config_ind == 0:
            chord_mode = 1
            if len(config_inds) > 1:
                first_config_ind = config_inds[1][0]
                current_config_ind = 1
            else:
                has_config = False
        if has_config and not (other_inds
                               and first_config_ind > other_inds[0][0]):
            start_ind = first_config_ind
            config_part = f', {parse_set_attribute(get_part_in_parenthesis(current_data, config_inds, current_config_ind))}'
    if other_inds:
        start_ind = min(other_inds[0][0], start_ind)
        other_part = get_part_in_parenthesis(current_data, other_inds, 0)
    if chord_mode == 0:
        chord_part = current_data[:start_ind].strip()
        result = f'{variable_name} = C("{chord_part}"{config_part}) {other_part}'
    else:
        chord_part = get_part_in_parenthesis(current_data, config_inds, 0)
        result = f'{variable_name} = chord("{chord_part}"{config_part}) {other_part}'
    if current:
        return result
    else:
        lines[i] = result


def make_note_parser(lines=None,
                     variable_name=None,
                     current_data=None,
                     i=None,
                     current=None):
    config_part, other_part = '', ''
    config_inds = find_parenthesis(current_data)
    other_inds = find_parenthesis(current_data, '{', '}')
    start_ind = len(current_data)
    if config_inds:
        first_config_ind = config_inds[0][0]
        if not (other_inds and first_config_ind > other_inds[0][0]):
            start_ind = first_config_ind
            config_part = f', {parse_set_attribute(get_part_in_parenthesis(current_data, config_inds, 0))}'
    if other_inds:
        start_ind = min(other_inds[0][0], start_ind)
        other_part = get_part_in_parenthesis(current_data, other_inds, 0)
    note_name = current_data[:start_ind].strip()
    result = f'{variable_name} = N("{note_name}"{config_part}) {other_part}'
    if current:
        return result
    else:
        lines[i] = result


def make_scale_parser(lines=None,
                      variable_name=None,
                      current_data=None,
                      i=None,
                      current=None):
    if not (current_data.startswith('(') and current_data.endswith(')')):
        raise SyntaxError(
            'using `let` to construct a scale instance must start with `(` and end with `)`, for example `scale (C5 major)`'
        )
    current_scale_dict = {}
    current_scale_offset = 0
    current_scale_attributes = current_data[1:-1].split(';')
    current_scale_settings = current_scale_attributes[0].strip()
    if '=' not in current_scale_settings:
        current_scale_offset = 1
        current_scale_settings = current_scale_settings.split(' ', 1)
        current_scale_dict['start'] = f'"{current_scale_settings[0]}"'
        if len(current_scale_settings) > 1:
            current_scale_dict['mode'] = f'"{current_scale_settings[1]}"'
    for each_scale_attribute in current_scale_attributes[
            current_scale_offset:]:
        each_scale_attribute_name, each_scale_attribute_value = each_scale_attribute.strip(
        ).split(' ', 1)
        each_scale_attribute_name = each_scale_attribute_name.strip()
        if each_scale_attribute_name in scale_attributes_str:
            each_scale_attribute_value = f'"{each_scale_attribute_value}"'
        current_scale_dict[
            each_scale_attribute_name] = each_scale_attribute_value
    current_data_config_part = ','.join([
        '='.join(each_scale_attribute)
        for each_scale_attribute in current_scale_dict.items()
    ])
    result = f'{variable_name} = scale({current_data_config_part})'
    if current:
        return result
    else:
        lines[i] = result


def make_piece_parser(lines=None,
                      variable_name=None,
                      current_data=None,
                      i=None,
                      current=None):
    bracket_inds = find_parenthesis(current_data, '{', '}')
    if not bracket_inds:
        raise SyntaxError(
            'using `let` to construct a piece instance must start with `{` and end with `}`, for example `piece {tracks: (c1, c2)}`'
        )
    current_piece_dict = {}
    piece_tracks = []
    current_piece_attributes = get_part_in_parenthesis(current_data,
                                                       bracket_inds,
                                                       0).split(';')
    other_part = current_data[bracket_inds[0][1] + 1:]
    for each in current_piece_attributes:
        each = each.strip()
        if each.startswith('(') and each.endswith(')'):
            each_attribute_name, each_attribute_value = each[1:-1].split(
                ' ', 1)
            if each_attribute_name in piece_attributes:
                if each_attribute_name in piece_attributes_str:
                    current_piece_dict[
                        each_attribute_name] = f'"{each_attribute_value}"'
                else:
                    current_piece_dict[
                        each_attribute_name] = each_attribute_value
            else:
                piece_tracks.append(
                    f'track({parse_set_attribute(each[1:-1], track_attributes_str, split_symbol=",")})'
                )
        elif ':' in each:
            each_attribute_name, each_attribute_value = each.split(':', 1)
            each_attribute_name = each_attribute_name.strip()
            each_attribute_value = each_attribute_value.strip()
            if each_attribute_name in piece_attributes:
                if each_attribute_name in piece_attributes_str:
                    current_piece_dict[
                        each_attribute_name] = f'"{each_attribute_value}"'
                else:
                    if each_attribute_value.startswith(
                            '(') and each_attribute_value.endswith(')'):
                        each_attribute_value = f'[{each_attribute_value[1:-1]}]'
                    current_piece_dict[
                        each_attribute_name] = each_attribute_value
    if piece_tracks:
        result_attributes = ",".join(
            ["=".join(each) for each in current_piece_dict.items()])
        result = f'build({",".join(piece_tracks)},{result_attributes})'
    else:
        result_attributes = ",".join(
            ["=".join(each) for each in current_piece_dict.items()])
        result = f'piece({result_attributes})'
    result += other_part
    result = f'{variable_name} = {result}'
    if current:
        return result
    else:
        lines[i] = result


def make_drum_parser(lines=None,
                     variable_name=None,
                     current_data=None,
                     i=None,
                     current=None):
    config_part, other_part = '', ''
    config_inds = find_parenthesis(current_data)
    if not config_inds:
        raise SyntaxError(
            'using `let` to construct a drum instance must start with `(` and end with `)`, for example `drum (0,1,2,1)`'
        )
    other_inds = find_parenthesis(current_data, '{', '}')
    drum_part = get_part_in_parenthesis(current_data, config_inds, 0)
    if len(config_inds) > 1:
        config_part = f', {parse_set_attribute(get_part_in_parenthesis(current_data, config_inds, 1), drum_attributes_str)}'
    if other_inds:
        if other_inds[-1][0] > config_inds[0][1]:
            other_part = get_part_in_parenthesis(current_data, other_inds, -1)
    result = f'{variable_name} = drum("{drum_part}"{config_part}) {other_part}'
    if current:
        return result
    else:
        lines[i] = result


def define_piece_parser(lines, i, variable_name, current=None):
    j = i
    current_definition_range = i, len(lines)
    while j < len(lines):
        if lines[j].strip() != 'end':
            j += 1
        else:
            current_definition_range = i, j
            break
    piece_attribute_dict = {}
    piece_tracks = []
    for each in range(current_definition_range[0],
                      current_definition_range[1]):
        current_line_define = lines[each]
        if ':' in current_line_define:
            attribute_token, attribute_value = current_line_define.split(
                ':', 1)
            attribute_token = attribute_token.strip()
            attribute_value = attribute_value.lstrip()
            if attribute_token == 'name':
                piece_attribute_dict['name'] = f'"{attribute_value}"'
            elif attribute_token == 'bpm':
                attribute_value = attribute_value.strip()
                piece_attribute_dict['bpm'] = attribute_value
            elif attribute_token == 'track':
                track_parser(lines, current_definition_range, piece_tracks,
                             each)
            else:
                if attribute_token in piece_attributes_str:
                    current_text = ",".join(
                        [f'"{t.strip()}"' for t in attribute_value.split(",")])
                    piece_attribute_dict[attribute_token] = f'[{current_text}]'
                else:
                    piece_attribute_dict[
                        attribute_token] = f'[{attribute_value}]'
    if piece_tracks:
        current_piece_text = f'build({",".join(piece_tracks)},{",".join([f"{each_piece_attribute}={piece_attribute_dict[each_piece_attribute]}" for each_piece_attribute in piece_attribute_dict])})'
    else:
        current_piece_text = f'piece({",".join([f"{each_piece_attribute}={piece_attribute_dict[each_piece_attribute]}" for each_piece_attribute in piece_attribute_dict])})'
    result = f'{variable_name} = {current_piece_text}'
    if current:
        return result
    lines[current_definition_range[0]] = result
    del lines[current_definition_range[0] + 1:current_definition_range[1] + 1]


def track_parser(lines, current_definition_range, piece_tracks, each):
    for each_track in range(each + 1, current_definition_range[1]):
        current_line_track = lines[each_track]
        if ':' in current_line_track:
            break
        elif current_line_track.lstrip():
            current_track_dict = {}
            track_split = current_line_track.split(',')
            for each_track_split_ind in range(len(track_split)):
                each_track_split = track_split[each_track_split_ind].strip()
                each_track_split_info = each_track_split.split(' ', 1)
                if len(each_track_split_info) == 2:
                    each_track_split_attribute, each_track_split_value = each_track_split_info
                    each_track_split_value = each_track_split_value.strip()
                    if each_track_split_attribute in track_attributes_str:
                        each_track_split_value = f'"{each_track_split_value}"'
                    elif each_track_split_attribute == 'instrument' and not each_track_split_value.strip(
                    ).isdigit():
                        each_track_split_value = f'"{each_track_split_value}"'
                    if each_track_split_attribute in track_attributes:
                        current_track_dict[
                            each_track_split_attribute] = each_track_split_value
                else:
                    each_track_split_value = each_track_split_info[0]
                    if each_track_split_ind == 0:
                        current_track_dict['content'] = each_track_split_value
            current_track_attribute_text = ",".join([
                f"{each_attribute}={current_track_dict[each_attribute]}"
                for each_attribute in current_track_dict
            ])
            current_track_text = f'track({current_track_attribute_text})'
            piece_tracks.append(current_track_text)


def drum_pattern_parser(lines, current_definition_range, each):
    pattern_ind = current_definition_range[1]
    for i in range(each + 1, current_definition_range[1]):
        if ':' in lines[i]:
            pattern_ind = i
            break
    return '\n'.join(lines[each + 1:pattern_ind])


def sampler_channel_parser(lines, current_definition_range, each,
                           current_channels):
    channel_counter = 1
    for i in range(each + 1, current_definition_range[1]):
        current = lines[i].strip()
        if current.startswith('channel'):
            current_channel_info = [channel_counter, None, None]
            current_attributes = current.split(',')
            for each in current_attributes:
                current_attribute, current_value = each.strip().split(' ', 1)
                if current_attribute == 'channel':
                    current_channel_info[0] = int(current_value)
                elif current_attribute == 'name':
                    current_channel_info[1] = f'"{current_value}"'
                elif current_attribute == 'sound':
                    current_channel_info[2] = current_value
            current_channels.append(current_channel_info)
            channel_counter += 1
        elif ':' in current:
            break


def define_drum_parser(lines, i, variable_name, current=None):
    j = i
    current_definition_range = i, len(lines)
    while j < len(lines):
        if lines[j].strip() != 'end':
            j += 1
        else:
            current_definition_range = i, j
            break
    drum_attribute_dict = {}
    drum_attributes = drum.__init__.__code__.co_varnames
    ranges = []
    for each in range(current_definition_range[0],
                      current_definition_range[1]):
        current_line_define = lines[each]
        if ':' in current_line_define:
            attribute_token, attribute_value = current_line_define.split(
                ':', 1)
            attribute_token = attribute_token.strip()
            attribute_value = attribute_value.lstrip()
            if attribute_token in drum_attributes:
                ranges.append(each)
    ranges.append(current_definition_range[1])

    for i in range(len(ranges) - 1):
        current_start, current_stop = ranges[i], ranges[i + 1]
        current_part = ''.join(lines[current_start:current_stop])
        attribute_token, attribute_value = current_part.split(':', 1)
        attribute_token = attribute_token.strip()
        attribute_value = attribute_value.lstrip()
        if attribute_token == 'name':
            drum_attribute_dict['name'] = f'"{attribute_value}"'
        elif attribute_token == 'pattern':
            drum_attribute_dict['pattern'] = f'"{attribute_value}"'
        else:
            drum_attribute_dict[attribute_token] = attribute_value
    current_drum_text = f'drum({",".join([f"{each_drum_attribute}={drum_attribute_dict[each_drum_attribute]}" for each_drum_attribute in drum_attribute_dict])})'
    result = f'{variable_name} = {current_drum_text}'
    if current:
        return result
    lines[current_definition_range[0]] = result
    del lines[current_definition_range[0] + 1:current_definition_range[1] + 1]


def define_sampler_parser(lines, i, variable_name, current=None):
    if 'sampler' not in globals():
        if parse_state == 1:
            print(
                "sampler module is not imported, please import by 'use musicpy.sampler'"
            )
            result = ''
            if current:
                return result
            lines[current_definition_range[0]] = result
            del lines[current_definition_range[0] +
                      1:current_definition_range[1] + 1]
            return
    j = i
    current_definition_range = i, len(lines)
    while j < len(lines):
        if lines[j].strip() != 'end':
            j += 1
        else:
            current_definition_range = i, j
            break
    sampler_attribute_dict = {}
    current_channels = []
    for each in range(current_definition_range[0],
                      current_definition_range[1]):
        current_line_define = lines[each]
        if ':' in current_line_define:
            attribute_token, attribute_value = current_line_define.split(
                ':', 1)
            attribute_token = attribute_token.strip()
            attribute_value = attribute_value.lstrip()
            if attribute_token == 'name':
                sampler_attribute_dict['name'] = f'"{attribute_value}"'
            elif attribute_token == 'channels':
                sampler_channel_parser(lines, current_definition_range, each,
                                       current_channels)
            elif attribute_token in sampler_attributes:
                sampler_attribute_dict[attribute_token] = attribute_value
    current_sampler_text = f'sampler({",".join([f"{each_sampler_attribute}={sampler_attribute_dict[each_sampler_attribute]}" for each_sampler_attribute in sampler_attribute_dict])})'
    if current_channels:
        current_channels_text = '\n'
        for k in current_channels:
            current_channel_num, current_channel_name, current_channel_sound = k
            if current_channel_name is not None:
                current_channels_text += f'{variable_name}.set_channel_name({current_channel_num}, {current_channel_name})\n'
            if current_channel_sound is not None:
                current_path = current_channel_sound[1:-1]
                if os.path.splitext(current_path)[1][1:].lower() == 'esi':
                    current_channels_text += f'{variable_name}.load({current_channel_num}, esi={current_channel_sound})\n'
                else:
                    current_channels_text += f'{variable_name}.load({current_channel_num}, {current_channel_sound})\n'
        current_channels_text = current_channels_text[:-1]
        current_sampler_text += current_channels_text
    result = f'{variable_name} = {current_sampler_text}'
    if current:
        return result
    lines[current_definition_range[0]] = result
    del lines[current_definition_range[0] + 1:current_definition_range[1] + 1]


def parse(text=None, file=None, debug=0):
    result = parser(text, file)
    print(111, result, flush=True)
    if debug > 0:
        print(result)
    if debug == 0 or debug == 2:
        exec(result, globals(), globals())


def interactive_parse():
    global python_state
    global define_state
    global define_variable
    print('Welcome to mplang')
    while True:
        current = input('> ')
        if current.strip():
            try:
                if python_state:
                    if current.strip() == 'end':
                        current = python_code_parser(define_body, 0, current)
                        python_state = False
                        define_body.clear()
                    else:
                        define_body.append(current)
                        current = ''
                elif define_state:
                    if current.strip() == 'end':
                        if define_state == 'piece':
                            current = define_piece_parser(
                                define_body, 0, define_variable, current)
                        elif define_state == 'drum':
                            current = define_drum_parser(
                                define_body, 0, define_variable, current)
                        elif define_state == 'sampler':
                            current = define_sampler_parser(
                                define_body, 0, define_variable, current)
                        define_state = False
                        define_variable = None
                        define_body.clear()
                    else:
                        define_body.append(current)
                        current = ''
                else:
                    current_split = current.split(' ', 1)
                    current_split_length = len(current_split)
                    if current_split_length == 2:
                        start_token, remain_part = current_split
                        if start_token == 'let':
                            current = make_token_parser(
                                remain_part=remain_part, current=current)
                        elif start_token == 'define':
                            current = define_token_parser(
                                remain_part=remain_part, current=current)
                        else:
                            current = special_token_parser(
                                start_token,
                                remain_part=remain_part,
                                current=current)
                    elif current_split_length == 1:
                        current = single_token_parser(
                            current_split=current_split, current=current)
                exec(current, globals(), globals())
            except Exception as e:
                print(traceback.format_exc())


if __name__ == '__main__':
    argv = sys.argv
    parse_as_text = False
    wait_for_playing = False
    parse_state = 0
    if len(argv) == 1:
        parse_state = 1
        interactive_parse()
    else:
        if '-t' in argv:
            parse_as_text = True
        if '-w' in argv:
            wait_for_playing = True
        for each in argv[1:]:
            if each not in special_argv:
                if parse_as_text:
                    parse(text=each)
                else:
                    parse(file=each)
        if wait_for_playing:
            input('please press enter to continue')
else:
    pass
