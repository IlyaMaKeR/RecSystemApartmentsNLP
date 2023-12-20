import spacy
from nltk.corpus import stopwords
import nltk

nltk.download('stopwords')

def process_query(query):
    nlp = spacy.load("ru_core_news_sm")

    doc = nlp(query)

    tags = []

    stop_words = set(stopwords.words('russian'))
    sw = ['хотеть','желать','квартира','жильё']

    current_number = None
    current_pos = None

    for token in doc:
        
        if token.pos_ == 'NUM':
            current_number = token.text
            current_pos = token.pos_
            
        elif token.pos_ == 'NOUN' and current_number is not None:
            tags.append(f'{current_number} {token.lemma_}')
            current_number = None 
            
        elif token.lemma_.lower() not in stop_words and current_number is None:
            tags.append(token.lemma_)

    if current_number is not None:
        tags.append(current_number)
    tags = [tag for tag in tags if tag not in sw and tag != ' ']

    return tags
