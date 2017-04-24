import logging

from sklearn import model_selection
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.svm import LinearSVR

from processors.abstract_processor import Processor
from utils import file_helper

log = logging.getLogger(__name__)


class S140Processor(Processor):

    def process(self):
        log.info("S140Processor begun")

        input_tweets = file_helper.read_input_data(self.options.input_file_path)
        s140_lexicon = list(file_helper.read_s140_lexicon(self.options.lexicon_file_path))

        y_train = list()
        x_train = list()

        count = 1
        for input_tweet in input_tweets:
            log.debug("On tweet " + str(count))
            count += 1
            x_vector = list()
            for lexicon_word in s140_lexicon:
                if lexicon_word.word in input_tweet.text:
                    x_vector.append(lexicon_word.score)
                else:
                    x_vector.append(0.0)
            x_train.append(x_vector)
            y_train.append(input_tweet.intensity)

        log.debug("Computing model")
        scores = \
            model_selection.cross_val_score(
                LinearSVR(), x_train, y_train, cv=10, scoring='r2'
            )
        mean_score = scores.mean()

        log.info("Accuracy: %0.2f (+/- %0.2f)" % (mean_score, scores.std() * 2))

        log.info("S140Processor ended")
