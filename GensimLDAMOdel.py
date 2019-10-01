import gensim
from gensim import corpora, models
from preprocessing import get_sentenses

def run_lda(num_topics, fname):

	processed_result = get_sentenses(fname)
	texts = []
	discriptions = []
	
	with open('finalDataSet_2.txt') as f:
		dataSet = f.readlines()
	with open('KeyPhrasesOfDescriptions.txt') as f:
		KeyPhrases = f.readlines()
		
	data_to_keyPhrases = {}
	for i in range(len(dataSet)):
		data_to_keyPhrases[KeyPhrases[i]] = dataSet[i]
	
	for sentense in processed_result:
		temp = sentense.split()
		texts.append(temp)
		discriptions.append(processed_result[sentense])
	
	dictionary = corpora.Dictionary(texts)
	corpus = [dictionary.doc2bow(text) for text in texts]
	LDAModel = gensim.models.ldamodel.LdaModel(corpus, num_topics = num_topics, id2word = dictionary, passes = 30)
	
	topic_probabilities = {}
	for i in range(len(corpus)):
		temp = LDAModel.get_document_topics(corpus[i], minimum_probability = 0.75)
		if len(temp) == 0:
			continue
		topic_probabilities[discriptions[i]] = temp[0][0]
	
	cluster = []
	
	for topic_no in range(num_topics):
		temp = ''
		for comment in topic_probabilities:
			if topic_probabilities[comment] == topic_no:
				temp += data_to_keyPhrases[comment]
		cluster.append(temp)
	
	topics = LDAModel.print_topics(num_topics = num_topics, num_words = 10)
	
	for i in topics:
		print(i[1])
	
	fhand = open('cluster_LDA_1.txt', 'w')
	
	for i in cluster:
		fhand.write(i + '\n\n\n')
		
	fhand.close()
	
if __name__ == "__main__":
	run_lda(8, 'KeyPhrasesOfDescriptions.txt')