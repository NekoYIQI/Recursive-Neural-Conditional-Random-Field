from nltk import CoreNLPDependencyParser

dep_parser = CoreNLPDependencyParser(url='http://localhost:9000')
out_file = open('./data_semEval/laptop/raw_parse_laptop_test', 'w')
in_file = open('./data_semEval/laptop/laptop_test.txt', 'r')

for line in in_file:
	parse, = dep_parser.raw_parse(line)
	out_file.write(parse.to_conll(4))
	out_file.write('\n')

in_file.close()
out_file.close()
