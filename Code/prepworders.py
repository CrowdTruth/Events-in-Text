import csv
import statistics
import Metrics
import create_analysis
import plotdistributions
import sys
import os


def removekey(d, key):
    r = dict(d)
    del r[key]
    return r

def getcrowdspans(row, lensentence):
    aspect_class = {}
    annotations = [0 for i in range(0,lensentence+1)]
    #print len(annotations)
    
    for i in range(12, 42):
       annotation = row[i].replace("'", '').replace(".", "").strip()
       
       #print len(annotation)
       if len(row[102]) > 1:
           annotations[lensentence]=1
        
       elif len(annotation) > 0:
           if i == 23:
               aspect_annotation  =row[i+20]
               class_annotation = row[i+50]
           elif i == 34:
               aspect_annotation  =row[i+20]
               class_annotation = row[i+50]
           elif i == 13:
               aspect_annotation  =row[i+31]
               class_annotation = row[i+52]
           else:
                aspect_annotation  =row[i+30]
                class_annotation = row[i+60]
           if aspect_annotation == '' or class_annotation == '':
               print i, row[136] , annotation,aspect_annotation, class_annotation
           aspect_class[annotation] = (aspect_annotation, class_annotation)
           splitannotation = annotation.split('-')
           if len(splitannotation) >1 :
               #annotations.append(annotation)
               for j in range(int(splitannotation[0]), int(splitannotation[1])+1):
                   #print j
                   if j+1 <= lensentence:
                       annotations[j] = annotations[j]+1
                   else:
                         print   row ,  lensentence
               
               
           else:
                 #print"lensentence", lensentence
                 #print int(splitannotation[0])
                 
                 annotations[int(splitannotation[0])] = annotations[int(splitannotation[0])]+1
   # print "annotations", annotations,aspect_class
    return annotations , aspect_class


def getcrowdspans_as_spans(row, lensentence):
    maxindex = len(row[136].split(' '))
    #print maxindex
    #print row[136]
    annotations = []
    aspect_class= {}
    #print len(annotations)
    if len(row[102]) > 1:
        annotations.append(str(maxindex+5))
    for i in range(12, 42):
       annotation = row[i].replace("'", '').replace(".", "").strip()
       if len(annotation) > 0:
           if i == 23:
               aspect_annotation  =row[i+20]
               class_annotation = row[i+50]
           elif i == 34:
               aspect_annotation  =row[i+20]
               class_annotation = row[i+50]
           elif i == 13:
               aspect_annotation  =row[i+31]
               class_annotation = row[i+52]
           else:
                aspect_annotation  =row[i+30]
                class_annotation = row[i+60]
           annotations.append(annotation)
           aspect_class[annotation] = (aspect_annotation, class_annotation)
    return remove_singletons(clean_spans(annotations)) , aspect_class


def remove_singletons(annotations):
    for i in range(0, len(annotations)):
         if len(annotations[i].split('-')) ==1:
             annotations[i] = annotations[i]+'-'+annotations[i]
    return annotations

def clean_spans(annotations):
    return annotations
    i = 0
    for i in range(0, len(annotations)-1):
        if len(annotations[i].split('-')) > 1:
           if len(annotations[i+1].split('-')) == 1:
               #print  (annotations[i].split('-'))
               if int(annotations[i+1]) - int( annotations[i].split('-')[1]) == 1:
                   annotations[i] = str(annotations[i].split('-')[0]) +'-' + str(annotations[i+1])
                   annotations.pop(i+1)
                   clean_spans(annotations)
                   break
                   
        elif len(annotations[i].split('-')) ==1:
            if len(annotations[i+1].split('-')) == 1:
                if int(annotations[i+1]) - int( annotations[i]) == 1:
                    annotations[i] =str(annotations[i]) +'-' + str(annotations[i+1])
                    annotations.pop(i+1)
                    clean_spans(annotations)
                    break
        
        elif len(annotations[i].split('-')) == 1:
           if len(annotations[i+1].split('-')) > 1:
               if int(annotations[i+1].split('-')[2]) - int( annotations[i]) == 1:
                   annotations[i] = str(annotations[i]) +'-' + str(annotations[i+1].split('-')[1])
                   annotations.pop(i+1)
                   clean_spans(annotations)
                   break
    return annotations
                     
                 
