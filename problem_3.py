from collections import defaultdict, Counter
from resource_track import ResourceUsageTracker

def importer(func):
    def wrapper(self,lst):
        from collections import defaultdict, Counter
        print('Imported sucessfully!')
        func(self, lst)

    return wrapper

#Approach1: compare all string and group similar ones after sorting
#Approach2: Make counter and compare counters if same append to list otherwise create a new list

class Accumulator:

    def __init__(self, lst):
        self.lst = lst
        self.result = defaultdict(list)

    @ResourceUsageTracker()
    def approach1(self):
        for s in self.lst:
            ts = ''.join(sorted(s))
            self.result[ts].append(s)

    def splitStr(self, s):
        return [i for i in s]
    
    @ResourceUsageTracker()
    def formSet(self):
        for s in self.lst:
            d = Counter(self.splitStr(s)).items()
            l = sorted(list(d))
            self.result[tuple(l)].append(s)

    def getResult(self):
        self.formSet()
        # self.approach1()    #O(n * klogk)
        return list(self.result.values())
    
inp = ["eat","tea","tan","ate","nat","bat"]
testCases = [
    ["eat","tea","tan","ate","nat","bat"],
    [''],
    ['aa', 'aaa'],
]
print(f"Default case: {inp}")
want = input('Want to add custom input: type "y": ')
if want == 'y':
    lst_size = input('Number of anagrams you want to enter: ')
    inp_lst = []
    for i in lst_size:
        inp1 = input(f'Enter {i+1}th anagrams: ')
        inp_lst.append(inp1)
    inp = inp_lst

ac = Accumulator(inp)
result = ac.getResult()

print(result)