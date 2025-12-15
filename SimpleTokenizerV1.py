import re
import os

cwd = os.getcwd()
path = os.path.join(cwd, "the-verdict.txt")

with open(path, "r", encoding= "utf-8") as f:
    raw_text = f.read()

#Gets tokens, but includes white spaces, Nones, etc
uncleanedTokens = re.split(r'([,.:;?_!"()\']|--|\s+)', raw_text)

#Creates new list without white spaces/Nones
tokens = [token for token in uncleanedTokens if token.strip()]
tokens.extend(['<|endoftext|>', '<|unk|>'])

#Gives unique tokens an integer value, could have also used zip(sorted(set(tokens)), range(0, len(tokens)))
vocab = {word: key for key, word in enumerate(sorted(set(tokens)))}

class SimpleTokenizerV1:
    def __init__(self, vocab):
        self.vocab = vocab
        self.reverseVocab = {i:s for s,i in vocab.items()}
    
    def encode(self, text):
        words = re.split(r'([,.:;?_!"()\']|--|\s)', text)
        words = [word for word in words if word.strip()] #remove white space
        words = [word if word in self.vocab else "<|unk|>" for word in words] #replace unknown words with |<unk>|
        ids = [self.vocab[s] for s in words] #convert to ids
        return ids
        
    def decode(self, ids):
        text = " ".join([self.reverseVocab[i] for i in ids])
        # Replace spaces before the specified punctuations
        text = re.sub(r'\s+([,.?!"()\'])', r'\1', text)
        return text
    
tokenizer = SimpleTokenizerV1(vocab)

text1 = "Hello, do you like tea?"
text2 = "In the sunlit terraces of the palace."

text = " <|endoftext|> ".join((text1, text2)) 
print(tokenizer.encode(text))
print(tokenizer.decode(tokenizer.encode(text)))