import argparse
import fontutil
import tkinter as tk
from tkinter import filedialog

def open_select_yaml():
    root = tk.Tk()
    root.withdraw()

    select_yaml = filedialog.askopenfilename(initialdir="../data", title="Select file", filetypes=(("YAML files", "*.yaml"), ("all files", "*.*")))
    return select_yaml

def main():
    parser = argparse.ArgumentParser(
        description='A CLI utility for processing data.',
        epilog='Enjoy using the CLI utility!'
    )

    # Adding command line options
    parser.add_argument('-i', '--input', type=str, help='Specify the input file path.')
    parser.add_argument('-o', '--output', type=str, help='Specify the output file path.')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose mode.')

    args = parser.parse_args()

    # Accessing the command line options
    input_file = args.input
    output_file = args.output
    verbose_mode = args.verbose

    # Perform actions based on options
    if verbose_mode:
        print("Verbose mode enabled.")

    if output_file:
        print(f"Output file path: {output_file}")

    if input_file:
        print(f"input file path: {input_file}")

    # Add more functionality based on your application needs


if __name__ == '__main__':
    main()
