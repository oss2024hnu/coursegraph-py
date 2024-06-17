import re
from typing import Union, List
import strictyaml
from strictyaml import EmptyList, Str, Int, Map, Seq, Optional
from strictyaml.exceptions import YAMLValidationError

# 과목명,트랙,마이크로디그리,선수과목에는 문자만 사용되었는지 확인하는 함수
def validate_string_or_sequence(value: Union[str, List[str], int]) -> Union[str, List[str], int]:
    """
    과목명, 트랙, 마이크로디그리, 선수 과목에 문자만 사용되었는지 확인하는 함수입니다.

    parameter:
    value : 과목 하나당 문자열 또는 문자열 리스트

    return:
    값이 유효하다면 value를 반환하고, 그렇지 않다면 ValueError 를 발생시킵니다.
    """
    pattern = r'^[A-Za-z가-힣\w./&]+$'

    if value is None:
        return value

    if isinstance(value, list):
        for item in value:
            if not isinstance(item, str):
                raise ValueError("리스트 내 모든 항목은 문자열이어야 합니다.")
            if not re.match(pattern, item):
                raise ValueError(f"'{item}'는 올바른 형식이 아닙니다.")
    elif isinstance(value, str):
        if not re.match(pattern, value):
            raise ValueError(f"'{value}'는 올바른 형식이 아닙니다.")
    else:
        raise ValueError("올바른 형식이 아닙니다.")

    return value

def validate_field(subject, field_name):
    if field_name in subject:
        validate_string_or_sequence(subject[field_name])

def handle_validation(subject, field_name):
    try:
        validate_field(subject, field_name)
    except ValueError as e:
        raise ValueError(f"과목 '{subject['과목명']}'의 '{field_name}'에 유효하지 않은 값이 있습니다.") from e

def validate_grade(grade):
    if grade not in [1, 2, 3, 4, 5, 6]:
        raise ValueError("학년은 1부터 6까지의 정수여야 합니다.")

# 우선적으로 (학년, 학기, 과목명, 실습여부, 트랙, 마이크로디그리, 선수과목, 구분) 의 스키마를 정의해뒀습니다.
schema = strictyaml.Map({
    "과목": strictyaml.Seq(strictyaml.Map({
        "학년": strictyaml.Int(),
        "학기": strictyaml.Int(),
        "과목명": strictyaml.Str(),
        strictyaml.Optional("트랙"): EmptyList() | strictyaml.Seq(strictyaml.Str()),
        strictyaml.Optional("마이크로디그리"): EmptyList() | strictyaml.Seq(strictyaml.Str()),
        strictyaml.Optional("선수과목"): EmptyList() | strictyaml.Seq(strictyaml.Str()),
        "실습여부": strictyaml.Str(),
        "구분": strictyaml.Str()
    }))
})

def validate_yaml(file_path):
    """
    데이터가 들어있는 yaml 파일의 유효성을 검사합니다. validate_string_or_sequence 함수를 사용합니다.

    Parameter:
    file_path : yaml 파일의 경로

    return:
    반환값은 없습니다. 하지만 유효하지 않다면, ValueError 를 출력합니다.
    """
    try:
        with open(file_path, 'r', encoding='UTF8') as file:
            yaml_content = file.read()
            data = strictyaml.load(yaml_content, schema)
            for index, subject in enumerate(data["과목"], start=1):
                subject_name = subject["과목명"]
                try:
                    validate_grade(subject["학년"])
                    for field_name in ["과목명", "트랙", "마이크로디그리", "선수과목"]:
                        handle_validation(subject , field_name)
                except ValueError as e:
                    raise ValueError(f"과목 '{subject_name}'의 '{field_name}'에 유효하지 않은 값이 있습니다.") from e
            print("파일이 유효합니다.")
            return "파일이 유효합니다."
    except FileNotFoundError:
        print(f"파일 '{file_path}'을(를) 찾을 수 없습니다. 경로를 확인해 주세요.")
    except strictyaml.YAMLValidationError as e:
        print(f"YAML 오류: {e}")
    except ValueError as e:
        print(f"유효성 검사 오류: {e}")

def main():
    while True:
        file_path = input("파일명을 입력해주세요: ").strip()
        try:
            validate_yaml(file_path)
            break  # 유효성 검사 통과 시 반복문 종료
        except ValueError:
            print("유효하지 않은 값이 있습니다. 다시 시도해주세요.")
            continue  # 유효하지 않은 입력이면 다시 입력 받음

if __name__ == '__main__':
    main()