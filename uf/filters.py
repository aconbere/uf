def to_vobject(o):
    import vobject
    return vobject.readOne(o)

def to_str(o):
    return str(o)

def atom2python(o):
    print o
    from feedparser import parse
    return parse(o)
