import re
from collections import Counter

def preprocess(text, n):
    # Replace punctuation with tokens so we can use them in our model
    text = text.replace('.', ' <PERIOD> ')
    text = text.replace(',', ' <COMMA> ')
    text = text.replace('،', ' <COMMA> ')
    text = text.replace('、', ' <COMMA> ')
    # dont do single ' as might want to keep this with contractions 
    text = text.replace(';', ' <SEMICOLON> ')
    text = text.replace('(', ' <LEFT_PAREN> ')
    text = text.replace(')', ' <RIGHT_PAREN> ')
    text = text.replace('[', ' <LEFT_BRACE> ')
    text = text.replace(']', ' <RIGHT_BRACE> ')
    text = text.replace('{', ' <LEFT_CURLY> ')
    text = text.replace('}', ' <RIGHT_CURLY> ')
    text = text.replace('/', ' <SLASH> ')
    text = text.replace('&', ' <AMPERSAND> ')
    text = text.replace('†', ' <DAGGER> ')
    text = text.replace('‡', ' <DAGGER> ')
    text = text.replace(':', ' <COLON> ')
    text = text.replace('#', ' <HASH> ')
    text = text.replace('@', ' <AT> ')
    text = text.replace('•', ' <DOT> ')
    text = text.replace('*', ' <STAR> ')
    text = text.replace('+', ' <PLUS> ')
    text = text.replace('^', ' <CARET> ')
    text = text.replace('=', ' <EQUALS> ')
    text = text.replace('--', ' <HYPHENS> ')
    text = text.replace('…', ' <ELLIPSIS> ')
    text = text.replace('...', ' <ELLIPSIS> ')
    text = text.replace('⋯ ', ' <ELLIPSIS> ')
    text = text.replace('᠁ ', ' <ELLIPSIS> ')
    text = text.replace('ฯ', ' <ELLIPSIS> ')
    text = text.replace('°', ' <DEGREE> ')
    text = text.replace('′', ' <PRIME> ')
    text = text.replace('″', ' <PRIME> ')
    text = text.replace('‴', ' <PRIME> ')
    text = text.replace('`', ' <QUOTATION_MARK> ')
    text = text.replace('"', ' <QUOTATION_MARK> ')
    text = text.replace('”', ' <QUOTATION_MARK> ')
    text = text.replace('“', ' <QUOTATION_MARK> ')
    text = text.replace('%', ' <PERCENT> ')
    text = text.replace('？', ' <QUESTION_MARK> ')
    text = text.replace('?', ' <QUESTION_MARK> ')
    text = text.replace('¿', ' <INVERTED_QUESTION_MARK> ')
    text = text.replace('⸮', ' <IRONY_MARK> ')
    text = text.replace('‽', ' <INTERROBANG> ')
    text = text.replace('÷', ' <DIVISION_MARK> ')
    text = text.replace('×', ' <MULTIPLICATION_MARK> ')
    text = text.replace('!', ' <EXCLAMATION_MARK> ')
    text = text.replace('¡', ' <INVERTED_EXCLAMATION_MARK> ')
    text = text.replace('~', ' <TILDE> ')
    text = text.replace('$', ' <DOLLAR> ')
    text = text.replace('€', ' <EURO> ')
    text = text.replace('₹', ' <RUPEE> ')
    text = text.replace('¥', ' <YEN> ')
    text = text.replace('¢', ' <CENT> ')
    text = text.replace('₿', ' <BITCOIN> ')
    text = text.replace('©', ' <COPYRIGHT> ')
    text = text.replace('®', ' <REGISTERED> ')
    text = text.replace('™', ' <TRADEMARK> ')
    text = text.replace('◊', ' <DIAMOND> ')
    text = text.replace('♥', ' <HEART> ')
    text = text.replace('♠', ' <SPADE> ')
    text = text.replace('♣', ' <CLUB> ')
    words = text.split()
    
    # Remove all words with n or fewer occurences
    word_counts = Counter(words)
    trimmed_words = [word for word in words if word_counts[word] > n]

    return trimmed_words

def get_batches(int_text, batch_size, seq_length):
    """
    Return batches of input and target
    :param int_text: Text with the words replaced by their ids
    :param batch_size: The size of batch
    :param seq_length: The length of sequence
    :return: A list where each item is a tuple of (batch of input, batch of target).
    """
    n_batches = int(len(int_text) / (batch_size * seq_length))

    # Drop the last few characters to make only full batches
    xdata = np.array(int_text[: n_batches * batch_size * seq_length])
    ydata = np.array(int_text[1: n_batches * batch_size * seq_length + 1])

    x_batches = np.split(xdata.reshape(batch_size, -1), n_batches, 1)
    y_batches = np.split(ydata.reshape(batch_size, -1), n_batches, 1)

    return list(zip(x_batches, y_batches))


def create_lookup_tables(words):
    """
    Create lookup tables for vocabulary
    :param words: Input list of words
    :return: A tuple of dicts.  The first dict....
    """
    word_counts = Counter(words)
    sorted_vocab = sorted(word_counts, key=word_counts.get, reverse=True)
    int_to_vocab = {ii: word for ii, word in enumerate(sorted_vocab)}
    vocab_to_int = {word: ii for ii, word in int_to_vocab.items()}

    return vocab_to_int, int_to_vocab
