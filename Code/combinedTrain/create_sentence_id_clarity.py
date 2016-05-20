sentencestats = open('sentencestats.csv', 'r')
sentencesid = open('sentences.txt' , 'r')
sentences_id_stats = {}

for sentencestat in sentencestats.readlines():
    info = sentencestat.split('|')
    sentence = info[0].strip()
    stat = info[1].strip()
    sentences_id_stats[sentence] = [stat]

#print sentences_id_stats.keys()

for ids in sentencesid.readlines():
    info = ids.split('|')
    sentence_id = info[0].strip()
    sentence = info[1].strip()
    try:
        old = sentences_id_stats[sentence]
        old.append(sentence_id)
        sentences_id_stats[sentence] = old
    except:
        print sentence



