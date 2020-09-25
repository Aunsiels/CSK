# Inspired by https://huggingface.co/transformers/perplexity.html


from transformers import GPT2LMHeadModel, GPT2TokenizerFast
import torch

device = 'cuda'
model_id = 'gpt2-large'
model = GPT2LMHeadModel.from_pretrained(model_id).to(device)
tokenizer = GPT2TokenizerFast.from_pretrained(model_id)


def get_perplexity(sentence):
	encodings = tokenizer(sentence, return_tensors='pt')
	max_length = model.config.n_positions
	stride = 512
	lls = []
	for i in range(0, encodings.input_ids.size(1), stride):
		begin_loc = max(i + stride - max_length, 0)
		end_loc = i + stride
		input_ids = encodings.input_ids[:,begin_loc:end_loc].to(device)
		target_ids = input_ids.clone()
		target_ids[:,:-stride] = -100
		with torch.no_grad():
			outputs = model(input_ids, labels=target_ids)
			log_likelihood = outputs[0]  # * stride
		lls.append(log_likelihood)
	ppl = torch.exp(torch.stack(lls).sum() / (i+1))
	return ppl


result_file = open("sentences_ppl.tsv", "a")

with open("sentences_to_process.txt") as f:
	for i, line in enumerate(f):
		print(i, end="\r")
		line = line.strip()
		if not line:
			continue
		ppl = get_perplexity(line)
		_ = result_file.write(line + "\t" + str(ppl.item()) + "\n")

result_file.close()
