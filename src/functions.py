# -*- coding: utf-8 -*-
"""functions.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1G59TKxd8NN7bI4gIP_FUGMFihaowL8lq
"""

!pip install transformers sentence-transformers
import pandas as pd
import ast
from itertools import permutations
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import re
import spacy
from sentence_transformers import SentenceTransformer, models
from transformers import BertTokenizer
from transformers import get_linear_schedule_with_warmup
import torch
from torch.optim import AdamW
from torch.utils.data import DataLoader
from tqdm import tqdm
import time
import datetime
import random
import numpy as np
import pandas as pd
from transformers import AutoTokenizer, AutoModel
from transformers import BertTokenizer, RobertaTokenizer, RobertaModel
import math

def extract_words_from_json_string(input_string):
    try:
        # Use ast.literal_eval to safely convert the string to a list
        result_list = ast.literal_eval(input_string)
        if isinstance(result_list, list):
            return result_list
        else:
            raise ValueError("Input is not a string representation of a list.")
    except (ValueError, SyntaxError) as e:
        print(f"Error converting string to list: {e}")
        return None

def len_chcek(row):
      return [w for w in row if (len(w) >4) or (w == "sars") ]

#######################          BOW       ########################################################################
def generate_term_orders(terms):
    words = terms.split()
    if len(words) ==2:
      all_permutations = list(permutations(words))
      orders = [' '.join(permutation) for permutation in all_permutations]
      return orders
    else: return [terms]

def generate_term_orders_list_of_sords(words):
    X=[]
    for i in words:
      X+=generate_term_orders(i)
    return X
#Gard['Synonyms_bow']=Gard['Synonyms'].apply(lambda x: generate_term_orders_list_of_sords(x) )

########################      Removing stop words  #########################################################
def process_row(row):
    words = row.split()
    if len(words) > 2 :
        words = [word.lower()  for word in words if word.lower() not in ['syndrome','syndromes', 'disease','diseases']]
    return ' '.join(words)
def process_row_list(row):
      return [process_row(w) for w in row]

def remove_stop_words(text):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text)
    filtered_words = [word for word in words if word.lower() not in stop_words]
    return ' '.join(filtered_words)
def process_row_list_2(row):
    return [remove_stop_words(w) if (remove_stop_words(w) != '' and len(w.split()) > 2) else w for w in row]

def stem_text(text):
    # Initialize the Porter Stemmer
    stemmer = PorterStemmer()
    # Remove punctuation
    text_without_punctuation = re.sub(r'[^\w\s]', '', text)
    # Tokenize the text into words
    words = word_tokenize(text_without_punctuation)
    # Perform stemming on each word
    stemmed_words = [stemmer.stem(word) for word in words]
    # Join the stemmed words back into a single string
    stemmed_text = ' '.join(stemmed_words)
    return stemmed_text
def stem_text_list(row):
      return [stem_text(w) for w in row if len(stem_text(w)) >2 ]

def get_def(a):
    A=source_dict[a.lower()]
    if type(A)==str: return A
    else: return a

nltk.download('stopwords')
nltk.download('punkt')
Gard = pd.read_csv('/content/Gard_V1.csv')
Gard['Synonyms'] = Gard['Synonyms'].apply(lambda x: extract_words_from_json_string(x))
Gard['Synonyms'] =Gard['GardName'].apply(lambda x: [x])+Gard['Synonyms']

Gard['Synonyms_sw'] = Gard['Synonyms']#.apply(lambda x: process_row_list(x))
Gard['Synonyms_sw_bow']=Gard['Synonyms_sw'].apply(lambda x: generate_term_orders_list_of_sords(x) )
Gard['Synonyms_sw_bow']=Gard['Synonyms_sw_bow'].apply(lambda x: list(set(len_chcek(x))) )

