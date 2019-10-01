import nltk
from string import punctuation
from nltk.corpus import stopwords
import json

stop_words = stopwords.words('english')
custom_stop_words = ['nil', 'system', 'areas', 'world', 'ideas', 'things', 'society', 'someone', 'build', 'engineering', 'need', 'user', 'area', 'study', 'future', 'passion', 'passionate', 'medium', 'time', 'computer', 'field', 'interest', 'company', 'thing', 'learn', 'experience','help', 'love', 'skill', 'want', 'bring', 'tech', 'technology', 'people', 'person', 'life', 'family', 'use', 'would', 'work', 'matter', 'idea', 'way', 'skill', 'program', 'project']
#custom_stop_words = ['nil']
lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()

def processComment(comment):
    """
        Preprocessing including removing stop words, punctuations, tokenization and lemmatization
    Args: 
        comment: a single input sentence or doc (a single data point)
    Return: 
        Prepocessed string
    """
    try:
        tokens = nltk.tokenize.word_tokenize(comment)
        filtered_tokens = []
        # Remove punctuation and stopwords
        for token in tokens:
            token = token.lower()
            if token in stop_words or token in punctuation or len(list(set(token).intersection(punctuation))) > 0:
                pass
            elif token in custom_stop_words:
                pass
            else:
                filtered_tokens.append(token)

        sentence = ' '.join(filtered_tokens)
        
        # Get POS tagging for the sentence and lemmatize nouns and verbs, other POS are added without any processing
        pos_tree = nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sentence))).leaves()
        sentence_words = []
        for leaf in pos_tree:
            if 'NN' in leaf[1] or 'NP' in leaf[1]:
                lemma = lemmatizer.lemmatize(leaf[0])
                if lemma not in custom_stop_words:
                    sentence_words.append(lemma)
            elif 'VB' in leaf[1]:
                lemma = lemmatizer.lemmatize(leaf[0], 'v')
                if lemma not in custom_stop_words:
                    sentence_words.append(lemma)
            else:
                sentence_words.append(leaf[0])

        return ' '.join(sentence_words)
    except Exception as e:
        return ""
    
def get_sentenses(fname):
    """
        Get sentences (data points) from input file and writes the output to a txt file by the name 'preprocessed.txt'. Assuming the file is in the same folder
    Args:
        fname: Input file name
    Return: 
        A dictionary mapping preprocessed sentenses to actual input sentences
    """
    fhand = open(fname, errors = 'ignore')
     
    preprocessing_result = {}
    actual_sentenses = fhand.readlines()
    preprocessed_sentenses = []
              
    for i in actual_sentenses:
        preprocessed_sentenses.append(processComment(i))
    
    for i in range(len(actual_sentenses)):
        preprocessing_result[preprocessed_sentenses[i]] = actual_sentenses[i]
    
    fhand.close()

    fhand = open('preprocessed.txt', 'w')
    
    for i in preprocessed_sentenses:
        fhand.write(i + '\n')

    fhand.close()

    return preprocessing_result

def get_lemma(phrase):
    """
        Lemmatization for single word phrases
    Args: 
        phrase: a single word phrase
    Return: 
        lemma of the phrase
    """
    pos_tag = nltk.pos_tag(nltk.word_tokenize(phrase))
    if 'NN' in pos_tag[0][1] or 'NP' in pos_tag[0][1]:
        lemma = lemmatizer.lemmatize(pos_tag[0][0])
        if lemma not in custom_stop_words:
            phrase = lemma
        elif 'VB' in pos_tag[0][1]:
            lemma = lemmatizer.lemmatize(pos_tag[0][0], 'v')
        if lemma not in custom_stop_words:
            phrase = lemma
        
    return phrase


def get_phrases(fname):
    """
        Extract key phrases fromthe json response of the Microsoft Text Analytics Api
    Args: 
        fname: json file name 
    Return: 
        None
        Saves the extracted phrases (coma separated for a single description and '\n' separated for 2 different descriptions)
    """
    with open(fname) as f:
        data = f.read().casefold()
        data = json.loads(data)
        
    keyPhrases = []
    for i in data['documents']:
        keyPhrases.append(i['keyphrases'])
    
    histo = {}
    
    for keyPhrase in keyPhrases:
        for phrase in keyPhrase:
            if len(phrase.split()) == 1 and phrase in custom_stop_words: 
                continue
            if len(phrase.split()) == 1:
                pos_tag = nltk.pos_tag(nltk.word_tokenize(phrase))
                if 'NN' in pos_tag[0][1] or 'NP' in pos_tag[0][1]:
                    lemma = lemmatizer.lemmatize(pos_tag[0][0])
                    if lemma not in custom_stop_words:
                        phrase = lemma
                elif 'VB' in pos_tag[0][1]:
                    lemma = lemmatizer.lemmatize(pos_tag[0][0], 'v')
                    if lemma not in custom_stop_words:
                        phrase = lemma

            histo[phrase] = histo.get(phrase, 0) + 1
    
    result = sorted(histo.items(), key = lambda x : x[1], reverse = True)

    with open('KeyPhrasesOfDescriptions.txt', 'w') as f:
        for keyPhrase in keyPhrases:
            for phrase in keyPhrase:
                if phrase in histo:
                    if len(phrase.split()) == 1:
                        phrase = get_lemma(phrase)
                    f.write(phrase + ', ')
            f.write('\n')
            
if __name__ == '__main__':
    get_phrases('keyPhrases.json')
    print('Done')