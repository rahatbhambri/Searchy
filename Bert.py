import torch, requests
from transformers import BertForQuestionAnswering
from transformers import BertTokenizer
from bs4 import BeautifulSoup
import warnings

# Suppress all warnings
warnings.filterwarnings("ignore", message = "Be aware, overflowing tokens are not returned for the setting you have chosen.*" \
, category=RuntimeWarning)



#Model
model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')

#Tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')

topic = input("Enter topic you want to enquire \n")
response = requests.get(f"https://en.wikipedia.org/wiki/{topic.lower()}")
soup = BeautifulSoup(response.content, "html.parser")

# Find all paragraphs on the webpage
paragraphs = soup.find_all("p")

para = ""
# Extract and print the text content of each paragraph
for paragraph in paragraphs:
    para += paragraph.text

paragraph = para


def getAnswer(question):
    # Encode question and paragraph
    encoding = tokenizer.encode_plus(text=question, text_pair=paragraph, max_length=512, truncation=True, return_tensors="pt")

    # Perform inference
    start_scores, end_scores = model(**encoding, return_dict=False)

    # Get the index of the start and end tokens with the highest score
    start_index = torch.argmax(start_scores)
    end_index = torch.argmax(end_scores)

    # Get the tokens corresponding to the answer
    tokens = tokenizer.convert_ids_to_tokens(encoding['input_ids'].squeeze())
    answer_tokens = tokens[start_index:end_index+1]

    # Convert answer tokens back to string
    answer = tokenizer.convert_tokens_to_string(answer_tokens)
    corrected_answer = ''

    for word in answer.split():
        #If it's a subword token
        if word[0:2] == '##':
            corrected_answer += word[2:]
        else:
            corrected_answer += ' ' + word

    return corrected_answer



while True:
    question = input("Enter question or 1 to print context or 0 to end \n")
    if question == "0":
        break
    elif question == "1":
        print(paragraph)
    else:
        answer = getAnswer(question)

        print("Question:", question)
        if answer == "[SEP]":
            print("Answer:", "I don't know that")
        else:
            print("Answer:", answer)



