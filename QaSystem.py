import torch, requests
from transformers import BertForQuestionAnswering
from transformers import BertTokenizer, BertTokenizerFast, BertConfig
from bs4 import BeautifulSoup
import warnings, re, random
import spacy


warnings.filterwarnings("ignore", message = "Be aware, overflowing tokens are not returned for the setting you have chosen.*" \
, category=RuntimeWarning)
spacy.cli.download("en_core_web_sm")
nlp = spacy.load('en_core_web_sm')



class QASystem:
    def __init__(self):
        model_name = "bert-large-uncased-whole-word-masking-finetuned-squad"
        config = BertConfig.from_pretrained(model_name)
        config.max_position_embeddings = 512 
        
        self.model = BertForQuestionAnswering.from_pretrained(model_name, config = config, ignore_mismatched_sizes=True)
        self.tokenizer = BertTokenizerFast.from_pretrained(model_name, config = config) 
        self.context = None
        self.topic = None
        self.image = None
        #self.context = self.SetContext(input("Enter topic you want to enquire \n"))


    def SetContext(self, topic):
        topic = topic.title()
        print(topic, " topic")
        self.topic = topic
        response = requests.get(f"https://en.wikipedia.org/wiki/{topic}")
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
        
        # if "may refer to" in self.context.split(":")[0]:
        #     l = soup.find_all('a')
        #     for link in l:
        #         print(link, topic)
        #         if topic.lower() in link.lower():
        #             self.SetContext(link.split(" ")[2].split("/")[-1])
        #             break
        
            
        

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
        #print(answer)
        corrected_answer = ''

        for word in answer.split():
            if word[0:2] == '##':
                corrected_answer += word[2:]
            else:
                corrected_answer += ' ' + word

        pattern = r"\[\s*\d+\s*\]"
        corrected_answer = re.sub(pattern, "", corrected_answer)
        print(corrected_answer, len(corrected_answer), type(corrected_answer))

        corrected_answer = "I don't know that" if ( "Other reasons this message may be displayed:" in self.context or "[SEP]" in corrected_answer or len(corrected_answer) < 5) else corrected_answer 
        if "may refer to:" in self.context[:30]:
            corrected_answer = "Ambiguous context"
            
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



