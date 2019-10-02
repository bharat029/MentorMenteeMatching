# Mentor-Mentee Matching

The goal of this project is to create a system for automated matching of mentor-mentee based on their general descriptions and expectations.

## Components: 

- extractFromRawData.py: This script's role is to parse through the raw data, extract only relevant data and properly format it to be used as input to the model. 
    It uses the rawData.txt to then generate the requiredData.txt.

- APIReq.py: This script's role is to make the api request to the Microsoft Text Analytics API (which we are using to extract key phrases from the data).
    It uses the requiredData.txgt and stores the response body in the keyphrases.json file.

- preprocessing.py: This script's roles include removal of stop words, tokenization, lemmatization of the api response and creating a mapping between the key pharses and the original input.

- GensimLDAModel.py : This script uses the Grnsim LDA inplementation to form clusters and saves the results to clusters.txt.

- LDA.py: This is the custom LDA implementation.