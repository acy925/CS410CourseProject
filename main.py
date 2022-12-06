import json
import sys
import pandas as pd
import nltk

from utils.data_puller import DataPuller
from utils.remove_lemmanization import RemoveUrlEmojiLemmanization
from utils.remove_stopwords import StopwordsRemove
from utils.topic_model import TopicModel
from utils.sentiment_analysis import SentimentAnalysis


def main(file_path: str, custom_stopwords: list[str], usePretrain: bool,
         isNewPull: bool, num_topics: int, isUpdate: bool = False):
    nltk.download('stopwords')

    if isNewPull:
        # New pull from tweet
        print('Pulling from Tweet starts ...')
        data_puller = DataPuller(
            bearer_token="AAAAAAAAAAAAAAAAAAAAAE5XjAEAAAAAQ1rZv%2BCvEajebtp%2F1iA0wPoKkl4%3DDsikDqeoxudFiDWudHqJSCjgI64Z5jnheSnSdKpKLdpaRIqC9J")
        data = data_puller.pull_data(
            query='("california heat wave" OR #CaliforniaHeatWave) lang:en',
            start_time="2022-09-03T00:00:00Z",
            end_time="2022-09-09T00:00:00Z",
            max_results=500,
            twitter_fields='author_id,created_at,geo,lang'
        )
    else:
        print('Using existing pulled tweets ...')
        data_path = file_path
        data = [json.loads(line) for line in open(data_path, 'r')]
    df = pd.DataFrame(data)

    text = df['text']
    idx_start = 0 
    idx_end = 1000

    rm_lemma = RemoveUrlEmojiLemmanization(data=text)
    text = rm_lemma.preprocess_text(convertTostring=False)

    rm_stop = StopwordsRemove(custom_stopwords=custom_stopwords)
    text = rm_stop.rm_stopwords(text, tokenizer_flag=False)

    if not usePretrain:
        # Train a new model
        print('Start training new model ...')
        lda = TopicModel(isPretrained=False, text=text)
        topic_contents = lda.fit_transform(num_topics=num_topics)
        lda.save_trained_lda(save_path='./model/lda')
    else:
        # Use pretrained model
        Print('Using pretrained model ...')
        if isUpdate:
            lda = TopicModel(isPretrained=True, text=text)
        else:
            lda = TopicModel(isPretrained=True)

    lda.topic_word_dist(print_formatted=True)

    sen_ana = SentimentAnalysis(corpus = text[idx_start:idx_end])
    sen_ana.fit_transform()
    res_df = sen_ana.reading_conversion()
    print(res_df[['text', 'polarity_text', 'subjectivity_text']].head())
    res_df_s = res_df[['text', 'polarity_text', 'subjectivity_text']]
    res_df_s["raw"] = df["text"].iloc[idx_start:idx_end].copy()
    res_df_s.to_csv("./sentiment_analysis.csv")



if __name__ == "__main__":
    # Get user inputs from command lines
    args = sys.argv

    path = './data/results.txt'
    num_topics = 5
    isPretrain = False
    isNewPull = False

    if len(args) >= 3:
        isPretrain = bool(args[1] == "True")
        isNewPull = bool(args[2] == "True")

        if 4 >= len(args) > 3:
            if args[3].isdigit():
                num_topics = int(args[3])
            else:
                path = args[3]

        if len(args) > 4:
            path = args[3]
            num_topics = int(args[4])

    custom_stopwords = ['rt',
                        '#heat', 'heat', '#wave', 'wave', '#heatwave', 'heatwave', 'heatwave2022',
                        '#california', 'california',
                        '#californiaheatwave', 'californiaheatwave',
                        'sfchronicle', '2022',
                        '\n', '\n\n', '&', ' ', '.', '-', 'got',
                        "it's", 'it’s', "i'm", 'i’m', 'im', 'want', 'use',
                        'like', '$', '@']

    main(
        file_path=path,
        custom_stopwords=custom_stopwords,
        usePretrain=isPretrain,
        isNewPull=isNewPull,
        num_topics=num_topics
    )
