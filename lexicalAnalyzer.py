import re
import csv

program_file_name = 'program'
# program_file_name = input('Input name of program file: ')

announcements_block = True

white_separator = r"^\s{1}$"
characters = r"^[A-Za-z]{1}$"
identifier = r"^\w{1}$"
digits = r"^\d{1}$"
single_separator = r"^[,;:()\-+*\/]{1}$"
dot = r"^[.]{1}$"
more = r"^[>]{1}$"
less = r"^[<]{1}$"
equal = r"^[=]{1}$"
not_equal = r"^[!]{1}$"
label = r"^[#]{1}$"

tokens_id = {
    'int': 1,
    'float': 2,
    'begin': 3,
    'end': 4,
    'goto': 5,
    'cin': 6,
    'cout': 7,
    'for': 8,
    'by': 9,
    'to': 10,
    'do': 11,
    'rof': 12,
    'if': 13,
    'then': 14,
    'fi': 15,
    ';': 16,
    ':': 17,
    ',': 18,
    '=': 19,
    '>>': 20,
    '<<': 21,
    '>': 22,
    '<': 23,
    '>=': 24,
    '<=': 25,
    '==': 26,
    '!=': 27,
    '+': 28,
    '-': 29,
    '*': 30,
    '/': 31,
    '(': 32,
    ')': 33,
    'IDN': 100,
    'CON': 101,
    'LAB': 102,
}


def add_token(tok, token_type):
    global announcements_block
    if token == 'begin':
        announcements_block = False

    with open(program_file_name + '_tokens.csv', 'a', newline='') as f:
        writer = csv.writer(f)

        if token_type == 'IDN':
            writer.writerow([tokens_count, line, tok, 'id', '', '', 100])
            with open(program_file_name + '_IDN.csv', 'a', newline='') as file_identifiers:
                writer_identifiers = csv.writer(file_identifiers)
                writer_identifiers.writerow([idn_count, tok, 'type', 'value'])
        elif token_type == 'CON':
            writer.writerow([tokens_count, line, tok, '', 'id', '', 101])
            with open(program_file_name + '_CON.csv', 'a', newline='') as file_constants:
                writer_constants = csv.writer(file_constants)
                writer_constants.writerow([con_count, tok, 'type'])
        elif token_type == 'LAB':
            writer.writerow([tokens_count, line, tok, '', '', 'id', 102])
            with open(program_file_name + '_LAB.csv', 'a', newline='') as file_labels:
                writer_labels = csv.writer(file_labels)
                writer_labels.writerow([lab_count, tok])
        else:
            writer.writerow([tokens_count, line, tok, '', '', '', 'id'])


