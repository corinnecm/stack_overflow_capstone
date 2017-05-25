# Predicting Post Scores for Questions and Answers on StackOverflow

## Motivation

As a data scientist I write code almost every day, which means that I am on StackOverflow almost every day searching for answers to coding questions I come across. StackOverflow is a question-answer forum for programming languages, and posts get scored based on the combination of their up votes and down votes. For this project I was interested in predicting the score of a post and looking for inherent features that would predict the scores. This would help posters write better questions and answers, as well as help those searching find better answers.

## Data

StackOverflow releases data dumps every few months. From the January 2017 data dump I downloaded a compressed 15GB .mdf file (Microsoft SQL format). Once uncompressed the data was about 114GB and contained 6 tables each ranging from 50 to 116 million rows. The data spans from August 2008 to December 2016. In its original form, the data was hard to work with (especially on a Mac), so I underwent the process to migrate the data from SQL Server into Postgres. This was done with the help of a few EC2 instances, and the python-SQL adaptors `psycopg2` for Postgres and `pyodbc` for SQL Server.

## Methods & Results

After the data had been migrated to Postgres (which took several days), real exploration could commence. Several of the tables in the dataset were not relevant to predicting scores, below in an overview of the columns I chose to examine:

| Question Posts     | Answer Posts   |
| :----------------- | :------------- |
| Post ID            | Post ID        |
| Accepted Answer ID | Parent ID      |
| Answer Count       | Comment Count  |
| Body (HTML)        | Body (string)  |
| Comment Count      | View Count     |
| Favorite Count     | Creation Date  |
| Tags (HTML)        | Score          |
| Title (string)     |                |
| View Count         |                |
| Creation Date      |                |
| Score              |                |

I also engineered several features including title length, number of tags, and the code extracted from the body of the post.

I decided to predict scores for questions and answers separately because of the differences in their features. I also ran a simple A/B test that showed the different between the the averages scores for each type of post was significantly different.

| Average Question Score | Average Answer Score |
| :--------------------- | :------------------- |
| 1.8                    | 2.5                  |

For modeling I compared linear regression, random forest, and gradient boosted regression. Gradient boosted regression performed slightly better for all variations I tried, so I chose this as my final model. I used R-squared and MSE as my goodness-of-fit metrics because I was predicting continuous values. My initial results on a small sample (1000 rows) were erratic, but once I trained my model on a larger sample (100,000 rows) the results were high enough to make me suspect I had a leakage problem with time. I attempted to plug my leak normalizing the scores over the leaky columns (view count, and days since creation), and removing those columns from the model data. The normalizations proved to be tricky, the scores became so small that I at risk of numeric underflow. With the leakage resolved to best of my abilities, my finals models had lower scores than my first few iterations.

| Questions Model | Answers Model |
| :-------------- | :------------ |
| R-Sq: 0.52      | R-Sq: 0.16    |
| Baseline: 0.0   | Baseline: 0.0 |

__Note:__ The baseline model simply predicts the average score every time, therefore the baseline R-squared score is always 0.0.

## Conclusion & Next Steps

The best predictors of a posts' score are view count and days since creation. What this tells us is that how often people search for a topic over time, not any features inherent to the post, is the most indicative of score.

Continuing to work on this project in the future I would like to incorporate some NLP features, like sentiment similarity between questions and their respective answers. I would also like to predict post scores for individual programming languages and look for any differences there, and continue to brainstorm ways to deal with leakage.