#Gard['Synonyms_stem'] = Gard['Synonyms'].apply(lambda x: stem_text_list(x))
#Gard['Synonyms_stem_bow']=Gard['Synonyms_stem'].apply(lambda x: generate_term_orders_list_of_sords(x) )
Gard['Synonyms_sw_stem'] = Gard['Synonyms_sw'].apply(lambda x: stem_text_list(x))
Gard['Synonyms_sw_stem_bow']=Gard['Synonyms_sw_stem'].apply(lambda x: generate_term_orders_list_of_sords(x) )
#### make different
Gard['Synonyms_sw_stem'] = Gard['Synonyms_sw_stem'].apply(lambda x:list(set(len_chcek(x))) )
Gard['Synonyms_sw_stem_bow']=Gard['Synonyms_sw_stem_bow'].apply(lambda x: list(set(len_chcek(x))) )

Gard['Synonyms_sw'] = Gard['Synonyms_sw'].apply(lambda x: list(set(len_chcek(x))) )


Excluding_list = [
    'GARD:10311', 'GARD:10984', 'GARD:12351', 'GARD:12352', 'GARD:12638',
    'GARD:12915', 'GARD:12976', 'GARD:12977', 'GARD:15010', 'GARD:15042',
    'GARD:15066', 'GARD:15076', 'GARD:15080', 'GARD:15092', 'GARD:15112',
    'GARD:15119', 'GARD:15191', 'GARD:15192', 'GARD:15211', 'GARD:15300',
    'GARD:15315', 'GARD:15316', 'GARD:15357', 'GARD:15388', 'GARD:15394',
    'GARD:15395', 'GARD:15401', 'GARD:15402', 'GARD:15403', 'GARD:15415',
    'GARD:15422', 'GARD:15432', 'GARD:15443', 'GARD:15467', 'GARD:15483',
    'GARD:15504', 'GARD:15513', 'GARD:15525', 'GARD:15555', 'GARD:15564',
    'GARD:15565', 'GARD:15566', 'GARD:15567', 'GARD:15587', 'GARD:15600',
    'GARD:15603', 'GARD:15604', 'GARD:15605', 'GARD:15606', 'GARD:15607',
    'GARD:15608', 'GARD:15632', 'GARD:15637', 'GARD:15650', 'GARD:15651',
    'GARD:15657', 'GARD:15659', 'GARD:15696', 'GARD:15697', 'GARD:15752',
    'GARD:15779', 'GARD:15784', 'GARD:15785', 'GARD:15788', 'GARD:15848',
    'GARD:15853', 'GARD:15854', 'GARD:15986', 'GARD:15992', 'GARD:16059',
    'GARD:16131', 'GARD:16161', 'GARD:16184', 'GARD:16265', 'GARD:16267',
    'GARD:16269', 'GARD:16334', 'GARD:16337', 'GARD:16823', 'GARD:17047',
    'GARD:17343', 'GARD:17457', 'GARD:17458', 'GARD:17459', 'GARD:17460',
    'GARD:17461', 'GARD:17462', 'GARD:17463', 'GARD:17464', 'GARD:17465',
    'GARD:17514', 'GARD:17612', 'GARD:17795', 'GARD:17861', 'GARD:18046',
    'GARD:18057', 'GARD:18059', 'GARD:18060', 'GARD:18061', 'GARD:18259',
    'GARD:18285', 'GARD:18304', 'GARD:18384', 'GARD:18385', 'GARD:18472',
    'GARD:18477', 'GARD:18479', 'GARD:18485', 'GARD:18486', 'GARD:18512',
    'GARD:18550', 'GARD:18575', 'GARD:18577', 'GARD:18578', 'GARD:18579',
    'GARD:18580', 'GARD:18581', 'GARD:18582', 'GARD:18594', 'GARD:18595',
    'GARD:18596', 'GARD:18608', 'GARD:18609', 'GARD:18613', 'GARD:20322',
    'GARD:21425', 'GARD:2162', 'GARD:21865', 'GARD:22318', 'GARD:22319',
    'GARD:2456', 'GARD:3363', 'GARD:3364', 'GARD:3365', 'GARD:3366',
    'GARD:3367', 'GARD:3368', 'GARD:9185'
]
Excluding_list = ['GARD:{:07d}'.format(int(gard_id.split(':')[1])) for gard_id in Excluding_list]
Gard['GardId'] = Gard['GardId'].str.strip('"')
Gard = Gard[~Gard['GardId'].isin(Excluding_list)]


