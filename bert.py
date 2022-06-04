import pandas as pd
import numpy as np

import torch
from transformers import BertForQuestionAnswering
from transformers import BertTokenizer

def question_answer(question, text):
    model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
    tokenizer = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')

    input_ids = tokenizer.encode(question, text) #tokenize question and text in ids as a pair
    tokens = tokenizer.convert_ids_to_tokens(input_ids) #string version of tokenized ids
    
    sep_idx = input_ids.index(tokenizer.sep_token_id) #first occurence of [SEP] token
    num_seg_a = sep_idx+1 #number of tokens in segment A - question
    num_seg_b = len(input_ids) - num_seg_a #number of tokens in segment B - text
    
    segment_ids = [0]*num_seg_a + [1]*num_seg_b #list of 0s and 1s
    assert len(segment_ids) == len(input_ids)
    
    output = model(torch.tensor([input_ids]), token_type_ids=torch.tensor([segment_ids])) #model output using input_ids and segment_ids
    
    #reconstructing the answer
    answer_start = torch.argmax(output.start_logits)
    answer_end = torch.argmax(output.end_logits)

    if answer_end >= answer_start:
        answer = tokens[answer_start]
        for i in range(answer_start+1, answer_end+1):
            if tokens[i][0:2] == "##":
                answer += tokens[i][2:]
            else:
                answer += " " + tokens[i]
                
    if answer.startswith("[CLS]"):
        answer = "Unable to find the answer to your question."
    
    return format(answer.capitalize())
    #print("\nAnswer:\n{}".format(answer.capitalize()))