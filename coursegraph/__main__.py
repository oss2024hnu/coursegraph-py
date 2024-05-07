
import tkinter as tk
from tkinter import filedialog
import sys
from show_yaml import ShowYaml
import fontutil
from tkinter import filedialog
from parsing import parse_arguments

from save_file import Save_file

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
    update_file = args.update


    # Perform actions based on options
    if verbose_mode:
        print("Verbose mode enabled.")

    if output_file:
        data_processor = Save_file()
        data_processor.output_process(output_file)

    if input_file:
        data_processor = Save_file()
        data_processor.input_process(input_file)
    
    if show_data:
        data_processor = ShowYaml()
        data_processor.process_data()
    if update_file:
        data_processor = Save_file()
        data_processor.choice_file()
      
    # Add more functionality based on your application needs

if __name__ == '__main__':
    main()