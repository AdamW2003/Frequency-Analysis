import string
from collections import Counter
import os


def get_ciphertext_frequencies(ciphertext):
    frequencies = Counter(
        char for char in ciphertext.lower() if char in string.ascii_lowercase
    )
    return frequencies


def get_english_letter_frequencies():
    english_freq = {
        "e": 12.70,
        "t": 9.06,
        "a": 8.17,
        "o": 7.51,
        "i": 6.97,
        "n": 6.75,
        "s": 6.33,
        "h": 6.09,
        "r": 5.99,
        "d": 4.25,
        "l": 4.03,
        "c": 2.78,
        "u": 2.76,
        "m": 2.41,
        "w": 2.36,
        "f": 2.23,
        "g": 2.02,
        "y": 1.97,
        "p": 1.93,
        "b": 1.29,
        "v": 0.98,
        "k": 0.77,
        "j": 0.15,
        "x": 0.15,
        "q": 0.10,
        "z": 0.07,
    }
    return english_freq


def get_common_bigrams():
    common_bigrams = ["th", "he", "in", "er", "an", "re", "on", "at", "en", "nd"]
    return common_bigrams


def get_common_trigrams():
    common_trigrams = [
        "the",
        "ing",
        "and",
        "her",
        "hat",
        "tha",
        "ent",
        "ion",
        "for",
        "ter",
    ]
    return common_trigrams


def refine_mapping_with_bigrams_trigrams(
    ciphertext, potential_mappings, common_bigrams, common_trigrams
):
    ciphertext_bigrams = Counter(
        ciphertext[i : i + 2] for i in range(len(ciphertext) - 1)
    )
    ciphertext_trigrams = Counter(
        ciphertext[i : i + 3] for i in range(len(ciphertext) - 2)
    )

    # Analyze bigrams
    bigram_counts = sorted(ciphertext_bigrams.items(), key=lambda x: x[1], reverse=True)
    for cipher_bigram, _ in bigram_counts:
        for english_bigram in common_bigrams:
            if all(char in potential_mappings for char in cipher_bigram):
                continue  # Already mapped
            if (
                english_bigram[0] in potential_mappings.values()
                or english_bigram[1] in potential_mappings.values()
            ):
                continue  # Conflicting mapping
            potential_mappings[cipher_bigram[0]] = english_bigram[0]
            potential_mappings[cipher_bigram[1]] = english_bigram[1]
            break  # Assign only the first matching bigram

    # Analyze trigrams
    trigram_counts = sorted(
        ciphertext_trigrams.items(), key=lambda x: x[1], reverse=True
    )
    for cipher_trigram, cipher_trigram_count in trigram_counts:
        for english_trigram in common_trigrams:
            if all(char in potential_mappings for char in cipher_trigram):
                continue  # Already mapped
            if (
                english_trigram[0] in potential_mappings.values()
                or english_trigram[1] in potential_mappings.values()
                or english_trigram[2] in potential_mappings.values()
            ):
                continue  # Conflicting mapping
            potential_mappings[cipher_trigram[0]] = english_trigram[0]
            potential_mappings[cipher_trigram[1]] = english_trigram[1]
            potential_mappings[cipher_trigram[2]] = english_trigram[2]
            break  # Assign only the first matching trigram


# Decrypt cipher function with bigram/trigram analysis
def decrypt_cipher(ciphertext):
    # Get frequencies and sort by frequency
    ciphertext_freq = get_ciphertext_frequencies(ciphertext)
    sorted_ciphertext_freq = sorted(
        ciphertext_freq.items(), key=lambda x: x[1], reverse=True
    )

    # Get English letter frequencies
    english_freq = get_english_letter_frequencies()

    # Create a mapping for potential decryptions
    potential_mappings = {}
    for cipher_char, cipher_freq in sorted_ciphertext_freq:
        for english_char, _ in english_freq.items():
            if english_char not in potential_mappings.values():
                potential_mappings[cipher_char] = english_char
                break

    # Refine mapping using bigrams and trigrams
    common_bigrams = get_common_bigrams()
    common_trigrams = get_common_trigrams()

    refine_mapping_with_bigrams_trigrams(
        ciphertext, potential_mappings, common_bigrams, common_trigrams
    )

    # Apply the mapping to decrypt the ciphertext
    plaintext = ""
    for char in ciphertext:
        if char in potential_mappings:
            plaintext += potential_mappings[char]
        else:
            plaintext += char

    return plaintext


