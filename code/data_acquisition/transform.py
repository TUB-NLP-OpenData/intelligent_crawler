import pandas as pd
import json


def lcs(S, T):

    """
    Find longest common matching string for title field
    :param:
        S, T: Type [String] Input strings
    :return:
        lcs_set: Type [set] Return a set of longest common substrings
    """
    m = len(S)
    n = len(T)
    counter = [[0] * (n + 1) for x in range(m + 1)]
    longest = 0
    lcs_set = set()
    for i in range(m):
        for j in range(n):
            if S[i] == T[j]:
                c = counter[i][j] + 1
                counter[i + 1][j + 1] = c
                if c > longest:
                    lcs_set = set()
                    longest = c
                    lcs_set.add(S[i - c + 1:i + 1])
                elif c == longest:
                    lcs_set.add(S[i - c + 1:i + 1])

    return lcs_set


if __name__ == "__main__":
    elements=["title","published","content"]
    json_input="out.json"
    pdf=pd.read_json(json_input)
    print (pdf.columns)

    for index, r in pdf.iterrows():
        for e in elements:
            print (r[e])
            longest_string=str(lcs(r[e],r.html).pop())
            offset_start=r.html.find(longest_string)
            if offset_start>0:
                offset_end=offset_start+len(longest_string)
            else:
                print ("not found")
            print (offset_start)
            print (offset_end)
            print ("---")
        break

