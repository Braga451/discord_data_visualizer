import argparse
from Interface import Interface

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", help="The discord data folder path")
    args = parser.parse_args()
    GUI = Interface(args.folder)
    GUI.start()

if __name__ == "__main__":
    main()
