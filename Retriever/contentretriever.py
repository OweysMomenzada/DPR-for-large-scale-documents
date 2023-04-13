import pdfplumber
import requests
import re
import html2text


CLEANR = re.compile('/n') 
CLEANH = re.compile('#') 


def pdf_to_text(pdf):
  pdf = pdfplumber.open(pdf)

  content = []
  for i in range(len(pdf.pages)):
    retrieved_page = pdf.pages[i].extract_text()
    content.append(retrieved_page)

  res = " ".join(content)
  pdf.close()
  
  return res


def pdf_page_to_text(pdf, page):
  pdf = pdfplumber.open(pdf)

  retrieved_page = pdf.pages[page-1].extract_text()
  
  return retrieved_page


def cleanhtml(raw_html):
    h = html2text.HTML2Text()
    h.ignore_links = True
    raw_html = h.handle(raw_html)
    cleantext = re.sub(CLEANR, ' ', raw_html)
    cleantext = re.sub(CLEANH, '', raw_html)
    
    return cleantext

def retrieve_webcontent(url):
    r = requests.get(url)
    raw_html = r.text
    doc = cleanhtml(raw_html)

    return doc