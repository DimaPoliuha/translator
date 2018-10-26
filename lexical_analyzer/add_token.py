import csv

root_dir = './'
tables_path = root_dir + 'tables/'
announcements_block = True
token_count = 0
idn_count = 0
con_count = 0
lab_count = 0


def add_token(tok, token_type, program_file_name, line):
    global announcements_block
    global token_count
    global idn_count
    global con_count
    global lab_count
    # check end announcements_block
    if tok == 'begin':
        announcements_block = False

    with open(tables_path + program_file_name + '/tokens.csv', 'a', newline='') as f:
        writer = csv.writer(f)

        if token_type == 'IDN':
            writer.writerow([token_count, line, tok, 'id', '', '', 100])
            # write to IDN file
            with open(tables_path + program_file_name + '/IDN.csv', 'a', newline='') as file_identifiers:
                writer_identifiers = csv.writer(file_identifiers)
                writer_identifiers.writerow([idn_count, tok, 'type', 'value'])
            idn_count += 1

        elif token_type == 'CON':
            writer.writerow([token_count, line, tok, '', 'id', '', 101])
            # write to CONST file
            with open(tables_path + program_file_name + '/CONST.csv', 'a', newline='') as file_constants:
                writer_constants = csv.writer(file_constants)
                writer_constants.writerow([con_count, tok, 'type'])
            con_count += 1

        elif token_type == 'LAB':
            writer.writerow([token_count, line, tok, '', '', 'id', 102])
            # write to LAB file
            with open(tables_path + program_file_name + '/LAB.csv', 'a', newline='') as file_labels:
                writer_labels = csv.writer(file_labels)
                writer_labels.writerow([lab_count, tok])
            lab_count += 1
        else:
            writer.writerow([token_count, line, tok, '', '', '', 'id'])

        token_count += 1
