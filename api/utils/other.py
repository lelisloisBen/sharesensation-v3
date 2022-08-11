def split_name(name):
    list = name.split(" ", 1)
    while len(list) < 2:
        list.append("")
    return list[0], list[1]