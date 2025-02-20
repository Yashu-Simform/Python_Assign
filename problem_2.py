import logging as log

log.basicConfig(level=log.INFO)

logg = log.getLogger(__name__)

#All combinations of valid parentheses

class AllCombinations:
    def __init__(self, n):
        self.n = n

    def combination_generator(self):
        '''
            n = 3

            0               (

            1           (       )(

            2         (   )(   (   )(
        '''
        result = []
        self.recursion(0, self.n, '', 0, result)

        log.info(f'Result: {result}')
        pass


    def recursion(self, i, p_n, p_curr, opens, result):
        #Never going to be case still lets check
        if i > p_n:
            log.info('level iterator > total levels')
            return
        
        if i == p_n:
            while opens > 0:
                p_curr = p_curr + ')'
                opens = opens - 1
            result.append(p_curr)
        
        if i == 0:
            self.recursion(i + 1, p_n, p_curr + '(', opens+1, result)
        else:
            self.recursion(i + 1, p_n, p_curr + '(', opens + 1, result)
            self.recursion(i + 1, p_n, p_curr + ')(', opens, result)

obj = AllCombinations(5)
obj.combination_generator()