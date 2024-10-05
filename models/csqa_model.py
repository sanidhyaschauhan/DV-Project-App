import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration
import json
from torch.utils.data import Dataset, DataLoader

class CSQAModel:
    def __init__(self, model_name="t5-small", data_path="train_rand_split.jsonl", model_path=None):
        self.tokenizer = T5Tokenizer.from_pretrained(model_name)
        self.model = T5ForConditionalGeneration.from_pretrained(model_name)
        
        if model_path:
            self.model.load_state_dict(torch.load(model_path))
            self.model.eval()  

        self.data_path = data_path
        if data_path:
            self.sample_data = self.load_data()
            self.prompts, self.answers = self.extract_prompts_and_answers(self.sample_data)
            self.train_prompt_encodings, self.train_answer_encodings = self.tokenize_data(self.prompts, self.answers)

    def load_data(self):
        sample_data = []
        with open(self.data_path, 'r') as file:
            for line in file:
                sample_data.append(json.loads(line))
        return sample_data
    
    def extract_prompts_and_answers(self, data):
        prompts = []
        answers = []
        for entry in data:
            prompts.append(entry['question'])
            answers.append(entry['answerKey'])
        return prompts, answers
    
    def format_prompt(self, prompt):
        stem = prompt['stem']
        choices_text = ' '.join([f"({choice['label']}) {choice['text']}" for choice in prompt['choices']])
        formatted_prompt = f"{stem} Choices: {choices_text}"
        return formatted_prompt
    
    def tokenize_data(self, prompts, answers):
        formatted_prompts = [self.format_prompt(prompt) for prompt in prompts]
        prompt_encodings = self.tokenizer(formatted_prompts, truncation=True, padding=True, max_length=512, return_tensors="pt")
        answer_encodings = self.tokenizer(answers, truncation=True, padding=True, max_length=512, return_tensors="pt")

        prompt_encodings["labels"] = answer_encodings["input_ids"]
        
        return prompt_encodings, answer_encodings

    def predict(self, question_data):
        prompt = self.format_prompt(question_data)
        
        inputs = self.tokenizer(prompt, return_tensors="pt")

        outputs = self.model.generate(**inputs)

        predicted_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        return {"answer": predicted_text}
    
    def get_data_loader(self, batch_size=8):
        train_dataset = T5Dataset(self.train_prompt_encodings)
        return DataLoader(train_dataset, batch_size=batch_size, shuffle=True)


class T5Dataset(Dataset):
    def __init__(self, encodings):
        self.encodings = encodings

    def __getitem__(self, idx):
        return {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}

    def __len__(self):
        return len(self.encodings.input_ids)

