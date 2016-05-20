import os
import math
def create_tfidf(dataset, sentences, wordtoid):
    words_to_document_sentence_id_word ={}
    words_to_document_sentence_id = {}
    document_sentence_id_to_word_id_dict = {}
    for line in wordtoid:
        line = line.strip()
        info = line.split('|')
        word = info[0]
        document_sentence_word_id = info[1]
        document_sentence_id = "_".join(document_sentence_word_id.split("_")[:-1])
        if not document_sentence_id in document_sentence_id_to_word_id_dict:
            document_sentence_id_to_word_id_dict[document_sentence_id] = [(word, document_sentence_word_id)]
        else:
            temp = document_sentence_id_to_word_id_dict[document_sentence_id]
            temp.append((word, document_sentence_word_id))
            document_sentence_id_to_word_id_dict[document_sentence_id] = temp
    for line in sentences:
        line = line.strip()
        info = line.split('|')
        document_sentence_id = info[0]
        sentence = info[1]
        words = sentence.split(' ')
        for word in words:
            if word not in words_to_document_sentence_id:
                words_to_document_sentence_id[word] = [document_sentence_id]
                for obj in document_sentence_id_to_word_id_dict[document_sentence_id]:
                    wordtocomp = obj[0]
                    if word == wordtocomp:
                        #print word, wordtocomp, obj
                        document_sentence_word_id = obj[1]
                        words_to_document_sentence_id_word[word] = [document_sentence_word_id]
            else:
                temp = words_to_document_sentence_id[word]
                temp.append(document_sentence_id)
                words_to_document_sentence_id[word] = temp
                temp = words_to_document_sentence_id_word[word]
                for obj in document_sentence_id_to_word_id_dict[document_sentence_id]:
                    wordtocomp = obj[0]
                    if word == wordtocomp:
                        document_sentence_word_id = obj[1]
                        if not document_sentence_word_id in words_to_document_sentence_id_word[word]: 
                            words_to_document_sentence_id_word[word] = [document_sentence_word_id]
                            temp.append(document_sentence_word_id)
                words_to_document_sentence_id_word[word] = temp
               
        
    writer = open('D:\\Dropbox\\241 Software Solutions\\Studie\\MA-Thesis\\Maurits\\Data\\EventTask\\Preproccesing\\word_Crowd_TF_IDFVALUES.csv', 'w+')
    document_sentence_wordid_TF_CROWD_pos = {}
    document_sentence_wordid_IDF_CROWD_pos ={}
    document_sentence_wordid_TF_CROWD_neg = {}
    document_sentence_wordid_IDF_CROWD_neg ={}
    document_sentence_wordid_TFDIDF_CROWD_neg = {}
    sentence_to_annotation_counts = {}
    document_sentence_word_id_counts = {}
    document_sentence_wordid_TFDIDF_CROWD_pos = {}
    for line in dataset:
        info = line.split("|")
        document_sentence_word_id = info[0] 
        crowdCount = int(info[1])
        document_sentence_word_id_counts[document_sentence_word_id] = crowdCount
        document_sentence_id = "_".join(document_sentence_word_id.split("_")[:-1])
        if not document_sentence_id in sentence_to_annotation_counts:
            
            sentence_to_annotation_counts[document_sentence_id] = crowdCount
        else:
            sentence_to_annotation_counts[document_sentence_id] += crowdCount
    for document_sentence_word_id in document_sentence_word_id_counts:
        document_sentence_id = "_".join(document_sentence_word_id.split("_")[:-1])
        total_annotation_count = sentence_to_annotation_counts[document_sentence_id]
        word_annotation_count = document_sentence_word_id_counts[document_sentence_word_id]
        document_sentence_wordid_TF_CROWD_pos[document_sentence_word_id] = float(word_annotation_count)/float(15)
        document_sentence_wordid_TF_CROWD_neg[document_sentence_word_id] = float(15.0-word_annotation_count)/float(15)
    
    for word in words_to_document_sentence_id:
        if word == ',':
            document_sentence_wordid_IDF_CROWD_pos[word] = 0.0
            document_sentence_wordid_IDF_CROWD_neg[word] = 0.0
        else:
            
            if word == 'believe':
                print len(words_to_document_sentence_id[word])
            totalsentences = len(words_to_document_sentence_id[word])
            totalsum= 0.0
            totalsumneg =0.0
            for document_sentence_word_id in words_to_document_sentence_id_word[word]:
                #print document_sentence_wordid_TF_CROWD[document_sentence_word_id]
                totalsum+=(document_sentence_wordid_TF_CROWD_pos[document_sentence_word_id]*15.0)
                totalsumneg+= (document_sentence_wordid_TF_CROWD_neg[document_sentence_word_id]*15.0)
                #print '*******'
            if word == 'believe':
                print totalsum
            #print word, totalsentences, totalsum, words_to_document_sentence_id[word],math.log((totalsentences*15.0)), math.log((totalsentences*15.0)/ totalsum)
            try:
                #document_sentence_wordid_IDF_CROWD_pos[word] =1/math.log((totalsentences*15.0)/ totalsum, 10)
                document_sentence_wordid_IDF_CROWD_pos[word] =math.log(1+(totalsentences*15.0)/ totalsum, 10)
            except :
                document_sentence_wordid_IDF_CROWD_pos[word] = 0.0
            #print 1.0/math.log((totalsentences*15.0)/ totalsumneg)
            try:
                document_sentence_wordid_IDF_CROWD_neg[word] =math.log(1+(totalsentences*15.0)/ totalsumneg, 10)
            except :
                document_sentence_wordid_IDF_CROWD_neg[word] = 0.0
        
    for word in document_sentence_wordid_IDF_CROWD_pos:
        for document_sentence_word_id in words_to_document_sentence_id_word[word]:
            #print word, document_sentence_wordid_TF_CROWD[document_sentence_word_id], document_sentence_wordid_IDF_CROWD[word]
            
            document_sentence_wordid_TFDIDF_CROWD_pos[document_sentence_word_id] = document_sentence_wordid_TF_CROWD_pos[document_sentence_word_id]*document_sentence_wordid_IDF_CROWD_pos[word]
            document_sentence_wordid_TFDIDF_CROWD_neg[document_sentence_word_id] = document_sentence_wordid_TF_CROWD_neg[document_sentence_word_id]*document_sentence_wordid_IDF_CROWD_neg[word]
    print 'tf',document_sentence_wordid_TF_CROWD_pos['ABC19980108.1830.0711_20_1']
    print 'idf', document_sentence_wordid_IDF_CROWD_pos['believe']
    normalized_pos = {}
    normalized_neg ={}

    posvalues = document_sentence_wordid_TFDIDF_CROWD_pos.values()
    minpos = min(posvalues)
    maxpos = max(posvalues)
    negvalues = document_sentence_wordid_TFDIDF_CROWD_neg.values()
    minneg = min(negvalues)
    maxneg = max(negvalues)
    print minpos, maxpos
    print minneg, maxneg
                
        
    for key in document_sentence_wordid_TF_CROWD_pos:
        #print document_sentence_wordid_TFDIDF_CROWD_pos[key]
        #print document_sentence_wordid_TFDIDF_CROWD_neg[key]
        #normalized_pos[key] = (document_sentence_wordid_TFDIDF_CROWD_pos[key]-min(minpos, minneg))/(max(maxpos,maxneg)-min(minpos, minneg))
        #normalized_neg[key] = (document_sentence_wordid_TFDIDF_CROWD_neg[key]-min(minpos, minneg))/(max(maxpos,maxneg)-min(minpos, minneg))
        
        writer.write(key+'|'+str(document_sentence_wordid_TFDIDF_CROWD_pos[key])+'|'+str(document_sentence_wordid_TFDIDF_CROWD_neg[key]))
        writer.write('\n')
    writer.flush()   
    os.fsync(writer.fileno())
    writer.close()          
    return document_sentence_wordid_TF_CROWD_pos , document_sentence_wordid_TF_CROWD_pos


dataset = open('word_Crowd_classifications_FinalCrowdClassifications.csv', 'r')
sentences = open ('sentences.txt', 'r')
wordtoid =  open ('wordtoid.txt', 'r')
create_tfidf(dataset,sentences,wordtoid)
