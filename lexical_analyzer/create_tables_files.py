import csv


def create_tables_files(program_file_name, tables_path):
    # file to write tokens
    with open(tables_path + program_file_name + '/tokens.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Token number', 'Line number', 'Token', 'IDN id', 'CON id', 'LAB id', 'TOK id'])
    # file to write identifiers
    with open(tables_path + program_file_name + '/IDN.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Id', 'Name', 'Value', 'Type'])
    # file to write constants
    with open(tables_path + program_file_name + '/CONST.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Id', 'Value', 'Type'])
    # file to write labels
    with open(tables_path + program_file_name + '/LAB.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Id', 'Name'])
