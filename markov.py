# Predictive Text with Markov Chains

import numpy
import string

class MarkovChain(object):
    def __init__(self,input_text):
        self.input_text = input_text
        self.chain = {}
        self.words = []
        self.frequencies = []

        self.generate_chain()

    def generate_chain(self):
        clean_text = self.input_text.lower()
        for punc in ('!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n\x0b\x0c\r'):
            clean_text = clean_text.replace(punc," ")

        split_text = [word for word in clean_text.split(" ") if word != "" and word != "'"]
        total_words = float(len(split_text))
        unique_words = [split_text[i] for i in range(len(split_text)) if split_text.index(split_text[i]) == i]
        self.words = unique_words[:]

        for word in unique_words:
            count = 0.
            temp = {}
            last_index = -1
            self.chain[word] = {}
            occurances = split_text.count(word)
            self.frequencies.append(occurances/total_words)
            for i in range(occurances):
                index = split_text.index(word,last_index+1)
                try:
                    next_word = split_text[index+1]
                except IndexError:
                    continue
                if temp.has_key(next_word):
                    temp[next_word] += 1
                else:
                    temp[next_word] = 1
                last_index = index
                count += 1
            for key,value in temp.iteritems():
                self.chain[word][key] = value/count

    def get_lists(self,word):
        both = self.get_suggestions_by_probability(word)
        return ([x[0] for x in both],[x[1] for x in both])

    def get_suggestions_by_probability(self,word):
        return sorted([(key,value) for key,value in self.chain[word].iteritems()],key=lambda x:x[1],reverse=True)

    def suggest(self,word):
        if word not in self.words:
            return self.get_random_word()
        lists = self.get_lists(word)
        return numpy.random.choice(lists[0],p=lists[1]) if len(self.chain[word]) > 0 else self.get_random_word()

    def get_random_word(self):
        return numpy.random.choice(self.words,p=self.frequencies)

    def get_random_text(self,start_word,length):
        text = start_word
        last_word = start_word
        for i in range(length):
            last_word = self.suggest(last_word)
            text += (" "+last_word)
        return text
            
