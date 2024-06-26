import string
from collections import Counter
filename = 'english_random.txt'

def textstrip(filename):
    with open(filename, 'r') as file:
        data = file.read()
    return data
text_data = textstrip(filename)


def letter_distribution(s):
         return Counter(s)
s = textstrip(filename)
letter_counts = letter_distribution(s)
print(letter_distribution(text_data))
    
def substitution_encrypt(s, d):
    encrypted_string = ''.join(d[letter] for letter in s)
    return encrypted_string

s = textstrip(filename)
d = {
    'a': 'b', 'b': 'c', 'c': 'd', 'd': 'e', 'e': 'f', 'f': 'g', 'g': 'h', 'h': 'i', 'i': 'j',
    'j': 'k', 'k': 'l', 'l': 'm', 'm': 'n', 'n': 'o', 'o': 'p', 'p': 'q', 'q': 'r', 'r': 's',
    's': 't', 't': 'u', 'u': 'v', 'v': 'w', 'w': 'x', 'x': 'y', 'y': 'z', 'z': 'a'
}
encrypted_string = substitution_encrypt(s, d)


def substitution_decrypt(s, d):
    reversed_d = {v: k for k, v in d.items()}
    decrypted_chars = []
    for char in s:  
        decrypted_chars.append(reversed_d.get(char, char))
    return ''.join(decrypted_chars)


def substitution_decrypt(s, d):
    reversed_d = {v: k for k, v in d.items()}
    decrypted_chars = [reversed_d.get(char, char) for char in s]
    return ''.join(decrypted_chars)

def cryptanalyse_substitution(s):
    english_freq_order = 'etaoinshrdlcumwfgypbvkjxqz'
    
    letter_counts = Counter(s)
    sorted_encrypted_letters = [letter for letter, _ in letter_counts.most_common()]
    predicted_d = {enc_letter: eng_letter for enc_letter, eng_letter in zip(sorted_encrypted_letters, english_freq_order)}
    
    return predicted_d

def vigenere_encrypt(s,password):
    encrypted = ''
    for i in range(len(s)):
        c = s[i]
        if c.isalpha():
            c = c.lower()
            pos = ord(c) - ord('a')
            key = password[i % len(password)]
            key_pos = ord(key) - ord('a')
            encrypted += chr((pos + key_pos) % 26 + ord('a'))
        else:
            encrypted += c
    return encrypted
password='pranavropar' 
vig_encrypted=vigenere_encrypt(textstrip('english_random.txt'),password)
print(vig_encrypted)

def vigenere_decrypt(s,password):
    decrypted = ''
    for i in range(len(s)):
        c = s[i]
        if c.isalpha():
            c = c.lower()
            pos = ord(c) - ord('a')
            key = password[i % len(password)]
            key_pos = ord(key) - ord('a')
            decrypted += chr((pos - key_pos) % 26 + ord('a'))
        else:
            decrypted += c
    return decrypted
vig_decrypted=vigenere_decrypt(vig_encrypted,password)
print(vig_decrypted)

def rotate_compare(vig_encrypted,r):   
    length=len(vig_encrypted)
    rotated_vig_encrypted = vig_encrypted[r:] + vig_encrypted[:r]
    collisions = sum(1 for a, b in zip(vig_encrypted, rotated_vig_encrypted) if a == b)
    proportion = collisions / length
    return proportion
print("proportion of collisions: ",rotate_compare(vig_encrypted,3))

def cryptanalyse_vigenere_findlength(vig_encrypted):
    target_proportion = 0.065
    for r in range(2,50):
        proportion=rotate_compare(vig_encrypted,r)        
        if abs(proportion - target_proportion) < 0.01:  
            return r
    
    print("not enough iterations")
    return None
key_length=cryptanalyse_vigenere_findlength(vig_encrypted)
print("Length of key : ",key_length)

def split_text_into_groups(vig_encrypted, n):
    return [vig_encrypted[i::n] for i in range(n)]
def cryptanalyse_vigenere_afterlength(vig_encrypted,key_length):
    groups = split_text_into_groups(vig_encrypted, key_length)
    key = ''
    for group in groups:
        letter_count = letter_distribution(group)
        max_count = max(letter_count.values())
        max_letter = [k for k, v in letter_count.items() if v == max_count][0]
        pos1 = ord(max_letter) - ord('a')
        pos2 = ord('e') - ord('a')
        shift = (pos1 - pos2) % 26
        key += chr(shift + ord('a'))
    return key
key=cryptanalyse_vigenere_afterlength(vig_encrypted,key_length)
print("key : ",key)

def cryptanalyse_vigenere(vig_encrypted):
    key_length=cryptanalyse_vigenere_findlength(vig_encrypted)
    password=cryptanalyse_vigenere_afterlength(vig_encrypted,key_length)
    vig_decrypted=vigenere_decrypt(vig_encrypted,password)
    return vig_decrypted,password
vig_decrypted,password=cryptanalyse_vigenere(vig_encrypted)
print("decrypted: ",vig_decrypted)
print("password: ",password)

