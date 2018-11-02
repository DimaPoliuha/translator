import csv
from lexical_analyzer.tokens_identifiers import tokens_identifiers

root_dir = './'
tables_path = root_dir + 'tables/'
announcements_block = True
tokens = []
identifiers = []
constants = []
labels = []


def add_token(tok, token_type, program_file_name, line):
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
            raise Exception('Re-announcement')
        elif not announcements_block and tok not in identifiers:
            raise Exception('Use of undeclared identifier')
        if announcements_block:
            identifiers.append(tok)
        tokens.append([tok_count, line, tok, identifiers.index(tok), '', '', tokens_identifiers[token_type]])

    elif token_type == 'CON':
        con_id = len(constants) if constants else 0
        for i in range(len(constants)):
            if tok in constants[i].keys():
                con_id = i
        for con in constants:
            if tok in con.keys():
                con_exists = True
                break
        if not con_exists:
            # define const type
            con_type = 'float' if '.' in tok else 'int'
            constants.append({tok: con_type})
        tokens.append([tok_count, line, tok, '', con_id, '', tokens_identifiers[token_type]])

    elif token_type == 'LAB':
        if tok not in labels:
            labels.append(tok)
        tokens.append([tok_count, line, tok, '', '', labels.index(tok), tokens_identifiers[token_type]])

    # write token to file
    with open(tables_path + program_file_name + '/tokens.csv', 'a', newline='') as f:
        csv.writer(f).writerow(tokens[tok_count])
