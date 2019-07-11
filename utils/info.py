#!/usr/bin/env pypy
# -*- coding: utf-8 -*-

'''
:author: Maximilian Golla
:contact: maximilian.golla@rub.de
:version: 0.7.0, 2019-07-11
:description: Reports some statistics about password length, alphabet, ASCII encoding etc.
:usage: pypy utils/info.py input/eval.txt
'''

import sys
import operator

def is_ascii(s):
    return all((ord(c) >= 32 and ord(c) <= 126) for c in s)

def main():
    min_len = sys.maxsize
    max_len = -sys.maxsize - 1
    alphabet = dict()
    lengths = set()
    everything_ascii = "Yes"

    with open(sys.argv[1], 'r') as passwordfile:
        for line in passwordfile:
            line = line.rstrip('\r\n')
            length = len(line)
            for char in line:
                if char in alphabet:
                    alphabet[char] += 1
                else:
                    alphabet[char] = 1
            if length < min_len:
                min_len = length
            if length > max_len:
                max_len = length
            lengths.add(length)
            if is_ascii(line) == False:
                everything_ascii = "No"

    # Alphabet
    alphabet = sorted(alphabet.items(), key=operator.itemgetter(1), reverse=True)
    lengths = sorted(lengths)
    alpha = []
    for e in alphabet:
        if e[0] == '"':
            alpha.append('\\"') # escape quotes
        elif e[0] == '\\':
            alpha.append('\\\\') # escape backslash
        else:
            alpha.append(e[0])
    print("File: {}".format(sys.argv[1].split('/')[-1]))
    print("Min length: {}".format(min_len))
    print("Max length: {}".format(max_len))
    print("Observed password lengths: [{}]".format(','.join([str(x) for x in list(lengths)])))
    print('Alphabet (escaped for Python, but watch out for the space char): "{}"'.format(''.join(alpha)))
    print("Alphabet length: {}".format(len(alphabet)))
    print("ASCII only: {}".format(everything_ascii))

if __name__ == '__main__':
    main()