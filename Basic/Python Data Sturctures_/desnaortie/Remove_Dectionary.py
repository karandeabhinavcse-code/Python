d = {"a": 1, "b": 2, "c": 3}

d.pop("b")   
print(d)        # removes 'b'
d.popitem()
print(d)       # removes last item
d.clear()
print(d)         # remove all items
del d["a"]
print(d)        # delete specific key
