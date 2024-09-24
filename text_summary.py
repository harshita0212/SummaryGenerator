import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

text = """Samsung is a global technology leader known for its innovation and cutting-edge advancements in
electronics, particularly in consumer devices like smartphones, televisions, and home appliances.
Founded in 1938 in South Korea, Samsung has grown into a multinational conglomerate, significantly 
shaping industries such as mobile communications, semiconductors, and display technologies. 

The company's Galaxy series of smartphones has become one of the most popular and competitive in
the market, rivaling other tech giants. Beyond consumer electronics, Samsung is a key player in
the development of 5G technology and smart home ecosystems, consistently pushing the boundaries
of digital innovation. With a strong focus on research and development, Samsung continues to 
influence global trends in technology, sustainability, and design."""

def summarizer(rawdocs):
    stopwords = list(STOP_WORDS)
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(rawdocs)
    tokens = [token.text for token in doc]

    word_freq = {}
    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            if word.text not in word_freq.keys():
                word_freq[word.text] = 1
            else:
                word_freq[word.text] += 1

    max_freq = max(word_freq.values())

    for word in word_freq.keys():
        word_freq[word] = word_freq[word] / max_freq

    sent_tokens = [sent for sent in doc.sents]

    sent_scores = {}
    for sent in sent_tokens:
        for word in sent:
            if word.text in word_freq.keys():
                if sent not in sent_scores.keys():
                    sent_scores[sent] = word_freq[word.text]
                else:
                    sent_scores[sent] += word_freq[word.text]

    select_len = int(len(sent_tokens) * 0.3)

    # Creating summary
    summary_sentences = nlargest(select_len, sent_scores, key=sent_scores.get)
    final_summary = [sent.text for sent in summary_sentences]
    summary = ' '.join(final_summary)

    return summary, doc, len(rawdocs.split(' ')), len(summary.split(' '))

# Example usage:
summary, doc, original_length, summary_length = summarizer(text)
print("Original Length:", original_length)
print("Summary Length:", summary_length)
print("Summary:\n", summary)
