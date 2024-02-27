import torch, requests
from transformers import BertForQuestionAnswering
from transformers import BertTokenizer
from bs4 import BeautifulSoup
import warnings, re, random
import spacy


warnings.filterwarnings("ignore", message = "Be aware, overflowing tokens are not returned for the setting you have chosen.*" \
, category=RuntimeWarning)
nlp = spacy.load('en_core_web_sm')



class QASystem:
    def __init__(self):
        self.model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
        self.tokenizer = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
        self.context = None
        self.topic = None
        self.image = None
        #self.context = self.SetContext(input("Enter topic you want to enquire \n"))


    def SetContext(self, topic):
        self.topic = topic
        response = requests.get(f"https://en.wikipedia.org/wiki/{topic.lower()}")
        soup = BeautifulSoup(response.content, "html.parser")
        paragraphs = soup.find_all("p")
        para = ""
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
        

    def getAnswer(self, question, model = nlp):
        if question == "1":
            return self.context, None        
        
        doc = model(question)
        s = ""
        s_alt = []
        c_pn = 0
        for token in doc:
            print(token, token.pos_)
            if token.pos_ == 'PROPN':
                s += (str(token) + " ") 
                c_pn += 1
            elif token.pos_ == 'NOUN':
                s_alt += [str(token)]
                
        if c_pn > 0 :
            self.SetContext(s.strip())
        else:
            self.SetContext(s_alt[0].strip())
        
        #Answering question based on context        
        encoding = self.tokenizer.encode_plus(text=question, text_pair=self.context, max_length=512, truncation=True, return_tensors="pt")
        start_scores, end_scores = self.model(**encoding, return_dict=False)
        start_index = torch.argmax(start_scores)
        end_index = torch.argmax(end_scores)
        tokens = self.tokenizer.convert_ids_to_tokens(encoding['input_ids'].squeeze())
        answer_tokens = tokens[start_index:end_index+1]
        answer = self.tokenizer.convert_tokens_to_string(answer_tokens)
        corrected_answer = ''

        for word in answer.split():
            if word[0:2] == '##':
                corrected_answer += word[2:]
            else:
                corrected_answer += ' ' + word

        pattern = r"\[\s*\d+\s*\]"
        corrected_answer = re.sub(pattern, "", corrected_answer)
        corrected_answer = corrected_answer if "[SEP]" not in corrected_answer else "I don't know that"
        
        i = random.randint(0, len(self.image)-1) if len(self.image) > 0 else -1
        curr_im = self.image[i] if i >= 0 else None

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



