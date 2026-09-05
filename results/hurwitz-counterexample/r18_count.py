"""Exact bare-triple counter; standard library only, no external LR engine."""
import json
import sys


def triangular(t, slow=False):
    amax, bmax = 7*t+2, 6*t+1
    width = bmax+1
    old = [0]*((amax+1)*width)
    old[0] = 1

    def diagonal(prefix, a, b, k):
        if a < 0 or b < 0:
            return 0
        s = a+b-k
        lo = max(0, a-k, s-bmax)
        hi = min(amax, a, s)
        if lo > hi:
            return 0
        value = prefix[hi*width+s-hi]
        if lo > 0 and s-lo+1 <= bmax:
            value -= prefix[(lo-1)*width+s-lo+1]
        return value

    for _ in range(18):
        new = [0]*len(old)
        if slow:
            for a in range(amax+1):
                for b in range(bmax+1):
                    new[a*width+b] = sum(
                        old[(a-i)*width+b-j]
                        for i in range(min(t, a)+1)
                        for j in range(min(t-i, b)+1)
                    )
        else:
            prefix = [0]*len(old)
            for a in range(amax+1):
                for b in range(bmax+1):
                    index = a*width+b
                    prefix[index] = old[index]
                    if a > 0 and b < bmax:
                        prefix[index] += prefix[index-width+1]
            for a in range(amax+1):
                for b in range(bmax+1):
                    index = a*width+b
                    value = old[index] - diagonal(prefix, a, b, t+1)
                    value += diagonal(prefix, a-1, b-1, t)
                    if a > 0:
                        value += new[index-width]
                    if b > 0:
                        value += new[index-1]
                    if a > 0 and b > 0:
                        value -= new[index-width-1]
                    if value < 0:
                        raise ArithmeticError("negative intermediate coefficient")
                    new[index] = value
        old = new

    def coefficient(a, b):
        return old[a*width+b] if a >= 0 and b >= 0 else 0

    return (coefficient(7*t, 6*t) - coefficient(7*t, 6*t+1)
            - coefficient(7*t+1, 6*t-1) + coefficient(7*t+1, 6*t+1)
            + coefficient(7*t+2, 6*t-1) - coefficient(7*t+2, 6*t))


def tableau(t):
    # Positive horizontal-strip recurrence, independent of alternant/convolution.
    states = {(0, 0, 0): 1}
    for _ in range(18):
        new = {}
        for (a, b, c), count in states.items():
            for da in range(min(t, 7*t-a)+1):
                for db in range(min(t-da, 6*t-b, a-b)+1):
                    dc = t-da-db
                    if c+dc > min(b, 5*t):
                        continue
                    key = a+da, b+db, c+dc
                    new[key] = new.get(key, 0)+count
        states = new
    return states.get((7*t, 6*t, 5*t), 0)


def main():
    if len(sys.argv) != 3:
        raise ValueError("usage: independent_count.py METHOD T")
    method, text = sys.argv[1:]
    if not text.isascii() or not text.isdecimal():
        raise ValueError("T must be a nonnegative decimal integer")
    t = int(text)
    if t > 37 or method not in ("fast", "slow", "tableau"):
        raise ValueError("outside frozen method or t range")
    if method != "fast" and t > 8:
        raise ValueError("control outside frozen t<=8 range")
    result = tableau(t) if method == "tableau" else triangular(t, method == "slow")
    if not isinstance(result, int) or result < 0:
        raise ArithmeticError("invalid exact LR count")
    print(json.dumps({"method": method, "t": t, "value": str(result)}, sort_keys=True))


if __name__ == "__main__":
    main()
