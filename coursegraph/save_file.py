class Save_file:
  def __init__(self):
    pass
  #파일의 주소를 적는 함수
  def input_command(self):
    command1 = str(input("변경할 파일의 주소를 입력하세요: "))
    return command1
  #새로운 파일의 주소를 적는 함수
  def input_file(self, command1):
    try:
        with open("save.txt", "r") as f:
            if f.readline().strip():
                print("이미 내용이 있습니다. 수정하려면 -u 명령어를 이용하세요")
                exit()
    except FileNotFoundError:  # 파일이 없는 경우
        pass  # 파일이 없으므로 아무 작업도 수행하지 않음

    with open("save.txt", "w") as f:
        f.write(command1 + "\n")


  #input파일주소와 output파일의 주소를 출력하는 함수
  def print_file(self):
    with open("save.txt", "r") as f:
       for line in f:
        print(line)

  #출력할 파일의 주소를 입력하는 함수
  def output_file(self, command1):
    with open("save.txt", "r") as f:
      lines = f.readlines()
      if len(lines) > 1 and lines[1].strip():
        print("이미 내용이 있습니다. 수정하려면 -u 명령어를 이용하세요")
        exit()

    with open("save.txt", "r") as f:
      lines = f.readlines()

      # 첫 번째 줄이 비어있으면 input파일부터 입력하라는 메시지 출력후 종료
    if not lines or not lines[0].strip():
        print("input파일의 주소부터 입력하세요")
        return

    # 두 번째 줄에 새로운 내용을 추가합니다.
    lines.insert(1, command1)

    with open("save.txt", "w") as f:
        f.writelines(lines)

  #input파일의 주소를 수정하는 함수
  def update_input_file(self, command1):
    with open("save.txt", "r") as f:
      lines = f.readlines()

    # 첫 번째 줄을 수정합니다.
    lines[0] = command1 + "\n"

    with open("save.txt", "w") as f:
      f.writelines(lines)

  def update_output_file(self, command1):
    with open("save.txt", "r") as f:
      lines = f.readlines()

    # 두 번째 줄을 수정합니다.
    lines[1] = command1 + "\n"

    with open("save.txt", "w") as f:
      f.writelines(lines)

  #input_file에서 사용할 함수
  def input_process(self, input_file):
    self.input_file(input_file)
    self.print_file()

  #output_file에서 사용할 함수
  def output_process(self, ouput_file):
    self.output_file(ouput_file)
    self.print_file()

  def input_update(self):
    filename = self.input_command()
    self.update_input_file(filename)
    self.print_file()

  def output_update(self):
    filename = self.input_command()
    self.update_output_file(filename)
    self.print_file()
  #input파일을 바꿀건지 output파일을 수정할 건지 입력
  def choice_file(self):
    select = str(input("1: input파일 수정 2: output파일 수정 : "))
    if (select == "1"):
      self.input_update()
    elif (select == "2"):
      self.output_update()
    else:
      exit()
  if __name__ == "__main__":
    pass