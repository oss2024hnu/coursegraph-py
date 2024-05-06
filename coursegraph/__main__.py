import argparse
import tkinter as tk
from tkinter import filedialog
import sys
from show_yaml import ShowYaml
import fontutil
from tkinter import filedialog
from parsing import parse_arguments

def open_select_yaml():
    root = tk.Tk()
    root.withdraw()

    select_yaml = filedialog.askopenfilename(initialdir="../data", title="Select file", filetypes=(("YAML files", "*.yaml"), ("all files", "*.*")))
    return select_yaml

def main():
    args = parse_arguments()

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
        print(f"Output file path: {input_file}")
    
    if show_data:
        data_processor = ShowYaml()
        data_processor.process_data()
      
    # Add more functionality based on your application needs

if __name__ == '__main__':
    main()
