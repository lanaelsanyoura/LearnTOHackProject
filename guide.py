"""
Create the back-end for a TV Show Recommendation system based on the prompts
the user inputs
"""
import requests
import random
import re


def get_tv_shows(input):
    """
    Return a list of the  (formatted) reccomended TV shows based on the input
    :param input: a word or phrase the user would like their TV show related to
    :return: list of show descriptions
    """
    # Find the words related to the input
    get_related_words = requests.get("https://api.datamuse.com/words?ml=" + input)
    word_list = get_related_words.json()[:10]

    # Request a random set of 3 shows that would fit this input
    show_list = []
    for word in word_list:
        show_response = requests.get(
                "http://api.tvmaze.com/search/shows?q=" + word["word"])
        all_shows = show_response.json()
        if not len(all_shows) == 0:
            show = random.choice(all_shows)
            show_info = format_show(show)
            show_list.append(show_info)
    return show_list


def format_show(show):
    """
    Return a string of the TV show formatted according to requirements
    e.g.
   >>> format_show(show_dict)
    - Desperate Romantics (rating: None  genre: Drama)
    A BBC six-part drama following the Pre-Raphaelite brotherhood - the men
    who blew the art world apart

    :param show: TV Show dictionary
    :return: The TV Show name, rating, genre, and summary
    """
    name = show['show']['name']
    rating = show['show']['rating']['average']
    space = ", "
    genre = space.join(show['show']['genres'])
    summary = show['show']['summary']

    if summary is not None:
        summary = re.sub(r'<..>', ' ', summary)
        summary = re.sub(r'<.>', ' ', summary)
        summary = summary.replace("</p>", "\n")
        summary = summary.replace("<p>", "  ")
    else:
        summary = "No summary available"

    show_description = '{} (rating: {}  genre: {}) \n{}\n'.format(
                        name,
                        rating,
                        genre,
                        summary)
    return show_description

# Retrieve the user's input word
user_input = input("First word that comes to mind? ")

recommended_shows = get_tv_shows(user_input)
print("\nRecommended Shows\n" )
for tv_show in recommended_shows:
    print("- " + tv_show)