def parse_lvls_from_str(string: str) -> tuple[int, int]:
    string = string.split('-')
    lvls = []
    for i in string:
        lvls.append(int(i.replace(' ', '')))
    return lvls[0], lvls[1]