help=pd.read_csv('/content/J_GARD_master.csv')
source_dict = {}
for index, row in help.iterrows():
    source_name = row['SourceName']
    source_description = row['SourceDescription']
    if type(source_name) ==str:
       source_dict[source_name.lower()] = source_description


Gard['GardNamedef']=Gard.apply(lambda x:   get_def(x['GardName']), axis=1)

word_pattern = re.compile(r'\b\w+\b')
def split_sentence(sentence):
    # Use the pre-compiled pattern for splitting
    words = word_pattern.findall(sentence)
    return words

def word_matching(text,word):
   for i in  split_sentence(word):
     if i not in text:
        return False
   return True

def get_gard_title(text, list_chcek):
  if list_chcek in ['Synonyms_stem','Synonyms_sw_stem','Synonyms_stem_bow','Synonyms_sw_stem_bow']: text1=stem_text(text.lower())
  elif list_chcek in [ 'Synonyms_sw_nltk']  :          text1=remove_stop_words(text.lower())
  else:                                                  text1=text.lower()
  text2=split_sentence(text1)
  out=dict()
  for i in Gard.index:
    if Gard[list_chcek][i] != []:
      for j in  Gard[list_chcek][i]:
         if j in text1 and word_matching(text2,j)==True:
           if Gard['GardName'][i] in out:
                if len(j.split()) ==1:   out[Gard['GardName'][i]][0]+=text2.count(j)
                else: out[Gard['GardName'][i]][0]+=text1.count(j)
           else:
                if len(j.split()) ==1:out[Gard['GardName'][i]]=[text2.count(j)]
                else:  out[Gard['GardName'][i]]=[text1.count(j)]
  if out== {}: return None
  return out

def get_gard_title_stem_exact(text):
    exact_matching = get_gard_title(text, 'Synonyms_sw_bow') or {}
    Stemming_check = get_gard_title(text, 'Synonyms_sw_stem_bow') or {}
    combined_dict = {**exact_matching, **Stemming_check}  # Merge dictionaries
    # Remove keys that are part of another key
    keys_to_remove = {key1 for key1 in combined_dict for key2 in combined_dict if key1 != key2 and key1 in key2}
    combined_dict = {key: 1 for key in combined_dict if key not in keys_to_remove}
    return combined_dict or None


# Function to determine verb tense
def get_verb_tense(verb):
    if "VBD" in verb.tag_:
        return "past"
    elif ("MD" in verb.tag_ and "will" in verb.lemma_.lower()) or ('aim' in verb.lemma_.lower() ) :
        return "future"
    elif "VBP" in verb.tag_ or "VBZ" in verb.tag_:
        return "present"
    else:
        return "unknown"
# Function to determine if a sentence is negated
def is_sentence_negated(sentence):
    for token in sentence:
        if token.dep_ == "neg":
            return True
    return False


def check_sen(text):
  # Process the text
  doc = nlp(text)
  # Iterate over sentences in the document
  first_sentence = ''
  Priority,Future_positive,present_positive,positive='','','',''
  for i, sent in enumerate(doc.sents, 1):
    # Initialize a set to store unique tenses in the sentence
    sentence_tenses = set()
    # Iterate over tokens in the sentence
    for token in sent:
        # Check if the token is a verb
        if token.pos == spacy.symbols.VERB or token.pos == spacy.symbols.AUX:
            # Check the tense of the verb
            tense = get_verb_tense(token)
            sentence_tenses.add(tense)

    # Determine the overall tense of the sentence
    if is_sentence_negated(sent)==False and  ("past" not in sentence_tenses):
        if i == 1:    first_sentence = sent.text
        #positive+=sent.text
        elif  ("the goal of" in sent.text.lower()) or ("aim" in sent.text.lower()):
           Priority         =  Priority       + ' '+ sent.text
        elif "future" in sentence_tenses:
           Future_positive  =  Future_positive+ ' '+ sent.text
        #elif "present" in sentence_tenses and is_sentence_negated(sent)==False:
        elif :
           present_positive =  present_positive+' '+sent.text
        if i == 1:    first_sentence = sent.text
  return first_sentence,Priority,Future_positive,present_positive #,
