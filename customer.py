#!env/bin/python

import DbManager

def Icont():
    _str = input('\ndo you want to continue?\n')
    if _str <> 1:
        sys.exit()


if __name__ == '__main__':
    print 'works...'
    _customer = DbManager.GetTable('leads')
    _names = [str(e[2]) for e in _customer]
    _words = {}
    for e in _names:
        _split = e.split()
        for _word in _split:
            if _word in _words:
                _words[_word] = _words[_word] + 1
            else:
                _words[_word] = 1
    for e in _words:
        if _words[e] > 3:
            print e, _words[e]
    Icont()
    _common_list = [[_names[0]]]
    from Levenshtein import distance
    for _name in _names[1:]:
        flag = False
        for _group in _common_list:
            for _e in _group:
                if distance(_e, _name) < 5:
                    _group.append(_name)
                    flag = True
                    break
            if flag:
                break
        if not flag:
            _common_list.append([_name])
    for e in _common_list:
        if len(e) > 1:
            print e

