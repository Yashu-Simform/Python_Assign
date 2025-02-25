def resourceUsageTracker(when, memory_usage = None, p_traceMallocObj = None):
    """
    memory_usage: A referenced object to be updated as value equal to total memory usage,\n
    when: 'before' - memory usage before function execution\n
          'after'  - memory usage after function execution\n
          'both'    - memory usage before and after function execution 
    """
    my_memory_usage = [float('-inf')]
    traceMallocObj = (p_traceMallocObj,)

    if memory_usage != None:
        my_memory_usage = memory_usage

    def resourceUsage(func):
        # memory_usage = [float('-ef')]


        def wrapper(*args):
            import tracemalloc, time

            if traceMallocObj[0] == None:
                traceMallocObj[0] = tracemalloc
            
            start = time.time()

            def trace_snap():
                inner_snapshot = traceMallocObj[0].take_snapshot()
                inner_top_stats = inner_snapshot.statistics('lineno')

                # To get the total memory usage in bytes
                inner_total_memory = sum(stat.size for stat in inner_top_stats)
                my_memory_usage[0] = max(my_memory_usage[0], (inner_total_memory / 1024))

            print('tracemallocobj: ', isinstance(traceMallocObj[0], tracemalloc))
            if when == 'before' or when == 'both':
                if p_traceMallocObj == None:
                    traceMallocObj[0].start()
                print('Is it still tracing', traceMallocObj[0].is_tracing())
                trace_snap()
                print(f"Memory Usage before function execution: {my_memory_usage[0]} KB")

            result = func(*args)
            print('Is it still tracing', traceMallocObj[0].is_tracing())

            if when == 'after' or when == 'both':
                trace_snap()
                print(f"Memory Usage after function execution: {my_memory_usage[0]} KB")

            end = time.time()
            print(f'Execution Time: {end-start}')
            print(f"Total memory usage: {my_memory_usage[0]} KB")

            return result
        
        if traceMallocObj[0] != None:
            traceMallocObj[0].stop()
        return wrapper
    return resourceUsage


class ResourceUsageTracker(object):
    import tracemalloc, time

    def __init__(self, when = 'both', memory_usage = None):
        self.when = when
        self.memory_usage = memory_usage
        if memory_usage == None:
            self.memory_usage = [float('-inf')]
        self.curr_calls = 0

    def calc_memory_from_snapshot(self, inner_snapshot):
        inner_top_stats = inner_snapshot.statistics('lineno')

        # To get the total memory usage in bytes
        inner_total_memory = sum(stat.size for stat in inner_top_stats)
        return inner_total_memory

    def compare_snaps(self, snap1, snap2):
        inner_top_stats = snap2.compare_to(snap1, 'lineno')

        inner_total_memory = sum(stat.size for stat in inner_top_stats)
        return inner_total_memory
    
    def before_trace(self):

        memory_consume = None
        
        try:
            self.snap_before = ResourceUsageTracker.tracemalloc.take_snapshot()
            memory_consume = self.compare_snaps(snap1=self.first_snap,snap2=self.snap_before)
        except Exception as e:
            print('Error occurs ', e)
            raise e
            pass

        else:
            print(f'Max Memory Consumption: {memory_consume / 1024} KB')
            self.memory_usage[0] = max(self.memory_usage[0], (memory_consume / 1024))

            if self.when == 'before' or self.when == 'both':
                if ResourceUsageTracker.tracemalloc.is_tracing():
                    memo = self.calc_memory_from_snapshot(self.snap_before)
                    # self.memory_usage[0] = max(self.memory_usage[0], (memo / 1024))
                else:
                    print('!Warning, tracemalloc is not tracing.')

                # print(f"Memory Usage before function execution: {memo} KB")
    
    def after_snap(self):
        memory_consume = None
        
        try:
            self.snap_after = ResourceUsageTracker.tracemalloc.take_snapshot()
            memory_consume = self.compare_snaps(snap1=self.first_snap,snap2=self.snap_after)
        except Exception as e:
            print('Error occurs ', e)
            raise e
            pass
        else:
            print(f'Max Memory Consumption: {memory_consume / 1024} KB')
            self.memory_usage[0] = max(self.memory_usage[0], (memory_consume / 1024))

            if self.when == 'before' or self.when == 'both':
                if ResourceUsageTracker.tracemalloc.is_tracing():
                    memo = self.calc_memory_from_snapshot(self.snap_before)
                    # self.memory_usage[0] = max(self.memory_usage[0], (memo / 1024))
                else:
                    print('!Warning, tracemalloc is not tracing.')

                # print(f"Memory Usage after function execution: {memo} KB")

    def __call__(self, original_fun):
        # print('Calls', self.curr_calls)

        def wrapper(*args):
            import tracemalloc, time

            self.curr_calls += 1

            if self.curr_calls <= 1:
                ResourceUsageTracker.tracemalloc.start()
                self.first_snap = ResourceUsageTracker.tracemalloc.take_snapshot()
                self.start_time = time.time()
            self.original_fun = original_fun
            print('Calls', self.curr_calls)
            
            try:
                self.before_trace()
            except Exception as e:
                raise e
                # print('Memory Used: ', self.memory_usage[0])

            result = self.original_fun(*args)

            # self.after_snap()

            if self.curr_calls == 1:
                self.end_time = time.time()
                self.last_snap = ResourceUsageTracker.tracemalloc.take_snapshot()
                print(f'Total Execution Time: {self.end_time-self.start_time}')
                print(f"Total memory usage by function call: {self.compare_snaps(snap1=self.first_snap,snap2=self.last_snap) / 1024} KB")
                ResourceUsageTracker.tracemalloc.stop()

            self.curr_calls -= 1
            return result
        
        return wrapper

    def __del__(self):
        ResourceUsageTracker.tracemalloc.stop()
        pass
