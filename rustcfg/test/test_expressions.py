import pytest
import rustcfg

testdata = [
    # None means expression is unparsable
    ('cfg(ok)', True),
    ('cfg(not_ok)', False),
    ('cfg( ok )', True),
    ('cfg(foo-bar-bar)', None),
    ('cfg(foo_bar_bar)', True),
    (' foo-bar-bar ', False),
    (' cfg(not(foo))', False),
    (' cfg(not(foo foo))', None),
    ('cfg(any(asdf, asdf))', True),
    ('cfg(all(asdf, asdf))', True),
    ('cfg(any())', None),
    ('cfg(all())', None),
    ('cfg(all(not(asdf)))', False),
    ('cfg(all(not(any(all(asdf)))))', False),
    ('cfg(foo="bar")', True),
    ('cfg(foo = "bar")', True),
    ('cfg(foo = " bar ")', True),
    ('cfg(foo = "not bar")', False),
    ('cfg(foo=bar)', None),
    ('cfg(foo foo = = " bar ")', None),
    ('cfg(foo = foo = " bar ")', None),
]

@pytest.fixture
def asdf_evaluator():
    options = ('ok',
               'foo_bar_bar',
               'foo',
               'asdf',
               ('foo', 'bar'),
               ('foo', ' bar '))
    return rustcfg.Evaluator(options=options)

@pytest.mark.parametrize("expression,result", testdata)
def test_parsing(expression, result, asdf_evaluator):
    g = rustcfg.cfg_grammar()
    try:
        t = g.parseString(expression)
    except Exception:
        good = False
    else:
        good = True
    assert good == (result is not None)

    if result is not None:
        res = asdf_evaluator.eval_tree(t)
        assert res == result
