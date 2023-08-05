import numpy as np

from .stat import _Statistic
import vaex.superagg

aggregates = {}

def register(f, name=None):
    name = name or f.__name__
    aggregates[name] = f
    return f

class AggregatorDescriptor:
    def __repr__(self):
        return 'vaex.agg.{}({!r})'.format(self.short_name, str(self.expression))

class AggregatorDescriptorBasic(AggregatorDescriptor):
    def __init__(self, name, expression, short_name, multi_args=False):
        self.name = name
        self.short_name = short_name
        self.expression = expression
        if not multi_args:
            if self.expression == '*':
                self.expressions = []
            else:
                self.expressions = [self.expression]
        else:
            self.expressions = expression

    def pretty_name(self, id=None):
        id = id or "_".join(map(str, self.expression))
        return '{0}_{1}'.format(id, self.short_name)

    def add_operations(self, agg_task, edges=True, **kwargs):
        return agg_task.add_aggregation_operation(self, edges=edges, **kwargs)

    def _create_operation(self, df, grid):
        if self.expression == '*':
            self.dtype_in = np.dtype('int64')
            self.dtype_out = np.dtype('int64')
        else:
            self.dtype_in = df[str(self.expressions[0])].dtype
            self.dtype_out = self.dtype_in
            if self.short_name == "count":
                self.dtype_out = np.dtype('int64')
        agg_op_type = vaex.utils.find_type_from_dtype(vaex.superagg, self.name + "_", self.dtype_in)
        agg_op = agg_op_type(grid)
        return agg_op

class AggregatorDescriptorMean(AggregatorDescriptor):
    def __init__(self, name, expression, short_name):
        self.name = name
        self.short_name = short_name
        self.expression = expression
        if self.expression == '*':
            self.expressions = []
        else:
            self.expressions = [self.expression]
        self.sum = sum(expression)
        self.count = count(expression)

    def pretty_name(self, id=None):
        id = id or "_".join(map(str, self.expression))
        return '{0}_{1}'.format(id, self.short_name)

    def add_operations(self, agg_task, **kwargs):
        task_sum = self.sum.add_operations(agg_task, **kwargs)
        task_count = self.count.add_operations(agg_task, **kwargs)
        self.dtype_in = self.sum.dtype_in
        self.dtype_out = self.sum.dtype_out
        @vaex.delayed
        def finish(sum, count):
            dtype = sum.dtype
            if sum.dtype.kind == 'M':
                sum = sum.view('uint64')
                count = count.view('uint64')
            with np.errstate(divide='ignore', invalid='ignore'):
                mean = sum / count
            if dtype.kind != mean.dtype.kind:
                # TODO: not sure why view does not work
                mean = mean.astype(dtype)
            return mean
        return finish(task_sum, task_count)

@register
def count(expression='*'):
    '''Creates a count aggregation'''
    return AggregatorDescriptorBasic('AggCount', expression, 'count')

@register
def sum(expression):
    '''Creates a sum aggregation'''
    return AggregatorDescriptorBasic('AggSum', expression, 'sum')

@register
def mean(expression):
    '''Creates a mean aggregation'''
    return AggregatorDescriptorMean('AggSum', expression, 'mean')

@register
def min(expression):
    '''Creates a min aggregation'''
    return AggregatorDescriptorBasic('AggMin', expression, 'min')

@register
def max(expression):
    '''Creates a max aggregation'''
    return AggregatorDescriptorBasic('AggMax', expression, 'max')

@register
def first(expression, order_expression):
    '''Creates a max aggregation'''
    return AggregatorDescriptorBasic('AggFirst', [expression, order_expression], 'first', multi_args=True)

@register
def std(expression):
    '''Creates a standard deviation aggregation'''
    return _Statistic('std', expression)

@register
def covar(x, y):
    '''Creates a standard deviation aggregation'''
    return _Statistic('covar', x, y)

@register
def correlation(x, y):
    '''Creates a standard deviation aggregation'''
    return _Statistic('correlation', x, y)