def create_clear_file_new(worker_dict, workerquality):
    #broken
    clearfileath = os.path.join(eventsPath,'clearfile.txt')
    f = open(clearfileath, 'w')
    for worker in sentencestoworker:
        a = workerquality[worker][0]
        wss = workerquality[worker][1]
        nra = workerquality[worker][2]
        ava = workerquality[worker][3]
        sentences = worker_dict[worker]
        for sentence in sentences:
            spansinwords =[]
            spans = worker_dict[worker][sentence]
            for span in spans:
                words = set(range(int(span.split('-')[0]),int(span.split('-')[1])+1))
                #print words, sentence, len(sentence.split(" "))
                annotationinwords = []
                for word in words:
                    if word < 999:
                        splitsentence = sentence.split(" ")
                        try:
                            annotationinwords.append(splitsentence[word])
                        except :
                            print splitsentence, word, len(splitsentence), span
                    else:
                        annotationinwords.append("no-event-in-text")
                spansinwords.append(" ".join(annotationinwords))
                    
                    
                #print worker, sentence, words,annotationinwords
            f.write(str(worker)+"|"+ str(sentence)+"|"+str(spansinwords)+"|"+str(a)+"|"+str(wss)+"|"+str(nra)+"|"+str(ava))
            f.write('\n')
            
    f.close()                          
                 
            
def create_clear_file(worker_dict):
    notspammers = []
    clearfileath = os.path.join(eventsPath,'clearfile.txt')
    f = open(clearfileath, 'w')
    for worker in sentencestoworker:
        sentences = worker_dict[worker]
        for sentence in sentences:
            spansinwords =[]
            annotationsTotalVector = []
            spans = worker_dict[worker][sentence]
            for span in spans:
                words = set(range(int(span.split('-')[0]),int(span.split('-')[1])+1))
                for w in words:
                    annotationsTotalVector.append(w)
                #print words, sentence, len(sentence.split(" "))
                annotationinwords = []
                for word in words:
                    if word < 999:
                        splitsentence = sentence.split(" ")
                        try:
                            annotationinwords.append(splitsentence[word])
                        except :
                            print splitsentence, word, len(splitsentence), span, annotationsTotalVector
                    else:
                        annotationinwords.append("no-event-in-text")
                        notspammers.append(worker)
                spansinwords.append(" ".join(annotationinwords))
                    
                    
                #print worker, sentence, words,annotationinwords
            words = ""
            for word in spansinwords:
                words = words+word+'| '
            f.write(str(worker)+"|"+ str(sentence)+"|"+words.strip()+"|"+str(len(spansinwords))+"|"+str(annotationsTotalVector))
            f.write('\n')
            
    f.close()
    return notspammers


def create_sentence_class_aspect_file(sentece_class_aspect_dict,sentencestoid):
    sentence_annotations_wordspath = os.path.join(eventsPath,'sentence_annotations_class_aspect.csv')

    f = open(sentence_annotations_wordspath, 'w')
    for worker in sentece_class_aspect_dict:
        sentences = sentece_class_aspect_dict[worker]
        for sentence in sentences:
            spans = sentece_class_aspect_dict[worker][sentence]
            totalspans = []
            total_aspect = []
            total_class = []
            towrite = ''
            
            for span in spans:
                totalspans.append(span)
                total_aspect.append(sentece_class_aspect_dict[worker][sentence][span][0])
                total_class.append(sentece_class_aspect_dict[worker][sentence][span][1])
                
                
                
            for i in range(0, len(totalspans)):
                towrite += str(totalspans[i])+'|'+ str(total_aspect[i])+'|'+str(total_class[i])+'|'

            f.write(str(sentencestoid[sentence])+"|"+str(sentence).replace(" '"," ").replace("  ", " ")+"|"+str(len(totalspans))+"|"+towrite)
            f.write('\n')
            
    f.close()
            
            
            

