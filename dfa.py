#encoding:UTF-8
import os
import sys
import time
import numpy as np
import yaml
import pickle
from functools import reduce

class DFA:
    def load(self, m):
        self.Q = m['states']
        self.S = m['alphabet']
        self.D = m['delta']
        self.q0 = m['initial']
        self.F = m['terminals']

    def load_from_yaml(self, filename):
        try:
            self.load(yaml.load(open(filename, 'r+')))
        except Exception as e:
            print (e)

    def load_from_pickle(self, filename):
        try:
            self.load(pickle.load(open(filename, 'rb')))
        except Exception as e:
            print (e)
            
    def load_sensitive(self, txt_path):
        with open(txt_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        #去掉头
        if lines[0][0] == '\ufeff':
            lines[0] = lines[0][1:]
        #去掉\n
        lines = [i.replace('\n', '') for i in lines if i != '\n']
        delta = {}
        states = [-1, 0]
        alphabet = []
        terminals = [-1]
        initial = 0
        for i in lines:
            end_count = len(i) - 1
            for j, item in enumerate(i):
                if j == end_count:
                    delta[(j, item, i[:j])] = -1
                else:
                    if delta.get((j, item, i[:j])) == -1:
                        break
                    delta[(j, item, i[:j])] = j+1
                if item not in alphabet:
                    alphabet.append(item)
                if j+1 not in states:
                    states.append(j+1)
        m = {}
        m['states'] = states
        m['alphabet'] = alphabet
        m['delta'] = delta
        m['initial'] = initial
        m['terminals'] = terminals
        #with open('automata/mydata.yaml', 'w') as outfile:
            #yaml.dump(m, outfile, default_flow_style=False)
        with open('automata/mydata.json', 'wb') as outfile:
            #pickle.dump(m, outfile, protocol=pickle.HIGHEST_PROTOCOL)            
            pickle.dump(m, outfile, protocol=2)
    
    def _accepts(self, string):
        def f(st, sy):
            st = list(st)
            if st[0] == -1:
                return st
            ret = self.D.get((st[0], sy, st[1]), 0)
            if ret == 0:
                rets = np.array([self.D.get((len(st[1][i:]), sy, st[1][i:]), 0) for i in range(1, len(
                    st[1])+1)])
                index = np.where(rets!=0)[0]
                if index.shape[0] != 0:
                    index = index[0]
                    ret = rets[index]
                    if ret != 0:
                        st[1] = st[1][index+1:]
                    #if -1 in rets:
                        #index = rets.index(-1)
                        #ret = rets[index]
                        #st[1] = st[1][index+1:]
                    #elif True in rets:
                        #index = rets.index(True)
                        #ret = rets[index]
                        #st[1] = st[1][index+1:]
            if ret != 0:
                ret_string = st[1] + sy
            else:
                ret_string = ''
            return (ret, ret_string, st[2]+1)
        ret = reduce(f, string, (self.q0, '', 0))
        return ret[0] in self.F, ret[1], ret[2]
    
    def get_sensitive_words(self, string):
        results = []
        cnt = 0
        end = False
        while not end:
            ret = self._accepts(string[cnt:])
            if ret[0]:
                results.append(ret[1])
            cnt += ret[2]
            end = len(string[cnt:]) == 0
        return results

    #def _accepts(self, string):
        #return reduce(lambda st, sy: self.D.get((st, sy), 0), string, self.q0) in self.F

    def accepts(self, string):
        ret = self._accepts(string)
        if ret[0]:
            print ("%s is accepted." % string)
            print ('\tthe sensitive is %s' % ret[1])
        else:
            print ("%s is rejected." % string)
    
    def predict(self, string):
        return self._accepts(string)[0]