def count_words(text):
    """Count nonempty whitespace-delimited words in a string."""
    return len([word for word in text.split(" ") if word])