def create_sentence_annotations_words(worker_dict,sentencestoid):
    notspammers = []
    sentence_annotations_wordspath = os.path.join(eventsPath,'sentence_annotations_words.csv')

    f = open(sentence_annotations_wordspath, 'w')
    for worker in sentencestoworker:
        sentences = worker_dict[worker]
        for sentence in sentences:
            annotationsTotalVector = []
            spansinwords =[]
            spans = worker_dict[worker][sentence]
            for span in spans:
                words = sorted(set(range(int(span.split('-')[0]),int(span.split('-')[1])+1)))
                for w in words:
                    annotationsTotalVector.append(w)
                #print words, sentence, len(sentence.split(" "))
                annotationinwords = []
                for word in words:
                    if word < 999:
                        splitsentence = sentence.split(" ")
                        try:
                            annotationinwords.append(splitsentence[word])
                        except :
                            print splitsentence, word, len(splitsentence), span, annotationsTotalVector
                    else:
                        annotationinwords.append("no-event-in-text")
                        notspammers.append(worker)
                spansinwords.append(" ".join(annotationinwords))
                    
                    
                #print worker, sentence, words,annotationinwords
            words = ""
            for word in spansinwords:
                words = words+word+'| '
            f.write(str(sentencestoid[sentence])+"|"+str(sentence).replace("  ", " ")+"|"+str(len(spansinwords))+"|"+words.strip()+str(spans)[1:len(str(spans))-1]+"|"+str(annotationsTotalVector))
            f.write('\n')
            
    f.close()
    return notspammers

   


     
#print Metrics.get_agreement_workers(sentencestoworker)
#print sentencestoworker
#print len(sentencestoworker)
#print create_analysis.get_total_number_of_videos(sentencestoworker)
#print create_analysis.get_unique_annotation_counts(sentencestoworker)
#print create_analysis.get_average_unique_video_annotations(sentencestoworker)
#print create_analysis.get_average_video_annotations(sentencestoworker)
#print create_analysis.get_average_annotations_per_worker_per_video(sentencestoworker)
#print create_analysis.get_video_annotation_popularity(sentencestoworker)

