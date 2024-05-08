import argparse
import tkinter as tk
from tkinter import filedialog
import sys
from show_yaml import ShowYaml
import fontutil




def main():
  try:

    parser = argparse.ArgumentParser(
        description='A CLI utility for processing data.',
        epilog='Enjoy using the CLI utility!'
    )

    # Adding command line options
    parser.add_argument('-i', '--input', type=str, help='Specify the input file path.')
    parser.add_argument('-o', '--output', type=str, help='Specify the output file path.')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose mode.')
    parser.add_argument('-s', '--show', action='store_true', help='Show data.')
    parser.add_argument('-u', '--update', action='store_true', help='update.')
    parser.add_argument('-img', '--image', action='store_true', help='Show data and Create image')
    args = parser.parse_args()

    # Accessing the command line options
    input_file = args.input
    output_file = args.output
    verbose_mode = args.verbose
    show_data = args.show
    image_mode = args.image



    # Perform actions based on options
    if verbose_mode:
        print("Verbose mode enabled.")

    if output_file:
        print("Specify the output file path.")

    if input_file:
        print('Specify the input file path.')
    
    if show_data:
        data_processor = ShowYaml(image_mode)
        data_processor.process_data2()
    

  except Exception as e:
      print(f"An error occurred: {e}")
      sys.exit(1)


      
    # Add more functionality based on your application needs

if __name__ == '__main__':
    main()
