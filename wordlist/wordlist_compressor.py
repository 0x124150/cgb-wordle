from typing import List


def load_wordlist():
    with open("full_wordlist.txt") as f:
        words =  f.readlines()
        clean_words = []
        for i in range(len(words)):
            words[i] = words[i].strip()
            if len(words[i]) != 5:
                continue

            clean_words.append(words[i])
        
        return sorted(clean_words)
    

def split_wordlist_on_first_char(wordlist: List[str]):
    word_dict = {}
    for i in range(97, 97+26):
        word_dict[chr(i)] = []
    
    for w in wordlist:
        if w[0] not in word_dict:
            raise Exception("invalid_word %s" % w)
        word_dict[w[0]].append(w)
    
    return word_dict


def get_word_as_number(word: str):
    result = 0
    # skip the first character for optimization (dict split by first char)
    for i in range(4, 0, -1):
        # A is 0
        # 26 characters, treat as 26 based number
        result += (ord(word[i]) - ord('a')) * (26 ** (4-i))
    
    return result


def compress_wordlist():
    wordlist = load_wordlist()
    if not wordlist:
        return []
    
    list_separator = b'\x00'
    cur_char = ''
    prev_val = 0
    diff = 0
    result = {}
    for i in range(26):
        result[chr(97+i)] = []

    total_bytes = 0 
    for w in wordlist:
        cur_val = get_word_as_number(w)
        diff = cur_val - prev_val
        if w[0] != cur_char or diff > 255:
            result[w[0]].append([list_separator])
            total_bytes += 1

            # 1 char = 5 bits, 26 possibilities
            packed_chars = 0
            for i in range(4, 0, -1):
                packed_chars <<= 5
                o = ord(w[i])-ord('a')
                packed_chars += o
            
            for i in range(3):
                result[w[0]][-1].append((packed_chars & 255).to_bytes())
                packed_chars >>= 8
            
            total_bytes += 3
            cur_char = w[0]
            prev_val = cur_val
        else:
            result[w[0]][-1].append((diff & 255).to_bytes())
            prev_val = cur_val
            total_bytes += 1
    
    return result, total_bytes


if __name__ == "__main__":
    print(compress_wordlist())