import re, datetime

my_list = ['item1', 'item2', 'item3', 'new_folder/item4', 'new_folder/item5', '/new_folder/folder_within_folder/item6']


my_string = '/new_folder/folder_within_folder/item7'
folder_regex = re.compile(r'.*/')


# print(list(filter(folder_regex.match, my_list))) # returns a list of 

new_string = folder_regex.sub('', my_string)
print(new_string)