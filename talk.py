import os


class Talk:
    def talk(self, phrase):
        formatted_phrase = "espeak -v en+f5 '{}'".format(phrase)
        os.system(formatted_phrase)
