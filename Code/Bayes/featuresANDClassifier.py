import gerenate_synsets_final as gs
import os



from sklearn.feature_selection import SelectKBest, chi2
import sys, getopt
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import f1_score, precision_score, recall_score,classification_report,average_precision_score,accuracy_score
from sklearn.metrics import roc_curve, auc
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import average_precision_score
import datetime
import os
import matplotlib.pyplot as plt
import math
import warnings


def init_features(dataset, count ):
    print "INIT FEATURES"
    allwords = []
    c = 0 
    for line in dataset:
        #print line
        sentence = line.split('|')[1].replace("  ", " ").strip()
        for word in sentence.split(' '):
            if count == c :
                print len(allwords)
                return gs.init_synset_lemmas(allwords)
            if not word in allwords:
                allwords.append(word)
            c+=1

    print len(allwords)
    gs.init_synset_lemmas(allwords)
    print "DONE INIT FEATURES"



def create_features(dataset, count):
    print "COUNT", count
    features = []
    c = 0
    for line in dataset:
       # print "GETTING LINE FEATURES"
        info = line.split('|')
        sentenceid = info[0]
        sentence = info[1].replace("  ", " ").strip()
        words = sentence.split(" ")
        words.insert(0, "START")
        words.insert(0, "START")
        words.append("STOP")
        words.append("STOP")
        
        for i in range(2, len(words)-2):
            if c == count:
                print "RETURNING" 
                print c, count
                return features
                break
            
            segment = words[i-2:i+3]
            document_sentence_wordid = sentenceid +"_"+ str(i-2)
            postagfeatures = gs.postags_to_vector(gs.get_postags([[str(i),str(i)]], sentence, posrange=2))
            modalities = gs.extract_modalities(segment)
            allsynset_features, segment_synsets = gs.generate_synset_features(segment)
            alllemma_features = gs.generate_lemma_feature(segment_synsets)
            word_features_to_write = []
            word_features_to_write.extend(postagfeatures)
            word_features_to_write.extend(modalities)
            word_features_to_write.extend(allsynset_features)
            word_features_to_write.extend(alllemma_features)
            features.append(word_features_to_write)
            c+=1
    return features
        #print "DONE GETTING LINE FEATURES"




warnings.filterwarnings("ignore")

def read_files(classificationfile,weightfile, fasterread):
    classiciation_dict = {}
    features_dict = {}
    weights_dict = {}
    scaled_weight_dict = {}
    totalpos = 0.0
    totalneg = 0.0
    tocheck = classiciation_dict
    #print len(approvedfeatures)
    print 'reading weights'
    
    if weightfile:
        print weightfile
        for line in open(weightfile):
            info = line.split("|")
            document_sentence_wordid = info[0]
            weightpos = float(info[1])
            weightneg = float(info[2])
            weights_dict[document_sentence_wordid] = (weightpos,weightneg)
            totalpos+=weightpos
            totalneg+=weightneg
        scalepos = totalpos/totalneg
        print scalepos
        for key in weights_dict:
            scaled_weight_dict[key] = ((weights_dict[key][0]/scalepos), weights_dict[key][1])
  
    
    print 'reading Classifications'
    with open(classificationfile) as test_classific_with_keys:
        for line in test_classific_with_keys:
            info= line.split('|')
            document_sentence_word_id = info[0]
            classification = int(info[1])
            classiciation_dict[document_sentence_word_id] = classification
    print 'reading Dataset'
   
    return classiciation_dict, weights_dict

def init_clf_nopriors():
        clf = MultinomialNB()
        return clf
def init_clf(priors):
        clf = MultinomialNB( class_prior= priors)
        return clf
def MB_partial_noW(Xtrain,ytrain, clf):
        #Xtrain, ytrain are np arrays
        try:
                clf.partial_fit(Xtrain, ytrain )
                print clf.class_count_
        except:
                print np.unique(ytrain)
                
                clf.partial_fit(Xtrain, ytrain, classes=np.unique(ytrain))
                print 'classcount', clf.class_count_
        return clf            

def MB_partial(Xtrain,ytrain, weights, clf):
        #Xtrain, ytrain are np arrays
        try:
                clf.partial_fit(Xtrain, ytrain, sample_weight=weights)
                print clf.class_count_
        except:
                print np.unique(ytrain)
                
                clf.partial_fit(Xtrain, ytrain, sample_weight=weights, classes=np.unique(ytrain))
                print 'classcount', clf.class_count_
        return clf

