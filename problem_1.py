import logging as log
import time
import tracemalloc
from input_validation import InvalidInput
from resource_track import resourceUsageTracker, ResourceUsageTracker

log.basicConfig(level=log.INFO)

logg = log.getLogger(__name__)

memory_usage = [float('-inf')]
tracemalloc.start()

class CalcGCD:

    def __init__(self, x, y, approach = 'l'):
        self.memory_usage = float('-inf')
        self.tracMemory = {}
        if approach == 'r' or approach == 'l':
            self.approach = approach
        else:
            raise InvalidInput(f'approach {approach}')
        try:
            self.x = self.processData(CalcGCD.validateInp(x))
            self.y = self.processData(CalcGCD.validateInp(y))
        except Exception as e:
            raise e
        
    @staticmethod
    def validateInp(data):
        if data.isalpha():
            return data
        else:
            raise InvalidInput(data)

    def calculateGCD(self):

        a, b = CalcGCD.myMax(self.x, self.y)

        ans = self.calcGCD(a, b)
        log.info(f'GCD of {self.x} and {self.y}: {ans}')

        return self.resultFormat(ans)

    def calcGCD(self, p_high, p_low):
        '''
            Euclid's Algo:

            a = 6, b = 4
            6%4 = 2

            a = 4, b = 2
            4%2 = 0

            a = 2, b = 0    <=  Final state, ans = 2
        '''
        
        if p_low == 0:  #Final State reached  
            return p_high
        
        rmd = p_high%p_low

        a, b = CalcGCD.myMax(rmd, p_low)

        return self.calcGCD(a, b)
    
    # def validation(str):
        
    #     pass

    def processData(self, data):
        # Transform:    onetwo => 12
        words = {'zero': '0', 'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5', 'six': '6', 'seven': '7', 'eight': '8', 'nine': '9'}

        ans = 0
        try:
            if self.approach == 'r':
                print('Processing Data with recursion.')
                ans = int(self.recursion(0, data, '', words))
            elif self.approach == 'l':
                print('Processing Data with loop.')
                ans = int(self.withLoop(data, words))
        except Exception as e:
            raise e
        log.info(f'Processed Data: {ans}')
        return ans

    @ResourceUsageTracker(memory_usage=memory_usage, when='both')
    def recursion(self, i, p_str, p_curr, p_words):
        #Termination
        if i == len(p_str):
            if p_curr in list(p_words.keys()):
                return (p_words[p_curr])
            else:
                if len(p_curr) > 0:
                    raise InvalidInput(p_str)
                return ''
    
        #Conditional Calls
        if p_curr in list(p_words.keys()):
            return ((p_words[p_curr]) + self.recursion(i+1, p_str, p_str[i], p_words))
        else:
            return self.recursion(i+1, p_str, p_curr + p_str[i], p_words)
        

    # @resourceUsageTracker(memory_usage=memory_usage, when='both')
    @ResourceUsageTracker(memory_usage=memory_usage, when='both')
    def withLoop(self, p_data, p_words):
        curr = ''
        result = ''
        i = 0
        while i < len(p_data):
            curr = curr + p_data[i]
            if curr in list(p_words.keys()):
                result = result + p_words[curr]
                curr = ''
            i += 1
        if len(curr) > 0:
            raise InvalidInput(p_data)
        return result
    
    def resultFormat(self, p_data):
        if p_data < 10:
            return str(p_data)
        
        return self.resultFormat(p_data//10) + str(p_data%10)
    
    @staticmethod
    def myMax(p_high, p_low) -> tuple:
        a = 0
        b = 0 
        if p_high > p_low:
            a = p_high
            b = p_low
        else:
            b = p_high
            a = p_low
        
        return (a,b)

def main():
    inp1 = input('Enter 1st number in words: ')
    inp2 = input('Enter 2nd number in words: ')

    approach = input('Choose approach for process data\nRecursive: type "r"\nWhile Loop: type "l"\n: ')

    try:
        obj = CalcGCD(inp1, inp2, approach)
        result = obj.calculateGCD()
        print('Hello!')

        print(f'Result: {result}')
        # print(f'Execution Time: {end-start}')
        # print(f"Total memory usage: {memory_usage[0]} KB")
    except Exception as e:
        print('Error occurs: ', e)
        pass

if __name__ == '__main__':
    main()