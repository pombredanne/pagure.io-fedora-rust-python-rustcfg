import pytest
import rustcfg

"""
"cfg(ok)", "cfg( ok )".parse::<Target>().unwrap().to_string());
"foo-bar-baz", "foo-bar-baz".parse::<Target>().unwrap().to_string());
"foo-bar-baz-quz", " foo-bar-baz-quz ".parse::<Target>().unwrap().to_string());
"cfg(foo)", &Cfg::Is("foo".to_string()).to_string());
"cfg(not(foo))", &Cfg::Not(Box::new(Cfg::Is("foo".to_string()))).to_string());
"cfg(not(any(foo, bar)))
"""

testdata = [
    ('cfg(ok)', True),
    ('cfg( ok )', True),
    ('cfg(foo-bar-bar)', True),
    (' foo-bar-bar ', False),
    (' cfg(not(foo))', True),
    (' cfg(not(foo foo))', False),
    ('cfg(any(asdf, asdf))', True),
    ('cfg(all(asdf, asdf))', True),
    ('cfg(any())', False),
    ('cfg(all())', False),
    ('cfg(all(not(asdf)))', True),
    ('cfg(all(not(any(all(asdf)))))', True),
]

@pytest.mark.parametrize("expression,ok", testdata)
def test_parsing(expression, ok):
    g = rustcfg.cfg_grammar()
    try:
        t = g.parseString(expression)
    except Exception:
        good = False
    else:
        good = True
    assert good == ok
