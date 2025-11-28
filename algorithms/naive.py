# Naive string matching
def naive_search(text, pattern):
    n = len(text)
    m = len(pattern)
    matches = []

    for i in range(n - m + 1):
        if text[i:i + m] == pattern:
            matches.append(i)

    return matches
