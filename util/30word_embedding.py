import numpy as np
import pickle as cPickle

# import word2vec file with the format: word, vector
# change the path to the one containing your word2vec 
dic_file = open("./word2vec/word2vec_laptop.txt", "r")
dic = dic_file.readlines()
dic_file.close()

dictionary = {}

index = 0
for line in dic:
    if(index == 0):
        index = index + 1
        continue
    index = index + 1
    word_vector = line.split(" ")

    i = 1
    while '.' not in word_vector[i] or '..' in word_vector[i] or word_vector[i] == '.':
        i += 1
        
    word = ' '.join(word_vector[:i])
    
    vector_list = []
    for element in word_vector[i:len(word_vector)-1]:
        vector_list.append(element)
        
    vector = np.asarray(vector_list)
    dictionary[word] = vector



final_input = cPickle.load(open("data_semEval/final_laptop_train_input", "rb"))
vocab = final_input[0]

word_embedding = np.zeros((300, len(vocab)))

count = 0

for ind, word in enumerate(vocab):
    if word in dictionary.keys():
        vec = dictionary[word]
        row = 0
        for num in vec:
            word_embedding[row][ind] = float(num)
            row += 1
        count += 1
    else:
        print(word)
        for i in range(100):
            word_embedding[i][ind] = 2 * np.random.rand() - 1
    
print(len(vocab))
print(count)
#print word_embedding


cPickle.dump(word_embedding, open("data_semEval/word_embeddings_laptop", "wb"))