# Sample text
text = "The goal of tis project was ird. This aim is not to go the first sentence. This is not the second sentence? And this is the third sentence."
check_sen(text)


def split_sentences_(text):
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s', text)
    return sentences


def get_sentence_with_word(paragraph, target_word):
    if not isinstance(paragraph, str):
        return ''

    # Define characters indicating the start of a new sentence
    new_sentence_chars = ['-', ':', ';', '1)', '2)', '3)', '4)', '5)', '6)', '7)', '8)']

    # Split the paragraph into sentences using provided characters
    for char in new_sentence_chars:
        paragraph = paragraph.replace(char, '.')

    # Split the paragraph into sentences using standard punctuation
    sentences =split_sentences_(paragraph)

    # Check for the target word in each sentence
    sen=''
    for sentence in sentences:
        if target_word.lower() in sentence.lower():
            sen+= sentence

    return sen
def stem_text_finding(text):
    # Initialize the Porter Stemmer
    stemmer = PorterStemmer()
    # Remove punctuation
    text_without_punctuation = text
    # Tokenize the text into words
    words = word_tokenize(text_without_punctuation)
    # Perform stemming on each word
    stemmed_words = [stemmer.stem(word) for word in words]
    # Join the stemmed words back into a single string
    stemmed_text = ' '.join(stemmed_words)
    return stemmed_text

def split_sentence(sentence):
    # Use regular expression to split words without including punctuation
    words = re.findall(r'\b\w+\b', sentence)
    return words
def word_matching(text,word):
   for i in  split_sentence(word):
     if i not in text:
        return False
   return True

def get_gard_abstract(text, list_chcek):
  #text=check_sen(text)
  if list_chcek in ['Synonyms_stem','Synonyms_sw_stem','Synonyms_stem_bow','Synonyms_sw_stem_bow']: text1=stem_text(text.lower())
  elif list_chcek in [ 'Synonyms_sw_nltk']  :          text1=remove_stop_words(text.lower())
  else:                                                  text1=text.lower()
  text2=split_sentence(text1)
  out=dict()
  sen=dict()
  for i in Gard.index:
    if Gard[list_chcek][i] != []:
      for j in  Gard[list_chcek][i]:
         if j in text1 and word_matching(text2,j)==True:
           if Gard['GardName'][i] in out:
                if len(j.split()) ==1:
                   out[Gard['GardName'][i]][0]+=text2.count(j)
                   #if list_chcek in ['Synonyms_stem','Synonyms_sw_stem','Synonyms_stem_bow','Synonyms_sw_stem_bow']:sen[Gard['GardName'][i]] += get_sentence_with_word(stem_text_finding(text.lower()), j)
                   #else:    sen[Gard['GardName'][i]] += get_sentence_with_word(text1, j)
                else:
                   out[Gard['GardName'][i]][0]+=text1.count(j)
                   #if list_chcek in ['Synonyms_stem','Synonyms_sw_stem','Synonyms_stem_bow','Synonyms_sw_stem_bow']:sen[Gard['GardName'][i]] += get_sentence_with_word(stem_text_finding(text.lower()), j)
                   #else:    sen[Gard['GardName'][i]] += get_sentence_with_word(text1, j)
           else:
                if len(j.split()) ==1:
                     out[Gard['GardName'][i]]=[text2.count(j)]
                     #if list_chcek in ['Synonyms_stem','Synonyms_sw_stem','Synonyms_stem_bow','Synonyms_sw_stem_bow']:sen[Gard['GardName'][i]] = get_sentence_with_word(stem_text_finding(text.lower()), j)
                     #else:    sen[Gard['GardName'][i]] = get_sentence_with_word(text1, j)
                else:
                     out[Gard['GardName'][i]]=[text1.count(j)]
                     #if list_chcek in ['Synonyms_stem','Synonyms_sw_stem','Synonyms_stem_bow','Synonyms_sw_stem_bow']:sen[Gard['GardName'][i]] = get_sentence_with_word(stem_text_finding(text.lower()), j)
                     #else:    sen[Gard['GardName'][i]] = get_sentence_with_word(text1, j)
  if out== {}: return None,None
  return out , ''#sen

