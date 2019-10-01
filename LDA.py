import warnings
from gensim.scripts.word2vec2tensor import word2vec2tensor
warnings.filterwarnings(action = 'ignore', category = UserWarning, module = 'gensim')

from gensim import corpora
from gensim.models.wrappers import LdaMallet
import nltk
import json
from operator import itemgetter
from preprocessing import get_sentenses, processComment

class LDA:
    def __init__(self, fname, number_of_topics, number_of_lda_keywords, number_of_lda_keywords_processed, number_of_lda_keywords_for_assignment):
        
        self.number_of_topics = number_of_topics
        self.number_of_lda_keywords = number_of_lda_keywords
        self.number_of_lda_keywords_processed = number_of_lda_keywords_processed
        self.number_of_lda_keywords_for_assignment = number_of_lda_keywords_for_assignment
        self.total_topic_word = []

        self.get_topics(fname)
            
    def run_lda(self, processed_sentences):       
        lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()
        # list containing the final topic keywords
        topic_top_words = []
    
        documents = [comment.split() for comment in processed_sentences if comment]
        dictionary = corpora.Dictionary(documents)
        # Filter the words that occur in less than 5 comments or those that occur in more than half of the comments
        dictionary.filter_extremes(no_below=5, no_above=0.5)
        doc_term_matrix = [dictionary.doc2bow(doc) for doc in documents]
        mallet_path = 'C:\\Mallet-2.0.8\\bin\\mallet' 
        optimization_interval = 50
        lda_alpha = 1
    
        lda = LdaMallet(mallet_path, doc_term_matrix, num_topics=self.number_of_topics, id2word=dictionary, optimize_interval=optimization_interval, alpha=lda_alpha)
    
        # This list contains the word probabilities given a topic
        topic_words_and_probs = []

        for i in range(self.number_of_topics):
            # Get top number_of_lda_keywords_for_assignment words and corresponding probabilities for the topic
            topic_words_and_probs.append(lda.show_topic(i, topn = self.number_of_lda_keywords_for_assignment))
        
        for i in range(len(topic_words_and_probs)):
            temp = []
            for j in topic_words_and_probs[i]:
                if j[1] > 0.0:
                    temp.append(j)
                    self.total_topic_word.append(j[0])
            topic_words_and_probs[i] = temp
    
        for i in range(self.number_of_topics):
            # Get the top keywords for the topic and extract the top nouns
            topic_words = [component[0] for component in topic_words_and_probs[i]]
    
            final_topic_words = []
     
            for word in topic_words:
                if len(final_topic_words) >= self.number_of_lda_keywords:
                    break
     
                pos = nltk.pos_tag([word])
                word = lemmatizer.lemmatize(word)
                noun_tags = ['NN', 'NNS', 'NP', 'NPS']
                if word not in final_topic_words and pos[0][1] in noun_tags:
                    final_topic_words.append(word)
            topic_top_words.append(final_topic_words)
        return topic_top_words, topic_words_and_probs
    
    def process_result(self, processed_result, topic_top_words, topic_words_and_probs):
        # List containing the final result objects
        out = []
        processed_sentences = list(processed_result.keys())
        # Find the most appropriate topic for a comment by combining the topic-word probabilities and normalizing them
        for idx, comment in enumerate(processed_sentences):
            if comment:
                max_probability = 0
                best_topics = []
                words = comment.split(' ')
                useful_words_len = 0
                
                for word in words:
                    if word in self.total_topic_word:
                        useful_words_len += 1

                for j in range(self.number_of_topics):
                    try:
                       # probability = sum([1.0 for component in topic_words_and_probs[j] if component[0] in words and component[1] > 0.01]) / float(useful_words_len)
                        probability = sum([1.0 for component in topic_words_and_probs[j] if component[0] in words and component[1] > 0.01]) / float(useful_words_len)  
                    except:
                        probability = 0
                    
                    if probability > 0.02:
                        best_topics.append(j)

                for topic in best_topics:
                    out.append({
                        'comment': processed_sentences[idx],
                        'topic': topic
                    })
                    
                if len(best_topics) == 0:
                    out.append({
                        'comment': processed_sentences[idx],
                        'topic': 'Other'
                    })
    
            else:
                out.append({
                    'comment': processed_sentences[idx],
                    'topic': None
                })
    
        return out
    
    def get_topics(self, fname):
        processed_result = get_sentenses(fname)
        topic_top_words, topic_words_and_probs = self.run_lda(list(processed_result.keys()))
        result = self.process_result(processed_result, topic_top_words, topic_words_and_probs)
        clusters = []
        actual_clusters = []
        with open('finalDataSet_2.txt') as f:
            dataSet = f.readlines()
        with open('KeyPhrasesOfDescriptions.txt') as f:
            KeyPhrases = f.readlines()
            
        data_to_keyPhrases = {}
        for i in range(len(dataSet)):
            data_to_keyPhrases[KeyPhrases[i]] = dataSet[i]
    
        for i in range(self.number_of_topics):
            temp = ''            
            temp1 = ''
            for j in result:
                if j['topic'] == i:
                    temp += j['comment'] + '\n\n'
                    temp1 += data_to_keyPhrases[processed_result[j['comment']]]
            clusters.append(temp)
            actual_clusters.append(temp1)
                        
        fhand = open('clusters.txt', 'w')
        
        for i in actual_clusters:
            fhand.write(i + '\n\n\n')
            
        fhand.close()

        for i in range(self.number_of_topics):
            clusters[i] = clusters[i].split()

        for i in range(len(clusters)):
            temp = []
            for word in clusters[i]:
                pos = nltk.pos_tag([word])
                noun_tags = ['NN', 'NNS', 'NP', 'NPS']
                if (pos[0][1] in noun_tags):
                    temp.append(word)
            clusters[i] = temp

        best_topic_words = []
        count = []
        for i in range(self.number_of_topics):
            temp = []
            temp2 = {}
            best_topic_words.append(temp)
            count.append(temp2)
             
        for i in range(len(clusters)):
            for word in clusters[i]:
                count[i][word.lower()] = count[i].get(word.lower(), 0) +1
             
        for i in range(len(best_topic_words)):
            top_words = sorted(count[i].items(), key = itemgetter(1), reverse = True)[ : 5]
            for word in top_words:
                best_topic_words[i].append((word[0], word[1]))
    
#         for i, val in enumerate(best_topic_words):
#             print(i + 1, ":", val)
#         print('\n\n')
#         for i, val in enumerate(topic_top_words):
#             print(i + 1, ":", val)

        return result
  
if __name__ == '__main__':  
    LDA(fname = 'KeyPhrasesOfDescriptions.txt', number_of_topics = 5, number_of_lda_keywords = 20, number_of_lda_keywords_processed = 50, number_of_lda_keywords_for_assignment = 500)
