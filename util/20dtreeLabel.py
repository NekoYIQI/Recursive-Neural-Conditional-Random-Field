from dtree_util import *
import pickle as cPickle
from numpy import *

# import dependency parse trees
# f = open('data_semEval/raw_parse_laptop_train', 'r')
f = open('data_semEval/raw_parse_laptop_test', 'r')

indice = 0

data = f.readlines()
# in plist, each sentence is stored as a list of tuples(rel, [(ind1, word1), (ind2, word2)])
plist = []
tree_dict = []
vocab = []
rel_list = []

# import ground-truth aspect term labels and opinion term labels
# label_file = open('data_semEval/laptop_aspect_train.txt', 'r')
# label_sentence = open('data_semEval/train_laptop_opinion', 'r')

label_file = open('data_semEval/laptop_aspect_test.txt', 'r')
label_sentence = open('data_semEval/test_laptop_opinion', 'r')

vocab, rel_list, train_trees = cPickle.load(open("data_semEval/final_laptop_train_input", "rb"))

index = 1
for line in data:
    if line.strip():
        line_list = line.split('\n')
        line = line_list[0]
        rel_split = line.split('\t')
        # print(rel_split)
        word = rel_split[0]
        parent = rel_split[2]
        rel = rel_split[3]

        final_deps = (index, word, parent)
 
        plist.append((rel, final_deps))
        index += 1

    # each raw parsed dependency is separated by while space
    # line.strip() will return false if we have processed one sentence
    else:
        max_ind = -1
        print(plist)
        for rel, deps in plist:
            if deps[0] > max_ind:
                max_ind = deps[0]

        # load words into nodes, then make a dependency tree
        nodes = [None for i in range(0, max_ind + 1)]
        nodes[0] = 'ROOT'
        for rel, deps in plist:
            ind = deps[0]
            nodes[ind] = deps[1]
        print(nodes)

        tree = dtree(nodes)

        opinion_words = []
                   
        aspect_term = label_file.readline().rstrip()
        labeled_sent = label_sentence.readline().strip() #opinions
        
        aspect_BIO = {}
        
        #facilitate bio notation
        if labeled_sent != 'NIL':
            opinions = labeled_sent.split(', ')
            
            for opinion in opinions:
                op_list = opinion.split()[:-1]
                if len(op_list) > 1:
                    for ind, term in enumerate(nodes):
                        if term != None:
                            if term == op_list[0] and ind < len(nodes) - 1 and nodes[ind + 1] != None and nodes[ind + 1] == op_list[1]:
                                tree.get(ind).trueLabel = 3
                                for i in range(len(op_list) - 1):
                                    if nodes[ind + i + 1] != None and nodes[ind + i + 1] == op_list[i + 1]:
                                        tree.get(ind + i + 1).trueLabel = 4
                                    
                elif len(op_list) == 1:
                    for ind, term in enumerate(nodes):
                        if term != None:
                            if term == op_list[0] and tree.get(ind).trueLabel == 0:
                                tree.get(ind).trueLabel = 3
        
        if aspect_term != 'NULL':
            aspects = aspect_term.split(',')
                        
            #deal with same word but different labels
            for aspect in aspects:
                aspect = aspect.strip()
                #aspect is a phrase
                if ' ' in aspect:
                    aspect_list = aspect.split()
                    for ind, term in enumerate(nodes):
                        if term == aspect_list[0] and ind < len(nodes) - 1 and nodes[ind + 1] == aspect_list[1]:
                            tree.get(ind).trueLabel = 1
                            
                            for i in range(len(aspect_list) - 1):
                                if ind + i + 1 < len(nodes):
                                    if nodes[ind + i + 1] == aspect_list[i + 1]:
                                        tree.get(ind + i + 1).trueLabel = 2
                            break
                      
                #aspect is a single word
                else:
                    for ind, term in enumerate(nodes):
                        if term == aspect and tree.get(ind).trueLabel == 0:
                            tree.get(ind).trueLabel = 1
            
            
        # add dependency edges between nodes
        for rel, deps in plist:
            par_ind = int(deps[2])
            kid_ind = deps[0]
            tree.add_edge(par_ind, kid_ind, rel)

        print(tree.get_tree())
        tree_dict.append(tree)  
        
        for node in tree.get_nodes():
#             for training data
            # if node.word.lower() not in vocab:
            #     vocab.append(node.word.lower())

#             for testing data
            if node.word.lower() in vocab:
                node.ind = vocab.index(node.word.lower())
               
            # node.ind = vocab.index(node.word.lower())
            
            # for ind, rel in node.kids:
            #     if rel not in rel_list:
            #         rel_list.append(rel)

        plist = []
        index = 1
        indice += 1


print('rels: ', len(rel_list))
print('vocab: ', len(vocab))

cPickle.dump((vocab, rel_list, tree_dict), open("data_semEval/final_laptop_test_input", "wb"))


