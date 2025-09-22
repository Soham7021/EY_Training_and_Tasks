dictionary = {
    "name":"Soham",
    "age":22,
    "course":"AIML",
    "skills":["AI","ML","Python"]
}

print(dictionary["name"])
print(dictionary.get("age"))

dictionary["grade"] = 91
dictionary["age"] = 21

dictionary.pop("course")
del dictionary["grade"]

print(dictionary["skills"][2])

for key,value in dictionary.items():
    print(key,":",value)

print(dictionary["skills"][2])