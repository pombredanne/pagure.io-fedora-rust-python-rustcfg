import string
import pyparsing as pp
from functools import lru_cache

def paren_exp(keyword, contents):
    return pp.Keyword(keyword)('op') + pp.Suppress('(') + contents('args') + pp.Suppress(')')

@lru_cache()
def cfg_grammar():
    word = pp.Word(pp.alphanums + '_-')
    exp = pp.Forward()

    any_exp = paren_exp('any', pp.Group(pp.delimitedList(exp, delim=',')))
    all_exp = paren_exp('all', pp.Group(pp.delimitedList(exp, delim=',')))
    not_exp = paren_exp('not', exp)

    exp << (any_exp | all_exp | not_exp | word)
    exp.setName('expression')

    cfg_exp = paren_exp('cfg', exp)

    grammar = cfg_exp + pp.stringEnd()
    return grammar
