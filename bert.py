import pandas as pd
import numpy as np

import torch
from transformers import LongformerTokenizer, LongformerForQuestionAnswering

tokenizer = LongformerTokenizer.from_pretrained("allenai/longformer-large-4096-finetuned-triviaqa")
model = LongformerForQuestionAnswering.from_pretrained("allenai/longformer-large-4096-finetuned-triviaqa")

def question_answer(question, text):
    encoding = tokenizer(question, text, return_tensors="pt")
    input_ids = encoding["input_ids"]

    attention_mask = encoding["attention_mask"]

    outputs = model(input_ids, attention_mask=attention_mask)
    start_logits = outputs.start_logits
    end_logits = outputs.end_logits
    all_tokens = tokenizer.convert_ids_to_tokens(input_ids[0].tolist())

    answer_tokens = all_tokens[torch.argmax(start_logits) : torch.argmax(end_logits) + 1]
    answer = tokenizer.decode(tokenizer.convert_tokens_to_ids(answer_tokens))
       
    if answer.startswith("[CLS]"):
        answer = "Unable to find the answer to your question."
    
    return format(answer.capitalize())
    #print("\nAnswer:\n{}".format(answer.capitalize()))