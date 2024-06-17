import argparse
import sys
import logging

import fontutil
from show_table import ShowTable
from show_graph import read_subjects, draw_course_structure, cliprint
from show_dot import print_dot



def verbose_info(level , width , height , input_file , output_file) :
    if level == 0 : 
        logging.warning('Verbose level 0')
    elif level == 1 :
        logging.info('Verbose level 1 : Summary Information')
        print('width * height :', width, '*', height)
        print(f"The input YAML file path has been specified: {input_file}")
        print(f"The output image file path has been specified: {output_file}") 
    elif level == 2 : 
         logging.debug('Verbose level 2 : Detailed Developer Information')
         print('width * height :', width, '*', height)
         print(f"The input YAML file path has been specified: {input_file}")
         print(f"The output image file path has been specified: {output_file}")



def main():
    
    try:

        parser = argparse.ArgumentParser(
            description='A CLI utility for processing data.',
            epilog='Enjoy using the CLI utility!'
        )

        # Adding command line options
        parser.add_argument('input', type=str, help='Specify the input YAML data file path. (required)')
        parser.add_argument('-o', '--output', type=str, help='Specify the output image file path. (optional).')
        parser.add_argument('-f', '--format', choices=['graph', 'dot', 'table'], default='graph',
                            help='Specify the output format (graph, table). Defaults to graph.')
        parser.add_argument('-s', '--size', type=str, help='Specify the size of the output image in format WIDTH,HEIGHT. Example: -s 20,10', default='20,10')
        parser.add_argument('-v', '--verbose', type=int, choices = [0, 1, 2],
                            default = 0, 
                            help = 'Set the verbose level (optional)\n'
                            '0 - Minium output, option for end user\n'
                            '1 - Standard output, informational message\n'
                            '2 - Debug output, detailed information')
        args = parser.parse_args()

        # Accessing the command line options
        input_file = args.input
        output_file = args.output
        output_format = args.format
        show_mode = False
        # Perform actions based on options

        if args.size:
            try:
                width, height = map(int, args.size.split(','))
                if width <= 0 or height <= 0:
                    raise ValueError
            except ValueError:
                parser.error("Size must be in the format WIDTH,HEIGHT with positive integer values. Example: -s 20,10")
        else:
            width, height = 20, 10

        if not input_file :
            parser.print_help(sys.stderr)
            raise Exception("input file not specified")

        if not output_file : 
            show_mode = True
        
        logging.basicConfig(level = logging.WARNING)

        if args.verbose == 1: # 요약된 정보 출력
            logging.getLogger().setLevel(logging.INFO)
        elif args.verbose == 2: # 상세 정보 출력
            logging.getLogger().setLevel(logging.DEBUG)
        
        verbose_info(args.verbose , width , height , input_file , output_file)
        
        if output_format == 'graph':
            subjects = read_subjects(input_file)
            ref = draw_course_structure(subjects, output_file, width, height)
            if args.verbose == 2:
                cliprint(ref)
        elif output_format == 'dot':
            subjects = read_subjects(input_file)
            print_dot(subjects, output_file)
        
            
            # raise Exception(f"cannot handle output format {output_format}") # 아직 dot 파일 형식에 대한 내용 없음
        elif output_format in ['table', 'pdf']:
            data_processor = ShowTable(not show_mode, input_file, output_file, width, height)
            data_processor.process_data()
        else:
            raise Exception(f"cannot handle output format {output_format}")


    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)

    # Add more functionality based on your application needs


if __name__ == '__main__':
    main()
