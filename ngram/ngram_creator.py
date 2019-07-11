#!/usr/bin/env pypy
# -*- coding: utf-8 -*-

''' The Markov model
:author: Maximilian Golla
:contact: maximilian.golla@rub.de
:version: 0.7.1, 2019-07-11
'''

# External modules
from collections import OrderedDict # storing the alphabet
import os # load and save / file handling
import umsgpack # load and save # pip install u-msgpack-python
import math # only pow
import logging # logging debug infos
from rainbow_logging_handler import RainbowLoggingHandler # pip install rainbow_logging_handler
from tqdm import tqdm # progress bar while reading the file # pip install tqdm
import datetime

class NGramCreator:

    def __init__(self, dict):
        self.name = dict['name']
        logging.debug("Constructor started for '{}'".format(self.name))
        self.alphabet = dict['alphabet']
        self.alphabet_len = len(self.alphabet)
        self.alphabet_dict = OrderedDict.fromkeys(self.alphabet) #a 0, b 1, c 2
        i = 0
        for char in self.alphabet_dict:
            self.alphabet_dict[char] = i
            i += 1
        self.alphabet_list = list(self.alphabet)
        logging.debug("Used alphabet: {}".format(self.alphabet))
        self.length = dict['length']
        logging.debug("Model string length: {}".format(self.length))
        self.ngram_size = dict['ngram_size']
        assert self.ngram_size >= 2, "n-gram size < 2 does not make any sense! Your configured n-gram size is {}".format(self.ngram_size)
        logging.debug("NGram size: {}".format(self.ngram_size))
        self.training_file = dict['training_file']
        self.training_file_lines = sum(1 for line in open(self.training_file))
        self.disable_progress = False if dict['progress_bar'] else True
        self.ip_list = []
        self.cp_list = []
        self.ep_list = []
        self.no_ip_ngrams = int(math.pow(self.alphabet_len, (self.ngram_size-1)))
        self.no_cp_ngrams = int(math.pow(self.alphabet_len, (self.ngram_size)))
        self.no_ep_ngrams = self.no_ip_ngrams # save one exponentiation :-P
        logging.debug("len(IP) theo: {}".format(self.no_ip_ngrams))
        logging.debug("len(CP) theo: {} => {} * {}".format(self.no_cp_ngrams, int(math.pow(self.alphabet_len, (self.ngram_size-1))), self.alphabet_len))
        logging.debug("len(EP) theo: {}".format(self.no_ep_ngrams))

    def __del__(self):
        logging.debug("Destructor started for '{}'".format(self.name))

    def __str__(self):
        return "Hello {}!".format(self.name)

########################################################################################################################

    def _is_in_alphabet(self, string):
        for char in string:
            if not char in self.alphabet:
                return False
        return True

    # checks whether two floats are equal like 1.0 == 1.0?
    def _is_almost_equal(self, a, b, rel_tol=1e-09, abs_tol=0.0):
        #print '{0:.16f}'.format(a), '{0:.16f}'.format(b)
        return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

