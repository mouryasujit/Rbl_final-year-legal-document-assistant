# import json
# import torch
# import random

# from utils import tokenize, bag_of_words, stemming
# from model import Chatbot

# device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# with open('intents.json', 'r') as json_data:
#     intents = json.load(json_data)

# save_path = 'trained_model.pth'
# pretrained = torch.load(save_path)

# input_size = pretrained["input_size"]
# hidden_size = pretrained["hidden_size"]
# output_size = pretrained["output_size"]
# data = pretrained["data"]
# labels = pretrained["labels"]
# model_state = pretrained["model_state"]

# model = Chatbot(input_size, hidden_size, output_size).to(device)
# model.load_state_dict(model_state)
# model.eval()

# print("Legal Documentation Chatbot simulation. Enter q to quit")

# while (True):
#     sentence = input("User: ")
#     if (sentence == "q"):
#         break

#     sentence = tokenize(sentence)
#     word_tokens = stemming(sentence)
#     X = bag_of_words(word_tokens, data)

#     X = X.reshape(1, X.shape[0])
#     X = torch.from_numpy(X).to(device)

#     output = model(X.float())
#     _, predicted = torch.max(output, dim=1)
#     label = intents['intents'][predicted.item()]["tag"]
#     probs = torch.softmax(output, dim=1)
#     prob = probs[0][predicted.item()]
#     if prob.item() > 0.75:
#         for intent in intents['intents']:
#             if label == intent["tag"]:
#                 print(f"Legal Assistant: {random.choice(intent['responses'])}")
#     else:
#         print(f"Legal Assistant: I do not understand...")

import random
import json

import torch

from model import Chatbot
from utils import bag_of_words, tokenize

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('intents.json', 'r') as json_data:
    intents = json.load(json_data)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = Chatbot(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Sam"
print("Let's chat! (type 'quit' to exit)")
while True:
    # sentence = "do you use credit cards?"
    sentence = input("You: ")
    if sentence == "quit":
        break

    sentence = tokenize(sentence)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                print(f"{bot_name}: {random.choice(intent['responses'])}")
    else:
        print(f"{bot_name}: I do not understand...")
