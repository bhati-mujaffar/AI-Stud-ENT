import pickle


from transformers import BertForQuestionAnswering 
from transformers import BertTokenizer
model= BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
tokenizer= BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')


save_model = open(r"chatmodel.pickle","wb")
pickle.dump(model, save_model)
save_model.close()

save_tokenizer = open(r"chattokenizer.pickle","wb")
pickle.dump(tokenizer,save_tokenizer)
save_tokenizer.close()
