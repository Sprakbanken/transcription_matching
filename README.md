# Arbeidsrepo for NPSC+

## Innhold
* `data/` inneholder ASR-transkripsjoner og referater
* `matching` inneholder [matching-koden fra kroatene](https://github.com/clarinsi/parlaspeech/blob/main/utils/matching.py).

## Matching
ASR-transkripsjonene er ikke invers-normalisert: Tall er skrevet som "tre hundre og fire", ikke "304", datoer er skrevet som "fjortende september", ikke "14. september", og det fins ikke forkortelser. Før matching må transkripsjonene invers-normaliseres. Vi har kode for dette på Språkbankens github. Klon repoet og installer koden som en pakke:

```
git clone https://github.com/Sprakbanken/sprakbanken_normalizer.git

python -m pip install .
```

Eksempelkode:
```
from sprakbanken_normalizer.inverse_text_normalizer import inv_normalize

print(inv_normalize("dette tallet er tre hundre tusen fire hundre og tjueto"))
```
