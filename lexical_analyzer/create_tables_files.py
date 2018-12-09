root_dir = './'
tables_path = root_dir + 'tables/'


def create_tables_files(program_file_name):
    """
    Function, that creates (or makes blank) four files in directory ./tables/<input_file_name>
    for lexical analyzer tables for every input file
    :param program_file_name:
    :return:
    """
    with open(tables_path + program_file_name + '/tokens.csv', 'w', newline=''):
        pass
    with open(tables_path + program_file_name + '/IDN.csv', 'w', newline=''):
        pass
    with open(tables_path + program_file_name + '/CONST.csv', 'w', newline=''):
        pass
    with open(tables_path + program_file_name + '/LAB.csv', 'w', newline=''):
        pass
