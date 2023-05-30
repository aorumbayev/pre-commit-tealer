# Standard Library
from argparse import ArgumentParser
from os import path, chdir, getcwd
import subprocess
import glob


def gather_teal_files(input_folder: str):
    teal_files = glob.glob(f"{input_folder}/**/*.teal", recursive=True)
    teal_files = [f for f in teal_files if "/tealer/" not in f]
    return teal_files


def update_or_clone_tealer():
    tealer_path = "tealer"
    if path.exists(tealer_path):
        print("Repository exists, pulling latest changes")
        chdir(tealer_path)
        subprocess.run(["git", "pull", "origin", "main"], check=True)
    else:
        print("Cloning repository")
        subprocess.run(
            ["git", "clone", "https://github.com/crytic/tealer.git"], check=True
        )
        chdir(tealer_path)

    # Install the setup.py
    subprocess.run(["python3", "setup.py", "install"], check=True)


def run_tealer(input_folder: str):
    # Gather all teal files
    teal_files = gather_teal_files(input_folder)

    # Update or clone tealer repository and install
    update_or_clone_tealer()

    # Run tealer for each file
    for file_path in teal_files:
        print(f"Running tealer for {file_path}")
        result = subprocess.run(
            ["python3", "-m", "tealer", file_path], capture_output=True
        )
        print(result.stdout.decode())
        if result.returncode != 0:
            print(result.stderr.decode())


def main():
    parser = ArgumentParser(description=("Perform tealer static analysis"))
    parser.add_argument(
        "--input", help="Input folder with schemas", metavar="FILE", default=getcwd()
    )

    args = parser.parse_args()
    run_tealer(args.input)


if __name__ == "__main__":
    main()
