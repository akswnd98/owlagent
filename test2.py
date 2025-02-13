a: dict = {}

def get_str (mode):
  if mode:
    return "1"
  else:
    return "2"

var = 2
a[get_str(var)] = "hello"

print(a["1"])