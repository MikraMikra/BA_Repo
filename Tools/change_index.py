import os

folder_path = "/Tools/MainDir/SunDataSet/valid/labels"


def replace_first_number(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    content = content.replace('1 ', '0 ', 1)  # Ersetze nur die erste Instanz von '1 ' durch '0 '

    with open(file_path, 'w') as file:
        file.write(content)


def process_files_in_folder(folder):
    for filename in os.listdir(folder):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder, filename)
            replace_first_number(file_path)


if __name__ == "__main__":
    process_files_in_folder(folder_path)
