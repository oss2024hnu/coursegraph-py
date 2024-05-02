import argparse
import fontutil
import os
import sys
from matplotlib import font_manager, rc

current_dir = os.path.dirname(os.path.abspath(__file__))
show_yaml_path = os.path.join(current_dir, "show_yaml.py")
sys.path.append(current_dir)

from show_yaml import input_filename, read_subjects, get_system_font, make_data

def main():
    parser = argparse.ArgumentParser(
        description='A CLI utility for processing data.',
        epilog='Enjoy using the CLI utility!'
    )

    # Adding command line options
    parser.add_argument('-i', '--input', type=str, help='Specify the input file path.')
    parser.add_argument('-o', '--output', type=str, help='Specify the output file path.')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose mode.')
    parser.add_argument('-s', '--show', action='store_true', help='Show data.')
    args = parser.parse_args()

    # Accessing the command line options
    input_file = args.input
    output_file = args.output
    verbose_mode = args.verbose
    show_data = args.show

    # Perform actions based on options
    if verbose_mode:
        print("Verbose mode enabled.")

    if output_file:
        print(f"Output file path: {output_file}")

    if input_file:
        print(f"Output file path: {output_file}")
    
    if show_data:
        filename = input_filename()
        if filename:
            subjects = read_subjects(filename)
            get_system_font()
            if subjects:
                make_data(subjects)
            else:
                print("Data is empty")
        else:
            print("Flie not found")
    # Add more functionality based on your application needs


if __name__ == '__main__':
    main()
