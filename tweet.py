import  point
from nltk.corpus import opinion_lexicon
from nltk.tokenize import treebank

#Tweet class  be created that contains (composition) a Point object.
class Tweet():

    def __init__(self,point,text,source,id_str,lang,created_time):

        self.point=point    #The tweet spatial information
        self.text=text      #The text
        self.point.mark=self.classifier_fun(text)
        self.source=source  #the source
        self.id_str=id_str  #the id_str
        self.lang=lang      #the language
        self.created_time=created_time   #the create time

    def get_spatial_information(self):
        """
         Return the tweet spatial information.
        :return:(lat,lon)
        """
        return (self.point.x,self.point.y)

    def classifier_fun(self,sentence):

        tokenizer = treebank.TreebankWordTokenizer()
        pos_words = 0
        neg_words = 0
        tokenized_sent = [word.lower() for word in tokenizer.tokenize(sentence)]

        x = list(range(len(tokenized_sent))) # x axis for the plot
        y = []

        for word in tokenized_sent:
            if word in opinion_lexicon.positive():
                pos_words += 1
                y.append(1) # positive
            elif word in opinion_lexicon.negative():
                neg_words += 1
                y.append(-1) # negative
            else:
                y.append(0) # neutral

        if pos_words > neg_words:
            return 'Positive'
        elif pos_words < neg_words:
            return 'Negative'
        elif pos_words == neg_words:
            return 'Neutral'
        
    
