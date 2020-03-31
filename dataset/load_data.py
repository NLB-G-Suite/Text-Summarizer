import os
import json
from create_json import output_json_path, cnn_path 

limits = {
    'max_text' : 500,           # limit for max length of text
    'num_entries' : 50000,     # limit for max num of entries
    'vocab_size' : 10000,
}

###########################
#   Return index tables   #
###########################
def get_index_tables():
    freq_table = create_frequency_table()
    word2index = create_word2index(freq_table)
    index2word = create_index2word(freq_table)

    return (word2index, index2word)

#########################################################
#   Helper: return list of ints corresponding to data   #
#########################################################
def index_words(data, word2index):
    indexed_data = list()

    for entry in data:
        indexed_entry = list()
        for word in entry.split(' '):
            if word in word2index:
                value = word2index[word]
                indexed_entry.append(value)

        indexed_data.append(indexed_entry)

    return indexed_data

###############################################
#   Ensures length of text is within limits   #
###############################################
def filter_len():
    text = list()
    summary = list()
    data = load_json_data()

    for entry in data:
        text_len = len(entry['text'].split(' '))
        summary_len = len(entry['summary'].split(' '))

        # check to make sure that summary length is shorter than text length
        if text_len > summary_len and text_len < limits['max_text']:
            text.append(entry['text'])
            summary.append(entry['summary'])

    return (text, summary)

###############################
#   Returns frequency table   #
###############################
def create_frequency_table():
    data = load_json_data()

    freq_table = dict()

    for entry in data:
        text = entry['text'].split(' ')
        summary = entry['summary'].split(' ')

        count_words(freq_table, text)
        count_words(freq_table, summary)

    sorted_table = dict()

    for (i,key) in enumerate(sorted(freq_table, key=freq_table.get, reverse=True)):
        if i > limits['vocab_size']:
          break
        else:
            sorted_table[key] = freq_table[key]

    return sorted_table


###############################
# Returns word-to-index table #
###############################
def create_word2index(freq_table):
    word2index = dict()

    for (i, key) in enumerate(freq_table):
        word2index[key] = i

    return word2index


#################################
#   Returns index-to-word table #
#################################
def create_index2word(freq_table):
    index2word = dict()

    for (i ,key) in enumerate(freq_table):
        index2word[i] = key

    return index2word

#########################################
#   Helper: counts frequency of words   #
#########################################
def count_words(freq_table, words):
    for word in words:
        if word in freq_table:
            freq_table[word] += 1
        else:
            freq_table[word] = 1



#####################################
#   Load data from JSON data file   #
#####################################
def load_json_data():
    with open(output_json_path) as file:
        data = json.load(file)

    return data


def find_longest_sequence(data):
    count = -1

    for entry in data:
        if len(entry) > count:
            count = len(entry)

    return count