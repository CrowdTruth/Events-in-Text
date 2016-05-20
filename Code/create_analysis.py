import matplotlib.pyplot as plt
from pylab import *
import operator
"""
label_refined_count_file = open('label_refined_count.csv','r')
label_id_file = open('refined_label_ids.csv','r')
video_vectors_file = open('video_vectors.csv','r')
worker_video_vectors_file = open('worker_video_vectors.csv','r')
worker_video_annotation_file = open('worker_video_annotation_file.csv','r')

raw_to_refined = {}
raw_worker_videos_annotations_dict = {}
refined_worker_videos_annotations_dict = {}

for line in label_refined_count_file:
    info = line.strip().split('|')
    label = info[0]
    refined = info[1]
    raw_to_refined[label] = refined
label_refined_count_file.close()

for line in worker_video_annotation_file:
    info = line.strip().split('|')
    worker_id = info[0]
    video_url = info[1]
    label = info[2]
    refined_label = raw_to_refined[label]
    if worker_id in raw_worker_videos_annotations_dict:
        cur_raw_video_urls_annotations = raw_worker_videos_annotations_dict[worker_id]
    else:
        cur_raw_video_urls_annotations = {}
    if video_url in cur_raw_video_urls_annotations:
        cur_raw_annotations = cur_raw_video_urls_annotations[video_url]
    else:
        cur_raw_annotations = []
    cur_raw_annotations.append(label)
    cur_raw_video_urls_annotations[video_url] = cur_raw_annotations
    raw_worker_videos_annotations_dict[worker_id] = cur_raw_video_urls_annotations

    if worker_id in refined_worker_videos_annotations_dict:
        cur_refined_video_urls_annotations = refined_worker_videos_annotations_dict[worker_id]
    else:
        cur_refined_video_urls_annotations = {}
    if video_url in cur_refined_video_urls_annotations:
        cur_refined_annotations = cur_refined_video_urls_annotations[video_url]
    else:
        cur_refined_annotations = []
    cur_refined_annotations.append(refined_label)
    cur_refined_video_urls_annotations[video_url] = cur_refined_annotations
    refined_worker_videos_annotations_dict[worker_id] = cur_refined_video_urls_annotations
worker_video_annotation_file.close()
"""
def plot(vals, xLabel, yLabel):
    x = []
    y = []
    for val in vals:
        x.append(val[0])
        y.append(val[1])
    plt.plot(x, y, 'bo', x, y, 'k')
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    #plt.axis(axis)
    plt.show()

def get_total_number_of_videos(worker_videos_annotations_dict):
    unique_videos = []
    for worker in worker_videos_annotations_dict:
        videos = worker_videos_annotations_dict[worker]
        for video in videos:
            if not video in unique_videos:
                unique_videos.append(video)
    return len(unique_videos)

def get_unique_annotation_counts(worker_videos_annotations_dict):
    unique_annotation_counts = {}
    for worker in worker_videos_annotations_dict:
        videos = worker_videos_annotations_dict[worker]
        for video in videos:
            annotations = videos[video]
            for annotation in annotations:
                if annotation in unique_annotation_counts:
                    cur_count = unique_annotation_counts[annotation]
                else:
                    cur_count = 0
                unique_annotation_counts[annotation] = cur_count + 1
    return unique_annotation_counts

def get_unique_annotation_distribution(worker_videos_annotations_dict):
    count_count = {}
    unique_annotation_counts = get_unique_annotation_counts(worker_videos_annotations_dict)
    for label in unique_annotation_counts:
        count = unique_annotation_counts[label]
        if count in count_count:
            cur_count = count_count[count]
        else:
            cur_count = 0
        count_count[count] = cur_count+1
    return sorted(count_count.items(), key=operator.itemgetter(0))

def get_average_video_annotations(worker_videos_annotations_dict):
    video_annotation_count = {}    
    for worker in worker_videos_annotations_dict:
        videos = worker_videos_annotations_dict[worker]
        for video in videos:
            annotations = videos[video]
            if video in video_annotation_count:
                cur_annotation_count = video_annotation_count[video]
            else:
                cur_annotation_count = 0
            video_annotation_count[video] =  cur_annotation_count + len(annotations)
    return float(sum(video_annotation_count.values()))/len(video_annotation_count)
            

