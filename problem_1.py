import logging as log

log.basicConfig(level=log.INFO)

logg = log.getLogger(__name__)

class CalcGCD:
    def __init__(self, x, y):
        self.x = self.processData(x)
        self.y = self.processData(y)

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

    def processData(self, data):
        # Transform:    onetwo => 12
        words = {'zero': '0', 'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5', 'six': '6', 'seven': '7', 'eight': '8', 'nine': '9'}

        ans = int(self.recursion(0, data, '', words))
        log.info(f'Processed Data: {ans}')
        return ans

    def recursion(self, i, p_str, p_curr, p_words):
        #Termination
        if i == len(p_str):
            if p_curr in list(p_words.keys()):
                return (p_words[p_curr])
            else:
                return ''
    
        #Conditional Calls
        if p_curr in list(p_words.keys()):
            return ((p_words[p_curr]) + self.recursion(i+1, p_str, p_str[i], p_words))
        else:
            return self.recursion(i+1, p_str, p_curr + p_str[i], p_words)
        
    
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
        
obj = CalcGCD('onezerozerozero', 'onezerozerozero')
result = obj.calculateGCD()
print(f'Result: {result}')