import os
import argparse
import sys

def main():
    try:
        # 현재 스크립트가 실행되는 디렉터리의 경로를 가져옴
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(current_dir, 'data')  # data 디렉터리 경로
        coursegraph_script = os.path.join(current_dir, 'coursegraph')  # coursegraph 스크립트 경로

        parser = argparse.ArgumentParser(
            description='__main__.py test',
            epilog='test and delete'
        )

        parser.add_argument('-t', '--test', action='store_true', help='test __main__.py')
        parser.add_argument('-d', '--delete', action='store_true', help='delete png file')
        args = parser.parse_args()

        test_main = args.test
        delete_png = args.delete

        if test_main:
            os.system(f'python {coursegraph_script} -f graph -i {os.path.join(data_dir, "input.yaml")} -o {os.path.join(current_dir, "input_graph.png")}')
            os.system(f'python {coursegraph_script} -f table -i {os.path.join(data_dir, "input.yaml")} -o {os.path.join(current_dir, "input_table.png")}')
            os.system(f'python {coursegraph_script} -f graph -i {os.path.join(data_dir, "ce.yaml")} -o {os.path.join(current_dir, "ce_graph.png")}')
            os.system(f'python {coursegraph_script} -f table -i {os.path.join(data_dir, "ce.yaml")} -o {os.path.join(current_dir, "ce_table.png")}')
            os.system(f'python {coursegraph_script} -f graph -i {os.path.join(data_dir, "me.yaml")} -o {os.path.join(current_dir, "me_graph.png")}')
            os.system(f'python {coursegraph_script} -f table -i {os.path.join(data_dir, "me.yaml")} -o {os.path.join(current_dir, "me_table.png")}')
            os.system(f'python {coursegraph_script} -f graph -i {os.path.join(data_dir, "ai.yaml")} -o {os.path.join(current_dir, "ai_graph.png")}')
            os.system(f'python {coursegraph_script} -f table -i {os.path.join(data_dir, "ai.yaml")} -o {os.path.join(current_dir, "ai_table.png")}')

        if delete_png:
          os.system(f'del /Q {os.path.join(current_dir, "*.png")}')


    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
