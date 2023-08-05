import pathlib
from io import IOBase
from typing import Union, List

import attr

import paralleldots
import requests
from aylienapiclient import textapi

from srec_nlp.common import _ensure_utf, Query, Score
from srec_nlp.common import (_parallel)
from copy import deepcopy
from requests import HTTPError


class NLP:
    @_parallel
    @_ensure_utf
    def sentiment(self, text: Union[str, List[str], IOBase, pathlib.Path]) -> Query:
        """
        Sample class.
        :param text: Union[IOBase, str, Path, bytes] a file, pathtofile, bytes or string with the text.
                    Function guarantees the value will be converted to text
        :return: Query
        """
        return self._internal_sentiment(text)

    def _internal_sentiment(self, *vargs, **kwargs):
        raise NotImplemented

    @_parallel
    async def sentiment_async(self, text: Union[str, List[str], IOBase, pathlib.Path]):
        return self._internal_sentiment(text)

    def copy(self):
        return deepcopy(self)


@attr.s
class ParallelDots(NLP):
    """
       with ParallelDots(api_key) as nlp:
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
    def _internal_sentiment(self, text: Union[str, List[str], IOBase, pathlib.Path]) -> Query:
        """
        Produces a sentiment score for query text using ParallelDots API
        :param text: Union[IOBase, str, Path, bytes] a file, pathtofile, bytes or string with the text.
                    Function guarantees the value will be converted to text
        :return: Query
        """
        try:
            response = paralleldots.sentiment(text)
            return Query(text, Score.fromtriplet(**response["sentiment"]))
        except (HTTPError, KeyError) as _:
            raise HTTPError()

    def __exit__(self, *exc):
        pass


class TextProcessing(NLP):
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
    def _internal_sentiment(self, text: Union[str, List[str], IOBase, pathlib.Path]) -> Query:
        """
        Produces a sentiment score for query text using TextProcessing API
        :param text: Union[IOBase, str, Path, bytes] a file, pathtofile, bytes or string with the text.
                    Function guarantees the value will be converted to text
        :return: Query
        """
        data = dict(text=text)
        result = requests.post(self._url, data=data).json()
        result = result["probability"]
        result["positive"] = result["pos"]
        result["negative"] = result["neg"]
        del result["pos"]
        del result["neg"]
        try:
            return Query(content=text, score=Score.fromtriplet(**result))
        except (HTTPError, KeyError) as _:
            raise HTTPError()

    def __exit__(self, *exc):
        pass


try:
    import fastText


    class FastText(NLP):
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
            path = str(path).strip()
            path = pathlib.Path(path)
            self.model = FastText._load_model(path)
            self.path = path

        def __enter__(self):
            return self

        def __exit__(self, *vargs, **kwargs):
            del self.model

        @_ensure_utf
        def _sentiment_internal(self, text: Union[str, List[str], IOBase, pathlib.Path]) -> Query:
            """
            Produces a sentiment score for query text using FastText API
            Note that FastText needs to be installed for this to work.
            :param text: Union[IOBase, str, Path, bytes] a file, pathtofile, bytes or string with the text.
                        Function guarantees the value will be converted to text
            :return: Query
            """
            labels, scores = self.model.predict(text, 1)
            label = labels[0]
            score = scores[0]
            if label == "__label__1":
                score = 1 - score
            score = Score.fromsingle(score)
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

        def copy(self):
            return FastText(self.path)


except:
    pass


class Aylien(NLP):
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
    def _sentiment_internal(self, text: Union[str, List[str], IOBase, pathlib.Path]) -> Query:
        """
        Produces a sentiment score for query text using Aylien API
        :param text: Union[IOBase, str, Path, bytes] a file, pathtofile, bytes or string with the text.
                    Function guarantees the value will be converted to text
        :return: Query
        """
        sentiment = self.client.Sentiment(dict(text=text))
        try:
            confidence = sentiment["polarity_confidence"]
            klass = sentiment["polarity"]
            remaining = 1 - confidence
            vals = dict(positive=remaining, negative=remaining)
            vals[klass] = confidence
            return Query(content=text, score=Score(**vals))
        except (HTTPError, KeyError) as _:
            raise HTTPError()

    def __exit__(self, *exc):
        pass
