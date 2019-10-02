import json
f = open("missing_words.json","r")
json_missing_data = json.load(f)
json_ls = []

for key in json_missing_data:
    json_ls.append(key)

print(json_ls)


with open('python_dictionary.json','r+') as f:
    dic = json.load(f)
    dic.update(new_dictionary)
    json.dump(dic, f)



 #Save exceptions to a dictionary as json file
    json_string = json.dumps(missing_words)
    f = open("missing_words.json","a")
    f.write(json_string)
    f.close()
    print("\nFile saved as missing_words.json")
