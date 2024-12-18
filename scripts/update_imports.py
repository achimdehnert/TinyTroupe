import os
import re
from pathlib import Path

def update_imports(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update import patterns
    replacements = [
        (r'from tinytroupe\.agent import', 'from group_cases.src.core.characters import'),
        (r'from tinytroupe\.environment import', 'from group_cases.src.core.environment import'),
        (r'from tinytroupe\.extraction import', 'from group_cases.src.utils.result_processor import'),
        (r'from tinytroupe\.factory import', 'from group_cases.src.core.characters import'),
        (r'from db_utils import', 'from group_cases.src.utils.db_utils import'),
        (r'import tinytroupe', '# import tinytroupe  # Removed legacy import'),
        (r'from tinytroupe\.examples import \*', '# Removed legacy wildcard import'),
    ]
    
    new_content = content
    for old, new in replacements:
        new_content = re.sub(old, new, new_content)
    
    if new_content != content:
        print(f"Updating imports in {file_path}")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

def process_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                update_imports(file_path)

if __name__ == "__main__":
    group_cases_dir = Path(__file__).parent.parent / "group_cases"
    process_directory(group_cases_dir)
