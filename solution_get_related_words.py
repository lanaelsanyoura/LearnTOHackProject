import requests

def get_related_words_json(input):
    """
    :param input: the word we're querying
    :return:
    """
    # get the response from "https://api.datamuse.com/words?ml=<word>"
    word_response = requests.get("https://api.datamuse.com/words",
                                 params={"ml": input})

    return word_response.json()

# Try the function out
#print( get_related_words_json("happy"))
#get_related_words_json("sad")
#get_related_words_json("excited")
