import torch
from transformers import DPRQuestionEncoder, DPRQuestionEncoderTokenizer, DPRContextEncoder, DPRContextEncoderTokenizer

import heapq
from tqdm import tqdm
import pandas as pd

CTX_TOKENIZER = "DPR/DPR_Context/Tokens"
QUE_TOKENIZER = "DPR/DPR_Question/Tokens"
CTX_ENCODER_ARCHITECTURE = "./DPR/DPR_Context"
QUE_ENCODER_ARCHITECTURE = "./DPR/DPR_Question"


class IBMDPR:
    def __init__(self):
        self.que_tokenizer = DPRQuestionEncoderTokenizer.from_pretrained(QUE_TOKENIZER)
        self.que_encoder = DPRQuestionEncoder.from_pretrained(QUE_ENCODER_ARCHITECTURE)
        self.ctx_tokenizer = DPRContextEncoderTokenizer.from_pretrained(CTX_TOKENIZER)
        self.ctx_encoder = DPRContextEncoder.from_pretrained(CTX_ENCODER_ARCHITECTURE)
        self.char_len = 600
        self.char_shift = 100


    def set_vals(self, char_len, char_shit):
        self.char_len = char_len
        self.char_shift = char_shit


    def matmul(self, E_q, E_p):
        E_p_t = torch.transpose(E_p, 0, 1) 

        return E_q @ E_p_t


    def create_passages(self, doc):
        passage_list = []

        i = 0
        while i < len(doc):
            input = doc[i:i+self.char_len]
            passage_list.append(input)

            i = i + self.char_len - self.char_shift

        return passage_list
    

    def retrieve_k_passages(self, top_k_scores, scores, passages):
        top_k_passages = []

        for k_score in top_k_scores:
            index = scores.index(k_score)
            top_k_passages.append(passages[index])

        return top_k_passages


    def question_encoding(self, question):
        input_ids = self.que_tokenizer(question, return_tensors='pt')["input_ids"]
        embeddings_que = self.que_encoder(input_ids).pooler_output

        return embeddings_que


    def context_encoding(self, context):
        input_ids = self.ctx_tokenizer(context, return_tensors='pt')["input_ids"]
        embeddings_ctx = self.ctx_encoder(input_ids).pooler_output

        return embeddings_ctx


    def get_relevant_passages(self, k, doc, questions):
        passages = self.create_passages(doc)

        # get embedding for each question
        embedded_questions = []
        for question in questions:
            embedded_questions.append(self.question_encoding(question))

        scores = []
        for i in tqdm(range(len(passages))):
            embedded_ctx = self.context_encoding(passages[i])

            score_each_question = []
            # now go into each embedded question and create score.
            for embedded_question in embedded_questions:
                score = self.matmul(embedded_question, embedded_ctx)
                score_each_question.append(float(score))

            scores.append(tuple(score_each_question))
        
        scores_df = pd.DataFrame(columns=questions, data=scores)

        retrieved_passages = []
        # top questions for all columns
        for question in questions:
            scores = list(scores_df[question])
            top_k_scores = heapq.nlargest(k, scores)
            res = self.retrieve_k_passages(top_k_scores, scores, passages)
            retrieved_passages.append(res)

        scores.sort(reverse=True)

        return [retrieved_passages, scores[:k]]


if __name__ == "__main__":
    DPR = IBMDPR()
    print(DPR.get_relevant_passages(1, "HEY THIS IS A TEXT", ["Is this a question?"]))