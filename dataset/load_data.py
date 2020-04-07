import os
import json
from create_json import output_json_path, cnn_path 

limits = {
    'max_text' : 500,           # limit for max length of text
    'num_entries' : 50000,     # limit for max num of entries
    'vocab_size' : 10000,
}

start_token = 'sssss '
end_token = ' eeeee'

############################
#   Return lookup tables   #
############################
def get_lookup_tables():
    freq_table = create_frequency_table()
    word2int = create_word2int(freq_table)
    int2word = create_int2word(freq_table)

    return (word2int, int2word)

#########################################################
#   Helper: return list of ints corresponding to data   #
#########################################################
def word2int(data, word2int):
    int_data = list()

    for entry in data:
        int_entry = list()
        for word in entry.split(' '):
            if word in word2int:
                value = word2int[word]
                int_entry.append(value)

        int_data.append(int_entry)

    return int_data

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
        if text_len > summary_len:
            text.append(entry['text'])
            summary.append(entry['summary'])


    # add the start and end tokens to the summary
    summary = [start_token + entry + end_token for entry in summary]

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


#############################
# Returns word-to-int table #
#############################
def create_word2int(freq_table):
    word2int = dict()

    for (i, key) in enumerate(freq_table, 1):
        word2int[key] = i

    return word2int


#################################
#   Returns int-to-word table #
#################################
def create_int2word(freq_table):
    int2word = dict()

    for (i ,key) in enumerate(freq_table, 1):
        int2word[i] = key

    return int2word

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