import argparse
import sys

import fontutil
from show_table import ShowTable
from show_graph import read_subjects, draw_course_structure

def main():
  try:

    parser = argparse.ArgumentParser(
        description='A CLI utility for processing data.',
        epilog='Enjoy using the CLI utility!'
    )

    # Adding command line options
    parser.add_argument('-i', '--input', type=str, help='Specify the input YAML data file path.')
    parser.add_argument('-o', '--output', type=str, help='Specify the output image file path.')
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
        print("Specify the output file path.")

    if input_file:
        print('Specify the input file path.')
    
    # kyahnu: 이 부분 --input 과 --output 을 활용하도록 일관된 인터페이스로 수정할 것
    if show_data:
        image_mode = True if output_file else False
        data_processor = ShowTable(image_mode)
        data_processor.process_data()
    

  except Exception as e:
      print(file=sys.stderr, f"An error occurred: {e}",)
      sys.exit(1)


      
    # Add more functionality based on your application needs

if __name__ == '__main__':
    main()