def combine_dictionaries_count(dict1, dict2):
    combined_dict = {}
    # Update combined_dict with values from dict1
    for key, value in dict1.items():
        combined_dict[key] = combined_dict.get(key, 0) + sum(value)
    # Update combined_dict with values from dict2
    for key, value in dict2.items():
        combined_dict[key] = combined_dict.get(key, 0) + sum(value)
    return combined_dict

def combine_dictionaries_sent(dict1, dict2):
    combined_dict = {}
    # Update combined_dict with values from dict1
    for key, value in dict1.items():
        if key in combined_dict:
            combined_dict[key] += value
        else:
            combined_dict[key] = value
    # Update combined_dict with values from dict2
    for key, value in dict2.items():
        if key in combined_dict:
            combined_dict[key] += value
        else:
            combined_dict[key] = value
    return combined_dict

def  modified_dict(combined_dict):#,combined_dict_sen):
    keys_to_remove = set()
    for key1 in combined_dict:
        for key2 in combined_dict:
          #try:
            if key1 != key2 and (key1 in key2) and (combined_dict[key1] <= combined_dict[key2]):# and (combined_dict_sen[key1] in combined_dict_sen[key2]):
                keys_to_remove.add(key1)
          #except:
          #  pass
    for key in keys_to_remove:
        del combined_dict[key]
        #del combined_dict_sen[key]
    return combined_dict


def get_gard_abstract_stem_exact(text):
  if text and isinstance(text, str):
    exact_matching, exact_matching_sen=get_gard_abstract(text, 'Synonyms_sw')
    #print(exact_matching)
    Stemming_chcek, Stemming_chcek_sen=get_gard_abstract(text, 'Synonyms_sw_stem')
    #print(Stemming_chcek)
    if exact_matching is None:exact_matching = {}
    if Stemming_chcek is None:Stemming_chcek = {}
    #if exact_matching_sen is None:exact_matching_sen = {}
    #if Stemming_chcek_sen is None:Stemming_chcek_sen = {}

    combined_dict    = combine_dictionaries_count(exact_matching,Stemming_chcek)
    #combined_dict_sen= combine_dictionaries_sent(exact_matching_sen,Stemming_chcek_sen)
    # Remove keys that are part of another key
    combined_dict=modified_dict(combined_dict)#,combined_dict_sen)
    if combined_dict=={}:return {}
    return combined_dict
  return {}


class BertForSTS(torch.nn.Module):
    def __init__(self):
        super(BertForSTS, self).__init__()
        #self.bert = models.Transformer("bert-base-uncased", max_seq_length=512)
        self.bert = models.Transformer('microsoft/BiomedNLP-PubMedBERT-base-uncased-abstract-fulltext', max_seq_length=1000)
        #model = AutoModel.from_pretrained(model_name)
        self.pooling_layer = models.Pooling(self.bert.get_word_embedding_dimension())
        self.sts_bert = SentenceTransformer(modules=[self.bert, self.pooling_layer])
    def forward(self, input_data):
        output = self.sts_bert(input_data)['sentence_embedding']
        return output
