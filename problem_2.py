import logging as log
from resource_track import ResourceUsageTracker
from input_validation import InvalidInput

log.basicConfig(level=log.INFO)

logg = log.getLogger(__name__)

memory_usage = [float('-inf')]

#All combinations of valid parentheses

class AllCombinations:
    def __init__(self, n):
        self.n = AllCombinations.validation(n)

    @staticmethod
    def validation(data):
        if data.isnumeric():
            try:
                x = int(data)
                return x
            except:
                raise InvalidInput(f'n = {data}')
        else:
            raise InvalidInput(f'n = {data}')

    def combination_generator(self):
        '''
            Numbr of combinations for n: 2^n - n,
            
            n = 3

            0               (

            1           (       )(

            2         (   )(   (   )(


                            (
                        (             )
                      (     )       (   |
                      )    ( )     ( )  NA         
                      )   )  (     ) (
                      )   )  )     ) )
                      1   2  3     4 5

                      Thus 5 valid combos at leaf nodes.
        '''
        result = []
        # self.recursion(0, self.n, '', 0, result)

        result = self.loop_it(self.n)

        log.info(f'Result: {result}')
        return result


    #Tree Traversal
    @ResourceUsageTracker(memory_usage=memory_usage, when='both')
    def recursion(self, i, p_n, p_curr, opens, result):
        #Never going to be case still lets check
        if i > p_n:
            log.info('level iterator > total levels')
            return
        
        if (i == p_n) or (p_n == -1):
            while opens > 0:
                p_curr = p_curr + ')'
                opens = opens - 1
            result.append(p_curr)
        
        if i == 0:
            self.recursion(i + 1, p_n, p_curr + '(', opens+1, result)
        else:
            j = opens
            st = p_curr
            while j > 0:
                st = st + ')'
                self.recursion(i + 1, p_n, st + '(', j, result)
                j = j - 1
            self.recursion(i + 1, p_n, p_curr + '(', opens + 1, result)

    @ResourceUsageTracker(memory_usage=memory_usage, when='both')
    def loop_it(self, p_n):
        memo = []
        result = []
        for i in range(0, p_n):
            if i == 0:
                memo.append(['(', 1])
            else:
                temp = memo[:]
                for i, t in enumerate(temp):
                    j = memo[i][1]
                    st = memo[i][0]
                    while j > 0:
                        st = st + ')'
                        memo.append([st + '(', j])
                        j = j - 1

                    memo[i][0] = memo[i][0] + '('
                    memo[i][1] += 1

            log.info(f'List at id {i+1}: {memo}')
                    

        for i, t in enumerate(memo):
            while memo[i][1] > 0:
                memo[i][0] = memo[i][0] + ')'
                memo[i][1] = memo[i][1] - 1
            result.append(memo[i][0])
        return result


if __name__ == '__main__':
    inp = input('Enter number of parenthesis pairs: ')
    obj = AllCombinations(inp)
    result = obj.combination_generator()

    print(f'Result: {result}')
    print(f'Total Combinations: : {len(result)}')