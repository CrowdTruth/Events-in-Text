#Worker agreement  = number of words annotated the same

#needs worker per shared sentence

#{workerid : {sentence: vector}}
import operator
import csv
import scipy.spatial


def get_sentences_in_common(worker_dict):
    #sentences_in_common_dict = {worker: {worker2 : [[sentenceannotation_worker1], [sentenceannotation_worker2]]}}
    sentences_in_common_dict = {}
    for worker in worker_dict:        
        #print worker, sentencestoworker[worker]
        sentences = worker_dict[worker]
        for worker2 in worker_dict:
            if not worker == worker2:
                worker2annotations = []
                worker1annotations = []
                sentences2 = worker_dict[worker2]
                for sentence in sentences:
                    if sentence in sentences2:
                        worker1annotations.append(worker_dict[worker][sentence])
                        worker2annotations.append(worker_dict[worker2][sentence])
                if len(worker1annotations) > 0:
                    if worker in sentences_in_common_dict:
                        other_worker_sentences_in_common = sentences_in_common_dict[worker]
                    else:
                        other_worker_sentences_in_common = {}
                    sentences_in_common = [worker1annotations, worker2annotations]
                    other_worker_sentences_in_common[worker2] = sentences_in_common
                    sentences_in_common_dict[worker] = other_worker_sentences_in_common
    return sentences_in_common_dict

def get_worker_worker_agreement(sentences_in_common):
    #OUTPUT: score [0..1]
    sentence_annotations_worker_1 = sentences_in_common[0]
    sentence_annotations_worker_2 = sentences_in_common[1]
    if len(sentence_annotations_worker_1) == 0:
        return 0
    agreements = 0
    total_annotations = 0
    #print sentence_annotations_worker_2
    for i in range(0, len(sentence_annotations_worker_1)):
        annotations_worker_1 = sentence_annotations_worker_1[i]
        annotations_worker_2 = sentence_annotations_worker_2[i]
        total_annotations += sum(annotations_worker_1)
        for j in range(0, len(annotations_worker_1)):
            annotation_worker_1 = annotations_worker_1[j]
            annotation_worker_2 = annotations_worker_2[j]
            if annotation_worker_1 > 0 and annotation_worker_2 > 0:
                agreements += 1
    if total_annotations == 0:
        return 0
    return float(agreements)/total_annotations

def get_worker_agreement_spans(worker_dict):
    #OUTPUT: {worker : agreement}
    worker_agreement = {}
    worker_worker_sentences_in_common = get_sentences_in_common(worker_dict)
    for worker in worker_worker_sentences_in_common:
        total_sentences_in_common = 0
        total_agr = 0
        other_workers_sentences_in_common = worker_worker_sentences_in_common[worker]
        for other_worker in other_workers_sentences_in_common:
            sentences_in_common = other_workers_sentences_in_common[other_worker]
            agrw_w = get_worker_worker_agreement_spans(sentences_in_common)
            total_agr += agrw_w*len(sentences_in_common[0])
            total_sentences_in_common += len(sentences_in_common[0])
        worker_agreement[worker] = float(total_agr)/total_sentences_in_common
    return worker_agreement


def get_worker_agreement(worker_dict):
    #OUTPUT: {worker : agreement}
    worker_agreement = {}
    worker_worker_sentences_in_common = get_sentences_in_common(worker_dict)
    for worker in worker_worker_sentences_in_common:
        total_sentences_in_common = 0
        total_agr = 0
        other_workers_sentences_in_common = worker_worker_sentences_in_common[worker]
        for other_worker in other_workers_sentences_in_common:
            sentences_in_common = other_workers_sentences_in_common[other_worker]
            agrw_w = get_worker_worker_agreement(sentences_in_common)
            total_agr += agrw_w*len(sentences_in_common[0])
            total_sentences_in_common += len(sentences_in_common[0])
        worker_agreement[worker] = float(total_agr)/total_sentences_in_common
    return worker_agreement

