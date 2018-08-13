import string
import pyparsing as pp
from functools import lru_cache

def paren_exp(keyword, contents):
    return pp.Keyword(keyword)('op') + pp.Suppress('(') + contents + pp.Suppress(')')

def cfg_exp():
    word = pp.Word(pp.alphanums + '_-')('word')
    exp = pp.Forward()

    any_exp = paren_exp('any', pp.delimitedList(exp, delim=','))
    all_exp = paren_exp('all', pp.delimitedList(exp, delim=','))
    not_exp = paren_exp('not', exp)

    exp << pp.Group(any_exp | all_exp | not_exp | word)

    return paren_exp('cfg', exp)

def multiarch_tuple():
    word = pp.Word(pp.alphanums + '_')
    opt = pp.Optional(pp.Suppress('-') + word)
    tup = (word('a') + pp.Suppress('-') + word('b') + opt('c') + opt('d'))
    return tup

@lru_cache()
def cfg_grammar():
    grammar = (cfg_exp() | multiarch_tuple()) + pp.stringEnd()
    return grammar

def eval_tree(tree):
    kind = tree.getName()
    assert kind
    if kind == 'word':
        return True
    elif kind == 'op':
        op = tree[0]
        if op == 'cfg':
            assert(len(tree) == 2)
            return eval_tree(tree[1])
        if op == 'any':
            assert(len(tree) >= 2)
            return any(eval_tree(item) for item in tree[1:])
        if op == 'all':
            assert(len(tree) >= 2)
            return all(eval_tree(item) for item in tree[1:])
        if op == 'not':
            assert(len(tree) == 2)
            return not eval_tree(tree[1])
        assert False, f'Unknown operator {op}'
    else:
        assert False, f'Unknown element {kind}'

def dump_tree(t, level=0, evalf=eval_tree):
    print('{}structure {}{}{}{}'.format('    '*level, t.getName(),
                                        ' [' if evalf else '',
                                        evalf(t) if evalf else '',
                                        ']' if evalf else ''))
    for item in t:
        if isinstance(item, str):
            print('{}{!r}'.format('    '*(level+1), item))
        else:
            dump_tree(item, level+1, evalf=evalf)
