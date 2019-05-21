import json


class Language:
    code = 'es'

    def __init__(self, code, dict_file='dictionary.json'):
        """
        Loads the content from dictionaries set in the `dictionary.json` file
        :param code: language code
        :param dict_file: path to the dictionary file
        """
        self.code = code
        with open(dict_file, 'r') as f:
            self.lang_dict = json.load(f)

    def render(self, word):
        """
        Renders a word from a dictionary
        :param word: the word key for rendering
        :return: translated word
        """
        try:
            return self.lang_dict[self.code][word]
        except KeyError:
            pass
