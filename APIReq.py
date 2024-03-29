import json
import requests
import os
 
fhand = open('requiredData.txt')
 
data = fhand.readlines()
json_data = {"documents" : []}
id = 1
 
for line in data:
    temp = {"language" : "en", "id" : str(id), "text" : line}
    json_data["documents"].append(temp)
    id += 1

subscription_key = os.environ['TEXT_ANALYTICS_API_KEY']
assert subscription_key
text_analytics_base_url =  "https://australiaeast.api.cognitive.microsoft.com/text/analytics/v2.0/" 
key_phrase_api_url = text_analytics_base_url + "keyPhrases"  
headers   = {'Ocp-Apim-Subscription-Key': subscription_key}
response  = requests.post(key_phrase_api_url, headers=headers, json=json_data)
key_phrases = response.json()

with open('keyPhrases.json', 'w') as f:
    json.dump(key_phrases, f, indent = 2)

with open('ApiInput.json', 'w') as f:
    json.dump(json_data, f, indent = 2)

print('Done')