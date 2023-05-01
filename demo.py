import streamlit as st
from Retriever import contentretriever as cr
from DPR import DPR
import os

st.set_page_config(page_title='IBM Content retriever', 
                   page_icon='./img/5a3a21e61dd0d6.02978359151375920612213253.png',
                   layout="wide")

_, _, icon_col = st.columns([3,3,1])

with icon_col:
    st.image("./img/5a3a21e61dd0d6.02978359151375920612213253.png")

st.title("Large scale content retrieval")
st.write("Demo for relevant passage retrievel for large scale documents such as PDFs or URLs.")

with st.spinner(text="We are loading the model..."):
    DPR = DPR.IBMDPR() 

_, pdfupload_col, _ = st.columns([1,1,1])
content_display = ""

with pdfupload_col:
    uploaded_file = st.file_uploader('Input your Pdf file you want to upload.', 
                                     type="pdf")
    
    if uploaded_file is not None:
        filename = uploaded_file.name
        file_path = os.path.join("pdf_documents", filename)
        
        with open(file_path, 'wb') as f:
            f.write(uploaded_file.getbuffer())
        
        st.success("File uploaded successfully!")
    
    pdf_dir = "pdf_documents"
    pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith('.pdf')]
    selected_file = st.selectbox("Select a PDF file", pdf_files)
    selected_file_path = os.path.join(pdf_dir, selected_file)

    content_display = cr.pdf_to_text(selected_file_path)


_, num_col, _ = st.columns([1,1,1])
_, que_col, _ = st.columns([1,1,1])
_, run_b_col, _ = st.columns([1,1,1])



with num_col:
    number = st.number_input('Insert the no. of relevant passages you want to retrieve.', step=1, min_value=3)

with que_col:
    question = st.text_input('Input the question.', 'What goals are set to reduce the emission?')

relevant_passages = False

with run_b_col:
    run_b = st.button("Run model")

    if run_b:
        with st.spinner(text="In progress..."):
            if not content_display == "":
                relevant_passages = DPR.get_relevant_passages(number, 
                                                              content_display,
                                                              [question])

            else:
                st.error("No content to retrieve. Make sure to input a valid PDF-Document.")

if relevant_passages:
    st.write("### Relevant passages:")

    st.write(relevant_passages)

st.write("### Retrieved content:")
st.write(content_display[:5000] + " ...")