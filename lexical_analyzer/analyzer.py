import re
import csv

from lexical_analyzer.regex_patterns import regex_patterns
from lexical_analyzer.create_tables_files import create_tables_files, tables_path
from lexical_analyzer.create_tables_dir import create_tables_dir
from lexical_analyzer.tokens_identifiers import tokens_identifiers

announcements_block = True
tokens = []
identifiers = []
constants = []
labels = []


def raise_exception(msg=None):
    """
    Function, that helps to raise exceptions with error message
    :return:
    """
    err = token if token else program[line][i]
    raise Exception('Lexical analyzer exception'
                    '\n\n' + msg +
                    '\nline: ' + str(line) +
                    '\nposition: ' + str(i) +
                    '\ntoken: ' + repr(err))


def add_token(tok, token_type, program_file_name, line):
    """
    Function, that appends new token to tokens array and to 1-4 files (depending on the token)
    :param tok:
    :param token_type:
    :param program_file_name:
    :param line:
    :return:
    """
    global announcements_block
    global tokens
    global identifiers
    global constants
    global labels
    con_exists = False
    tok_count = len(tokens) if len(tokens) else 0
    # check end announcements_block
    if tok == 'begin':
        announcements_block = False

    if tok in tokens_identifiers:
        tokens.append([tok_count, line, tok, '', '', '', tokens_identifiers[tok]])

    elif token_type == 'IDN':
        if announcements_block and tok in identifiers:
            raise_exception('re-announcement of identifier')
        elif not announcements_block and tok not in identifiers:
            raise_exception('use of undeclared identifier')

        # add IDN
        if announcements_block:
            identifiers.append(tok)
            with open(tables_path + program_file_name + '/IDN.csv', 'a', newline='') as file_identifiers:
                csv.writer(file_identifiers).writerow([len(identifiers) - 1, identifiers[-1]])
        tokens.append([tok_count, line, tok, identifiers.index(tok), '', '', tokens_identifiers[token_type]])

    elif token_type == 'CON':
        con_id = len(constants) if constants else 0
        for const in constants:
            if tok in const.keys():
                con_id = constants.index(const)
                con_exists = True
                break
        # add CON
        if not con_exists:
            # define const type
            con_type = 'float' if '.' in tok else 'int'
            constants.append({tok: con_type})
            with open(tables_path + program_file_name + '/CONST.csv', 'a', newline='') as file_constants:
                csv.writer(file_constants).writerow([len(constants) - 1, tok, con_type])
        tokens.append([tok_count, line, tok, '', con_id, '', tokens_identifiers[token_type]])

    elif token_type == 'LAB':
        # add LAB
        if tok not in labels:
            labels.append(tok)
            with open(tables_path + program_file_name + '/LAB.csv', 'a', newline='') as file_labels:
                csv.writer(file_labels).writerow([len(labels) - 1, labels[-1]])
        tokens.append([tok_count, line, tok, '', '', labels.index(tok), tokens_identifiers[token_type]])

    # write token to file
    with open(tables_path + program_file_name + '/tokens.csv', 'a', newline='') as f:
        csv.writer(f).writerow(tokens[tok_count])


def generate_tokens(program_file_path):
    """
    Function, that separates tokens from input file
    :param program_file_path:
    :return:
    """

    global announcements_block
    global tokens
    global identifiers
    global constants
    global labels
    announcements_block = True
    tokens = []
    identifiers = []
    constants = []
    labels = []

    global program
    # read program text from file
    with open(program_file_path, 'r') as f:
        program = [row.strip(' ') for row in f]

    program_file_name = program_file_path.split('/')[-1]
    create_tables_dir(program_file_name)
    create_tables_files(program_file_name)

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
        # if we reached EOF
        if line >= len(program):
            if token == '':
                break

        # if we reached EOL or blank line
        while len(program[line]) == 0 or i >= len(program[line]):
            i = 0
            line += 1
            # if we reached EOF
            if line >= len(program):
                break

        # if we reached EOF
        if line >= len(program):
            if token == '':
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

        char = program[line][i] if line < len(program) else ''

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
            elif re.match(regex_patterns['white_separator'], char) and i < len(program[line]):
                while re.match(regex_patterns['white_separator'], program[line][i]) and i < len(program[line]):
                    i += 1
                    if i >= len(program[line]):
                        break
            else:
                state = 1
                has_to_read = True
                raise_exception()

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
                raise_exception()

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
                raise_exception()

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
                raise_exception()
    return tokens
