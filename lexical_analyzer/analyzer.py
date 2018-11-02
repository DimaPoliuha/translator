import re
from lexical_analyzer.regex_patterns import regex_patterns
from lexical_analyzer.create_tables_files import create_tables_files
from lexical_analyzer.create_tables_dir import create_tables_dir
from lexical_analyzer.add_token import add_token

root_dir = './'
tables_path = root_dir + 'tables/'
program_file_name = 'program'


def generate_tokens():
    create_tables_dir(program_file_name)
    create_tables_files(program_file_name)
    # read program text from file
    with open(root_dir + program_file_name + '.txt', 'r') as f:
        program = [row.rstrip() for row in f]

    global has_to_read
    has_to_read = False
    global state
    state = 1
    global i
    i = 0
    global line
    line = 0
    global token
    token = ''
    global char

    while True:
        # if we reached EOL or blank line
        while len(program[line]) == 0 or i >= len(program[line]):
            i = 0
            line += 1
            # if we reached EOF
            if line >= len(program):
                break
        # if we reached EOF
        if line >= len(program):
            break

        # if there's need to start new token when we end previous
        if has_to_read:
            i += 1
            # if we reached EOL or blank line
            while len(program[line]) == 0 or i >= len(program[line]):
                i = 0
                line += 1
                # if we reached EOF
                if line >= len(program):
                    break
            # if we reached EOF
            if line >= len(program):
                break
            token = ''
            has_to_read = False

        char = program[line][i]

        try:
            if state == 1:
                if re.match(regex_patterns['character'], char):
                    token += char
                    state = 2
                    i += 1
                elif re.match(regex_patterns['number_sign'], char):
                    token += char
                    state = 3
                    i += 1
                elif re.match(regex_patterns['digit'], char):
                    token += char
                    state = 5
                    i += 1
                elif re.match(regex_patterns['dot'], char):
                    token += char
                    state = 7
                    i += 1
                elif re.match(regex_patterns['single_separator'], char):
                    token += char
                    add_token(token, 'TOK', program_file_name, line)
                    state = 1
                    has_to_read = True
                elif re.match(regex_patterns['more'], char):
                    token += char
                    state = 8
                    i += 1
                elif re.match(regex_patterns['less'], char):
                    token += char
                    state = 9
                    i += 1
                elif re.match(regex_patterns['equal'], char):
                    token += char
                    state = 10
                    i += 1
                elif re.match(regex_patterns['not_equal'], char):
                    token += char
                    state = 11
                    i += 1
                # if next char is white separator
                elif re.match(regex_patterns['white_separator'], char) and i < len(program[line]) - 1:
                    while re.match(regex_patterns['white_separator'], program[line][i]) and i < len(program[line]) - 1:
                        i += 1
                else:
                    state = 1
                    has_to_read = True
                    raise Exception

            elif state == 2:
                if re.match(regex_patterns['identifier'], char) or re.match(regex_patterns['digit'], char):
                    token += char
                    i += 1
                else:
                    add_token(token, 'IDN', program_file_name, line)
                    state = 1
                    token = ''

            elif state == 3:
                if re.match(regex_patterns['identifier'], char):
                    token += char
                    i += 1
                    state = 4
                else:
                    state = 1
                    has_to_read = True
                    raise Exception

            elif state == 4:
                if re.match(regex_patterns['identifier'], char):
                    token += char
                    i += 1
                else:
                    add_token(token, 'LAB', program_file_name, line)
                    state = 1
                    token = ''

            elif state == 5:
                if re.match(regex_patterns['digit'], char):
                    token += char
                    i += 1
                elif re.match(regex_patterns['dot'], char):
                    token += char
                    i += 1
                    state = 6
                else:
                    add_token(token, 'CON', program_file_name, line)
                    state = 1
                    token = ''

            elif state == 6:
                if re.match(regex_patterns['digit'], char):
                    token += char
                    i += 1
                else:
                    add_token(token, 'CON', program_file_name, line)
                    state = 1
                    token = ''

            elif state == 7:
                if re.match(regex_patterns['digit'], char):
                    token += char
                    i += 1
                    state = 6
                else:
                    state = 1
                    has_to_read = True
                    raise Exception

            elif state == 8:
                if re.match(regex_patterns['more'], char):
                    token += char
                    i += 1
                    add_token(token, 'TOK', program_file_name, line)
                    state = 1
                    token = ''
                elif re.match(regex_patterns['equal'], char):
                    token += char
                    add_token(token, 'TOK', program_file_name, line)
                    state = 1
                    has_to_read = True
                else:
                    add_token(token, 'TOK', program_file_name, line)
                    state = 1
                    token = ''

            elif state == 9:
                if re.match(regex_patterns['less'], char):
                    token += char
                    i += 1
                    add_token(token, 'TOK', program_file_name, line)
                    state = 1
                    token = ''
                elif re.match(regex_patterns['equal'], char):
                    token += char
                    add_token(token, 'TOK', program_file_name, line)
                    state = 1
                    has_to_read = True
                else:
                    add_token(token, 'TOK', program_file_name, line)
                    state = 1
                    token = ''

            elif state == 10:
                if re.match(regex_patterns['equal'], char):
                    token += char
                    add_token(token, 'TOK', program_file_name, line)
                    state = 1
                    has_to_read = True
                else:
                    add_token(token, 'TOK', program_file_name, line)
                    state = 1
                    token = ''

            elif state == 11:
                if re.match(regex_patterns['equal'], char):
                    token += char
                    add_token(token, 'TOK', program_file_name, line)
                    state = 1
                    has_to_read = True
                else:
                    state = 1
                    has_to_read = True
                    raise Exception

        except Exception as err_type:
            err = token if token else program[line][i]
            print('Lexical analyzer exception\n' +
                  str(err_type) +
                  '\nline: ' + str(line) +
                  '\ntoken: ' + err + '\n')
            break
