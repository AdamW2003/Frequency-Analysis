import os
import re

def remove_non_ascii_and_newlines(file):
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Remove non-ASCII characters
    content = re.sub(r'[^\x00-\x7F]+', '', content)

    # Remove newlines
    content = content.replace('\n', '').replace('\r', '')

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

# Example usage:
file_name = 'txt3.txt'
remove_non_ascii_and_newlines(file_name)
