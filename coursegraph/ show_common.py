import sys
import os
import strictyaml as syaml
from fontutil import get_system_font

def get_script_dir():
    return os.path.dirname(os.path.abspath(__file__))

def read_yaml(filename):
    script_dir = get_script_dir()
    try:
        with open(os.path.join(script_dir, filename), 'r', encoding='UTF8') as file:
            yaml_data = file.read()
            data = syaml.load(yaml_data).data
            return data
    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.", file=sys.stderr)
        return None
    except Exception as e:
        print(f"파일을 읽는 중 오류가 발생했습니다: {e}", file=sys.stderr)
        return None

def get_system_font():
    try:
        return get_system_font()[1]['file']
    except:
        try:
            return get_system_font()[0]['file']
        except:
            try:
                return get_system_font()[2]['file']
            except:
                print("시스템내에 적합한 한글 폰트 파일을 찾을 수 없습니다.", file=sys.stderr)
                sys.exit(2)

if __name__ == "__main__":
    script_dir = get_script_dir()
