import pathlib
from typing import Union

import attr
import fastText
import paralleldots
import requests
from aylienapiclient import textapi

from srec_nlp.common import _ensure_utf, Query, Score
from srec_nlp.common import valuetoscore


class NLP:
    @_ensure_utf
    def sentiment(self, text) -> Query:
        """
        Sample class.
        :param text: Union[IOBase, str, Path, bytes] a file, pathtofile, bytes or string with the text.
                    Function guarantees the value will be converted to text
        :return: Query
        """
        raise NotImplemented()


@attr.s
class ParallelDots:
    """
       with ParallelDots(api_key) as nlp:
               nlp.sentiment(text)
               nlp.sentiment(bytes)
               nlp.sentiment(open(path/to/text.txt,'r'))
               nlp.sentiment(pathlib.Path('path/to/text.txt'))

           # ParallelDots is still usable at this point.
           # So reusing it is still valid

           nlp.sentiment(text)
           nlp.sentiment(bytes)
           nlp.sentiment(open(path/to/text.txt,'r'))
           nlp.sentiment(pathlib.Path('path/to/text.txt'))
       """
    api_key: str = attr.ib()

    @api_key.validator
    def setkey(self, _, value):
        paralleldots.set_api_key(value)

    def __enter__(self):
        return self

    @_ensure_utf
    def sentiment(self, text) -> Query:
        """
        Produces a sentiment score for query text using ParallelDots API
        :param text: Union[IOBase, str, Path, bytes] a file, pathtofile, bytes or string with the text.
                    Function guarantees the value will be converted to text
        :return: Query
        """
        response = paralleldots.sentiment(text)
        return Query(text, Score(**response["sentiment"]))

    def __exit__(self, *exc):
        pass


class TextProcessing:
    """
    with TextProcessing() as nlp:
            nlp.sentiment(text)
            nlp.sentiment(bytes)
            nlp.sentiment(open(path/to/text.txt,'r'))
            nlp.sentiment(pathlib.Path('path/to/text.txt'))

        # TextProcessing is still usable at this point.
        # So reusing it is still valid

        nlp.sentiment(text)
        nlp.sentiment(bytes)
        nlp.sentiment(open(path/to/text.txt,'r'))
        nlp.sentiment(pathlib.Path('path/to/text.txt'))
    """

    _url = "http://text-processing.com/api/sentiment/"

    def __enter__(self):
        return self

    @_ensure_utf
    def sentiment(self, text) -> Query:
        """
        Produces a sentiment score for query text using TextProcessing API
        :param text: Union[IOBase, str, Path, bytes] a file, pathtofile, bytes or string with the text.
                    Function guarantees the value will be converted to text
        :return: Query
        """
        data = dict(text=text)
        result = requests.post(self._url, data=data).json()
        result = result["probability"]
        q = Query(
            content=text, score=Score(result["pos"], result["neutral"], result["neg"])
        )
        return q

    def __exit__(self, *exc):
        pass


class FastText:
    """
    model: str/pathlib.Path  the path to the model.

    # Usage example:

    with FastText(path/to/model.bin) as nlp:
        nlp.sentiment(text)
        nlp.sentiment(bytes)
        nlp.sentiment(open(path/to/text.txt,'r'))
        nlp.sentiment(pathlib.Path('path/to/text.txt'))

    # at this point, nlp.sentiment WILL RAISE AN ERROR because the model has been
    # dealloc'd, to avoid this, use the following:

    nlp = FastText(path/to/model.bin)
    nlp.sentiment(text)
    nlp.sentiment(bytes)
    nlp.sentiment(open(path/to/text.txt,'r'))
    nlp.sentiment(pathlib.Path('path/to/text.txt'))

    """

    def __init__(self, path: Union[str, pathlib.Path]):
        self.model = FastText._load_model(path)

    def __enter__(self):
        return self

    def __exit__(self, *vargs, **kwargs):
        del self.model

    @_ensure_utf
    def sentiment(self, text) -> Query:
        """
        Produces a sentiment score for query text using FastText API
        Note that FastText needs to be installed for this to work.
        :param text: Union[IOBase, str, Path, bytes] a file, pathtofile, bytes or string with the text.
                    Function guarantees the value will be converted to text
        :return: Query
        """
        labels, scores = self.model.predict(text, 1)
        score = self._result_to_score(labels, scores)
        return Query(text, score)

    @staticmethod
    def _load_model(path: Union[str, pathlib.Path]):
        p = pathlib.Path(path).expanduser()
        if not p.is_file():
            raise ValueError(f"{p} is not a file.")
        try:
            return fastText.load_model(str(p))
        except Exception as e:
            print(e)
            raise ValueError(f"{p} is not a valid FastText model")

    @staticmethod
    def _result_to_score(labels, scores):
        """
        Assumes labels is in form (label,)
        Assumes scores is in form [score,]
        """
        label = labels[0]
        score = scores[0]
        if label == "__label__1":
            score = 1 - score
        score = valuetoscore(score)
        return score


class Aylien:

    def __init__(self, appid, appkey):
        """
        :param appid: string Aylien application id
        :param appkey: string Aylien application key

        with Aylien(id, key) as nlp:
            nlp.sentiment(text)
            nlp.sentiment(bytes)
            nlp.sentiment(open(path/to/text.txt,'r'))
            nlp.sentiment(pathlib.Path('path/to/text.txt'))

        # Aylien is still usable at this point.
        # So reusing it is still valid

        nlp.sentiment(text)
        nlp.sentiment(bytes)
        nlp.sentiment(open(path/to/text.txt,'r'))
        nlp.sentiment(pathlib.Path('path/to/text.txt'))
        """
        self.client = textapi.Client(applicationId=appid, applicationKey=appkey)

    def __enter__(self):
        return self

    @_ensure_utf
    def sentiment(self, text: str) -> Query:
        """
        Produces a sentiment score for query text using Aylien API
        :param text: Union[IOBase, str, Path, bytes] a file, pathtofile, bytes or string with the text.
                    Function guarantees the value will be converted to text
        :return: Query
        """
        sentiment = self.client.Sentiment(dict(text=text))
        confidence = sentiment["polarity_confidence"]
        klass = sentiment["polarity"]
        remaining = (1 - confidence) / 2
        vals = dict(positive=remaining, negative=remaining, neutral=remaining)
        vals[klass] = confidence
        return Query(content=text, score=Score(**vals))

    def __exit__(self, *exc):
        pass