########################################################################################################################

    # ngram-to-intial-prob-index
    def _n2iIP(self, ngram):
        ngram = list(ngram)
        if self.ngram_size == 5:
            return ( self.alphabet_len**0 * self.alphabet_dict[ngram[3]] ) + ( self.alphabet_len**1 * self.alphabet_dict[ngram[2]] ) + ( self.alphabet_len**2 * self.alphabet_dict[ngram[1]] ) + ( self.alphabet_len**3 * self.alphabet_dict[ngram[0]] )
        if self.ngram_size == 4:
            return ( self.alphabet_len**0 * self.alphabet_dict[ngram[2]] ) + ( self.alphabet_len**1 * self.alphabet_dict[ngram[1]] ) + ( self.alphabet_len**2 * self.alphabet_dict[ngram[0]] )
        if self.ngram_size == 3:
            return ( self.alphabet_len**0 * self.alphabet_dict[ngram[1]] ) + ( self.alphabet_len**1 * self.alphabet_dict[ngram[0]] )
        if self.ngram_size == 2:
            return ( self.alphabet_len**0 * self.alphabet_dict[ngram[0]] )

    # intial-prob-index-to-ngram
    def _i2nIP(self, index):
        if self.ngram_size == 5:
            third, fourth = divmod(index,  self.alphabet_len)
            second, third = divmod(third,  self.alphabet_len)
            first, second = divmod(second, self.alphabet_len)
            return self.alphabet_list[first] + self.alphabet_list[second] + self.alphabet_list[third] + self.alphabet_list[fourth]
        if self.ngram_size == 4:
            second, third = divmod(index,  self.alphabet_len)
            first, second = divmod(second, self.alphabet_len)
            return self.alphabet_list[first] + self.alphabet_list[second] + self.alphabet_list[third]
        if self.ngram_size == 3:
            first, second = divmod(index,  self.alphabet_len)
            return self.alphabet_list[first] + self.alphabet_list[second]
        if self.ngram_size == 2:
            return self.alphabet_list[index]

    # ngram-to-conditial-prob-index
    def _n2iCP(self, ngram):
        ngram = list(ngram)
        if self.ngram_size == 5:
            return ( self.alphabet_len**0 * self.alphabet_dict[ngram[4]] ) + ( self.alphabet_len**1 * self.alphabet_dict[ngram[3]] ) + ( self.alphabet_len**2 * self.alphabet_dict[ngram[2]] ) + ( self.alphabet_len**3 * self.alphabet_dict[ngram[1]] ) + ( self.alphabet_len**4 * self.alphabet_dict[ngram[0]] )
        if self.ngram_size == 4:
            return ( self.alphabet_len**0 * self.alphabet_dict[ngram[3]] ) + ( self.alphabet_len**1 * self.alphabet_dict[ngram[2]] ) + ( self.alphabet_len**2 * self.alphabet_dict[ngram[1]] ) + ( self.alphabet_len**3 * self.alphabet_dict[ngram[0]] )
        if self.ngram_size == 3:
            return ( self.alphabet_len**0 * self.alphabet_dict[ngram[2]] ) + ( self.alphabet_len**1 * self.alphabet_dict[ngram[1]] ) + ( self.alphabet_len**2 * self.alphabet_dict[ngram[0]] )
        if self.ngram_size == 2:
            return ( self.alphabet_len**0 * self.alphabet_dict[ngram[1]] ) + ( self.alphabet_len**1 * self.alphabet_dict[ngram[0]] )

    # conditial-prob-index-to-ngram
    def _i2nCP(self, index):
        if self.ngram_size == 5:
            fourth, fifth = divmod(index,  self.alphabet_len)
            third, fourth = divmod(fourth, self.alphabet_len)
            second, third = divmod(third,  self.alphabet_len)
            first, second = divmod(second, self.alphabet_len)
            return self.alphabet_list[first] + self.alphabet_list[second] + self.alphabet_list[third] + self.alphabet_list[fourth] + self.alphabet_list[fifth]
        if self.ngram_size == 4:
            third, fourth = divmod(index,  self.alphabet_len)
            second, third = divmod(third,  self.alphabet_len)
            first, second = divmod(second, self.alphabet_len)
            return self.alphabet_list[first] + self.alphabet_list[second] + self.alphabet_list[third] + self.alphabet_list[fourth]
        if self.ngram_size == 3:
            second, third = divmod(index,  self.alphabet_len)
            first, second = divmod(second, self.alphabet_len)
            return self.alphabet_list[first] + self.alphabet_list[second] + self.alphabet_list[third]
        if self.ngram_size == 2:
            first, second = divmod(index,  self.alphabet_len)
            return self.alphabet_list[first] + self.alphabet_list[second]

########################################################################################################################

    # Adds all possible combinations of ngrams to the list with initial count = 1
    def _init_lists(self, kind):
        if kind == "ip_list":
            for i in range(0, int(math.pow(self.alphabet_len, self.ngram_size-1))):
                self.ip_list.append(1) # Smoothing, we initialize every possible ngram with count = 1
        elif kind == "cp_list":
            for i in range(0, int(math.pow(self.alphabet_len, self.ngram_size))):
                self.cp_list.append(1) # Smoothing, we initialize every possible ngram with count = 1
        elif kind == "ep_list":
            for i in range(0, int(math.pow(self.alphabet_len, self.ngram_size-1))):
                self.ep_list.append(1) # Smoothing, we initialize every possible ngram with count = 1
        else:
            raise Exception('Unknown list given (required: ip_list, cp_list, or ep_list)')

