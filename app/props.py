import ujson

def load_props():
  with open('props.json') as f:
    props = ujson.loads(f.read())
  return props