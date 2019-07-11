#!/usr/bin/env pypy
# -*- coding: utf-8 -*-

''' This script loads the training and estimates the probability (strength) of some passwords
:author: Maximilian Golla
:contact: maximilian.golla@rub.de
:version: 0.7.1, 2019-07-11
'''

# Load external modules
from configs.configure import *

''' Loads the training data from disk '''
def worker(length):
    ngram_creator = NGramCreator({
        "name": CONFIG.NAME,
        "alphabet": CONFIG.ALPHABET,
        "ngram_size": CONFIG.NGRAM_SIZE,
        "training_file": "input/"+CONFIG.TRAINING_FILE,
        "length": length,
        "progress_bar": CONFIG.PROGRESS_BAR
    })
    logging.debug("Thread: {} - ip_list load() ...".format(length))
    ngram_creator.load("ip_list")
    logging.debug("Thread: {} - cp_list load() ...".format(length))
    ngram_creator.load("cp_list")
    logging.debug("Thread: {} - ep_list load() ...".format(length))
    ngram_creator.load("ep_list")
    logging.debug("Thread: {} - Loading done ...".format(length))
    MARKOV_MODELS.append(ngram_creator)

''' Every length has its own model, we select the correct model for every password '''
def _select_correct_markov_model(pw_length, markov_models):
    result = markov_models[0] # Fallback solution, if there is no model for the selected length
    for model in markov_models:
        if model.length == pw_length:
            result = model
    return result

''' This function manages the password strength evaluation '''
def eval():
    # ngram creator
    global MARKOV_MODELS
    MARKOV_MODELS = []
    threads = []
    for length in CONFIG.LENGTHS:
        # Using threads is not beneficial, because it's a disk intensive task
        thread = Thread(target = worker, args = (length,))
        thread.start()
        threads.append(thread)
    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    logging.debug("Training loaded from disk ...")
    logging.debug("Number of Markov models: "+str(len(MARKOV_MODELS)))
    fo = open("results/"+CONFIG.EVAL_FILE.rstrip('.txt')+"_result.txt", "w")
    with open("input/"+CONFIG.EVAL_FILE, 'r') as inputfile:
        for line in inputfile:
            line = line.rstrip('\r\n')
             # Determine correct model
            ngram_creator = _select_correct_markov_model(len(line), MARKOV_MODELS)
            if len(line) != ngram_creator.length: # Important to prevent generating "passwor", or "iloveyo", or "babygir"
                sys.stderr.write("\x1b[1;%dm" % (31) + "Info: No Markov model for this length: {} {}\n".format(len(line),line) + "\x1b[0m")
                fo.write("{} {}\t{}\n".format("Info: No Markov model for this length:", len(line), line))
                continue
            if ngram_creator._is_in_alphabet(line): # Filter non-printable
                ip = line[:ngram_creator.ngram_size-1]
                ip_prob = ngram_creator.ip_list[ngram_creator._n2iIP(ip)]
                ep = line[len(line)-(ngram_creator.ngram_size-1):]
                ep_prob = ngram_creator.ep_list[ngram_creator._n2iIP(ep)]
                old_pos = 0
                cp_probs = []
                for new_pos in range(ngram_creator.ngram_size, len(line)+1, 1):
                    cp = line[old_pos:new_pos]
                    cp_probs.append(ngram_creator.cp_list[ngram_creator._n2iCP(cp)])
                    old_pos += 1
                pw_prob = ip_prob * ep_prob
                for cp_prob in cp_probs:
                    pw_prob = pw_prob * cp_prob
                fo.write("{}\t{}\n".format(pw_prob,line))
                fo.flush()
            else:
                sys.stderr.write("\x1b[1;%dm" % (31) + "Info: Password contains invalid characters: {}\n".format(line) + "\x1b[0m")
                fo.write("{}\t{}\n".format("Info: Password contains invalid characters:", line))
                continue
    fo.close()

def main():
    try:
        global CONFIG
        CONFIG = Configure({"name":"My Config"})
        eval()
    except KeyboardInterrupt:
        print('User canceled')
        sys.exit(1)
    except Exception as e:
        sys.stderr.write("\x1b[1;%dm" % (31) + "Error: {}\n".format(e) + "\x1b[0m")
        sys.exit(1)

if __name__ == '__main__':
    print("{0}: {1:%Y-%m-%d %H:%M:%S}\n".format("Start", datetime.datetime.now()))
    print("Press Ctrl+C to shutdown")
    main()
    print("{0}: {1:%Y-%m-%d %H:%M:%S}".format("Done", datetime.datetime.now()))
