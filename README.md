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

### Run the Demo App on Docker!
#### Before building the image please get the multi-DPR or single-DPR model.

Build image:
```
  $ docker build -t demo-dpr-image .
```
Run it:
```
  $ docker run -p 8501:8501 demo-dpr-image
````

It is then exposed on `http://localhost:8501`