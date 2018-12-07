q = 0.0057565

# all the equations are based off those from Professor. Glickman at Harvard.
# the equations can be found at this link: http://www.glicko.net/glicko/glicko.pdf
def g(RD):
    x = (3 * (q ** 2) * (RD ** 2)) / (3.1415 ** 2)
    denominator = (1 + x) ** (1/2)
    return (1/denominator)

def estimated(r, rj, RDj):
    exponent = (g(RDj) * (r - rj)) / (400)
    denominator = 1 + (10 ** -exponent)
    return (1/denominator)

def d(r, rj, RDj):
    estimate = estimated(r, rj, RDj)
    d = (q ** 2) * (g(RDj) ** 2) * estimate * (1 - estimate)
    return (d ** -1)

def newRating(r, RD, rj, RDj, outcome, MoV, total):
    d1 = d(r, rj, RDj)
    estimate = estimated(r, rj, RDj)
    k = q / (1 / ((RD ** 2) + 1 / d1))
    # this line is our own personal touch
    k = k * (1 + (MoV / 80) + (MoV / total))
    result = g(RDj) * (outcome - estimate)
    result = result * k + r
    return result

def newRD(r, RD, rj, RDj):
    d1 = d(r, rj, RDj)
    x = (1 / (RD **2)) + (1 / (d1))
    x = (x ** -1) ** (1/2)
    return x