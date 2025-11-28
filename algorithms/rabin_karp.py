# Rabin-Karp search
def rabin_karp(text, pattern):
    n = len(text)
    m = len(pattern)
    matches = []
    base = 256
    mod = 10**9 + 7

    if m > n:
        return matches

    # compute initial hashes
    p_hash = 0
    t_hash = 0
    h = pow(base, m - 1, mod)

    for i in range(m):
        p_hash = (p_hash * base + ord(pattern[i])) % mod
        t_hash = (t_hash * base + ord(text[i])) % mod

    for i in range(n - m + 1):
        if p_hash == t_hash:
            if text[i:i + m] == pattern:
                matches.append(i)

        if i < n - m:
            t_hash = (t_hash - ord(text[i]) * h) * base + ord(text[i + m])
            t_hash %= mod

    return matches
