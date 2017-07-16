import nltk


class Analyzer():
    """Implements sentiment analysis."""


    def __init__(self, positives, negatives):
        """Initialize Analyzer."""
        with open("positive-words.txt") as positive:
            # make a list
            self.positives = []
            # add the word to the list if it does not start with a ; and is longer than 1 character
            for line in positive:
                if line.startswith(";") == False and len(line)>1:
                    self.positives.append(line.strip(" \n"))


        with open("negative-words.txt") as negative:
            # make a list
            self.negatives = []
            # add the word to the list if it does not start with a ; and is longer than 1 character
            for line in negative:
                if line.startswith(";") == False and len(line)>1:
                    self.negatives.append(line.strip(" \n"))
                    

    def analyze(self, text):
        """Analyze text for sentiment, returning its score."""
        score = 0
        
        # initialize the tokenizer and the list 'tokens'
        tokenizer = nltk.tokenize.TweetTokenizer()
        tokens = tokenizer.tokenize(text)
        
        # for every token in the list, check if it's either positive, negative or neutral and add or substract a point correspondingly
        for token in tokens:
            if token.lower() in self.positives:
                score += 1
            elif token.lower() in self.negatives:
                score -= 1
        return score