# Instantiate the model and move it to GPU
if torch.cuda.is_available():
    device = torch.device("cuda")
    print(f'There are {torch.cuda.device_count()} GPU(s) available.')
    print('We will use the GPU:', torch.cuda.get_device_name(0))
else:
    print('No GPU available, using the CPU instead.')
    device = torch.device("cpu")


def predict_similarity(sentence_pair):
  test_input = tokenizer(sentence_pair, padding=True, truncation=True, return_tensors="pt").to(device) # max_length = 512,
  test_input['input_ids'] = test_input['input_ids']
  test_input['attention_mask'] = test_input['attention_mask']
  del test_input['token_type_ids']
  output = model(test_input)
  sim = torch.nn.functional.cosine_similarity(output[0], output[1], dim=0).item()
  return sim

def is_about_term(input_text, target_term):
  sentence_pair=[input_text, target_term]
  test_input = tokenizer(sentence_pair, padding=True, truncation=True, return_tensors="pt").to(device) # max_length = 512,
  test_input['input_ids'] = test_input['input_ids']
  test_input['attention_mask'] = test_input['attention_mask']
  del test_input['token_type_ids']
  output = model(test_input)
  sim = torch.nn.functional.cosine_similarity(output[0], output[1], dim=0).item()
  return  round(sim,2)

def get_sen(paragraph, target_word,title):
    if not isinstance(paragraph, str):
        return title.lower()
    # Define characters indicating the start of a new sentence
    new_sentence_chars = ['-', ':', ';', '1)', '2)', '3)', '4)', '5)', '6)', '7)', '8)']
    # Split the paragraph into sentences using provided characters
    for char in new_sentence_chars:
        paragraph = paragraph.replace(char, '.')

    # Split the paragraph into sentences using standard punctuation
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s', paragraph)

    # Check for the target word in each sentence
    sen=''
    words_to_check=list(Gard[Gard['GardName']==target_word]['Synonyms_sw'].values)[0]
    words_to_check2=list(Gard[Gard['GardName']==target_word]['Synonyms_sw_stem'].values)[0]
    for sentence in sentences:
       for i in words_to_check:
         if i.lower() in sentence.lower() and (sentence.lower() not in sen):
            sen+= sentence
            break
       for i in words_to_check2:
         if i.lower() in stem_text(sentence.lower()) and (sentence.lower() not in sen):
            sen+= sentence
            break
    if sen != '': return sen.lower()
    else: return title.lower()

def normalize(x):
   if x < 7:
       return math.log(x) / math.log(7)
   else:
    return 1

