import json, operator
from pprint import pprint

with open('output.json') as json_file:
	data = json.load(json_file)



my_list = []

for m in data['KeyPhrases']:
	my_results = dict(text=m['Text'], score=m['Score'])
	my_list.append(my_results)
	# for i in my_results:
	# 	my_list.append(i)

sorted_results = sorted(my_list, key=lambda i: i['score'])

#pprint(sorted_results)

with open('my_sorted_results.txt', 'wt') as my_file:
	pprint(sorted_results, stream=my_file)











# with open('my_sorted_results.txt', 'w') as my_file:
# 	for i in sorted_results:
# 		my_data = my_file.write(str(i))