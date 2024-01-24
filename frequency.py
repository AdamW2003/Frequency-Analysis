import string
import matplotlib.pyplot as plt
import os

class Parser():
    def __init__(self):
        self.singleLetterFreq = ['E', 'T', 'A', 'O', 'I', 'N', 'S', 'H', 'R', 'D', 'L',
                    'C', 'U', 'M', 'W', 'F', 'G', 'Y', 'P', 'B', 'V', 'K', 'J', 'X', 'Q', 'Z']
        self.doubleLetterFreq = ['TH', 'HE', 'IN', 'ER', 'AN', 'RE', 'ND', 'ON', 'EN',
                            'AT', 'OU', 'ED', 'HA', 'HA', 'TO', 'OR', 'IT', 'IS', 'HI', 'ES', 'NG']
        self.trippleLetterFreq = ['the', 'and', 'ing', 'her', 'hat', 'his', 'tha', 'ere', 'for',
                            'ent', 'ion', 'ter', 'was', 'you', 'ith', 'ver', 'all', 'wit', 'thi', 'tio']
        self.quadLetterFreq = ['that', 'ther', 'with', 'tion', 'here', 'ould', 'ight', 'have', 'hich',
                        'whic', 'this', 'thin', 'they', 'atio', 'ever', 'from', 'ough', 'were', 'hing', 'ment']
        
        self.charFrequency = dict.fromkeys(string.ascii_uppercase, 0)
        self.doubleFreq = dict(zip(self.doubleLetterFreq, [0] * len(self.doubleLetterFreq)))
        self.tripleFreq = dict(zip(self.trippleLetterFreq, [0] * len(self.trippleLetterFreq)))
        self.quadFreq = dict(zip(self.quadLetterFreq, [0] * len(self.quadLetterFreq)))

    def open_file(self, file):
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), file), "r") as file:
            file_content = file.read()
            return file_content.replace('\n', ' ')

    def filter_text(self, text):
        return ''.join(char.upper() for char in text if char.isalpha() or char.isspace())

    def parse_text_single(self, text):
        for c in text.upper():
            if c in list(string.ascii_uppercase):
                self.charFrequency[c] += 1

        self.charFrequency = dict(sorted(self.charFrequency.items(), key=lambda item: item[1], reverse=True))

    def parse_text_multi(self, text, ngram_freq_dict):
        for i in range(len(text) - 1):
            ngram = text[i:i+2]
            if ngram in ngram_freq_dict:
                ngram_freq_dict[ngram] += 1

    def decipher_cipher(self, text):
        self.parse_text_single(text)
        self.parse_text_multi(text, self.doubleFreq)
        self.parse_text_multi(text, self.tripleFreq)
        self.parse_text_multi(text, self.quadFreq)

        cipher_to_english = dict(zip(self.singleLetterFreq, sorted(self.charFrequency.keys(), key=lambda x: self.charFrequency[x], reverse=True)))
        cipher_to_english.update(dict(zip(self.doubleLetterFreq, sorted(self.doubleFreq.keys(), key=lambda x: self.doubleFreq[x], reverse=True))))
        cipher_to_english.update(dict(zip(self.trippleLetterFreq, sorted(self.tripleFreq.keys(), key=lambda x: self.tripleFreq[x], reverse=True))))
        cipher_to_english.update(dict(zip(self.quadLetterFreq, sorted(self.quadFreq.keys(), key=lambda x: self.quadFreq[x], reverse=True))))

        deciphered_text = ''.join(cipher_to_english.get(char, char) for char in text)

        return deciphered_text
    
        
    def plot_letter_frequencies(self):
        # Extract keys (letters) and values (frequencies) from the dictionary
        letters = list(self.charFrequency.keys())
        frequencies = list(self.charFrequency.values())

        # Plotting the bar chart
        plt.bar(letters, frequencies, color='blue')
        
        # Adding labels and title
        plt.xlabel('Letters')
        plt.ylabel('Frequency')
        plt.title('Letter Frequency in Text')

        # Display the plot
        plt.show()

if __name__ == "__main__":
    p = Parser()
    text = p.open_file("cypher.txt")
    p.parse_text_single(text)
    p.plot_letter_frequencies()
    print(p.decipher_cipher(text))

