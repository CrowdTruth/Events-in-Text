import operator
import os
import nltk
from nltk.parse import stanford
from nltk.tokenize import WhitespaceTokenizer
from nltk.corpus import wordnet as wn
all_synsets =[]
all_lemmas = []
previous_sentence_tagged = {}


def init_synset_lemmas(allwords):
    global all_synsets
    global all_lemmas
    for word in allwords:
        
        word_synsets = wn.synsets(word)
        for word_synset in word_synsets:
            if word_synset not in all_synsets:
                all_synsets.append(word_synset)
                for lemma in word_synset.lemmas():
                    if lemma.name() not in all_lemmas:
                        all_lemmas.append(lemma.name())
    print len(all_synsets)
    print len(all_lemmas)
                

    

def generate_synset_features(segment):
    allsynset_features = [0.0 for i in range(0, len(all_synsets))]
    segment_synsets = []
    for word in segment:
        try:
            word_synsets = wn.synsets(word)
            
            for wordsynset in word_synsets:
                allsynset_features[all_synsets.index(wordsynset)] +=1
        except:
            word_synsets = []
        segment_synsets.append(word_synsets)
        
    return allsynset_features, segment_synsets

def generate_lemma_feature(segment_synsets):
    alllemma_features = [0.0 for i in range(0, len(all_lemmas))]
    for synset in segment_synsets:
        if type(synset) != type(segment_synsets):
            synsetlist = [synset]
        else:
            synsetlist = list(synset)
        for synset in synsetlist:
            try:
                for lemma in synset.lemmas():
                    alllemma_features[all_lemmas.index(lemma.name())] += 1
            except:
                pass
    return alllemma_features
        
        
                       
def extract_modalities(segment):
    modalities = ['to', 'should', 'would', 'could','can', 'might']
    modalities_features = [0.0 for i in range(0, len(modalities))]
    for word in segment:
        if word in modalities:
            modalities_features[modalities.index(word)]+=1
    if sum(modalities_features) == 0.0:
        modalities_features.append(1.0)
    else:
        modalities_features.append(0.0)
    return modalities_features
            
                          
def get_postags(annotations, sentence,posrange):
    global previous_sentence_tagged
    #posrange = 2
    if str(sentence) in previous_sentence_tagged:
        postagsandwords = previous_sentence_tagged[str(sentence)]
    else:    
        os.environ['STANFORD_PARSER'] = os.getcwd() +'\\jars\\stanford-parser.jar'
        os.environ['STANFORD_MODELS'] = os.getcwd() +'\\jars\\stanford-parser-3.5.2-models.jar'
        #os.environ['JAVAHOME'] ="C:\\Program Files (x86)\\Java\\jre1.8.0_31\\bin\\java.exe"
        os.environ['JAVAHOME'] ="C:\Program Files (x86)\Java\jre1.8.0_65\\bin\\java.exe"
        #os.environ['JAVAHOME'] ="C:\Program Files (x86)\Java\jre1.8.0_45\\bin\\java.exe"
        #print sentences
        parser = stanford.StanfordParser(model_path=os.getcwd() +"\\jars\\englishPCFG.ser.gz")
        sentenceParsed = parser.parse_one([sentence])
        postagsandwords = sentenceParsed.pos()
        previous_sentence_tagged[str(sentence)] = postagsandwords
    postags = [i[1] for i in postagsandwords]
    #print postags 
    annotations_postags = []
    for annotation in annotations:
        annotationpostags = []
        start = int(annotation[0]) - posrange
        end = int(annotation[1]) + posrange
        for i in range(start, end+1):
            if i < 0:
                annotationpostags.append("S")
            elif i > len(postags)-1:
                annotationpostags.append("E")
            else:
                annotationpostags.append(postags[i])
        annotations_postags.append(annotationpostags)
    
    return annotations_postags
    
                
def postags_to_vector(postags):
    alltags = ['-RRB-','-LRB-','S','E','PRP$', 'VBG', 'VBD', '``', 'VBN', ',', "''", 'VBP', 'WDT', 'JJ', 'WP', 'VBZ', 'DT', 'RP', '$', 'NN', ')', '(', 'FW', 'POS', '.', 'TO', 'LS', 'RB', ':', 'NNS', 'NNP', 'VB', 'WRB', 'CC', 'PDT', 'RBS', 'RBR', 'CD', 'PRP', 'EX', 'IN', 'WP$', 'MD', 'NNPS', '--', 'JJS', 'JJR', 'SYM', 'UH']
    postag_vector = [0.0 for i in range(0, len(alltags))]

    for postag in postags:
        for realtag in postag:
            postag_vector[alltags.index(realtag)]+=1
        
    return postag_vector

  
        
