import pandas as pd
import sqlite3
import json

from pathlib import Path

# Constants

SEG_QUERY = "SELECT segmentid, sessionid, segmentindex, audiofilename, duration, proceedingsfile, transcriptionfile, matched FROM segment JOIN session USING (sessionid);"
SCORE_QUERY_TEMPLATE = "SELECT segmentid, score, language, pos_start, pos_end FROM score WHERE language = '{language}';"


# Classes

class ProceedingsCorpus(object):
    """Object for processing proceedings files"""
    def __init__(self, corpuspath):
        self._corpus_path = Path(corpuspath)
        self.tokens = []
        self._tokenize()
    
    def _tokenize(self):
        with self._corpus_path.open(mode="r") as f:
            for l in f:
                for w in l.strip().split():
                    self.tokens.append(w)
    
    def get_corpus_text(self, start, end):
        """Return slice of corpus text from start word index to 
        (but not including) end word index"""
        return " ".join(self.tokens[start:end])

class Transcriptions(object):
    """Object for processing transcription json files"""
    def __init__(self, transcriptionjson):
        self._transfile = Path(transcriptionjson)
        self._transcriptions = {}
        self._parse_transfile()
    
    def _parse_transfile(self):
        with self._transfile.open(mode="r") as f:
            for l in f:
                ldict = json.loads(l)
                filename = ldict["file"]
                self._transcriptions[filename] = {
                    "text_bm": ldict["text_bm"],
                    "text_nn": ldict["text_nn"],
                }
    
    def get_transcription(self, audiofile, lang):
        """Return the transcription for a given audio file and language"""
        if lang == "bm":
            return self._transcriptions[audiofile]["text_bm"]
        elif lang == "nn":
            return self._transcriptions[audiofile]["text_nn"]


# Methods

def make_match_df(con: sqlite3.Connection, cutoff=0.5) -> pd.DataFrame:
    """Produce a dataframe from the results database with the score of the best match.
    If the match score is best for Nynorsk, only the nynorsk match is returned and the language code
    is 'nn'. Else, the Bokmål match is returned with the language code 'bm'."""
    
    score_query_bm = SCORE_QUERY_TEMPLATE.format(language="bm")
    score_query_nn = SCORE_QUERY_TEMPLATE.format(language="nn")
    df_segments = pd.read_sql(SEG_QUERY, con)
    df_score_bm = pd.read_sql(score_query_bm, con)
    df_score_nn = pd.read_sql(score_query_nn, con)
    df_segments["score_bm"] = df_score_bm["score"]
    df_segments["score_nn"] = df_score_nn["score"]
    df_segments_bm = df_segments.query("score_bm >= score_nn & score_bm > @cutoff").drop(["score_bm", "score_nn"], axis=1)
    df_segments_nn = df_segments.query("score_nn > score_bm & score_nn > @cutoff").drop(["score_bm", "score_nn"], axis=1)
    df_results_bm = df_segments_bm.merge(df_score_bm, on="segmentid")
    df_results_nn = df_segments_nn.merge(df_score_nn, on="segmentid")
    
    return pd.concat([df_results_bm, df_results_nn]).sort_values(by=["sessionid", "segmentid", "segmentindex"])

def add_text_cols(df: pd.DataFrame) -> pd.DataFrame:
    """Add columns 'proceedings_text' and 'transcription_text' to a results df with the proceedings match
    and the asr output respectively. The implementation is set ut so that the asr json files and the proceedings
    text files are opened only once, provided that the input df is sorted by sessionid."""

    corpfile = ""
    transfile = ""
    corpobj = None
    transobj = None
    
    def add_proceedings_text(row):
        nonlocal corpfile
        nonlocal corpobj
        if corpfile != row.proceedingsfile:
            corpfile = row.proceedingsfile
            corpobj = ProceedingsCorpus(corpfile)
        return corpobj.get_corpus_text(row.pos_start, row.pos_end)
    
    def add_transcription_text(row):
        nonlocal transfile
        nonlocal transobj
        if transfile != row.transcriptionfile:
            transfile = row.transcriptionfile
            transobj = Transcriptions(transfile)
        return transobj.get_transcription(row.audiofilename, row.language)
    
    df["proceedings_text"] = df.apply(lambda row: add_proceedings_text(row), axis=1)
    df["transcription_text"] = df.apply(lambda row: add_transcription_text(row), axis=1)
    return df
