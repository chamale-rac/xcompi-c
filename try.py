from src._expression import Expression
# print(ord(' '))
# print(ord('\''))
# print(ord("'"))
# print(chr(40))
# print(chr(41))
# print(chr(42))
# print(chr(76))


# string = "\\\'"

# expr = Expression(string)
# print(expr.hardCodify(string))

# string = '\\\\'
# expr = Expression(string)
# print(expr.hardCodify(string))

string = f"(['A'-'Z''a'-'z''0'-'9'' ']|\\\'|\-|\||\(|\)|\[|\]|\+|\*|\?|.|\\\\)+"
expr = Expression(string)
print(expr.transformGroupsOfCharacters(expr.hardCodify(string)))

string = "[' ''\t''\n']"
expr = Expression(string)
print(expr.softCodify(string))