def get_worker_worker_agreement_spans(sentences_in_common):
    #OUTPUT: score [0..1]
    sentence_annotations_worker_1 = sentences_in_common[0]
    sentence_annotations_worker_2 = sentences_in_common[1]
    if len(sentence_annotations_worker_1) == 0:
        return 0
    agreements = 0.0
    total_annotations = 0.0
    for i in range(0, len(sentence_annotations_worker_1)):
        annotations_worker_1 = sentence_annotations_worker_1[i]
        annotations_worker_2 = sentence_annotations_worker_2[i]
        #print annotations_worker_1
        #print annotations_worker_2
        total_annotations += len(annotations_worker_1)
        for j in range(0, len(annotations_worker_1)):
            for k in range(0, len(annotations_worker_2)): 
                annotation_worker_1 = annotations_worker_1[j]
                annotation_worker_2 = annotations_worker_2[k]
                #print  annotation_worker_1 , annotation_worker_2
                if annotation_worker_1 == annotation_worker_2:
                    agreements += 1
                    #print "agreements",  agreements/total_annotations
                else:
                    annotation_worker1_range_set =  set(range(int(annotation_worker_1.split('-')[0]),int(annotation_worker_1.split('-')[1])+1))
                    annotation_worker2_range_set =  set(range(int(annotation_worker_2.split('-')[0]),int(annotation_worker_2.split('-')[1])+1))
                    """
                    if annotation_worker_1.split('-')[0] == annotation_worker_1.split('-')[1]:
                        annotation_worker1_range_set = set([annotation_worker_1.split('-')[0]])
                    if annotation_worker_2.split('-')[0] == annotation_worker_2.split('-')[1]:
                        annotation_worker2_range_set = set([annotation_worker_2.split('-')[0]])
                    print annotation_worker1_range_set , annotation_worker2_range_set
                    """
                    both_annotated_set = (annotation_worker1_range_set.intersection(annotation_worker2_range_set))
                    #print both_annotated_set
                    if len(both_annotated_set) > 0:
                        agreements += float(len(both_annotated_set)) /float(len(annotation_worker1_range_set))
                        #print" partial", float(len(both_annotated_set)) /float(len(annotation_worker1_range_set))
                        #print "agreements",  agreements/total_annotations
    #print "final - agreements",  agreements/total_annotations
    if total_annotations == 0:
        return 0
    return float(agreements)/total_annotations
    
def get_agreement_worker_spans(sentences_in_common_dict):
    #print sentences_in_common_dict
    #OUTPUT: worker_agreement_dict = {worker : score (0..1)}
    worker_agreement_dict = {}
    for worker in sentences_in_common_dict:
        other_workers = sentences_in_common_dict[worker]
        sum_agr = 0
        sum_sentences_in_common = 0
        for other_worker in other_workers:
            sentences_in_common = other_workers[other_worker]
            worker_worker_agreement = get_worker_worker_agreement_spans(sentences_in_common)
            sum_agr += worker_worker_agreement
            sum_sentences_in_common += len(sentences_in_common[0])
        if sum_sentences_in_common > 0:
            worker_agreement_dict[worker] = float(sum_agr)/sum_sentences_in_common
    return worker_agreement_dict#sorted(worker_agreement_dict.items(), key=operator.itemgetter(1))

def get_average_annotations_per_sentence(worker_dict):
    #OUTPUT: worker_annotations_per_sentence = {worker : average}
    worker_annotations_per_sentence = {}
    for worker in worker_dict:
        sentences = worker_dict[worker]
        total_annotations = 0
        total_sentences = len(sentences)
        for sentence in sentences:
            annotations = sentences[sentence]
            total_annotations += sum(annotations)
        if len(sentences) > 0:
            average_annotations = float(total_annotations)/total_sentences
        else:
            average_annotations = 0
        worker_annotations_per_sentence[worker] = average_annotations
    return worker_annotations_per_sentence

