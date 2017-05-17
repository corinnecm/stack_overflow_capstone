from bs4 import BeautifulSoup
from sklearn.model_selection import train_test_split
import re


class DataCleaner(object):
    """
    Class to clean StackOverflow data.
    """

    def __init__(self, df, training=True, simple_regression=True):
        self.df = df
        self.simple_regression = simple_regression

        self.df['normed_score'] = self.df.score/self.df.view_count
        indicies = xrange(len(df))
        X_train, X_test = train_test_split(indicies, train_size=.8,
                                           random_state=123)
        training_data = self.df.iloc[X_train, :]
        test_data = self.df.iloc[X_test, :]

        if training:
            self.df = training_data
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

    def text_parse(self):
        '''
        Remove html tags from columns with text.
        '''
        soupy = []
        text_columns = ['body', 'title']
        for col in text_columns:
            for row in col:
                soup = BeautifulSoup(row, "html.parser")
                soupy.append(soup.get_text())
        self.df['parsed_body'] = soupy

    def check_value_range(self):
        '''
        Make sure that numeric columns have reasonable ranges (usually >0)
        '''
        numeric_columns = ['id', 'parent_id', 'accepted_answer_id',
                           'answer_count', 'comment_count', 'favorite_count',
                           'view_count']
        rows_to_drop = []
        for col in numeric_columns:
            for idx, row in enumerate(col):
                if row < 0:
                    rows_to_drop.append(idx)
        self.df.drop(self.df.index[rows_to_drop])

    def nlp_features(self):
        pass

    def add_length_cols(self):
        '''
        For columns listed, take the length of the text in each row, add to
        Dataframe as new columns.
        '''
        title_lengths = []
        body_lengths = []
        for title, body in zip(self.df['title'], self.df['body']):
            title_lengths.append(len(title))
            body_lengths.append(len(body))
        self.df['title_length'] = title_lengths
        self.df['body_length'] = body_lengths

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

    def drop_text_columns(self):
        '''
        Drop text columns for regression purposes.
        '''
        text_columns = ['title', 'body', 'tags']
        for col in text_columns:
            self.df = self.df.drop(col, axis=1)

    def parse_datetime_cols(self):
        '''
        Tranform datetime columns into regression-usable formats.
        '''
        datetime_cols = ['closed_date', 'community_owned_date',
                         'creation_date', 'last_activity_date',
                         'last_edit_date']
        pass

    def nan_to_zero(self):
        '''
        Converts all NaNs to zero.
        '''
        self.df.fillna(0, inplace=True)

    def only_numeric(self):
        '''
        Drops all unique or non-numeric columns for simple regression.
        '''
        to_drop = ['id', 'accepted_answer_id', 'body', 'code', 'tags',
                   'tags_list', 'title']
        for col in to_drop:
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

    def get_clean(self):
        '''
        Runs all pertinent cleaning methods.
        '''
        self.extract_code_for_col()
        self.transform_tags()
        self.check_value_range()
        self.add_length_cols()
        self.dumify_code()
        self.parse_datetime_cols()
        self.nan_to_zero()
        self.drop_leaky_columns()
        self.num_tags()
        self.num_paragraphs()

        if self.simple_regression:  # if simple regression is true
            self.only_numeric()
        else:
            self.text_parse()
            self.nlp_features()

        # if training = True, y = y_train, X = X_train
        y = self.df.pop('normed_score')
        X = self.df

        return X, y
