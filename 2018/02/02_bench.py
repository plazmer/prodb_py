import csv
import re
from collections import Counter

def timereps(reps, func):
    from time import time
    start = time()
    for i in range(0, reps):
        func()
    end = time()
    return (end - start) / reps


def func_dict_byrow():
    with open("02_alice.txt") as file:
        counter = {}
        for line in file:
            line = re.sub('\W', " ", line).strip().lower().split()
            for subline in line:
                if len(subline)>3:
                        counter[subline] = counter.get(subline,0) + 1
    return sorted(counter.items(), reverse=False, key=lambda element: (-element[1], element[0]))[:5]


def func_dict_full():
    reg = re.compile('\W')
    with open("02_alice.txt") as file:
        counter = {}
        line = re.sub(reg, " ", file.read()).lower().split()
        for subline in line:
            if len(subline)>3:
                counter[subline] = counter.get(subline,0) + 1
    return sorted(counter.items(), reverse=False, key=lambda element: (-element[1], element[0]))[:5]


def func_counter_splice_full():
    with open('02_alice.txt') as f:
        reg = re.compile('\W')
        f1 = reg.sub(' ', re.sub(reg, '', f.read().lower())) 
        return sorted( Counter(f1.split()).most_common(5), key=lambda element: (-element[1], element[0]))

                  
def main():
    print('func_dict_byrow',timereps(100,func_dict_byrow))
    print('func_dict_full',timereps(100,func_dict_full))
    print('func_counter_splice_full',timereps(100,func_counter_splice_full))

if __name__ == '__main__':
    main()