def get_sentence_annotations(sentence, worker_dict):
    #OUTPUT: total_annotations = [annotation]
    total_annotations = []
    for worker in worker_dict:
        sentences = worker_dict[worker]
        if sentence in sentences:
            annotations = sentences[sentence]
            #print worker,annotations, sentence
            if len(total_annotations) == 0:
                total_annotations = annotations
            else:
                #print total_annotations
                #print annotations
                total_annotations = [total_annotations[i]+annotations[i] for i in range(0, len(annotations))]
                #print total_annotations
    return total_annotations

def get_sentence_annotations_spans(sentence, worker_dict, workertocompare):
    #TODO, ADD PARTIALS
    #OUTPUT: total_annotations = [annotation]
    #print sentence
    tempannotations = []
    total_annotations = []
    worker_to_vec_annotations = []


    for worker in worker_dict:            
        sentences = worker_dict[worker]
        if sentence in sentences:
            annotations = sentences[sentence]
           # print annotations , worker
            if len(total_annotations) == 0:
                tempannotations = list(annotations)
                total_annotations = [1 for x in range(0, len(annotations))]
            else:
                for annotation in annotations:
                    if annotation in tempannotations:
                        total_annotations[tempannotations.index(annotation)] = total_annotations[tempannotations.index(annotation)] +1
                    else:
                        tempannotations.append(annotation)
                        total_annotations.append(1)
                #total_annotations = [total_annotations[i]+annotations[i] for i in range(0, len(annotations))]
       # print "total_annotations", total_annotations
    sentences2 = worker_dict[workertocompare]
    annotations2 = sentences2[sentence]
    
    #print 'total', total_annotations
    #print "order ", tempannotations
    #print "worker annotations" , annotations2, workertocompare
    workerannotatedsentence = [0 for x in range(0, len(total_annotations))]
    for annotation in annotations2:
        if annotation in tempannotations:
            #print annotation
           # print tempannotations.index(annotation)
           # print total_annotations[tempannotations.index(annotation)]
            total_annotations[tempannotations.index(annotation)] = total_annotations[tempannotations.index(annotation)] -1
            workerannotatedsentence[tempannotations.index(annotation)] = workerannotatedsentence[tempannotations.index(annotation)] +1
    #print workerannotatedsentence
    return total_annotations , workerannotatedsentence
            

def get_worker_annotations(worker_dict):
    #OUTPUT: {worker} = [annoations per unit avg , units annotated]
    worker_numbers = {}
    for worker in worker_dict:
        #print worker
        total_annotations = 0
        sentences = worker_dict[worker]
        total_units_annotated = len(sentences)
        for sentence in sentences:
            #print sentence
            annotations = sentences[sentence]
            #print annotations
            if total_annotations == 0:
                total_annotations = len(annotations)
            else:
                #print sum (annotations)
                total_annotations = total_annotations+ len(annotations)
        worker_numbers[worker] =[ total_units_annotated, total_annotations/total_units_annotated]
    return worker_numbers



def get_cosine_similarity_spans(worker_dict):
    #OUTPUT: worker_cosine = {worker : score}
    worker_cosine = {}
    for worker in worker_dict:
        sentences = worker_dict[worker]
        total_cosine = 0
        total_sentences = len(sentences)
        for sentence in sentences:
            worker_annotations = sentences[sentence]
            #print worker_annotations
            total_annotations, workerannotatedsentence = get_sentence_annotations_spans(sentence, worker_dict, worker)
            #print "total_annotations", total_annotations            
            #total_annotations = [total_annotations[i]-worker_annotations[i] for i in range(0, len(worker_annotations))]
            sentence_cosine = 1.0-scipy.spatial.distance.cosine(workerannotatedsentence,total_annotations)
            total_cosine += sentence_cosine
        if total_sentences > 0:
            average_cosine = float(total_cosine)/total_sentences
        else:
            average_cosine = 0
        worker_cosine[worker] = average_cosine
    return worker_cosine#sorted(worker_cosine.items(), key=operator.itemgetter(1))

