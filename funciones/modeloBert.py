#BERT Modelo
import torch
from torch.utils.data import TensorDataset, DataLoader, RandomSampler, SequentialSampler
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
from pytorch_pretrained_bert import BertTokenizer, BertConfig
import pickle

with open(f'datos/Bert_unicornio','rb') as ba:
	global model
	model=pickle.load(ba)

def rayo_sesamo(frase):
	global model
	array_frase=np.array([frase])
	tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True)
	# load test data
	sentences = ["[CLS] " + query + " [SEP]" for query in array_frase]

	# tokenize test data
	tokenized_texts = [tokenizer.tokenize(sent) for sent in sentences]
	MAX_LEN = 128
	# Pad our input tokens
	input_ids = pad_sequences([tokenizer.convert_tokens_to_ids(txt) for txt in tokenized_texts],
		maxlen=MAX_LEN, dtype="long", truncating="post", padding="post"
		)
	# Use the BERT tokenizer to convert the tokens to their index numbers in the BERT vocabulary
	input_ids = [tokenizer.convert_tokens_to_ids(x) for x in tokenized_texts]
	input_ids = pad_sequences(input_ids, maxlen=MAX_LEN, dtype="long", truncating="post", padding="post")
	# Create attention masks
	attention_masks = []
	# Create a mask of 1s for each token followed by 0s for padding
	for seq in input_ids:
		seq_mask = [float(i>0) for i in seq]
		attention_masks.append(seq_mask) 

	# create test tensors
	prediction_inputs = torch.tensor(input_ids)
	prediction_masks = torch.tensor(attention_masks)
	#prediction_labels = torch.tensor(np.array(labels))
	batch_size = 32  
	prediction_data = TensorDataset(prediction_inputs, prediction_masks)#, prediction_labels)
	prediction_sampler = SequentialSampler(prediction_data)
	prediction_dataloader = DataLoader(prediction_data, sampler=prediction_sampler, batch_size=batch_size)

	## Prediction on test set
	# Put model in evaluation mode
	model.eval()
	for batch in prediction_dataloader:
		b_input_ids, b_input_mask = batch#, b_labels
	logits = model(b_input_ids, token_type_ids=None, attention_mask=b_input_mask)
	logits = logits.detach().cpu().numpy()
	#label_ids = b_labels.to('cpu').numpy()
	np.argmax(logits, axis=1).flatten()
	flat_predictions = [item for sublist in [logits] for item in sublist]
	flat_predictions = np.argmax(flat_predictions, axis=1).flatten()
	return flat_predictions[0], logits