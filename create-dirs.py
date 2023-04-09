import json
import os


def create_tree(folder):
    # First, escape the '/' character
    folder = folder.replace("/", "_")
    folder_path = os.path.join("videos", folder)
    print(f"Creating folder: {folder_path}")
    os.mkdir(folder_path)
    for i in range(1, 6):
        for j in ["A", "B"]:
            print(f"Creating folder: {folder_path}/{i}/{j}")
            os.makedirs(os.path.join(folder_path, str(i), j))


def main():
    with open("folders.json", "r") as f:
        data: list[str] = json.load(f)
    for folder in data:
        create_tree(folder)


if __name__ == "__main__":
    main()
