# DPR-for-large-scale-documents

We present a way to extract relevant text passages from PDF files and rank them by relevancy to a corresponding question.
The methods being used is based on Dense Passage Retrieval for Multicontext. PDF files are naivly converter from pdf to txt. Currently, multicolumn extraction is not supported.


### Install Requirements
Install packages by running:

```
$ pip install -r requirements.txt
```

Now either get the multi-DPR model:
```
$ python train.py -modeltype multi
```

or for the single-DPR model:
```
$ python train.py -modeltype single
```

### Run Demo App:
```
$ streamlit run demo.py
```