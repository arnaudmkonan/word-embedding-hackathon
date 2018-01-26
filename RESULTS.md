# Hackathon Results


Data sources

1. small wikipedia https://radimrehurek.com/gensim/wiki.html
2. Underwriting notes
3. Class descriptions


Results are on simplified Arthur model

| Model   | Embeddings & data source | Embeddings dimension | Accuracy | Precision   | Recall  |
|:--------|:-------------------------|---------------------:|---------:|------------:|--------:|
| 1 LSTM  | glove                    |  300                 |          |             |         |
| 2 LSTM  | glove                    |  100                 |          |             |         |
| 3 LSTM  | d1                       |  100                 |          |             |         |
| 4 LSTM  | d2                       |  100                 |          |             |         |
| 5 LSTM  | d3                       |  100                 |          |             |         |
| 6 LSTM  | d1 d2                    |  100                 |          |             |         |
| 7 LSTM  | d1 d3                    |  100                 |          |             |         |
| 8 LSTM  | d2 d3                    |  100                 |          |             |         |
| 9 LSTM  | d1 d2 d3                 |  100                 |          |             |         |

