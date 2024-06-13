import re
import sys
import strictyaml
from strictyaml import EmptyList


# 과목명,트랙,마이크로디그리,선수과목에는 문자만 사용되었는지 확인하는 함수
def validate_string_or_sequence(value : str) -> str:
    """
    과목명, 트랙, 마이크로디그리, 선수 과목에 문자만 사용되었는지 확인하는 함수입니다.

    parameter:
    value(str) : 과목 하나당 문자열

    return:
    값이 유효하다면 value를 반환학고, 그렇지 않다면 ValueError 를 발생시킵니다.
    """
    if value is None or value ==  None:
        value
        return value
    elif isinstance(value, list):
        for item in value:  # 리스트 내 각 항목을 확인
            if not isinstance(item, str):
                raise ValueError("올바른 형식이 아닙니다.")
            if not re.match(r'^[A-Za-z가-힣\w./&]+$', item):
                raise ValueError("올바른 형식이 아닙니다.")
        return value
    elif isinstance(value, str):
        if re.match(r'^[A-Za-z가-힣\w./&]+$', value):
            return value
        else:
            raise ValueError("올바른 형식이 아닙니다.")
    
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


def validate_yaml(file_path : str):
    """
    데이터가 들어있는 yaml 파일의 유효성을 검사합니다. validate_string_or_sequence 함수를 사용합니다.

    Parameter:
    file_path(str) : yaml 파일의 경로

    return:
    반환값은 없습니다 하지만 유효하지 않다면, ValueError 를 출력합니다.
    """
    try:
        with open(file_path, 'r', encoding='UTF8') as file:
            yaml_content = file.read()
            data = strictyaml.load(yaml_content, schema)
            for index, subject in enumerate(data["과목"], start=1):
                subject_name = subject["과목명"]
                try:
                    if subject["학년"] not in [1, 2, 3, 4, 5, 6]:
                        raise ValueError("학년은 1부터 6까지의 정수여야 합니다.")
                    for field_name in ["과목명", "트랙", "마이크로디그리", "선수과목"]:
                        if field_name in subject:
                            validate_string_or_sequence(subject[field_name].data)
                except ValueError as e:
                    raise ValueError(f"과목 '{subject_name}'의 '{field_name}'에 유효하지 않은 값이 있습니다.") from e
            print("파일이 유효합니다.")
    except strictyaml.YAMLValidationError as e:
        print(f"오류: {e}")
    except ValueError as e:
        print(f"오류: {e}")


def main():
    file_path = input("파일명을 입력해주세요: ")
    validate_yaml(file_path)


if __name__ == '__main__':
    main()
