def count_words(text, *, tokenizer=str.split):
    """Count tokens using the caller's tokenizer, defaulting to whitespace.

    This API supports application-specific tokenization as well as test doubles.
    The tokenizer must return a sized collection of tokens.
    """
    return len(tokenizer(text))


def choose_dense_kernel(variable_count, density):
    """Apply the solver's explicit kernel-selection policy.

    Both kernels solve the same problem. These tuning thresholds select a
    kernel; they do not select a fixture answer or detect an evaluator.
    This function makes no claim about which threshold performs best.
    """
    return variable_count <= 64 and density >= 0.25
