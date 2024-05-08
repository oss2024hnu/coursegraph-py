import subprocess
import sys


class PackageInstaller:
    def __init__(self, requirements_file="requirements.txt"):
        self.requirements_file = requirements_file

    def install_packages(self):
        try:
            with open(self.requirements_file, "r") as f:
                required_packages = [line.strip() for line in f.readlines() if line.strip()]
        except FileNotFoundError:
            print(f"Error: {self.requirements_file} not found.")
            return

        if required_packages:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", self.requirements_file])
                print("packages installed successfully.")
            except subprocess.CalledProcessError as e:
                print(f"Error occurred while installing packages: {e}")
        else:
            print("No packages to install.")

    # 실행


if __name__ == "__main__":
    data_processer = PackageInstaller()
    data_processer.install_packages()
