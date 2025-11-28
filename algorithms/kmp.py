# KMP – Efficient string pattern matching
def build_lps(pattern):
    m = len(pattern)
    lps = [0] * m
    i = 1
    length = 0

    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps


def kmp_search(text, pattern):
    n = len(text)
    m = len(pattern)
    lps = build_lps(pattern)
    matches = []

    i = 0  # text pointer
    j = 0  # pattern pointer

    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1

            if j == m:
                matches.append(i - j)
                j = lps[j - 1]
        else:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return matches
