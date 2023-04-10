#!/usr/bin/env python3

import os
import re


class CombineFiles:
    def __init__(self, folder_path=None, main_file="main.py"):
        if folder_path is None:
            folder_path = os.path.dirname(os.path.abspath(__file__))
        self.folder_path = folder_path
        self.target_file_path = os.path.join(folder_path, "tgpt")
        self.main_file = main_file

    def process_file(self, file_path):
        with open(file_path, "r") as file:
            content = file.read()
            imports = re.findall(r'^import .*|from .* import .*', content, re.MULTILINE)

            # Filter out local file imports
            imports = [imp for imp in imports if not any(local_file[:-3] in imp for local_file in os.listdir(self.folder_path) if local_file.endswith(".py"))]

            for imp in imports:
                content = content.replace(imp, "").strip()

            main_section = re.search(r'if __name__ == ["\']__main__["\']:', content)

            if main_section and file_path != self.main_file:
                main_start = main_section.start()
                if "__name__" in content[main_start+1:]:
                    content = content[:main_start].strip()

        return imports, content


    def combine_files(self):
        imports = set()
        combined_content = []
        local_files = set()

        standard_library_modules = {'os.py', 're.py', 'sys.py', 'requests.py', 'argparse.py'}

        for file_name in os.listdir(self.folder_path):
            if file_name.endswith(".py") and file_name != "combine_files.py" and file_name not in standard_library_modules:
                local_files.add(file_name[:-3])

        print("Found local python files:")
        for file in local_files:
            print(file + ".py")

        main_class_content = None

        for local_file in local_files:
            file_path = os.path.join(self.folder_path, local_file + ".py")

            file_imports, content = self.process_file(file_path)
            imports.update(file_imports)

            # Remove local imports from content
            for local_file_name in local_files:
                local_import_pattern = rf"from {local_file_name} import .*|import {local_file_name}.*"
                content = re.sub(local_import_pattern, "", content).strip()

            # Check if the current file path is the main file
            if file_path == self.main_file:
                main_class_content = content
            else:
                combined_content.append(content)

        filtered_imports = set()
        for imp in imports:
            if not any(local_file in imp for local_file in local_files):
                filtered_imports.add(imp)

        with open(self.target_file_path, "w") as target_file:
            target_file.write("#!/usr/bin/env python3" + "\n")
            target_file.write("\n".join(sorted(filtered_imports)) + "\n\n")
            target_file.write("\n\n".join(combined_content) + "\n")

            if main_class_content:
                target_file.write("\n\n" + main_class_content + "\n")

        print("Combined file saved to " + self.target_file_path)


def main():
    folder_path = None  # or "/path/to/your/folder"
    if folder_path is None:
        main_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "main.py")
    else:
        main_file = os.path.join(folder_path, "main.py")
    combiner = CombineFiles(folder_path=folder_path, main_file=main_file)
    combiner.combine_files()


if __name__ == "__main__":
    main()