def lexical_analyzer():
    # file to read program
    with open(program_file_name + '.txt', 'r') as f:
        program = [row.strip() for row in f]
    # file to write tokens
    with open(program_file_name + '_tokens.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Token number', 'Line number', 'Token', 'IDN id', 'CON id', 'LAB id', 'TOK id'])
    # file to write identifiers
    with open(program_file_name + '_IDN.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Id', 'Name', 'Value', 'Type'])
    # file to write constants
    with open(program_file_name + '_CON.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Id', 'Value', 'Type'])
    # file to write labels
    with open(program_file_name + '_LAB.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Id', 'Name'])

    global hasToRead
    hasToRead = False
    global state
    state = 1
    global i
    i = 0
    global line
    line = 0
    global token
    token = ''
    global char

    global tokens_count
    tokens_count = 0
    global con_count
    con_count = 0
    global idn_count
    idn_count = 0
    global lab_count
    lab_count = 0

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
        if hasToRead:
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
            # # if next char is white separator
            # while re.match(white_separator, program[line][i]) and i < len(program[line]) - 1:
            #     i += 1
            #     # if we reached EOL
            #     if len(program[line]) == 0 or i >= len(program[line]):
            #         i = 0
            #         line += 1

            token = ''
            hasToRead = False

        char = program[line][i]

        try:
            if state == 1:
                if re.match(characters, char):
                    token += char
                    state = 2
                    i += 1

                elif re.match(label, char):
                    token += char
                    state = 3
                    i += 1

                elif re.match(digits, char):
                    token += char
                    state = 5
                    i += 1

                elif re.match(dot, char):
                    token += char
                    state = 7
                    i += 1

                elif re.match(single_separator, char):
                    token += char
                    add_token(token, 'TOK')
                    tokens_count += 1
                    state = 1
                    hasToRead = True

                elif re.match(more, char):
                    token += char
                    state = 8
                    i += 1

                elif re.match(less, char):
                    token += char
                    state = 9
                    i += 1

                elif re.match(equal, char):
                    token += char
                    state = 10
                    i += 1

                elif re.match(not_equal, char):
                    token += char
                    state = 11
                    i += 1

                # if next char is white separator
                elif re.match(white_separator, char) and i < len(program[line]) - 1:
                    while re.match(white_separator, program[line][i]) and i < len(program[line]) - 1:
                        i += 1

                else:
                    state = 1
                    hasToRead = True
                    raise SyntaxError

            elif state == 2:
                if re.match(identifier, char) or re.match(digits, char):
                    token += char
                    i += 1
                else:
                    add_token(token, 'IDN')
                    idn_count += 1
                    tokens_count += 1
                    state = 1
                    token = ''

            elif state == 3:
                if re.match(identifier, char):
                    token += char
                    i += 1
                    state = 4
                else:
                    state = 1
                    hasToRead = True
                    raise SyntaxError

            elif state == 4:
                if re.match(identifier, char):
                    token += char
                    i += 1
                else:
                    add_token(token, 'LAB')
                    lab_count += 1
                    tokens_count += 1
                    state = 1
                    token = ''

            elif state == 5:
                if re.match(digits, char):
                    token += char
                    i += 1
                elif re.match(dot, char):
                    token += char
                    i += 1
                    state = 6
                else:
                    add_token(token, 'CON')
                    con_count += 1
                    tokens_count += 1
                    state = 1
                    token = ''

            elif state == 6:
                if re.match(digits, char):
                    token += char
                    i += 1
                else:
                    add_token(token, 'CON')
                    con_count += 1
                    tokens_count += 1
                    state = 1
                    token = ''

            elif state == 7:
                if re.match(digits, char):
                    token += char
                    i += 1
                    state = 6
                else:
                    state = 1
                    hasToRead = True
                    raise SyntaxError

            elif state == 8:
                if re.match(more, char):
                    token += char
                    i += 1
                    add_token(token, 'TOK')
                    tokens_count += 1
                    state = 1
                    token = ''
                elif re.match(equal, char):
                    token += char
                    add_token(token, 'TOK')
                    tokens_count += 1
                    state = 1

                    hasToRead = True
                else:
                    add_token(token, 'TOK')
                    tokens_count += 1
                    state = 1
                    token = ''

            elif state == 9:
                if re.match(less, char):
                    token += char
                    i += 1
                    add_token(token, 'TOK')
                    tokens_count += 1
                    state = 1
                    token = ''
                elif re.match(equal, char):
                    token += char
                    add_token(token, 'TOK')
                    tokens_count += 1
                    state = 1

                    hasToRead = True
                else:
                    add_token(token, 'TOK')
                    tokens_count += 1
                    state = 1
                    token = ''

            elif state == 10:
                if re.match(equal, char):
                    token += char
                    add_token(token, 'TOK')
                    tokens_count += 1
                    state = 1

                    hasToRead = True
                else:
                    add_token(token, 'TOK')
                    tokens_count += 1
                    state = 1
                    token = ''

            elif state == 11:
                if re.match(equal, char):
                    token += char
                    add_token(token, 'TOK')
                    tokens_count += 1
                    state = 1

                    hasToRead = True
                else:
                    state = 1
                    hasToRead = True
                    raise SyntaxError

        except SyntaxError:
            err = token if token else program[line][i]
            print('SyntaxError\n'
                  'line = ' + str(line) + '\n'
                                          'token: ' + err + '\n')


lexical_analyzer()
