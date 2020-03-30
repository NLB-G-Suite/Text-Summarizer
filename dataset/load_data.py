import json

output_json_path = "output.json"

def filter_len(json_path, max_text):
	text = list()
	summary = list()

	with open(json_path) as file:
		data = json.load(file)

	for entry in data[:2]:
		text_len = len(entry['text'].split(' '))
		summary_len = len(entry['summary'].split(' '))

		# check to make sure that summary length is shorter than text length
		if text_len > summary_len:





if __name__ == "__main__":
	filter_len(output_json_path, 10)
