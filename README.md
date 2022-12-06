# Mining and analyzing heat waves-related topics using social media

link to video: https://drive.google.com/file/d/1wkCJF_Xq6AquJIvG8Y4lPp_tJTsCRiHI/view?usp=share_link

## 1) An overview of the function of the code (i.e., what it does and what it can be used for).

The code provides three main functions:

- pull the Tweets 

  (NOTE: Users need to apply for for their own Twitter API for Academic Research access via the link [HERE](https://developer.twitter.com/en/products/twitter-api/academic-research). We offer an API through a GitHub repository, but we'll turn it off by the end of the semester.)

  based on:

  - query/search words (e.g. "california heat wave" OR #CaliforniaHeatWave) lang:en)
  - start_time (e.g. "2022-09-03T00:00:00Z")
  - end_time (e.g. "2022-09-09T00:00:00Z")

- perform topic modelling

- perform sentiment analysis

## 2) Documentation of how the software is implemented with sufficient detail so that others can have a basic understanding of your code for future extension or any further improvement.

The software has a `main.py` file that brings the submodules/functions together:

- `from utils.data_puller import DataPuller`
  - `DataPuller` is used for pulling tweets data based on query/search words, start_time, and end_time. 
  
    ```python
    bearer_oauth(self, r): 
    # twitter required authentication.
            
    connect_to_endpoint(self, params): 
    # connect to endpoint, query data
            
    pull_data(self, query, start_time, end_time, max_results, twitter_fields):
    # build query based on parameter,pull all the data from the endpoint based on query.
    ```
  
    To be more specific, it queries data from Twitter full-archive endpoint based on Twitter official API. To perform search, user must create an project on Twitter developer portal, and apply for the Academic Research API access.
  
    Twitter's API requires a bearer token from an existing project for authentication. We will provide a temporary token for the grading purpose.
  
    After authentication, users can build a query to search tweets. For this software, we include keywords, language, time interval in the query. There are more things supported but after some experiments we find some of them like geography bounding boxes or city filters are not usable for this project, but those query conditions can be added as needed in the query parameters of the `DataPuller.pull_data` function.
  
- `from utils.remove_lemmanization import RemoveUrlEmojiLemmanization`
  
  - `RemoveUrlEmojiLemmanization()` is used for removing emoji, url, Twitter usernames, and lemmatization
  
- `from utils.remove_stopwords import StopwordsRemove`
  - `StopwordsRemove()` is used for removing stopwords from corpus
  
- `from utils.topic_model import TopicModel`
  - `TopicModel()` is used for topic modelling
  
- `from utils.sentiment_analysis import SentimentAnalysis` 
  - `SentimentAnalysis()` is used for sentiment analysis

## 3) Documentation of the usage of the software including either documentation of usages of APIs or detailed instructions on how to install and run a software, whichever is applicable. 

**Installation**

Step 1: clone the source code from GitHub

```bash
$ git clone https://github.com/acy925/CS410CourseProject
```

Step 2: create an environment (code from terminal/powershell)

``` bash
# create and activate the environment; might take several minutes
$ conda env create -f environment.yml
$ conda activate heatwaver

# install en_core_web_md; might take ~1 minute
$ python -m spacy download en_core_web_md

# (optional, if the code above doesn't work for your next steps) 
# install all the required packages from requirements.txt
$ pip install -r requirements.txt
```

**How to use it?**

Step 1: edit the parameters in the `main.py`, such as query, start_time, end_time, number of topics, and custom stopwords, etc.

Step 2: run the code as follows:

```bash
$ python main.py

# Using pretrained (True) or train or new model (False), start new pull from tweet (True) or use existing file (False)
$ python main.py [True or False] [True or False]

# Using customized file path
$ python main.py [True or False] [True or False] [your_file_path]

# Specify the number of topics (default 5)
$ python main.py [True or False] [True or False] [int]
or
$ python main.py [True or False] [True or False] [your_file_path] [int]
```

## 4) Brief description of contribution of each team member in case of a multi-person team. 

Each team member made an equal contribution to this project.

| Tasks                                                     | Chengyuan Ai (ai13) | Linhan Yang (linhany2) | Yixuan Zhang (yixuan21) | Zhonghua Zheng (zzheng25) |
| --------------------------------------------------------- | ------------------- | ---------------------- | ----------------------- | ------------------------- |
| Data sources searching and evaluation                     | test                | test                   | develop                 | test                      |
| Data cleaning, exploration, and evaluation; Data curation | develop             | develop                | develop                 | develop                   |
| Topic model (clustering) for heat waves-related text      | test                | develop                | test                    | develop                   |
| Sentiment analysis                                        | test                | develop                | test                    | develop                   |
| Organization and integration                              | develop             | develop                | develop                 | develop                   |
| Documentation                                             | write               | write                  | write                   | write                     |

## 5) Self-evaluation

**We have successfully completed what we have planned and got the expected outcome.**

Due to time constraints, we were unable to complete the advanced functions that were **optional** in our proposal, including:

- Similarity-based Clustering techniques (e.g. Hierarchical Agglomerative Clustering (HAC) or K-means)
- Emotional sentiment analysis, aspect-based and multilingual sentiment analysis

However, these functions can be readily incorporated into our software.
