import json

final_json = []

with open("hazardasteroids.json") as json_file:
	json_data = json.load(json_file)
	for i in json_data:
		# print i['a']
		# break
		try:
			final_json.append({
			'a': float(i['a']),
			'e': float(i['e']),
			'i': float(i['i']),
			'om': float(i['om']),
			'w': float(i['w']),
			'ma': float(i['ma']),
			'per': float(i['per']),
			'full_name': i['full_name'].strip(),
			'epoch': float(i['epoch']),
			})
		except:
			print i
		# break
# print final_json


with open('hazardasteroids_final.json', 'w') as outfile:
    json.dump(final_json, outfile)

	# for i in json_data:
