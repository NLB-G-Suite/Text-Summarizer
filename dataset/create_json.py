import os
import json

cnn_path = "cnn//"
output_json_path = "output.json"
allowed_characters = "abcdefghijklmnopqrstuvwxyz0123456789 "

limit = {
	'max_text' : 4
	'max_summary' : 8
}

####################################
#   Creates JSON files from data   #
####################################

def turn_to_json(filepath):
	files = [cnn_path + f for f in os.listdir(filepath)]
	json_data = list()
	counter = 0

	for file in files:
		if counter%10000 == 0:
			print("Progress: {}/{} files".format(counter, len(files)))
		counter += 1

		data = dict()

		try:
			text, summary = get_text_summary(file)
		except:
			continue

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
	
	try:
		with open(filePath, 'r') as file:
			lines = file.readlines()
	except:
		raise Exception()

	
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



###############################################################################
#   Converts to lower case, removes extraneous characters and double spaces   #
###############################################################################

def filter_chars(line):
	filtered = []
	space = False	# used to remove double spaces
	for char in line:
		char = char.lower()
		if char in allowed_characters:
			if char == ' ':
				if not space:
					space = True
					filtered.append(char)
				else:
					space = False
			else:
				filtered.append(char)
				space = False

	return ''.join(filtered)

if __name__ == "__main__":
	turn_to_json(cnn_path)