def normalize_combined_dictionary(input_text,title_,dict1, dict2, dict3, dict4,min_, max_,type):
    if    type =='title':      factor=20
    elif  type =='statement':  factor=2
    else: factor=1
    dict1 = {key: value * 5 for key, value in dict1.items()}
    # Make the values of the second dictionary two times
    dict2 = {key: value * 7 for key, value in dict2.items()}
    dict3 = {key: value * 3 for key, value in dict3.items()}
    # Combine all dictionaries
    combined_dict = {key: dict1.get(key, 0) + dict2.get(key, 0) + dict3.get(key, 0) + dict4.get(key, 0) for key in set(dict1) | set(dict2) | set(dict3) | set(dict4)}
    # Normalize the values of the combined dictionary
    total_frequency = sum(combined_dict.values())
    # Check if total_frequency is zero to avoid division by zero
    if total_frequency == 0:
        return {}
    normalized_dict = {key: value   for key, value in combined_dict.items()}
    result_dict = {}
    for key, value in normalized_dict.items():
        #if  is_about_term(input_text.lower(), key) >=0.5:
        #sen_has_gard=get_sen(input_text.lower(), key,title_)
        defin=get_def(key)
        try:
          #result_dict[key] = [20 if  type =='title' else 1+(factor*value //2), is_about_term(sen_has_gard,  defin), is_about_term(input_text.lower(),  defin), sen_has_gard]
          result_dict[key] = [normalize(20 if  type =='title' else 1+(factor*value //2)),  is_about_term(input_text.lower(),  defin)]

        except:
          try:
              #result_dict[key] = [20 if  type =='title' else 1+ (factor*value //2), is_about_term(sen_has_gard[:2000],  defin[:2000]), is_about_term(input_text.lower()[:2000],  defin[:2000]), sen_has_gard]
              result_dict[key] = [normalize(20 if  type =='title' else 1+ (factor*value //2)), is_about_term(input_text.lower()[:2000],  defin[:2000])]
          except:
              try:
                  result_dict[key] = [normalize(20 if  type =='title' else 1+ (factor*value //2)) ,  is_about_term(input_text.lower()[:1500],  defin[:1500])]
                  #result_dict[key] = [20 if  type =='title' else 1+ (factor*value //2) , is_about_term(sen_has_gard[:1500],  defin[:1500]), is_about_term(input_text.lower()[:1500],  defin[:1500]), sen_has_gard]

              except:
                  #result_dict[key] = [20 if  type =='title' else 1+ (factor*value //2) , is_about_term(sen_has_gard[:1000],   defin[:1000]), is_about_term(input_text.lower()[:500],  defin[:1000]), sen_has_gard]
                  result_dict[key] = [normalize(20 if  type =='title' else 1+ (factor*value //2)) , is_about_term(input_text.lower()[:500],  defin[:1000])]


    return result_dict


def update_dictionary(dictionary):
    updated_dict = {}
    for key, value in dictionary.items():
        new_key = Gard[Gard['GardName'] == key]['GardId'].tolist()
        if new_key:
            new_key = new_key[0].replace('"', '')
            updated_dict[(key,new_key)] = value
        else:
            updated_dict[key] = value
    return updated_dict

def grad_id(title_, Public_health_relevance_statement, abstract_):
    if not isinstance(title_, str) and not isinstance(Public_health_relevance_statement, str) and not isinstance(abstract_, str):
        return ''  # Return default values when no string input is provided
    if title_ and isinstance(title_, str):
        name = get_gard_title_stem_exact(title_)
        if name:
          if abstract_ and isinstance(abstract_, str):
                return normalize_combined_dictionary(abstract_,title_,name,{},{},{},1,1,'title')
          else: return normalize_combined_dictionary(title_,title_,name,{},{},{},1,1,'title')

    if Public_health_relevance_statement and isinstance(Public_health_relevance_statement, str):
        A, B, C,D = check_sen(Public_health_relevance_statement)
        name1 = get_gard_abstract_stem_exact(A)
        name2 = get_gard_abstract_stem_exact(B)
        name3 = get_gard_abstract_stem_exact(C)
        name4 = get_gard_abstract_stem_exact(D)
        name=normalize_combined_dictionary(Public_health_relevance_statement,title_,name1,name2,name3,name4,0.7,0.9,'statement')
        if name and (name !={}): return name

    if abstract_ and isinstance(abstract_, str):
        A, B, C , D = check_sen(abstract_)
        name1 = get_gard_abstract_stem_exact(A)
        name2 = get_gard_abstract_stem_exact(B)
        name3 = get_gard_abstract_stem_exact(C)
        name4 = get_gard_abstract_stem_exact(D)
        name=normalize_combined_dictionary(abstract_,title_,name1,name2,name3,name4,0,0.7,'abstract')
        if name and (name !={}): return name

nlp = spacy.load("en_core_web_sm")
tokenizer = AutoTokenizer.from_pretrained('microsoft/BiomedNLP-PubMedBERT-base-uncased-abstract-fulltext')
model = BertForSTS()
model.to(device)
model.eval()
PATH = '/content/drive/My Drive/Finetunned_Bert_2.pt'
model = BertForSTS()
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.load_state_dict(torch.load(PATH, map_location=device))
model.eval()
def Find(a,b,c):
  grad_id(a, b,c)