def get_metrics(sentencestoworker, fileing=True):

    

    worker_annotations =  Metrics.get_worker_annotations(sentencestoworker)
    #print worker_annotations

    #sentence_scores = Metrics.get_sentence_scores(sentencestoworker)
    """
    f = open('sentenceworkerstats.csv', 'w')
    for sentence in sentence_scores:
        f.write(sentence)
        agreements = sentence_scores[sentence][0]
        cosines = sentence_scores[sentence][1]
        f.write(",".join(map(str, agreements)))
        f.write(",".join(map(str, cosines)))
        f.write('\n')
    f.close()
    """
    #SPANS
    incommen =  Metrics.get_sentences_in_common(sentencestoworker)
    worker_worker_agreement_spans =  Metrics.get_agreement_worker_spans(incommen)
    worker_sentence_score_spans = Metrics.get_cosine_similarity_spans(sentencestoworker)
    #NO SPANS
    incommen_no_spans =  Metrics.get_sentences_in_common(sentencestoworkernospans)
    worker_worker_agreement = Metrics.get_worker_agreement_spans(sentencestoworker)   
    worker_sentence_score_no_spans = Metrics.get_cosine_similarity(sentencestoworkernospans)
    if fileing:
        workers = os.path.join(eventsPath,'workerstats.csv')
        f = open(workers, 'w')
    avgagr = 0
    avgagr_nospans = 0
    avgcosine_nospan =0
    avgcosine = 0
    avgworker_ann_sentences = 0
    avgworker_ann = 0
    workers = 0
    cosineworker = 0
    agreementlist= []
    cosinesimlist =[]
    worker_annotationslist =[]
    worker_annotations_annlist =[]
    cosinesimlistnospans =[]
    worker_worker_agreementlist = []
    worker_worker_agreementlist_nospan =[]
    workerstats  ={}
    #print "agreement ",worker_worker_agreement
    for worker in worker_worker_agreement_spans:
        if fileing:
            f.write(str(worker)+','+str(worker_worker_agreement_spans[worker])+','+str(worker_sentence_score_spans[worker])+','+str(worker_worker_agreement[worker])+','+str(worker_sentence_score_no_spans[worker])+','+str(worker_annotations[worker][0])+','+str(worker_annotations[worker][1])  )
        workerstats[worker] = (worker_worker_agreement_spans[worker],worker_sentence_score_spans[worker],worker_worker_agreement[worker], worker_sentence_score_no_spans[worker] )
        #agreementlist.append(worker_worker_agreement_spans[worker])
        worker_worker_agreementlist_nospan.append(worker_worker_agreement[worker])
        worker_worker_agreementlist.append(worker_worker_agreement_spans[worker])
        worker_annotationslist.append(worker_annotations[worker][0])
        worker_annotations_annlist.append(worker_annotations[worker][1])
        avgagr +=worker_worker_agreement_spans[worker]
        avgagr_nospans+=worker_worker_agreement[worker]
        if worker_sentence_score_spans[worker] > 0:
            avgcosine +=worker_sentence_score_spans[worker]
            cosineworker+=1
            cosinesimlist.append(worker_sentence_score_spans[worker])
        #print cosinesim_nospans[worker]
        if worker_sentence_score_no_spans[worker] > 0:
            #print cosinesim_nospans[worker]
            avgcosine_nospan +=worker_sentence_score_no_spans[worker]
            #cosineworker+=1
            cosinesimlistnospans.append(worker_sentence_score_no_spans[worker])
        avgworker_ann_sentences +=worker_annotations[worker][0]
        avgworker_ann +=worker_annotations[worker][1]
        workers+=1
        if fileing:
            f.write('\n')
    if fileing:
        f.close()
    return workerstats,workers,cosineworker,avgagr,avgworker_ann_sentences,worker_worker_agreementlist_nospan,avgworker_ann,worker_worker_agreementlist,worker_annotationslist,avgcosine,worker_annotations_annlist,cosinesimlist,avgagr_nospans ,worker_worker_agreementlist_nospan ,avgcosine_nospan ,cosinesimlistnospans

files = ['f772125.csv','f767471.csv','f758722.csv','f755877.csv','f759591.csv','f760634.csv','f761975.csv' ]#['f755877andf757275.csv', 'f757275.csv']
#files = ['f755877.csv']
#files = ['test.csv']
fcombined= open('combinedTrain.csv', 'w')
sentencestoid =  {}
for line in open(files[0]):
    fcombined.write(line)
files.pop(0)
    
for filename in files:
    f = open(filename, 'r')
    f.next()
    for line in f:
        fcombined.write(line)
    f.close()
