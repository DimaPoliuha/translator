import os

root_dir = './'
tables_path = root_dir + 'tables/'


def create_tables_dir(program_file_name):
    if not os.path.isdir(tables_path):
        try:
            os.mkdir(tables_path)
        except OSError:
            print("Creation of the directory %s failed" % tables_path)
    program_tables_path = tables_path + program_file_name
    if not os.path.isdir(program_tables_path):
        try:
            os.mkdir(program_tables_path)
        except OSError:
            print("Creation of the directory %s failed" % program_tables_path)
