import json
import requests
 
fhand = open('finalDataSet_2.txt')
 
data = fhand.readlines()
json_data = {"documents" : []}
id = 1
 
for line in data:
    temp = {"language" : "en", "id" : str(id), "text" : line}
    json_data["documents"].append(temp)
    id += 1
     
# subscription key and base url
subscription_key = "a1cd3c4c72724acfb1906f6462367099"
assert subscription_key
text_analytics_base_url =  "https://australiaeast.api.cognitive.microsoft.com/text/analytics/v2.0/" 
key_phrase_api_url = text_analytics_base_url + "keyPhrases"
headers   = {'Ocp-Apim-Subscription-Key': subscription_key}
response  = requests.post(key_phrase_api_url, headers=headers, json=json_data)
key_phrases = response.json()
with open('finalDataSet_2_results.json', 'w') as f:
    json.dump(key_phrases, f, indent = 2)