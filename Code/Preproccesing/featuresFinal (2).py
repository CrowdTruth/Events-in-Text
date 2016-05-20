#create train, same way as before

#create test, using train lemmas, synsets
#for each line in test write sentencewordid, features, class
#needed : Trainsentences, Testsentences
import gerenate_synsets_final as gs
import os

def init_features(dataset):
    print "INIT FEATURES"
    allwords = []
    
    for line in dataset:
        #print line
        sentence = line.split('|')[1].replace("  ", " ").strip()
        for word in sentence.split(' '):
            if not word in allwords:
                allwords.append(word)

    print len(allwords)
    gs.init_synset_lemmas(allwords)
    print "DONE INIT FEATURES"



def create_features(dataset, filename, pos=False, mod=False, syn=False, lem=False):
    if pos:
        filename=filename+"_pos"
    if mod:
        filename=filename+"_mod"
    if syn:
        filename=filename+"_syn"
    if lem:
        filename=filename+"_lem"
    writer = open('D:\\Dropbox\\241 Software Solutions\\Studie\\MA-Thesis\\Maurits\\Data\\EventTask\\Preproccesing\\word_features_Final'+filename+'.csv', 'w')
    #writer2 = open('D:\\Dropbox\\241 Software Solutions\\Studie\\MA-Thesis\\Maurits\\Data\\EventTask\\Preproccesing\\word_features_Final'+filename+'_Laplace_smoothed.csv', 'w')
    for line in dataset:
       # print "GETTING LINE FEATURES"
        info = line.split('|')
        sentenceid = info[0]
        sentence = info[1].replace("  ", " ").strip()
        words = sentence.split(" ")
        words.insert(0, "START")
        words.insert(0, "START")
        #words.append("STOP")
        #words.append("STOP")
        print 'LINE'

        for i in range(2, len(words)):
            segment = words[i-2:i]
            document_sentence_wordid = sentenceid +"_"+ str(i-2)
            if pos:
                postagfeatures = gs.postags_to_vector(gs.get_postags([[str(i),str(i)]], sentence, posrange=2))
                print "Pos", sum(postagfeatures)
            if mod:
                modalities = gs.extract_modalities(segment)
                print  "Mod", sum(modalities)

            if syn:
                allsynset_features, segment_synsets = gs.generate_synset_features(segment)
                print segment_synsets
                print  "Syn", sum(allsynset_features)

            if lem:
                alllemma_features = gs.generate_lemma_feature(segment_synsets)
                print  "Lem",sum(alllemma_features)

            word_features_to_write = []
            if pos:
                word_features_to_write.extend(postagfeatures)
            if mod:
                word_features_to_write.extend(modalities)
            if syn:
                word_features_to_write.extend(allsynset_features)
            if lem:
                word_features_to_write.extend(alllemma_features)
            print sum (word_features_to_write)
            writer.write(str(document_sentence_wordid)+'|'+str(word_features_to_write)+'\n')
        #print "DONE GETTING LINE FEATURES"
    writer.flush()   
    os.fsync(writer.fileno())

    writer.close()      
            
        
                                        
def main():
    trainDataset =open('sample_only_sentences_0.csv','r')
    testDataset  =open('ExpertTest.csv', 'r')
    init_features(trainDataset)
    trainDataset.seek(0)
    print 'pos=True,mod=True,syn=True,lem=True' 
    create_features(trainDataset,'TrainFeatures', pos=True,mod=True,syn=True,lem=True)
    create_features(testDataset,'TestFeatures', pos=True ,mod=True,syn=True,lem=True)
    trainDataset.seek(0)
    testDataset.seek(0)
main()
