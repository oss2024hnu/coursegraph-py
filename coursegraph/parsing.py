import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(
        description='A CLI utility for processing data.',
        epilog='Enjoy using the CLI utility!'
    )

    # Adding command line options
    parser.add_argument('-i', '--input', type=str, help='Specify the input file path.')
    parser.add_argument('-o', '--output', type=str, help='Specify the output file path.')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose mode.')
    parser.add_argument('-s', '--show', action='store_true', help='Show data.')
    return parser.parse_args()