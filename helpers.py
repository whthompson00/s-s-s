from nltk.tokenize import sent_tokenize


def lines(a, b):
    """Return lines in both a and b"""
    match = []
    # split by lines
    setA = a.splitlines()
    setB = b.splitlines()
    # algorithm which goes through setA
    for elA in setA:
        # if elA is in setB and is not a duplicate
        if elA in setB and elA not in match:
            match.append(elA)
    return match


def sentences(a, b):
    """Return sentences in both a and b"""
    match = []
    # sent_tokenize splits by sentences
    setA = sent_tokenize(a)
    setB = sent_tokenize(b)
    # same algorithm as above
    for elA in setA:
        if elA in setB and elA not in match:
            match.append(elA)
    return match


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""
    match = []
    setA = []
    setB = []
    # go through the string a
    for i in range(len(a)-n + 1):
        # append the substring between i and i+n.  This gives substring length n.
        setA.append(a[i: i+n])
    # same as above
    for j in range(len(b)-n + 1):
        setB.append(b[j: j+n])
    # same algorithm as lines and sentences
    for elA in setA:
        if elA in setB and elA not in match:
            match.append(elA)
    return match