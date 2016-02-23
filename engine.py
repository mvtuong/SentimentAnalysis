import numpy as np
import re
from datetime import datetime
from string import punctuation
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import scale

#sample_feature_histogram = [5, 3, 0, 2, 2, 4, 12, 4, 0, 55, 0, 0, 3.6823115608848256, 1.157033005425523, 338, 20, 238, 17, 258, 4, -0.46875, -0.28125, -0.125, 1.03125, 0.84375]

class SentimentAnalysis:

    def __words(self, text):
        for word in text.split():
            # normalize words by lowercasing and dropping non-alpha characters
            normed = re.sub('[^a-z]', '', word.lower())
            if normed:
                yield normed

    def __build_histogram(self, text):
        #Descripton [0-spos, 1-wpos, 2-sneu, 3-wneu, 4-sneg, 5-wneg, 6-pos, 7-neg, 8-negation, 9-len, 10-day, 11-vote, 12-ps, 13-ns, 14 ... 24]
        result =    [0     , 0     , 0     , 0     , 0     , 0     , 0    , 0    , 0         , 0    , 0     , 0      , 0.0  , 0.0  , 0,0,0,0,0,0, 0.0,0.0,0.0,0.0,0.0]
        count = 0
        for word in self.__words(text):
            count += 1
            if self.dict6bins.has_key(word):
                keyword1 = self.dict6bins[word]["type"]
                keyword2 = self.dict6bins[word]["priorpolarity"]
                if keyword1 == 'strongsubj' and keyword2 == 'positive':
                    result[0]+=1
                elif keyword1 == 'weaksubj' and keyword2 == 'positive':
                    result[1]+=1
                elif keyword1 == 'strongsubj' and keyword2 == 'neutral':
                    result[2]+=1
                elif keyword1 == 'weaksubj' and keyword2 == 'neutral':
                    result[3]+=1
                elif keyword1 == 'strongsubj' and keyword2 == 'negative':
                    result[4]+=1
                elif keyword1 == 'weaksubj' and keyword2 == 'negative':
                    result[5]+=1
                elif keyword1 == 'weaksubj' and keyword2 == 'both':
                    result[1]+=1
                    result[5]+=1
                elif keyword1 == 'strongsubj' and keyword2 == 'both':
                    result[0]+=1
                    result[4]+=1

            if self.dict3bins.has_key(word):
                keyword = self.dict3bins[word][0]
                occurrence = self.dict3bins[word][1]
                if keyword == 'positive':
                    result[6]+=occurrence
                elif keyword == 'negative':
                    result[7]+=occurrence
                elif keyword == 'negation':
                    result[8]+=occurrence

            if self.dict2bins.has_key(word):
                result[12] += self.dict2bins[word][0]
                result[13] += self.dict2bins[word][1]
        
        result[9] = count #len(re.findall(r'\w+', text)) #word_count
        day = datetime.today().weekday()
        if day == 5 or day == 6: #day_unused_predictor
            result[10] = 1
        else:
            result[10] = 0
        result[11] = 0 #vote_unused_predictor

        result[14] = len(text) #character_count
        result[15] = sum(1 for c in text if c.isupper()) #uppercase_count
        result[16] = sum(1 for c in text if c.islower()) #lowercase_count
        result[17] = sum(1 for c in text if c in punctuation) #punctuation_count
        result[18] = sum(1 for c in text if c.isalpha()) #alphabetic_count
        result[19] = sum(1 for c in text if c.isdigit()) #numeric_count

        #Descripton [20-1star, 21-2star, 22-3star, 23-4star, 24-5star]
        resultBOW = [0       , 0       , 0       , 0       , 0       ]
        
        analyzed = self.analyze(text)        
        for item in analyzed:
            feature_index = self.vectorizer.vocabulary_.get(item)
            if feature_index:
                item_histogram = self.dtm[:, feature_index]
                resultBOW = [x + y for x, y in zip(resultBOW, item_histogram)]

        sumBOW = sum(resultBOW)
        if sumBOW != 0: #Normalize
            for i in xrange(len(resultBOW)):
                resultBOW[i] = resultBOW[i]*1.0/sumBOW

        result[20] = resultBOW[0]
        result[21] = resultBOW[1]
        result[22] = resultBOW[2]
        result[23] = resultBOW[3]
        result[24] = resultBOW[4]

        #Feature selection
        del result[10]
        del result[11]
        
        return result

    def get_predict_ratings(self, text):
        hist = self.__build_histogram(text)
        rating = self.model.predict(hist)
        return rating

    def __init__(self):
               
        #BOWs preparation
        filenames = ['bow/1StarsSamples.json', 'bow/2StarsSamples.json', 'bow/3StarsSamples.json', 'bow/4StarsSamples.json', 'bow/5StarsSamples.json']
        
        self.vectorizer = CountVectorizer(input='filename', ngram_range=(1,3), stop_words='english', strip_accents='unicode', token_pattern=ur'\b\w+\b')        
        dtm = self.vectorizer.fit_transform(filenames).toarray()
        self.dtm = scale(dtm)
        vocab = np.array(self.vectorizer.get_feature_names())        
        _vectorizer = CountVectorizer(input='content', ngram_range=(1,3), stop_words='english', strip_accents='unicode', token_pattern=ur'\b\w+\b')
        self.analyze = _vectorizer.build_analyzer()

        #Load dictionaries and model
        with open("dict/dict2bins.p", "rb") as f1, open("dict/dict3bins.p", "rb") as f2, open("dict/dict6bins.p", "rb") as f3, open("model/clf.pkl", "rb") as fm:
            self.dict2bins = pickle.load(f1)
            self.dict3bins = pickle.load(f2)
            self.dict6bins = pickle.load(f3)
            self.model = pickle.load(fm)     #load model