def get_cosine_similarity(worker_dict):
    
    #OUTPUT: worker_cosine = {worker : score}
    worker_cosine = {}
    #print worker_dict
    for worker in worker_dict:
        #print worker
        sentences = worker_dict[worker]
        #print sentences
        total_cosine = 0
        total_sentences = len(sentences)
        for sentence in sentences:
            worker_annotations = sentences[sentence]
            #print sentences[sentence]
            total_annotations = get_sentence_annotations(sentence, worker_dict)
            #print total_annotations
            total_annotations = [total_annotations[i]-worker_annotations[i] for i in range(0, len(worker_annotations))]
            #print total_annotations, worker_annotations
            sentence_cosine = 1.0-scipy.spatial.distance.cosine(worker_annotations,total_annotations)
            #print sentence_cosine
            total_cosine += sentence_cosine
        if total_sentences > 0:
            average_cosine = float(total_cosine)/total_sentences
        else:
            average_cosine = 0
        worker_cosine[worker] = average_cosine
    return worker_cosine#sorted(worker_cosine.items(), key=operator.itemgetter(1))

def get_sentence_relation_score(worker_dict):
    #OUTPUT: sentence_relation_scores = {sentence : {relation : score}}
    sentence_relation_scores = {}
    for worker in worker_dict:
        sentences = worker_dict[worker]
        for sentence in sentences:
            if not sentence in sentence_relation_scores:
                relation_scores = {}
                total_annotations = get_sentence_annotations(sentence, worker_dict)
                for i in range(0, len(total_annotations)):
                    unit_vector = [0 for j in range(0, len(total_annotations))]
                    unit_vector[i] = 1
                    sentence_relation_score = 1.0-scipy.spatial.distance.cosine(unit_vector,total_annotations)
                    relation_scores[i] = sentence_relation_score
                sentence_relation_scores[sentence] = relation_scores
    return sentence_relation_scores


def get_sentence_clarity(worker_dict):
    #OUTPUT: sentence_clarity = {sentence : score}
    sentence_clarity = {}
    sentence_relation_scores = get_sentence_relation_score(worker_dict)
    for sentence in sentence_relation_scores:
        relation_scores = sentence_relation_scores[sentence]
        scores = []
        for relation in relation_scores:
            scores.append(relation_scores[relation])
        clarity = max(scores)
        sentence_clarity[sentence.replace(" '","").replace("  ", " ")] = clarity 
    return sentence_clarity
        
def get_worker_sentence_score(worker_dict):
    #OUTPUT: worker_sentence_scores = {worker : {sentence : score}}
    sentence_clarity = get_sentence_clarity(worker_dict)
    worker_sentence_scores = {}
    for worker in worker_dict:
        sentences = worker_dict[worker]
        for sentence in sentences:
            worker_annotations = sentences[sentence]
            total_annotations = get_sentence_annotations(sentence, worker_dict)
            total_annotations = [total_annotations[i]-worker_annotations[i] for i in range(0, len(worker_annotations))]
            sentence_cosine = 1.0-scipy.spatial.distance.cosine(worker_annotations,total_annotations)
            sentence_score = sentence_cosine - sentence_clarity[sentence]
            if worker in worker_sentence_scores:
                sentence_scores = worker_sentence_scores[worker]
            else:
                sentence_scores = {}
            sentence_scores[sentence] = sentence_score
            worker_sentence_scores[worker] = sentence_scores
    return worker_sentence_scores