fcombined.close()
combinedfiles = ['combinedTrain.csv'] #add test
for filename in combinedfiles:
    eventsCounts = open(filename, 'r')
    eventsPath = os.getcwd()+'\\'+filename.split('.')[0]
    print eventsPath
    if not os.path.exists(eventsPath):
        os.makedirs(eventsPath)
    csvData = csv.reader(eventsCounts, delimiter=',', quotechar='"')
    headers = csvData.next()
    sentences = ()
    sentencestoworker= {} #sentence to workers
    sentencestoworkernospans = {}
    sentences_aspect_classtoworker_nospans = {}
    sentences_aspect_classtoworker = {}
    workerannotationspans={}
    workerannotationnospans={}
    #sentence, worker, annotations
    sentencesfilepath = os.path.join(eventsPath,'sentences.txt')
    f3 = open(sentencesfilepath, 'w')
    written =[]
    for row in csvData:
       # print row
        #workerannotationspans={}
        #workerannotation={}
        workerid = str(row[7])
        sentencetoadd = row[136]
        sentencetoaddid = row[135]
        sentencestoid[sentencetoadd] = sentencetoaddid
        if not sentencetoadd in written:
            f3.write(sentencetoaddid+"|"+sentencetoadd.replace("  ", " "))
            f3.write('\n')
            written.append(sentencetoadd)
        #sentencetoadd = sentencetoadd
        #print sentencetoadd
        #workerannotationspans[sentencetoadd] = getcrowdspans_as_spans(row, len(sentencetoadd.split(" ")))
        #workerannotationnospans[sentencetoadd] = getcrowdspans(row, len(sentencetoadd.split(" ")))
        if sentencetoadd not in sentences:
            sentences= sentences+(sentencetoadd,)

        if workerid in sentencestoworker:
            cursentences = sentencestoworker[workerid]
            cursentences_nospans = sentencestoworkernospans[workerid]
            cursentences_aspect_classtoworker = sentences_aspect_classtoworker [workerid]
            cursentences_aspect_classtoworker_nospans = sentences_aspect_classtoworker_nospans [workerid]
            
        else:
            cursentences = {}
            cursentences_nospans= {}
            cursentences_aspect_classtoworker = {}
            cursentences_aspect_classtoworker_nospans = {}
            
        annotations, aspect_class  =  getcrowdspans_as_spans(row, len(sentencetoadd.split(" ")))
        cursentences[sentencetoadd] = annotations
        sentencestoworker[workerid] = cursentences
        cursentences_aspect_classtoworker[sentencetoadd] = aspect_class
        sentences_aspect_classtoworker[workerid] = cursentences_aspect_classtoworker



        annotations, aspect_class  = getcrowdspans(row, len(sentencetoadd.split(" ")))
        cursentences_nospans[sentencetoadd] = annotations
        cursentences_aspect_classtoworker_nospans[sentencetoadd] = aspect_class
        sentences_aspect_classtoworker_nospans[workerid] = cursentences_aspect_classtoworker_nospans
        sentencestoworkernospans[workerid]= cursentences_nospans
        
    notspammers = create_clear_file(sentencestoworker)
    workerstats,workers,cosineworker,avgagr,avgworker_ann_sentences,worker_worker_agreementlist_nospan,avgworker_ann,worker_worker_agreementlist,worker_annotationslist,avgcosine,worker_annotations_annlist,cosinesimlist,avgagr_nospans ,worker_worker_agreementlist_nospan ,avgcosine_nospan ,cosinesimlistnospans = get_metrics(sentencestoworker,False)
    print '-----'
    print "AVERAGE worker_worker_agreement_spans, worker_sentence_score_spans, ANNOTATED SENTENCES, ANNOTATIONS"

    print avgagr/workers,avgcosine/cosineworker,avgworker_ann_sentences/workers,avgworker_ann/workers
    print '-----'
    print "STDEV worker_worker_agreement_spans, worker_sentence_score_spans, ANNOTATED SENTENCES, ANNOTATIONS"
    print statistics.stdev(worker_worker_agreementlist),statistics.stdev(cosinesimlist),statistics.stdev(worker_annotationslist),statistics.stdev(worker_annotations_annlist)
    print '-----'
    print "AVERAGE-STDEV worker_worker_agreement_spans, worker_sentence_score_spans, ANNOTATED SENTENCES, ANNOTATIONS"
    print avgagr/workers-statistics.stdev(worker_worker_agreementlist),avgcosine/cosineworker-statistics.stdev(cosinesimlist),avgworker_ann_sentences/workers-statistics.stdev(worker_annotationslist),avgworker_ann/workers-statistics.stdev(worker_annotations_annlist)



    print '-----'
    print "AVERAGE worker_worker_agreement, worker_sentence_score_no_spans, ANNOTATED SENTENCES, ANNOTATIONS"

    print avgagr_nospans/workers,avgcosine_nospan/cosineworker,avgworker_ann_sentences/workers,avgworker_ann/workers
    print '-----'
    print "STDEV worker_worker_agreement, worker_sentence_score_no_spans, ANNOTATED SENTENCES, ANNOTATIONS"
    print statistics.stdev(worker_worker_agreementlist_nospan),statistics.stdev(cosinesimlistnospans),statistics.stdev(worker_annotationslist),statistics.stdev(worker_annotations_annlist)
    print '-----'
    print "AVERAGE-STDEV worker_worker_agreement, worker_sentence_score_no_spans, ANNOTATED SENTENCES, ANNOTATIONS"
    print avgagr_nospans/workers-statistics.stdev(worker_worker_agreementlist_nospan),avgcosine_nospan/cosineworker-statistics.stdev(cosinesimlistnospans),avgworker_ann_sentences/workers-statistics.stdev(worker_annotationslist),avgworker_ann/workers-statistics.stdev(worker_annotations_annlist)
    print "AFTER SPAM"
    #print worker_worker_agreement_spans['30500146']
    T0 = avgagr/workers-statistics.stdev(worker_worker_agreementlist)
    T1=  avgcosine/cosineworker-statistics.stdev(cosinesimlist)
    T2 = avgagr_nospans/workers-statistics.stdev(worker_worker_agreementlist_nospan)
    T3 = avgcosine_nospan/cosineworker-statistics.stdev(cosinesimlistnospans)

    TP0 = avgagr/workers+statistics.stdev(worker_worker_agreementlist)
    TP1=  avgcosine/cosineworker+statistics.stdev(cosinesimlist)
    TP2 = avgagr_nospans/workers+statistics.stdev(worker_worker_agreementlist_nospan)
    TP3 = avgcosine_nospan/cosineworker+statistics.stdev(cosinesimlistnospans)
    #print T0, T1, T2, T3
    print sentencestoworker.keys()
    workerspammerspath = os.path.join(eventsPath,'workerspammers.csv')
    f = open(workerspammerspath , "w")
    for worker in sentencestoworker:
        if not worker in notspammers:
            try:
                if  workerstats[worker][2] < T2 and workerstats[worker][3] < T3:
                    #print worker
                    f.write(worker)
                    f.write(", Low")
                    f.write("\n")
                   # sentencestoworker =removekey(sentencestoworker, worker)
                    sentences_aspect_classtoworker =removekey(sentences_aspect_classtoworker, worker)
                    
                else:
                    f.write(worker)
                    #print worker
                    f.write(", Pass")
                    f.write("\n")
            

            except:
                print sys.exc_info()[0],  sys.exc_info()[1]
    f.close()

    notspammers = create_clear_file(sentencestoworker)
    create_sentence_annotations_words(sentencestoworker,sentencestoid)
    create_sentence_class_aspect_file(sentences_aspect_classtoworker,sentencestoid)
    #write to file  sorted(worker_worker_agreementlist)

    #plotdistributions.plot_distributions(sorted(worker_worker_agreementlist),"worker_worker_agreement_spans_spammers_full_task")
    #plotdistributions.plot_distributions(sorted(cosinesimlistnospans),"worker_sentence_score_no_spans_spammers_full_task")

    #plotdistributions.plot_distributions(sorted(worker_worker_agreementlist_nospan),"worker_worker_agreement_no_spans_spammers_full_task")

    #plotdistributions.plot_distributions(sorted(cosinesimlist),"worker_sentence_score_spans_spammers_full_task ")

            #remove worker from workerdict
    workerstats,workers,cosineworker,avgagr,avgworker_ann_sentences,agreementlist,avgworker_ann,worker_worker_agreementlist,worker_annotationslist,avgcosine,worker_annotations_annlist,cosinesimlist,avgagr_nospans ,worker_worker_agreementlist_nospan ,avgcosine_nospan ,cosinesimlistnospans = get_metrics(sentencestoworker,True)



    #print avgagr,avgcosine,avgworker_ann_sentences,avgworker_ann,workers,cosineworker
    print '-----'
    print "AVERAGE worker_worker_agreement_spans, worker_sentence_score_spans, ANNOTATED SENTENCES, ANNOTATIONS"

    print avgagr/workers,avgcosine/cosineworker,avgworker_ann_sentences/workers,avgworker_ann/workers
    print '-----'
    print "STDEV worker_worker_agreement_spans, worker_sentence_score_spans, ANNOTATED SENTENCES, ANNOTATIONS"
    print statistics.stdev(worker_worker_agreementlist),statistics.stdev(cosinesimlist),statistics.stdev(worker_annotationslist),statistics.stdev(worker_annotations_annlist)
    print '-----'
    print "AVERAGE-STDEV worker_worker_agreement_spans, worker_sentence_score_spans, ANNOTATED SENTENCES, ANNOTATIONS"
    print avgagr/workers-statistics.stdev(worker_worker_agreementlist),avgcosine/cosineworker-statistics.stdev(cosinesimlist),avgworker_ann_sentences/workers-statistics.stdev(worker_annotationslist),avgworker_ann/workers-statistics.stdev(worker_annotations_annlist)



    print '-----'
    print "AVERAGE worker_worker_agreement, worker_sentence_score_no_spans, ANNOTATED SENTENCES, ANNOTATIONS"

    print avgagr_nospans/workers,avgcosine_nospan/cosineworker,avgworker_ann_sentences/workers,avgworker_ann/workers
    print '-----'
    print "STDEV worker_worker_agreement, worker_sentence_score_no_spans, ANNOTATED SENTENCES, ANNOTATIONS"
    print statistics.stdev(worker_worker_agreementlist_nospan),statistics.stdev(cosinesimlistnospans),statistics.stdev(worker_annotationslist),statistics.stdev(worker_annotations_annlist)
    print '-----'
    print "AVERAGE-STDEV worker_worker_agreement, worker_sentence_score_no_spans, ANNOTATED SENTENCES, ANNOTATIONS"
    print avgagr_nospans/workers-statistics.stdev(worker_worker_agreementlist_nospan),avgcosine_nospan/cosineworker-statistics.stdev(cosinesimlistnospans),avgworker_ann_sentences/workers-statistics.stdev(worker_annotationslist),avgworker_ann/workers-statistics.stdev(worker_annotations_annlist)


    #print sorted(cosinesimlistnospans)
    #print statistics.stdev( cosinesimlistnospans )
    clar = Metrics.get_sentence_clarity(sentencestoworkernospans)
    sentencestatspath = os.path.join(eventsPath,'sentencestats.csv')
    f2 = open(sentencestatspath, 'w')

    for item in clar:
        #add number of annotations + number or ppl annotating
        f2.write(str(item).replace("  ", " ")+'|'+str(clar[item]))
        f2.write('\n')
    f3.close()
    f2.close()
    #plotdistributions.plot_distributions([sorted(agreementlist),sorted(cosinesimlistnospans) ,sorted(worker_worker_agreementlist) ,sorted(cosinesimlist)],["worker_worker_agreement_spans","worker_sentence_score_no_spans" ,"worker_worker_agreement_no_spans" ,"worker_sentence_score_spans "])
    #plotdistributions.plot_distributions(sorted(worker_worker_agreementlist),"worker_worker_agreement_spans_no_spammers_full_task")
    #plotdistributions.plot_distributions(sorted(cosinesimlistnospans),"worker_sentence_score_no_spans_no_spammers_full_task")

    #plotdistributions.plot_distributions(sorted(worker_worker_agreementlist_nospan),"worker_worker_agreement_no_spans_no_spammers_full_task")

    #plotdistributions.plot_distributions(sorted(cosinesimlist),"worker_sentence_score_spans_no_spammers_full_task ")


"""

#print Metrics.get_agreement_worker(a)
#avgnum =  Metrics.get_average_annotations_per_sentence(sentencestoworker)
cosinesim = Metrics.get_cosine_similarity(sentencestoworker)
sentencerelscore = Metrics.get_sentence_relation_score(sentencestoworker)
senntenceclarity =Metrics.get_sentence_clarity(sentencestoworker)
workersentencescore  =Metrics.get_worker_sentence_score(sentencestoworker)
#print cosinesim
#print sentencerelscore
print '---'
#print senntenceclarity
print '---'
#print workersentencescore[workersentencescore.keys()[6]]
"""

            
#output shoudl look like :
#Worker Agremeent avg, stdev, cosine avg, stdev 
   
 
