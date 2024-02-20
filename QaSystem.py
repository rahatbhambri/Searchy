import torch, requests
from transformers import BertForQuestionAnswering
from transformers import BertTokenizer
from bs4 import BeautifulSoup
import warnings, re, random
# Suppress all warnings
warnings.filterwarnings("ignore", message = "Be aware, overflowing tokens are not returned for the setting you have chosen.*" \
, category=RuntimeWarning)


class QASystem:
    def __init__(self):
        #Model
        self.model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
        #Tokenizer
        self.tokenizer = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
        self.context = None
        self.topic = None
        self.image = None
        #self.context = self.SetContext(input("Enter topic you want to enquire \n"))


    def SetContext(self, topic):
        self.topic = topic
        response = requests.get(f"https://en.wikipedia.org/wiki/{topic.lower()}")
        soup = BeautifulSoup(response.content, "html.parser")
        # Find all paragraphs on the webpage
        paragraphs = soup.find_all("p")
        para = ""
        # Extract and print the text content of each paragraph
        for paragraph in paragraphs:
            para += paragraph.text
        imgs = soup.find_all('img')
        #print(imgs)

        image_src = []
        t = self.topic.split(" ")
        t = t[-1].lower()
        for img in imgs:
            if t in img['src'].lower():
                image_src += [img['src']]
        
        self.context = para
        self.image = image_src
        

    def getAnswer(self, question):
        if question == "1":
            return self.context, None        
        # Encode question and paragraph
        encoding = self.tokenizer.encode_plus(text=question, text_pair=self.context, max_length=512, truncation=True, return_tensors="pt")
        # Perform inference
        start_scores, end_scores = self.model(**encoding, return_dict=False)
        # Get the index of the start and end tokens with the highest score
        start_index = torch.argmax(start_scores)
        end_index = torch.argmax(end_scores)
        # Get the tokens corresponding to the answer
        tokens = self.tokenizer.convert_ids_to_tokens(encoding['input_ids'].squeeze())
        answer_tokens = tokens[start_index:end_index+1]
        # Convert answer tokens back to string
        answer = self.tokenizer.convert_tokens_to_string(answer_tokens)
        corrected_answer = ''

        for word in answer.split():
            #If it's a subword token
            if word[0:2] == '##':
                corrected_answer += word[2:]
            else:
                corrected_answer += ' ' + word

        pattern = r"\[\s*\d+\s*\]"
        # Replace the pattern with an empty string
        corrected_answer = re.sub(pattern, "", corrected_answer)
        corrected_answer = corrected_answer if "[SEP]" not in corrected_answer else "I don't know that"
        
        i = random.randint(0, len(self.image)-1) if len(self.image) > 0 else -1
        curr_im = self.image[i] if i >= 0 else None

        #print("res = ", corrected_answer, curr_im)
        return corrected_answer, curr_im



    def startAsking(self):
        while True:
            question = input("Enter question or 1 to print context or 2 to switch context or 0 to end \n")
            if question == "0":
                break
            elif question == "1":
                print(self.context)
            elif question == "2":
                topic = input("Enter topic you want to switch to \n")
                self.context = self.SetContext(topic)
            else:
                answer = self.getAnswer(question)

                print("Question:", question)
                if "[SEP]" in answer:
                    print("Answer:", "I don't know that")
                else:
                    print("Answer:", answer)
    


#qasys.startAsking()