def get_worker_relation_score(worker_dict):
    #OUTPUT: worker_relation_score_dict = {worker : {relation : score}}
    relation_clarity = relation_clarity(worker_dict)
    relation_sentences_dict = {}
    sentences_done = []
    worker_relation_score_dict = {}
    for worker in worker_dict:
        sentences = worker_dict[worker]
        for sentence in sentences:
            if not sentence in sentences_done:
                sentences_done.append(sentence)
                total_annotations = get_sentence_annotations(sentence, worker_dict)
                max_annotation = max(total_annotations)
                max_index = total_annotations.index(max_annotation)
                relation_sentences_dict[sentence] = max_index
    for worker in worker_dict:
        worker_relation_scores = {}
        worker_relation_sentences_dict = {}
        sentences = worker_dict[worker]
        for sentence in sentences:
            for relation in relation_sentences_dict:
                relation_sentences = relation_sentences_dict[relation]
                if sentence in relation_sentences:
                    if relation in worker_relation_sentences_dict:
                        worker_relation_sentences = worker_relation_sentences_dict[relation]
                    else:
                        worker_relation_sentences = []
                    worker_relation_sentences.append(sentence)
                    worker_relation_sentences_dict[relation] = worker_relation_sentences
        for relation in worker_relation_sentences_dict:
            worker_relation_sentences = worker_relation_sentences_dict[relation]
            total_cosine = 0
            total_sentences = len(worker_relation_sentences)
            for sentence in worker_relation_sentences:
                worker_annotations = sentences[sentence]
                total_annotations = get_sentence_annotations(sentence, worker_dict)
                total_annotations = [total_annotations[i]-worker_annotations[i] for i in range(0, len(worker_annotations))]
                sentence_cosine = 1.0-scipy.spatial.distance.cosine(worker_annotations,total_annotations)
                total_cosine += sentence_cosine
            if total_sentences > 0:
                avg_relation_cos = float(total_cosine)/total_sentences
            else:
                avg_relation_cos = 1.0
            worker_relation_score = relation_clarity[relation] - avg_relation_cos
            worker_relation_scores[relation] = worker_relation_score
        worker_relation_score_dict[worker] = worker_relation_scores
    return worker_relation_score_dict

def relation_clarity(worker_dict):
    #Relation_clarity = {relation : score}
    relation_clarity = {}
    sentence_relation_scores = get_sentence_relation_score(worker_dict)
    for sentence in sentence_relation_scores:
        relation_scores = sentence_relation_scores[sentence]
        for relation in relation_scores:
            relation_score = relation_scores[relation]
            if relation in relation_clarity:
                max_relation_score = relation_clarity[relation]
            else:
                max_relation_score = 0
            if relation_score > max_relation_score:
                relation_clarity[relation] = relation_score
    return relation_clarity

def get_sentence__worker_annotations(worker_dict):
    #OUTPUT {sentence : {worker : annotations}}
    sentence_annotations = {}
    for worker in worker_dict:
        sentences = worker_dict[worker]
        for sentence in sentences:
            worker_annotation = sentences[sentence]
            if sentence in sentence_annotations:
                cur_annotations = sentence_annotations[sentence]
            else:
                cur_annotations = {}
            cur_annotations[worker] = worker_annotation
            sentence_annotations[sentence] = cur_annotations
    return sentence_annotations
    
def get_sentence_scores(worker_dict):
    #OUTPUT {sentence : [[agreement_worker_1 ... agreement_worker_n],[cosine_worker_1 ... cosine_worker_n]]}
    sentence_scores = {}
    sentence_worker_annotations = get_sentence__worker_annotations(worker_dict)
    for sentence in sentence_worker_annotations:
        cosines = []
        agreements = []
        total_annotations = get_sentence_annotations(sentence, worker_dict)
        worker_annotations = sentence_worker_annotations[sentence]
        for worker in worker_annotations:
            worker_annotation = worker_annotations[worker]
            total_annotations = [total_annotations[i]-worker_annotation[i] for i in range(0, len(worker_annotation))]
            worker_cosine = 1.0-scipy.spatial.distance.cosine(worker_annotation,total_annotations)
            cosines.append(worker_cosine)
            agreed = 0
            total = sum(worker_annotation)
            for i in range(0, len(worker_annotation)):
                if total_annotations[i] > 0 and worker_annotation[i] > 0:
                    agreed += 1
            if total == 0:
                agreement = 0
            else:
                agreement = float(agreed)/total
            agreements.append(agreement)
        sentence_scores[sentence] = [agreements, cosines]
    return sentence_scores


        
        
            
            

def get_relation_similarity():
    return None

def get_relation_ambiguity():
    return None

