import re
import pandas as pd

from gensim.corpora import Dictionary
from gensim.models.ldamulticore import LdaMulticore
from gensim.test.utils import datapath
from gensim.models.ldamodel import LdaModel


class TopicModel:

    def __init__(self, isPretrained: bool = True, text: pd.Series = None, min_doc: int = 10,
                 max_doc_frac: float = 0.85, *kwarg):
        """
        :param isPretrained: if it is True, a pretrained will be used for topic mining/modeling. Otherwise,
        a new model will be trained based on the input corpus.
        :param text: input corpus for training new model or retraining the pretrained model
        :param min_doc: minimum number of documents containing a word before excluding the word from consideration
        :param max_doc_frac: maximum fraction of the total number of documents containing a word before excluding the
        word from consideration
        """

        if isPretrained:
            # Load pre-trained LDA model 
            model_file = './model/lda'
            self.lda = LdaModel.load(model_file)

            if text:
                unseen_text = [self.lda.id2word.doc2bow(line) for line in text]
                self.lda.update(unseen_text)

        else:
            try:
                self.no_below = min_doc
                self.no_above = max_doc_frac
                
                self.id2word = Dictionary(text)
                self.id2word.filter_extremes(no_below=self.no_below, no_above=self.no_above)

                self.corpus = [self.id2word.doc2bow(doc) for doc in text]

            except:
                print('Please input a training text doc.')

    def fit(self, num_topics: int = 5, workers: int = 3, passes: int = 5):
        self.lda = LdaMulticore( 
            corpus=self.corpus, 
            num_topics=num_topics,
            id2word=self.id2word, 
            workers=workers,
            passes=passes
        )

    def transform(self) -> list[list[str]]:
        word_dist = [re.findall(r'"([^"]*)"', t[1]) for t in self.lda.print_topics()]
        topic_words = [[f"topic {t[0]}"] + w for t, w in zip(self.lda.print_topics(), word_dist)]
        return topic_words
    
    def fit_transform(self, num_topics: int = 5, workers: int = 3, passes: int = 5):
        self.fit(
            num_topics=num_topics,
            workers=workers,
            passes=passes
        )

        return self.transform()

    def save_trained_lda(self, save_path: str = None):
        try:
            self.lda.save(save_path)
        except:
            print('Please check the save_path parameter.')
    
    def topic_word_dist(self, top_n: int = 5, print_formatted: bool = False) -> list[list[str]]:
        """
        :param top_n: the number of top words for each topic to show
        :param print_formatted: if it is True, a formatted top_n words for each topic will be printed
        :return: list of all the topics and their associated words
        """
        word_dist = [re.findall(r'"([^"]*)"',t[1]) for t in self.lda.print_topics()]
        topic_words = [[f"topic {t[0]}"] + w[:top_n] for t, w in zip(self.lda.print_topics(), word_dist)]

        if print_formatted:   # Print word with weight and put each word in a new line for better reading experience
            for topic in self.lda.print_topics():
                print(f"----topic {topic[0]}----")
                words = topic[1].split('+')
                for w in words[:top_n]:
                    print(w)
                print("\n")

        return topic_words
