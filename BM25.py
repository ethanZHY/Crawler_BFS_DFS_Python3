import math
import os
import operator

#=============================================================#
# Composed by Yu Zhang
# This SE works mainly the same with the Lucene based one,
# although you can not set up the directory of corpus and index
#=============================================================#


# raw document directory:
directory = r'raw/'

class ResultType:
    invIndex = {}
    dl = {}
    avdl = 0
    def __init__(self,index,dl,avdl):
        self.invIndex = index
        self.dl = dl
        self.avdl = avdl

# indexing module
def indexer(curpus_Dir):
    invIndex = {}
    dl = {}
    avdl = 0
    filelist = os.listdir(curpus_Dir)
    print("Creating index.......")
    for file in filelist:
        if (file == '.DS_Store'):
            continue
        path = curpus_Dir + file
        doc = open(path, 'r')
        source_code = doc.read()
        doc.close()
        list = []
        split_list = source_code.split(r' ')


        # process /s
        for word in split_list:
            if word != r' ' and word != '':
                # print(each)
                list.append(word)

        # document length dl
        dl.update({file: len(list)})
        # average doc length avdl
        avdl += len(list)/1000

        for word in list:
            if word not in invIndex.keys():
                invIndex.update({word:dict()})
            if file not in invIndex.get(word).keys():
                invIndex.get(word).update({file:1})
            else:
                invIndex[word][file] += 1
    print("Indexer ends")
    fx = open('index.txt', 'w')
    for item in invIndex:
        fx.write(item +':'+ str(invIndex.get(item)) + '\n')
    fx.close()
    # the indexer return a ResultType object that contains invertedList, dl, avdl
    result = ResultType(invIndex,dl,avdl)
    return result

# BM25 ranking module
#=======================================================#
# N : the total num of documents in collection
# R : num of relevant documents for this query
# ni : the num of documents containing term i
# ri : the num of relevant documents containing term i
# fi : term frequency of i in the document
# qfi : term frequency of i in the query
# k1 = 1.2      k2 = 100    b = 0.75
# dl : document length
# avdl : average document length
#=======================================================#
def BM25(result):
    N = 1000
    R = 0
    ri = 0
    k1 = 1.2
    k2 = 100
    b = 0.75
    while 1:
        # get query terms from keyboard input
        query = input("Enter the search query (q=quit):\n")

        # query end
        if (query == 'q'):
            print("Query ends")
            return

        # query process
        else:
            print("Query fetched: " + query)
            qfi = {}
            terms = query.split(r' ')
            termList = []
            for word in terms:
                if word != r' ' and word != '':
                    termList.append(word)
            for term in termList:
                if term not in qfi.keys():
                    qfi.update({term:1})
                else:
                    qfi[term] += 1
            print(qfi)

        # retrieve inverted lists : ni fi K
        doc2terms = {}
        for term in termList:
            ni = len(result.invIndex.get(term))
            for doc in result.invIndex.get(term):
                K = k1*((1-b+b*result.dl.get(doc)/result.avdl))
                fi = result.invIndex[term][doc]
                # calculate doc-per-term score first
                # then add them together to get doc score
                d2tScore = math.log( (ri+0.5)*(N-ni-R+ri+0.5)/(R-ri+0.5)*(ni-ri+0.5) )\
                           *( (k1+1)*fi*(k2+1)*qfi[term] )/( (K+fi)*(k2+qfi[term]) )
                if doc not in doc2terms.keys():
                    doc2terms.update({doc:d2tScore})
                else:
                    doc2terms[doc] += d2tScore
        Rank = sorted(doc2terms.items(), key=operator.itemgetter(1), reverse=True)
        fx = open('BM25_' + query + '.txt', 'w')
        i = 1
        print('query_id' + ' '*(len(query)-8) + ' Q0 ' + ' Rank ' + ' Doc_id '
              + ' '*46 + ' Score ' + ' '*2 +' System '+ '\n')
        fx.write('query_id' + ' ' * (len(query) - 8) + ' Q0 ' + ' Rank ' + ' Doc_id '
              + ' ' * 46 + ' Score ' + ' ' * 2 + ' System '+ '\n')
        for each in Rank:
            if i > 100:
                print('\n')
                break
            print(query + ' Q0  ' + str(i) + ' '*(6 - len(str(i))) + str(each[0])
                  + ' '*(54-len(each[0])) + str(each[1])[0:7] + '  '+ 'Ethan\'s'+ '\n')
            fx.write(query + ' Q0  ' + str(i) + ' '*(6 - len(str(i))) + str(each[0])
                  + ' '*(54-len(each[0])) + str(each[1])[0:7] + '  '+ 'Ethan\'s'+ '\n')
            i += 1
        fx.close()

result = indexer(directory)
BM25(result)

