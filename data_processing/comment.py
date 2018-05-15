
def intersection(right=[], left=[]):
    return list(set(right).intersection(set(left)))

def union(right=[], left=[]):
    return list(set(right).union(set(left)))

def union(right=[], left=[]):
    return list(set(right).difference(set(left))) # not have in left
