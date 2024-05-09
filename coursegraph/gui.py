import sys
import tkinter as tk
from tkinter import filedialog

def open_select_yaml():
  try:

    root = tk.Tk()
    root.withdraw()

    select_yaml = filedialog.askopenfilename(initialdir="../data", title="Select file", filetypes=(("YAML files", "*.yaml"), ("all files", "*.*")))
    return select_yaml
  
  # 오류가 발생할 때 비정상적으로 종료되지 않도록 합니다
  except tk.TclError as e:
        print(f"An error occurred while opening file dialog: {e}")
        sys.exit(1)

