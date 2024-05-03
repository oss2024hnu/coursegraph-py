import sys
import yaml
import strictyaml
from strictyaml import Map, Seq, Str, Int, Optional
from typing import Any, Union


    
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

def validate_yaml(file_path: str):
    try:
        with open(file_path, 'r', encoding='UTF8') as file:
            yaml_content = file.read()
            data = yaml.safe_load(yaml_content)
            for index, subject in enumerate(data["과목"], start=1):
                subject_name = subject["과목명"]
                try:
                    for field_name in ["과목명", "트랙", "마이크로디그리", "선수과목"]: #문자로 잘 입력되었는지 적합성 검사 리스트
                        if field_name in subject:
                            value = subject[field_name]
                            if value is not None:
                                if isinstance(value, list):
                                    for item in value:
                                        if not isinstance(item, str):
                                            raise ValueError(f"과목 '{subject_name}'의 '{field_name}'에 유효하지 않은 값이 있습니다.")
                                elif not isinstance(value, str):
                                    raise ValueError(f"과목 '{subject_name}'의 '{field_name}'에 유효하지 않은 값이 있습니다.")
                except ValueError as e:
                    raise ValueError(f"과목 '{subject_name}'의 '{field_name}'에 유효하지 않은 값이 있습니다.") from e
            print("파일이 유효합니다.")
    except ValueError as e:
        print(f"오류: {e}")
    except yaml.YAMLError as e:
        print(f"오류: {e}")


file_path = input("파일명을 입력해주세요: ")
validate_yaml(file_path)