def get_average_unique_video_annotations(worker_videos_annotations_dict):
    unique_video_annotations = {}
    for worker in worker_videos_annotations_dict:
        videos = worker_videos_annotations_dict[worker]
        for video in videos:
            annotations = videos[video]
            if video in unique_video_annotations:
                cur_unique_annotations = unique_video_annotations[video]
            else:
                cur_unique_annotations = []
            for annotation in annotations:
                if not annotation in cur_unique_annotations:
                    cur_unique_annotations.append(annotation)
            unique_video_annotations[video] = cur_unique_annotations
    return float(sum([len(unique_annotations) for unique_annotations in unique_video_annotations.values()]))/len(unique_video_annotations)

def get_average_annotations_per_worker_per_video(worker_videos_annotations_dict):
    annotation_counts = []
    for worker in worker_videos_annotations_dict:
        videos = worker_videos_annotations_dict[worker]
        for video in videos:
            annotations = videos[video]
            annotation_counts.append(len(annotations))
    return float(sum(annotation_counts))/len(annotation_counts)

def get_video_annotation_popularity(worker_videos_annotations_dict):
    # n == 1 = low
    # n > max-(0.3*max) = high
    # max-(0.3*max)> n > 1 = medium
    average_video_popularity = [0,0,0]
    total_video_annotations = {}
    for worker in worker_videos_annotations_dict:
        videos = worker_videos_annotations_dict[worker]
        for video in videos:
            annotations = videos[video]
            if video in total_video_annotations:
                cur_annotations = total_video_annotations[video]
            else:
                cur_annotations = []
            cur_annotations.extend(annotations)
            total_video_annotations[video] = cur_annotations
    for video in total_video_annotations:
        annotations = total_video_annotations[video]
        annotation_counts = {}
        for annotation in annotations:
            if annotation in annotation_counts:
                cur_count = annotation_counts[annotation]
            else:
                cur_count = 0
            annotation_counts[annotation] = cur_count + 1
        max_count = max(annotation_counts.values())
        for annotation in annotation_counts:
            count = annotation_counts[annotation]
            if count == 1:
                average_video_popularity[0] += 1
            elif count > max_count-(float(0.3)*max_count):
                average_video_popularity[2] += 1
            elif count > 1:
                average_video_popularity[1] += 1
            else:
                average_video_popularity[0] += 1
    return [float(i)/len(total_video_annotations) for i in average_video_popularity]
            
'''
#Total number of videos
total_number_of_videos = get_total_number_of_videos(raw_worker_videos_annotations_dict)
print 'Total videos:', total_number_of_videos
#Distribution of unique annotation counts (raw | refined)
raw_distribution = get_unique_annotation_distribution(raw_worker_videos_annotations_dict)
refined_distribution = get_unique_annotation_distribution(refined_worker_videos_annotations_dict)

figure(1)
plot(raw_distribution, 'Raw label count','Frequency') 
figure(2)
plot(refined_distribution, 'Refined label count','Frequency')

#Average annotations per video (raw | refined | unique raw | unique refined)
average_video_annotations = get_average_video_annotations(raw_worker_videos_annotations_dict)
raw_average_unique_video_annotations = get_average_unique_video_annotations(raw_worker_videos_annotations_dict)
refined_average_unique_video_annotations = get_average_unique_video_annotations(refined_worker_videos_annotations_dict)
print 'Average video annotations:',average_video_annotations
print 'Raw average unique video annotatons:',raw_average_unique_video_annotations
print 'Refined average unique video annotatons:',refined_average_unique_video_annotations
#Average annotations per person per video
average_annotations_per_worker_per_video = get_average_annotations_per_worker_per_video(raw_worker_videos_annotations_dict)
print 'Average annotations per worker per video:',average_annotations_per_worker_per_video
#Distribution per video, how many annotations are high | medium | low
raw_average_video_popularity = get_video_annotation_popularity(raw_worker_videos_annotations_dict)
refined_average_video_popularity = get_video_annotation_popularity(refined_worker_videos_annotations_dict)
print 'Raw average video popularity:',raw_average_video_popularity
print 'Refined average video popularity:',refined_average_video_popularity
#Golden standards in distrubution, match to refined labels ( high | medium | low )

#Distrubution abstract | concrete | generic
# Abstract: love, success, freedom, good, moral, democracy, and any -ism (chauvinism, Communism, feminism, racism, sexism)
# Concrete: spoon, table, velvet eye patch, nose ring, sinus mask, green, hot, walking
# Generic: Classes such as furniture
'''
