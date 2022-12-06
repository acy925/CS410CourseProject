import pandas as pd
import spacy
from spacytextblob.spacytextblob import SpacyTextBlob


class SentimentAnalysis:

    def __init__(self, corpus: pd.Series):
        self.nlp = spacy.load('en_core_web_md')
        self.nlp.add_pipe("spacytextblob")
        self.text = corpus
        self.sent_df = pd.DataFrame()

    def fit_transform(self) -> pd.DataFrame:
        self.sent_df['text'] = [' '.join(map(str, w)) for w in self.text]
        self.sent_df['polarity'], self.sent_df['subjectivity'] = zip(
            *self.sent_df['text']
            .apply(
                lambda x: self.get_polar_subj(nlp_pipe=self.nlp, text=x)
            )
        )

        return self.sent_df

    def reading_conversion(self, pos_theta: list[float] = [0.6, 0.2], neg_theta: list[float] = [-0.2, -0.6],
                           sub_theta: float = 0.6) -> pd.DataFrame:
        """

        :param pos_theta: [1, 0.6) -> very positive, [0.6, 0.2) -> positive, [0.2, -0.2) -> neutral
        :param neg_theta: [-0.2, -0.6) -> negative, [-0.6, -1) -> very negative
        :param sub_theta: 1 - 0.6 -> subjective, 0.6 - 0.0 -> objective
        :param data: sentiment analysis result dataframe
        :return: dataframe with two new columns having polarity/subjective tag (e.g., 'positive', 'subjective'...)
        """
        rows, _ = self.sent_df.shape
        self.sent_df['polarity_text'] = self.sent_df['polarity']
        self.sent_df['subjectivity_text'] = self.sent_df['subjectivity']

        for r in range(rows):
            pol = self.sent_df.iloc[r]['polarity']
            subj = self.sent_df.iloc[r]['subjectivity']

            # Transform Polarity to text
            if pol > 0.6:
                self.sent_df.loc[r, 'polarity_text'] = 'Very Positive'
            elif 0.6 >= pol > 0.2:
                self.sent_df.loc[r, 'polarity_text'] = 'Positive'
            elif 0.2 >= pol > -0.2:
                self.sent_df.loc[r, 'polarity_text'] = 'Neutral'
            elif -0.2 >= pol > -0.6:
                self.sent_df.loc[r, 'polarity_text'] = 'Negative'
            else:
                self.sent_df.loc[r, 'polarity_text'] = 'Very Negative'

            # Transform Subjectivity to text
            if subj >= 0.6:
                self.sent_df.loc[r, 'subjectivity_text'] = 'Subjective'
            else:
                self.sent_df.loc[r, 'subjectivity_text'] = 'Objective'

        return self.sent_df

    def get_polar_subj(self, nlp_pipe, text: str):
        doc = nlp_pipe(text)
        polarity = doc._.polarity
        subjectivity = doc._.subjectivity

        return polarity, subjectivity