########################################################################################################################

    # Count the occurrences of ngrams in the training corpus
    '''
    password PW
    pa       IP
    pas      CP1
     ass     CP2
      ssw    CP3
       swo   CP4
        wor  CP5
         ord CP6
          rd EP
    '''
    def _count(self, kind):
        if kind == "ip_list":
            with open(self.training_file) as input_file:
                for line in tqdm(input_file, desc=self.training_file, total=self.training_file_lines, disable=self.disable_progress, miniters=1000, unit="pw"):
                    line = line.rstrip('\r\n')
                    if len(line) != self.length: # Important to prevent generating "passwor", or "iloveyo", or "babygir"
                        continue
                    if self._is_in_alphabet(line): # Filter non-printable
                        ngram = line[0:self.ngram_size-1] # Get IP ngram
                        self.ip_list[self._n2iIP(ngram)] = self.ip_list[self._n2iIP(ngram)] + 1 # Increase IP ngram count by 1
        elif kind == "cp_list":
            with open(self.training_file) as input_file: # Open trainingfile
                for line in tqdm(input_file, desc=self.training_file, total=self.training_file_lines, disable=self.disable_progress, miniters=1000, unit="pw"):
                    line = line.rstrip('\r\n')
                    if len(line) != self.length: # Important to prevent generating "passwor", or "iloveyo", or "babygir"
                        continue
                    if self._is_in_alphabet(line): # Filter non-printable
                        old_pos = 0
                        for new_pos in range(self.ngram_size, len(line)+1, 1): # Sliding window: pas|ass|ssw|swo|wor|ord
                            ngram = line[old_pos:new_pos]
                            old_pos += 1
                            self.cp_list[self._n2iCP(ngram)] = self.cp_list[self._n2iCP(ngram)] + 1 # Increase CP ngram count by 1
        elif kind == "ep_list":
            with open(self.training_file) as input_file: # Open trainingfile
                for line in tqdm(input_file, desc=self.training_file, total=self.training_file_lines, disable=self.disable_progress, miniters=1000, unit="pw"):
                    line = line.rstrip('\r\n')
                    if len(line) != self.length: # Important to prevent generating "passwor", or "iloveyo", or "babygir"
                        continue
                    if self._is_in_alphabet(line): # Filter non-printable
                        ngram = line[-self.ngram_size+1:] # Get EP ngram
                        self.ep_list[self._n2iIP(ngram)] = self.ep_list[self._n2iIP(ngram)] + 1 # Increase EP ngram count by 1
        else:
            raise Exception("Unknown dictionary given (required: ip_list, cp_list, or ep_list)")

