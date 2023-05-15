# Work repo for NPSC+
## Short introduction
This repo contains the code used for creating the NPSC+, a large speech corpus with speech from Stortinget and transcriptions
extracted from the proceedings at Stortinget. See [our paper](https://www.researchgate.net/publication/370766648_A_Large_Norwegian_Dataset_for_Weak_Supervision_ASR) for more information about this dataset. This is work in
progress, but once the project is completed, the dataset will be shared with an open license. For the time being, the documentation
of this code is rather basic.


## Content
* `data/` contains ASR transcriptions and proceedings
* `matching/` contains a modified version of [the matching code from CLARINSI](https://github.com/clarinsi/parlaspeech/blob/main/utils/matching.py).

## Matching
The ASR transcriptions need to be inverse-normalized. Clone and install the normalization code:

```
git clone https://github.com/Sprakbanken/sprakbanken_normalizer.git

python -m pip install .
```

Example code
```
from sprakbanken_normalizer.inverse_text_normalizer import inv_normalize

print(inv_normalize("dette tallet er tre hundre tusen fire hundre og tjueto"))
```

## Saving results to an SQLite database

An SQL database needs to be built first to save the references to the proceedings and the transcriptions.

```
python3 run.py results.db
```
