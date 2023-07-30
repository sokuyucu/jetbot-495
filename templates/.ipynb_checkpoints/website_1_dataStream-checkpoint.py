import json

    # a Python object (dict):
x = {
  "name": "John",
  "age": 30,
  "city": "New York"
}

# convert into JSON:
y = json.dumps(x)

with open("sample.json", "w") as outfile:
    outfile.write(y)
    
    print("json is written")