########################################################################################################################

    # Determine the probability (based on the counts) of a ngram
    def _prob(self, kind):
        if kind == "ip_list":
            no_ip_training_ngrams = 0.0 # must be a float
            for ngram_count in self.ip_list:
                no_ip_training_ngrams += ngram_count
            for index in range(0, len(self.ip_list)):
                self.ip_list[index] = self.ip_list[index] / no_ip_training_ngrams # count / all
            # Validate that prob sums to 1.0, otherwise coding error. Check for rounding errors using Decimal(1.0) instead of float(1.0)
            sum = 0.0
            for ngram_prob in self.ip_list:
                sum += ngram_prob
            logging.debug("IP probability sum: {0:.16f}".format(sum))
            if not self._is_almost_equal(sum, 1.0):
                raise Exception("ip_list probabilities do not sum up to 1.0! It is only: {}".format(sum))
        elif kind == "cp_list":
            for index in range(0, len(self.cp_list), self.alphabet_len):
                no_cp_training_ngrams = 0.0 # must be a float
                for x in range(index, index+self.alphabet_len):
                    no_cp_training_ngrams += self.cp_list[x] # Count all ngram occurrences within one ngram-1 category
                for x in range(index, index+self.alphabet_len):
                    self.cp_list[x] = self.cp_list[x] / no_cp_training_ngrams # count / all (of current [x])
                # Validate that prob sums to 1.0, otherwise coding error. Check for rounding errors using Decimal(1.0) instead of float(1.0)
                '''
                sum = 0.0
                for x in range(index, index+self.alphabet_len):
                    sum += self.cp_list[x]
                #logging.debug("CP probability sum: {0:.16f}".format(sum))
                if not self._is_almost_equal(sum, 1.0):
                    raise Exception("cp_list probabilities do not sum up to 1.0! It is only: {}".format(sum))
                '''
        elif kind == "ep_list":
            no_ep_training_ngrams = 0.0 # must be a float
            for ngram_count in self.ep_list:
                no_ep_training_ngrams += ngram_count
            for index in range(0, len(self.ep_list)):
                self.ep_list[index] = self.ep_list[index] / no_ep_training_ngrams # count / all
            # Validate that prob sums to 1.0, otherwise coding error. Check for rounding errors using Decimal(1.0) instead of float(1.0)
            sum = 0.0
            for ngram_prob in self.ep_list:
                sum += ngram_prob
            logging.debug("EP probability sum: {0:.16f}".format(sum))
            if not self._is_almost_equal(sum, 1.0):
                raise Exception("ep_list probabilities do not sum up to 1.0! It is only: {}".format(sum))
        else:
            raise Exception("Unknown dictionary given (required: ip_dict, cp_dict, or ep_dict)")

########################################################################################################################

    '''
    CP cPickle      Storing the data on disk took:   0:01:18.987257 # Native?
    CP simplejson   Storing the data on disk took:   0:01:14.158285 # pip install simplejson
    CP ujson        Storing the data on disk took:   0:01:05.501812 # pip install ujson
    CP cbor         Storing the data on disk took:   0:00:17.168384 # pip install cbor
    CP cbor2        Storing the data on disk took:   0:00:12.584272 # pip install cbor2
    CP marshal      Storing the data on disk took:   0:00:14.355625 # Native?
    CP umsgpack     Storing the data on disk took:   0:00:11.805770 # pip install u-msgpack-python
                    Loading the data from disk took: 0:00:17.505519
    CP msgpack      Storing the data on disk took:   0:00:07.918690 # pip install msgpack
                    ValueError: ('%s exceeds max_array_len(%s)', 804357, 131072)
    '''

    def save(self, kind):
        start = datetime.datetime.now()
        logging.debug("Start: Writing result to disk, this gonna take a while ...")
        path, file = os.path.split(self.training_file)
        with open('trained/'+file[:-4]+'_'+kind+'_'+str(self.ngram_size)+'_'+str(self.length)+'.pack', 'wb') as fp:
            if kind == "ip_list":
                umsgpack.dump(self.ip_list, fp)
            elif kind == "cp_list":
                umsgpack.dump(self.cp_list, fp)
            elif kind == "ep_list":
                umsgpack.dump(self.ep_list, fp)
            else:
                raise Exception("Unknown list given (required: ip_list, cp_list, or ep_list)")
        logging.debug("Done! Everything stored on disk.")
        logging.debug("Storing the data on disk took: {}".format(datetime.datetime.now()-start))

    def load(self, kind):
        start = datetime.datetime.now()
        path, file = os.path.split(self.training_file)
        with open('trained/'+file[:-4]+'_'+kind+'_'+str(self.ngram_size)+'_'+str(self.length)+'.pack', 'rb') as fp:
            if kind == "ip_list":
                self.ip_list = umsgpack.load(fp)
            elif kind == "cp_list":
                self.cp_list = umsgpack.load(fp)
            elif kind == "ep_list":
                self.ep_list = umsgpack.load(fp)
            else:
                raise Exception("Unknown list given (required: ip_list, cp_list, or ep_list)")
        logging.debug("Done! Everything loaded from disk.")
        logging.debug("Loading the data from disk took: {}".format(datetime.datetime.now()-start))
