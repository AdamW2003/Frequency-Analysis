import os

def caesar_cipher(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            # Determine if the character is uppercase or lowercase
            is_upper = char.isupper()
            # Shift the character by the specified amount
            char_code = ord(char) + shift
            # Ensure the new character is within the alphabet range
            if is_upper:
                char_code = (char_code - ord('A')) % 26 + ord('A')
            else:
                char_code = (char_code - ord('a')) % 26 + ord('a')
            result += chr(char_code)
        else:
            # Keep non-alphabetic characters unchanged
            result += char
    return result

def encrypt_and_save(input_file_name, shift, output_file_name):
    input_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), input_file_name)
    output_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), output_file_name)

    with open(input_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    encrypted_content = caesar_cipher(content, shift)

    # Save the encrypted content to another file
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(encrypted_content)

# Example usage:
input_file_name = "txt.txt"
output_file_name = "cypher.txt"
shift_amount = 3  # You can adjust this value to change the shift amount
encrypt_and_save(input_file_name, shift_amount, output_file_name)
