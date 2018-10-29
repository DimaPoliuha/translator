import csv
from lexical_analyzer.tokens_identifiers import tokens_identifiers

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

    # write token to file
    with open(tables_path + program_file_name + '/tokens.csv', 'a', newline='') as f:
        writer = csv.writer(f)

        if tok in tokens_identifiers:
            writer.writerow([token_count, line, tok, '', '', '', tokens_identifiers[tok]])

        elif token_type == 'IDN':
            # read IDNs from file
            with open(tables_path + program_file_name + '/IDN.csv', 'r', newline='') as file_identifiers:
                reader = csv.reader(file_identifiers, delimiter=',')
                idns = []
                for row in reader:
                    # skip first line
                    if row[0] == 'Id':
                        continue
                    idns.append(row[1])
            if announcements_block and tok in idns:
                raise Exception('Re-announcement')
            elif not announcements_block and tok not in idns:
                raise Exception('Use of undeclared identifier')

            idn_id = idns.index(tok) if tok in idns else idn_count
            # write to IDN file
            if announcements_block:
                with open(tables_path + program_file_name + '/IDN.csv', 'a', newline='') as file_identifiers:
                    writer_identifiers = csv.writer(file_identifiers)
                    # TODO add type and value in fields
                    writer_identifiers.writerow([idn_count, tok, '', ''])
                idn_count += 1

            # write to tokens file
            writer.writerow([token_count, line, tok, idn_id, '', '', 100])

        elif token_type == 'CON':
            # read CONs from file
            with open(tables_path + program_file_name + '/CONST.csv', 'r', newline='') as file_constants:
                reader = csv.reader(file_constants, delimiter=',')
                cons = []
                for row in reader:
                    # skip first line
                    if row[0] == 'Id':
                        continue
                    cons.append(row[1])

            con_id = cons.index(tok) if tok in cons else con_count
            # write to CONST file
            if tok not in cons:
                # define const type
                con_type = 'float' if '.' in tok else 'int'
                with open(tables_path + program_file_name + '/CONST.csv', 'a', newline='') as file_constants:
                    writer_constants = csv.writer(file_constants)
                    writer_constants.writerow([con_count, tok, con_type])
                con_count += 1
            # write to tokens file
            writer.writerow([token_count, line, tok, '', con_id, '', 101])

        elif token_type == 'LAB':
            # read LABs from file
            with open(tables_path + program_file_name + '/LAB.csv', 'r', newline='') as file_labels:
                reader = csv.reader(file_labels, delimiter=',')
                labs = []
                for row in reader:
                    # skip first line
                    if row[0] == 'Id':
                        continue
                    labs.append(row[1])

            lab_id = labs.index(tok) if tok in labs else lab_count

            # write to LAB file
            if tok not in labs:
                with open(tables_path + program_file_name + '/LAB.csv', 'a', newline='') as file_labels:
                    writer_labels = csv.writer(file_labels)
                    writer_labels.writerow([lab_count, tok])
                lab_count += 1
            # write to tokens file
            writer.writerow([token_count, line, tok, '', '', lab_id, 102])
        # else:
        #     writer.writerow([token_count, line, tok, '', '', '', 'id'])

        token_count += 1
