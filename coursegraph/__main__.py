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
        parser.add_argument('-i', '--input', type=str, help='Specify the input YAML data file path. (required)')
        parser.add_argument('-o', '--output', type=str, help='Specify the output image file path. (optional).')
        parser.add_argument('-f', '--format', choices=['graph', 'table'], default='graph',
                            help='Sepcify the output format (graph, table). Defaults to graph.')
        args = parser.parse_args()

        # Accessing the command line options
        input_file = args.input
        output_file = args.output
        output_format = args.format
        show_mode = False
        # Perform actions based on options

        if output_file:
            print(f"The output image file path has been specified: {output_file}")
        else:
            show_mode = True

        if input_file:
            print(f"The input YAML file path has been specified: {input_file}")
        else:
            parser.print_help(sys.stderr)
            raise Exception("input file not specified")
        if output_format == 'graph':
            subjects = read_subjects(input_file)
            draw_course_structure(subjects, output_file)
        elif output_format == 'table':
            # kyahnu: 이 부분 --input 과 --output 을 활용하도록 일관된 인터페이스로 수정할 것
            data_processor = ShowTable(not show_mode, input_file, output_file)
            data_processor.process_data()
        else:
            raise Exception(f"cannot handle output format {output_format}")


    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)

    # Add more functionality based on your application needs


if __name__ == '__main__':
    main()
