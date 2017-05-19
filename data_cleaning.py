# from bs4 import BeautifulSoup
from datetime import datetime
from sklearn.model_selection import train_test_split
import re


class DataCleaner(object):
    """
    Class to clean StackOverflow data.
    """

    def __init__(self, df, questions=True, training=True,
                 simple_regression=True, time_split=True):
        self.df = df
        self.simple_regression = simple_regression
        self.questions = questions
        self.time_split = time_split

        if time_split:
            self.df = self.df.sort_values('creation_date')
            indicies = xrange(len(self.df))
            split_index = int(len(self.df))*0.8
            train_data = self.df.iloc[:split_index, :]
            test_data = self.df.iloc[split_index:, :]

        else:
            X_train, X_test = train_test_split(indicies, train_size=.8, random_state=123)
            train_data = self.df.iloc[X_train, :]
            test_data = self.df.iloc[X_test, :]

        if training:
            self.df = train_data
        else:  # testing
            print "Using test data"
            self.df = test_data

    def extract_code_for_col(self):
        '''
        From posts.body extract the text inside <code> tags and outputs a
        new column.
        '''
        code_snips = []
        for row in self.df['body']:
            m = re.findall("<code>(.*?)</code>", row)
            if m:
                code_snips.append(m)
            else:
                code_snips.append(False)
        self.df['code'] = code_snips

    def transform_tags(self):
        '''
        From posts.tags transform the tags into a list of strings and outputs
        a new column.
        '''
        tags = []
        for row in self.df['tags']:
            tag = re.findall("<(.*?)>", str(row))
            tags.append(tag)
        self.df['tags_list'] = tags

    def text_parse(self, text_columns):
        '''
        Remove html tags from columns with text.
        '''
        soupy = []
        for col in text_columns:
            for row in col:
                soup = BeautifulSoup(row, "html.parser")
                soupy.append(soup.get_text())
        self.df['parsed_body'] = soupy

    def check_value_range(self, columns):
        '''
        Make sure that numeric columns have reasonable ranges (usually > 0)
        '''
        rows_to_drop = []
        for col in columns:
            for idx, row in enumerate(col):
                if row < 0:
                    rows_to_drop.append(idx)
        self.df.drop(self.df.index[rows_to_drop])

    def nlp_features(self):
        pass

    def add_length_cols(self, len_columns):
        '''
        For columns listed, take the length of the text in each row, add to
        Dataframe as new columns.
        '''
        for col in len_columns:
            col_name = str(col)+'_length'
            self.df[col_name] = self.df[col].apply(len)

    def dumify_code(self):
        '''
        Turn categoricals into dummies for regression purposes
        (here, we are making a code/no code column).
        '''
        dummy = []
        for row in self.df['code']:
            if row is not False:  # if the row has code
                dummy.append(1)
            else:
                dummy.append(0)
        self.df['code_yn'] = dummy

    def drop_leaky_columns(self):
        '''
        Drop columns used to make the new y column to prevent leakage.
        '''
        leaky_columns = ['score', 'view_count']
        for col in leaky_columns:
            self.df = self.df.drop(col, axis=1)

    def extract_month(self, mo_columns):
        '''
        Tranform datetime columns into regression-usable formats.
        '''
        # datetime_cols = ['closed_date', 'community_owned_date',
        #                  'creation_date', 'last_activity_date',
        #                  'last_edit_date']
        month = []
        for col in mo_columns:
            col_name = str(col)+'_month'
            self.df[col_name] = self.df[col].dt.month

    def nan_to_zero(self):
        '''
        Converts all NaNs to zero.
        '''
        self.df.fillna(0, inplace=True)

    def only_numeric(self, drop_cols):
        '''
        Drops all unique or non-numeric columns for simple regression.
        '''
        for col in drop_cols:
            self.df = self.df.drop(col, axis=1)

    def num_tags(self):
        '''
        Adds column that contains the number of tags per post.
        '''
        num_tags = []
        for tag in self.df['tags_list']:
            num_tags.append(len(tag))
        self.df['num_tags'] = num_tags

    def num_paragraphs(self):
        '''
        Adds column that contains the number of paragraphs
        in the body of the post.
        '''
        paragraphs = []
        for row in self.df['body']:
            paragraph = re.findall("<p>", str(row))
            paragraphs.append(len(paragraph))
        self.df['num_paragraphs'] = paragraphs

    def only_python_posts(self):
        '''
        Returns only the posts that have python as one of the tags.
        '''
        non_python = []
        for idx, row in enumerate(self.df['tags_list']):
            match = re.search(r"python", str(row))
            if not match:
                non_python.append(idx)
        self.df.drop(self.df.index[non_python])

    def get_clean(self):
        '''
        Runs all pertinent cleaning methods.
        '''
        dt_cols = ['creation_date']

        q_numeric_cols = ['id', 'accepted_answer_id', 'answer_count',
                          'comment_count', 'favorite_count', 'view_count']
        q_length_cols = ['body', 'title']
        q_drop_cols = ['id', 'accepted_answer_id', 'body', 'code', 'tags',
                       'tags_list', 'title']

        a_numeric_cols = ['id', 'answer_count', 'comment_count',
                          'favorite_count', 'view_count']
        a_length_cols = ['body']
        a_drop_cols = ['id', 'body', 'code', 'parent_id']

        if self.questions and self.simple_regression:
            self.transform_tags()
            self.nan_to_zero()
            self.num_tags()
            self.extract_code_for_col()
            self.check_value_range(q_numeric_cols)
            self.add_length_cols(q_length_cols)
            self.dumify_code()
            self.extract_month(dt_cols)
            self.num_paragraphs()
            self.only_numeric(q_drop_cols)
            # self.drop_leaky_columns()

        elif not self.questions and self.simple_regression:  # if answers
            self.nan_to_zero()
            self.extract_code_for_col()
            self.check_value_range(a_numeric_cols)
            self.add_length_cols(a_length_cols)
            self.dumify_code()
            self.extract_month(dt_cols)
            self.num_paragraphs()
            self.only_numeric(a_drop_cols)

        else:  # if not regression
            self.text_parse()
            self.nlp_features()

        # if training = True, y = y_train, X = X_train
        y = self.df.pop('score')
        X = self.df

        return X, y
