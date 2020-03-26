import os
import json

cnn_path = "cnn//"
output_json_path = "output.json"
allowed_characters = "abcdefghijklmnopqrstuvwxyz0123456789 "

####################################
#   Creates JSON files from data   #
####################################

def turn_to_json(filepath):
	files = [cnn_path + f for f in os.listdir(filepath)]
	json_data = list()

	for file in files[:5]:
		data = dict()

		text, summary = get_text_summary(file)

		data['text'] = text
		data['summary'] = summary

		json_data.append(data)

	# write json to file
	with open(output_json_path, 'w') as outputFile:
		json.dump(json_data, outputFile, indent=2)



#############################################################
#   Extract text and corresponding summary from data file   #
#############################################################

def get_text_summary(filePath):
	file_text = list()
	file_summary = list()
	
	with open(filePath, 'r') as file:
		lines = file.readlines()
	
	highlight_start = 0
	lines = [line.replace("\n", '') for line in lines]

	for (i, line) in enumerate(lines):
		if line != '':
			if line != "@highlight":
				file_text.append(filter_chars(line))
			else:
				highlight_start = i
				break;

	for line in lines[highlight_start:]:
		if line != '' and line != "@highlight":
			file_summary.append(filter_chars(line))


	text = " ".join(file_text)
	summary = " ".join(file_summary)

	return text, summary


def filter_chars(line):
	return ''.join([char for char in line if char in allowed_characters])



		






	




if __name__ == "__main__":
	turn_to_json(cnn_path)
