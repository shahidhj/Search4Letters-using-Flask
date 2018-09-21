def search_for_vowel(phrase:str)-> set:
    """Returns any vowels found in a supllied string"""
    vowels = set('aeiou')
    found_vowel = vowels.intersection(set(word))
    return found_vowel

def search_for_letters(phrase:str,letters:str='aeiou') ->set:
    """Returns set of letters in the given phrase"""
    return set(letters).intersection(set(phrase))
