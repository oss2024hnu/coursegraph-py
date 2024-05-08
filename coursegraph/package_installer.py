import subprocess
import sys
import os


class PackageInstaller:
    def __init__(self, requirements_file="requirements.txt"):
        self.requirements_file = requirements_file

    def find_top_dir(self):
        current_dir = os.path.abspath(os.path.dirname(__file__))

        while not os.path.exists(os.path.join(current_dir, self.requirements_file)):
            parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

            if parent_dir == current_dir:
                return None

            current_dir = parent_dir
        return current_dir

    def install_packages(self):
        top_level_dir = self.find_top_dir()
        if not top_level_dir:
            print("Error : requirements.txt file not found ")
            return

        requirements_path = os.path.join(top_level_dir, self.requirements_file)

        try:
            with open(requirements_path, "r") as f:
                required_packages = [line.strip() for line in f.readlines() if line.strip()]
        except FileNotFoundError:
            print(f"Error: {self.requirements_file} not found.")
            return

        if required_packages:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_path])
                print("packages installed successfully.")
            except subprocess.CalledProcessError as e:
                print(f"Error occurred while installing packages: {e}")
        else:
            print("No packages to install.")

    # 실행


if __name__ == "__main__":
    data_processer = PackageInstaller()
    data_processer.install_packages()