def MB_full(Xtrain,ytrain, weights, clf):
        #Xtrain, ytrain are np arrays
        try:
                clf.fit(Xtrain, ytrain, sample_weight=weights)
                print clf.class_count_
        except:
                print np.unique(ytrain)
                
                clf.fit(Xtrain, ytrain, sample_weight=weights, classes=np.unique(ytrain))
                print 'classcount', clf.class_count_
        return clf

def plot_classification_report(cr, title='Classification report ', with_avg_total=False, cmap=plt.cm.Blues):

    lines = cr.split('\n')

    classes = []
    plotMat = []
    for line in lines[2 : (len(lines) - 3)]:
        #print(line)
        t = line.split()
        # print(t)
        classes.append(t[0])
        v = [float(x) for x in t[1: len(t) - 1]]
        print(v)
        plotMat.append(v)

    if with_avg_total:
        aveTotal = lines[len(lines) - 1].split()
        classes.append('avg/total')
        vAveTotal = [float(x) for x in t[1:len(aveTotal) - 1]]
        plotMat.append(vAveTotal)

    plt.figure()
    plt.imshow(plotMat, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    x_tick_marks = np.arange(3)
    y_tick_marks = np.arange(len(classes))
    plt.xticks(x_tick_marks, ['precision', 'recall', 'f1-score'], rotation=45)
    plt.yticks(y_tick_marks, classes)
    plt.tight_layout()
    plt.ylabel('Classes')
    plt.xlabel('Measures')
    plt.savefig('Classification report.png')

def MB_test(preds, ytest):
        
        f1 =f1_score(ytest, preds, average=None)
        precision = precision_score(ytest, preds, average=None)
        recall = recall_score(ytest, preds, average=None)
        precisionbothclass = average_precision_score(ytest, preds)
        fpr, tpr, thresholds = roc_curve(ytest, preds)
        classifciationreprot =  classification_report(ytest, preds)
        f1 = f1.astype(float)
        precision = precision.astype(float)
        recall = recall.astype(float)
        return  f1, precision, recall,precisionbothclass, preds, fpr, tpr, thresholds ,classifciationreprot
    
def get_results(clf, X_test, y_test, typename):
    oldcwd = os.getcwd()
    os.chdir(currentrun)
   # for clf in Clfs:
    tempcwd = os.getcwd()
    dire = str(clf.class_prior) + typename
    if not os.path.exists(dire):
        os.makedirs(dire)
        os.chdir(dire)
   
    preds = clf.predict(np.array(X_test))
    
         
    print 'Getting ' + typename+' results...'         
    f1, precision, recall,precisionbothclass, preds,fpr, tpr, thresholds ,cr= MB_test(np.array(preds).astype(float), np.array(y_test).astype(float))
    
    fpr, tpr, thresholds = roc_curve(y_test, preds)
    roc_auc = auc(fpr, tpr)
    pr, rc,thr = precision_recall_curve(y_test, preds)
    #print precision_recall_curve(y_test, preds),  average_precision_score(y_test, preds, average="micro")
    #print accuracy_score(y_test, preds)
    average_precision = average_precision_score(y_test, preds, average="micro")
    
    plt.figure()
    plt.clf()
    plt.plot(pr, rc, label='Precision-Recall curve')
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.ylim([0.0, 1.05])
    plt.xlim([0.0, 1.0])
    plt.title('Precision-Recall Curve: AUC={0:0.2f}'.format(average_precision))
    plt.legend(loc="lower left")
    plt.savefig('Precision-Recall-Curve'+str(clf.class_prior)+'.png')



    roc_auc = auc(fpr, tpr)
    plt.figure()
    plt.plot([0, 1], [0, 1], 'k--')
    plt.plot(fpr, tpr, lw=1, label='ROC CrowdNB %s (area = %0.2f)' % (str(clf.class_prior), roc_auc))
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.legend(loc="lower right")
    plt.savefig('ROC'+str(clf.class_prior)+'.png')
    plt.close()
    plot_classification_report(cr)
    f = open('classificationreport.txt','w')
    f.write(str(cr))
    f.close()
    f = open('accuracy.txt','w')
    f.write(str(accuracy_score(y_test, preds)))
    f.close()
    #print str(precision)+','+str(recall)+','+str(f1)+','+str(precisionbothclass)
    os.chdir(tempcwd)
    os.chdir(oldcwd)   

def main_with_settings():
    fasterread =99999999999999999999999999999
    #run following : Expert traind on Expert with no weights for both features
    #Crowd Trained on expert no weights for both features
    #Crowd Trained on Crowd export weights both features
    #Expert run on crowdpartial with weights trained by expert both features
    global currentrun
    currentrun = os.path.join(os.getcwd(), datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
    currentrun = "double"
    if not os.path.exists(currentrun):
        os.makedirs(currentrun)
    #TODO ADD CHI2 ON FEATURES PER SET
    approvedfeatures = 0
    

    classificationfile = 'word_Crowd_classifications_FinalCrowdClassifications_one_zero.csv'
    #classificationfile = 'MV2.csv'
    
    #featurefile = 'word_features_FinalTrainFeatures_pos_mod_syn_lem.csv'
    weightfile = "clarweights.csv"
    classiciation_dictClarity, scaled_weight_dictClarity = read_files(classificationfile ,weightfile, fasterread)
    YClarity,WClarity, toaddOccurenceCountClarity = create_X_Y_W (classiciation_dictClarity, scaled_weight_dictClarity)

    #classificationfile = 'MV2.csv'
    classificationfile = 'word_Crowd_classifications_FinalCrowdClassifications_one_zero.csv'
    
    weightfile = "word_Crowd_TFIDFVALUES_proper.csv"
    classiciation_dictTFIDF, scaled_weight_dictTFIDF = read_files(classificationfile ,weightfile, fasterread)
    YTFIDF,WTFIDF,toaddOccurenceCountTFIDF  = create_X_Y_W (classiciation_dictTFIDF, scaled_weight_dictTFIDF)
    
    classificationfile = 'MV2.csv'
    
    weightfile = None
    print "DOING YMV"
    classiciation_dictMV, scaled_weight_dictMV = read_files(classificationfile ,weightfile, fasterread)
    YMV,WMV, toaddOccurenceCountMV = create_X_Y_W (classiciation_dictMV, scaled_weight_dictMV)
    print len(YMV), len(toaddOccurenceCountMV),len(WMV)  


    classificationfile = 'word_Expert_classifications_FinalExpertClassifications.csv'
    weightfile = None
    classiciation_dictTest, scaled_weight_dictTest = read_files(classificationfile ,weightfile, fasterread)
    Y_Test,_, _ = create_X_Y_W (classiciation_dictTest, scaled_weight_dictTest)

    
    print 'reading Test Dataset'
    print 'learnign rates'
    print len(YClarity)
    print len(toaddOccurenceCountClarity)
    YClarity = np.asarray(YClarity)
    YClarity =  np.repeat(YClarity, toaddOccurenceCountClarity, axis  = 0)
    WClarity =  np.repeat(WClarity, toaddOccurenceCountClarity, axis  = 0)
    YTFIDF =  np.repeat(YTFIDF, toaddOccurenceCountTFIDF, axis  = 0)
    WTFIDF =  np.repeat(WTFIDF, toaddOccurenceCountTFIDF, axis  = 0)
    print len(YMV)
    print len(toaddOccurenceCountMV)
    YMV =  np.repeat(YMV, toaddOccurenceCountMV, axis  = 0)
    #print len(toaddOccurenceCountMV), WMV.shape
    #WMV =  np.repeat(WMV, toaddOccurenceCountMV, axis  = 0)
    for i in range (100, len(YClarity), 100):
        trainDataset =open('sentences.txt','r')
        testDataset  =open('ExpertTest.csv', 'r')
        #if i > len(YClarity)
        print "Starting Init"
        init_features(trainDataset, i )
        print "Creating Train"
        
        
        X =  create_features(trainDataset, i)
        X = np.asarray(X)
        print X.shape, len(toaddOccurenceCountClarity[:i])
        if i > X.shape[0]:
            
             X =  np.repeat(X, toaddOccurenceCountClarity[:X.shape[0]], axis = 0)
        else:
             X =  np.repeat(X, toaddOccurenceCountClarity[:i], axis = 0)
            
        
        ch2 = SelectKBest(chi2, k='all')
        
        print "I Chi2", i
        print "Shape X chi2", X.shape
        print "Shape Y chi2", YClarity.shape
        print "Len Y chi2", len(YClarity[:i])
        ch2.fit_transform(X, YClarity[:X.shape[0]])
        scores = ch2.scores_
        toremove = []
        for j in range(0, len(scores)):
            if scores[j] < 10.83:
                toremove.append(j)
        print len(scores)," Features before features selection "
        print len(toremove)," Features Removed"
        print len(scores)-len(toremove), " Features Remaining"
        
        X = np.delete(X, toremove, 1)
        print len(X)
        print "Shape X", X.shape
        print "Shape Y", YClarity.shape,YMV.shape,  YTFIDF.shape
                
        clfsClaritySoFar = MB_partial(X,YClarity[:X.shape[0]],WClarity[:X.shape[0]], init_clf_nopriors())
        clfsCrowdTrainSoFar = MB_partial_noW(X,YMV[:X.shape[0]], init_clf_nopriors())
        clfsTFIDFSoFar =  MB_partial(X,YTFIDF[:X.shape[0]],WTFIDF[:X.shape[0]], init_clf_nopriors())
        print "Done Train"
        print "Creating Test"
        X_test = create_features(testDataset, 9499 )
        X_test = np.delete(X_test, toremove, 1)
        print "Getting Results"
        get_results(clfsClaritySoFar, X_test, Y_Test[:9499], 'Clarity TestResults_'+str(i))
        get_results(clfsCrowdTrainSoFar, X_test, Y_Test[:9499], 'CROWD Majority Voting TestResults_'+str(i))
        get_results(clfsTFIDFSoFar, X_test, Y_Test[:9499], 'TFIDF TestResults_'+str(i))
        trainDataset.close()
        testDataset.close()
    get_results(clf1, features_dictExpertTestLDA, classiciation_dictExpertTest, 'CrowdMajorityVoting')
    get_results(clf2, features_dictExpertTestLDA, classiciation_dictExpertTest, 'ExpertMajorityVoting')
    get_results(clf3, features_dictExpertTestLDA, classiciation_dictExpertTest, 'ExpertMajorityVoting')


   


    
def create_X_Y_W ( classification_dict, weights_dict):
    Y = []
    W = []
    #print weights_dict
   
    print len(classification_dict.values()),  sum(classification_dict.values())
       
    #print len(classification_dict.values())
    #print sum(classification_dict.values())
    possum = sum(classification_dict.values())
    negsum = len(classification_dict.values()) - sum(classification_dict.values())
    diff = negsum - possum
    plus = False
    neg = False
    if diff > 0 :
        plus = True
    else:
        neg = True
        diff = abs(diff)
    runningtotal = 0
    done = False
    toaddOccurenceCount = [1 for i in range(0, len(classification_dict.values()))]
    while not done:
        for j in range(0, len(classification_dict.keys())):
            key = classification_dict.keys()[j]
            if classification_dict[key] > 0:
                if plus:
                    toaddOccurenceCount[j]+=1
                    runningtotal+=1
                    #print runningtotal, diff
                    if runningtotal == diff:
                        done = True
                        break
            elif neg:
                toaddOccurenceCount[j]+=1
                runningtotal+=1
                #print runningtotal, diff
                if runningtotal == diff:
                    done = True
                    break

    for key in classification_dict:
        #print key
        
        if weights_dict:
            w1 = 1
            w2 =1
            if key in weights_dict:
                w = weights_dict[key]
                w1 = w[0]
                w2 = w[1]
        #if classification_dict[key] > 0:
            #for i in range(0, 10):
                
        Y.append(classification_dict[key])
        if weights_dict:
            W.append(w1)
        
        #else:
           
           
        Y.append(classification_dict[key])
        if weights_dict:
            W.append(w2)
        #print "dictvalue",classification_dict[key]
        #print 'print Y appneded',Y
        #break
        
    #print len(Y)
    print "weightsum"
    print len(W)
    #print len(toaddOccurenceCount)
    #print toaddOccurenceCount[:100]
    #print min(W)
    toaddOccurenceCount = np.repeat(toaddOccurenceCount, 2)
    return  np.asarray(Y), np.asarray(W), toaddOccurenceCount

      

if __name__ == "__main__":
   main_with_settings()





