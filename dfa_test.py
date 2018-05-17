#encoding:UTF-8

import os
import time
import numpy as np
from dfa import DFA

def test_1():
    sensitive_path = 'sensitive/sensitive.txt'
    dfa = DFA()
    dfa.load_sensitive(sensitive_path)
    dfa = DFA()
    #dfa.load_from_yaml('automata/mydata.yaml')
    dfa.load_from_pickle('automata/mydata.json')
    dfa.accepts('我爱北京天安门\n')
    dfa.accepts('我喜欢做假证\n')
    dfa.accepts('我喜欢做嗳\n')
    with open(sensitive_path, 'r', encoding='UTF-8') as f:
        lines = f.readlines()
    result = []
    lines = [i for i in lines if i != '\n']
    for i in lines:
        i = '我喜欢' + i
        print(i)
        dfa.accepts(i)
    start_time = time.time()
    for i in lines:
        i = '我喜欢' + i
        result.append(dfa.predict(i))
    during_time = time.time() - start_time
    print(r'耗时:', during_time)
    print(r'平均z耗时:', during_time/len(lines))
    result = np.array(result)
    print(r'正确个数:', len(result[result==True]))
    print(r'错误个数:', len(result[result==False]))
    print(r'正确率:',len(result[result==True])/len(result))
    


def test_2():
    sensitive_path = 'sensitive/sensitive.txt'
    dfa = DFA()
    dfa.load_from_pickle('automata/mydata.json')
    dfa.accepts('我爱北京天安门\n')
    dfa.accepts('我喜欢做假证\n')
    dfa.accepts('我喜欢做嗳\n')
    with open(sensitive_path, 'r', encoding='UTF-8') as f:
        lines = f.readlines()
    result = []
    lines = [i for i in lines if i != '\n']
    #for i in lines:
        #print(i, '*70')
        #i = ('我喜欢' + i)*70
        #print(dfa.get_sensitive_words(i))
    start_time = time.time()
    for i in lines:
        i = ('我喜欢' + i)*2
        dfa.get_sensitive_words(i)
        result.append(True)
    during_time = time.time() - start_time
    print(r'耗时:', during_time)
    print(r'平均z耗时:', during_time/len(lines))
    start_time = time.time()
    print(i)
    i = i*200
    a = dfa.get_sensitive_words(i)
    during_time = time.time() - start_time
    print(a)
    print(r'耗时:', during_time)
    start_time = time.time()
    for i in lines:
        i = ('我喜欢' + i)*4
        dfa.get_sensitive_words(i)
        result.append(True)
    during_time = time.time() - start_time
    print(r'耗时:', during_time)
    print(r'平均z耗时:', during_time/len(lines))
    start_time = time.time()
    for i in lines:
        i = ('我喜欢' + i)*8
        dfa.get_sensitive_words(i)
        result.append(True)
    during_time = time.time() - start_time
    print(r'耗时:', during_time)
    print(r'平均z耗时:', during_time/len(lines))
    start_time = time.time()
    for i in lines:
        i = ('我喜欢' + i)*16
        dfa.get_sensitive_words(i)
        result.append(True)
    during_time = time.time() - start_time
    print(r'耗时:', during_time)
    print(r'平均z耗时:', during_time/len(lines))
    result = np.array(result)
    print(r'正确个数:', len(result[result==True]))
    print(r'错误个数:', len(result[result==False]))
    print(r'正确率:',len(result[result==True])/len(result))    

if __name__ == '__main__':
    test_1()