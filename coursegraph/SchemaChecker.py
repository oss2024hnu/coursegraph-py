import sys
import strictyaml
import re

# 과목명,트랙,마이크로디그리,선수과목에는 문자만 사용되었는지 확인하는 함수
def validate_string_or_sequence(value):

    if isinstance(value, str):
        if re.match(r'^[A-Za-z가-힣]+$', value):
            return value
        else:
            raise ValueError("올바른 형식이 아닙니다.")
    elif isinstance(value, list):
        for item in value:
            if not re.match(r'^[A-Za-z가-힣]+$', item):
                raise ValueError(f"올바른 형식이 아닙니다: {item}")
        return value
    else:
        raise ValueError("올바른 형식이 아닙니다.")
    
# 우선적으로 (학년, 학기, 과목명, 트랙, 마이크로디그리, 선수과목) 의 스키마를 정의해뒀습니다.
schema = strictyaml.Map({
    "과목": strictyaml.Seq(strictyaml.Map({
        "학년": strictyaml.Int(),
        "학기": strictyaml.Int(),
        "과목명": strictyaml.Str(),
        strictyaml.Optional("트랙"): strictyaml.Seq(strictyaml.Str()),
        strictyaml.Optional("마이크로디그리"): strictyaml.Seq(strictyaml.Str()),
        strictyaml.Optional("선수과목"): strictyaml.Seq(strictyaml.Str())
    }))
})

def validate_yaml(file_path):
    try:
        with open(file_path, 'r', encoding='UTF8') as file:
            yaml_content = file.read()
            data = strictyaml.load(yaml_content, schema)
            for index, subject in enumerate(data["과목"], start=1):
                subject_name = subject["과목명"]
                try:
                    for field_name in ["과목명", "트랙", "마이크로디그리", "선수과목"]:
                        if field_name in subject:
                            validate_string_or_sequence(subject[field_name].data)  # 해당 필드의 값을 가져와 문자열로 변경하고 적합성 검사
                except ValueError as e:
                    raise ValueError(f"과목 '{subject_name}'의 '{field_name}'에 유효하지 않은 값이 있습니다.") from e
            print("파일이 유효합니다.")
    except strictyaml.YAMLValidationError as e:
        print(f"오류: {e}")
    except ValueError as e:
        print(f"오류: {e}")

if __name__ == "__main__":
    file_path = input("파일명을 입력해주세요: ")
    validate_yaml(file_path)
