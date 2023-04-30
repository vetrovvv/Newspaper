
def goga():
    p = {'kind_of_post': 'NW'}
    value1 = list(p.values())
    if value1[0] == 'NW':
        return ("ДА")
    else:
        value1.append("Статья")
        print(value1)

print(goga())