# def decrypt_cipher(ciphertext):
#     # Get frequencies and sort by frequency
#     ciphertext_freq = get_ciphertext_frequencies(ciphertext)
#     sorted_ciphertext_freq = sorted(
#         ciphertext_freq.items(), key=lambda x: x[1], reverse=True
#     )

#     # Get English letter frequencies
#     english_freq = get_english_letter_frequencies()

#     # Create a mapping for potential decryptions
#     potential_mappings = {}
#     for cipher_char, cipher_freq in sorted_ciphertext_freq:
#         for english_char, _ in english_freq.items():
#             if english_char not in potential_mappings.values():
#                 potential_mappings[cipher_char] = english_char
#                 break

#     # Refine mapping using bigrams and trigrams
#     common_bigrams = get_common_bigrams()
#     common_trigrams = get_common_trigrams()

#     # Identify space positions
#     space_positions = [i for i, char in enumerate(ciphertext) if char.isspace()]

#     # Refine mapping with bigrams and trigrams
#     refine_mapping_with_bigrams_trigrams(
#         ciphertext, potential_mappings, common_bigrams, common_trigrams
#     )

#     # Predict single letters and adjust mappings
#     for i, char in enumerate(ciphertext):
#         if i in space_positions:
#             continue  # Skip spaces
#         if len(char) == 1:
#             # Analyze single letter using frequency and context
#             predict_and_adjust_mapping(char, i, potential_mappings, ciphertext)

#     # Apply mappings to get plaintext
#     plaintext = "".join(potential_mappings.get(char, char) for char in ciphertext)

#     # Replace mapped spaces
#     for space_position in space_positions:
#         plaintext = plaintext[:space_position] + " " + plaintext[space_position:]

#     return plaintext


# def predict_and_adjust_mapping(char, index, potential_mappings, ciphertext):
#     # Analyze single-letter frequency
#     if char in potential_mappings:  # Already mapped
#         return
#     ciphertext_freq = get_ciphertext_frequencies(ciphertext)
#     english_freq = get_english_letter_frequencies()
#     top_english_letters = sorted(
#         english_freq.items(), key=lambda x: x[1], reverse=True
#     )[:5]
#     # Check if the ciphertext character's frequency aligns with common English letters
#     for english_char, _ in top_english_letters:
#         if ciphertext_freq[char] == ciphertext_freq.get(
#             potential_mappings.get(english_char, ""), 0
#         ):
#             potential_mappings[char] = english_char
#             return

#     # Analyze context clues (bigrams/trigrams)
#     if index > 0:
#         previous_bigram = ciphertext[index - 1 : index + 1]
#         for english_bigram in get_common_bigrams():
#             if all(char in potential_mappings for char in previous_bigram):
#                 continue  # Already mapped
#             if (
#                 english_bigram.startswith(potential_mappings.get(previous_bigram[0]))
#                 and english_bigram[1] not in potential_mappings.values()
#             ):
#                 potential_mappings[char] = english_bigram[1]
#                 return
#     if index < len(ciphertext) - 1:
#         next_bigram = ciphertext[index : index + 2]
#         # ... (Similar logic for next_bigram)

#     # Check for common single-letter words
#     if char in ("a", "i", "o"):  # Consider other common single letters as needed
#         potential_mappings[char] = char


def open_file(file):
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), file), "r"
    ) as file:
        file_content = file.read()
        return file_content.replace("\n", " ")


ciphertext = open_file("cypher.txt")
plaintext = decrypt_cipher(ciphertext)
print(plaintext)  # Output: hello world!
