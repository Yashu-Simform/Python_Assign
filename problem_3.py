from collections import defaultdict, Counter

def importer(func):
    def wrapper(self,lst):
        from collections import defaultdict, Counter
        print('Imported sucessfully!')
        func(self, lst)

    return wrapper

#Approach1: compare all string and group similar ones after sorting
#Approach2: Make counter and compare counters if same append to list otherwise create a new list
#Approach3: 


class Accumulator:

    @importer
    def __init__(self, lst):
        self.lst = lst
        self.result = defaultdict(list)
        pass

    def approach1(self):
        for s in self.lst:
            ts = ''.join(sorted(s))
            self.result[ts].append(s)
        pass

    def splitStr(self, s):
        return [i for i in s]
    
    @importer
    def formSet(self):
        for s in self.lst:
            d = Counter(self.splitStr(s)).items()
            l = sorted(list(d))
            self.result[tuple(l)].append(s)

    def getResult(self):
        # self.formSet()
        self.approach1()    #O(n * klogk)
        return list(self.result.values())
    
inp = ["eat","tea","tan","ate","nat","bat"]
testCases = [
    ["eat","tea","tan","ate","nat","bat"],
    [''],
    ['aa', 'aaa'],
]

ac = Accumulator(inp)
result = ac.getResult()

print(result)