# NEMO: Modeling Password Guessability Using Markov Models

### tl;dr
This is our ongoing effort of using Markov models to build probabilistic password models.
Common use cases include:
* Strength estimation
* Guessing
* (Adaptive) Natural Language Encoders
* ...

### WARNING
- This is research-quality code that should only be used for a proof of concept (PoC).
- We share this code in the hope that the research community can benefit from it. Please share your code, too! :heart_eyes:
- We recommended running this software using [PyPy](https://pypy.org/download.html) (see performance stats below).

### About NEMO
The scope of this project is not limited to passwords, this software has also been used in the context of other human-chosen secrets like Emoji, PINs, and Android unlock patterns.

The architecture of the software is inspired by [OMEN](https://github.com/RUB-SysSec/OMEN). More background information about OMEN can be found [here](https://www.mobsec.ruhr-uni-bochum.de/forschung/veroeffentlichungen/omen/) and [here](https://www.mobsec.ruhr-uni-bochum.de/media/mobsec/arbeiten/2014/12/12/2013-ma-angelstorf-omen.pdf). An excellent Python implementation of OMEN, called `py_omen`, by [Matthew Weir](https://dblp.uni-trier.de/pers/hd/w/Weir:Matt) ([@lakiw](https://twitter.com/lakiw)) can be found [here](https://github.com/lakiw/py_omen).

#### Difference to OMEN
OMEN makes use of so-called levels (a form of binning). This implementation does not. Thus, efficient enumeration of password candidates (guessing passwords as OMEN does), is not (out of the box) possible, if the key space becomes too big. However, because of the non-binned output, this software has other advantages, for example it can produce [more accurate strength estimates](https://www.mobsec.ruhr-uni-bochum.de/forschung/veroeffentlichungen/accuracy-password-strength-meters/).

#### Overview: Markov Model-Based Password Guessing
* In 2005, [Arvind Narayanan](https://dblp.uni-trier.de/pers/hd/n/Narayanan:Arvind) and [Vitaly Shmatikov](https://dblp.uni-trier.de/pers/hd/s/Shmatikov:Vitaly) proposed the use of Markov models to overcome some problems of dictionary-based password guessing attacks in their work [Fast Dictionary Attacks on Passwords Using Time-Space Tradeoff](https://www.cs.cornell.edu/~shmat/shmat_ccs05pwd.pdf). The idea behind Markov models is based on the observation that subsequent tokens, such as letters in a text, are rarely independently chosen and can often be accurately modeled based on a short history of tokens.

* In 2008, the popular password cracker [John the Ripper](https://www.openwall.com/john/) introduced a `-markov` mode. More details can be found [here](https://github.com/magnumripper/JohnTheRipper/blob/bleeding-jumbo/doc/MARKOV), [here](https://openwall.info/wiki/john/markov), and [here](https://github.com/RUB-SysSec/Password-Guessing-Framework/blob/master/src/scripts/JTR_MARKOV.sh). [Simon Marechal](https://dblp.uni-trier.de/pers/hd/m/Marechal:Simon) ([@bartavelle](https://twitter.com/bartavelle)) compared this Markov model-based approach with various other guessing techniques in his work [Advances in Password Cracking](https://link.springer.com/article/10.1007/s11416-007-0064-y).

* In 2010, [Dell’Amico et al.](https://dblp.uni-trier.de/pers/hd/d/Dell=Amico:Matteo) used a Markov model-based approach to guess passwords in their work [Measuring Password Strength: An Empirial Analysis](https://arxiv.org/pdf/0907.3402.pdf).

* In 2012, [Castelluccia et al.](https://dblp.uni-trier.de/pers/hd/c/Castelluccia:Claude) (2012) and [Dürmuth et al.](https://dblp.uni-trier.de/pers/hd/d/D=uuml=rmuth:Markus) (2015) improved the concept by generating password candidates according to their occurrence probabilities, i.e., by guessing the most likely passwords first. Please refer to their works, [Adaptive Password-Strength Meters from Markov Models](https://www.ei.ruhr-uni-bochum.de/media/ei/veroeffentlichungen/2016/01/15/2012-ndss-pwd-strength.pdf), [OMEN: Faster Password Guessing Using an Ordered Markov Enumerator](https://hal.archives-ouvertes.fr/hal-01112124/document), and [When Privacy Meets Security: Leveraging Personal Information for Password Cracking](https://arxiv.org/pdf/1304.6584.pdf) for more details.

* In 2014, [Ma et al.](https://dblp.uni-trier.de/pers/hd/m/Ma:Jerry) discussed other sources for improvements such as smoothing, backoff models, and issues related to data sparsity in their excellent work [A Study of Probabilistic Password Models](https://www.ieee-security.org/TC/SP2014/papers/AStudyofProbabilisticPasswordModels.pdf).

* In 2015, [Matteo Dell’Amico](https://dblp.uni-trier.de/pers/hd/d/Dell=Amico:Matteo) and [Maurizio Filippone](https://dblp.uni-trier.de/pers/hd/f/Filippone:Maurizio) published their work on [Monte Carlo Strength Evaluation: Fast and Reliable Password Checking](http://www.eurecom.fr/~filippon/Publications/ccs15.pdf). Their [*backoff*](https://github.com/matteodellamico/montecarlopwd) Markov model can be found on GitHub, too. :heart_eyes:

* In 2015, [Ur et al.](https://dblp.uni-trier.de/pers/hd/u/Ur:Blase) compared various password cracking methods in their work [Measuring Real-World Accuracies and Biases in Modeling Password Guessability](https://www.blaseur.com/papers/sec15-guessability.pdf). For Markov model-based attacks they used a copy of Ma et al.'s code, which is now available via Carnegie Mellon University's [Password Guessability Service (PGS)](https://pgs.ece.cmu.edu/) where it is called "Markov Model: wordlist-order5-smoothed."

* In 2016, [Melicher et al.](https://dblp.uni-trier.de/pers/hd/m/Melicher:William) compared their RNN-based approach to a Markov model in their work [Fast, Lean, and Accurate: Modeling Password Guessability Using Neural Networks](https://www.usenix.org/conference/usenixsecurity16/technical-sessions/presentation/melicher). While some details are missing, their [model can be found on GitHub](https://github.com/cupslab/neural_network_cracking/blob/master/markov_model.py), too. :heart_eyes:

#### Publications
In the past, we used different versions of this code in the following publications: :bowtie:
* IEEE SP 2019: [Reasoning Analytically About Password-Cracking Software](https://www.mobsec.ruhr-uni-bochum.de/forschung/veroeffentlichungen/reasoning-analytically-about-password-cracking/) (`Markov: Multi`)
* ACM CCS 2018: [On the Accuracy of Password Strength Meters](https://www.mobsec.ruhr-uni-bochum.de/forschung/veroeffentlichungen/accuracy-password-strength-meters/) (`ID: 4B/4C Markov (Single/Multi)`)
* ACM CCS 2016: [On the Security of Cracking-Resistant Password Vaults](https://www.mobsec.ruhr-uni-bochum.de/forschung/veroeffentlichungen/cracking-resistant-password-vaults/) (`Markov Model`)

A simpler version of this code has been used for other user-chosen secrets such as [Emoji](https://www.mobsec.ruhr-uni-bochum.de/forschung/veroeffentlichungen/quantifying-security-emoji-based-authentication/) and [Android unlock patterns](https://www.mobsec.ruhr-uni-bochum.de/forschung/veroeffentlichungen/accuracy-android-pattern-strength-meters/).

### Design Decisions
Warning: Markov models are memory-eating monsters! :smiling_imp:

We use three copies of a data structure (in the past: Python OrderedDicts(), today: plain Python lists) to store the frequencies of the *n-grams* in the training corpus. We use:

- IP: Initial probabilities (ngram_size - 1)
- CP: Conditional probabilities
- EP: End probabilities (ngram_size - 1)

Here is an example for 3-grams:
```
password PW

pa       IP  (some literature uses this annotation: ^pa)

pas      CP1
 ass     CP2
  ssw    CP3
   swo   CP4
    wor  CP5
     ord CP6

      rd EP  (some literature uses this annotation: rd$)
```

#### How Big Are They?

```
IP: alphabet_length ^ (ngram_size - 1)
CP: alphabet_length ^  ngram_size
EP: alphabet_length ^ (ngram_size - 1)
```

#### Some Details For the Ones Interested:

:nerd_face:

__*n-gram* size__: Currently, we support 2,3,4,5-grams. The higher the order of the Markov chains, the more accurate the model becomes. Unfortunately, this also introduces the risk of overfitting and sparsity. If one does not have enough training data, e.g., when using the model with Android unlock patterns, computing the transition probabilities from too small count numbers will become too noisy. While we only support fixed-order Markov chains, we recommend using Dell’Amico and Filippone [*backoff*](https://github.com/matteodellamico/montecarlopwd) model for variable-order Markov chains.

__Smoothing__: Currently, we only support Additive smoothing (add '1' to the counts), also known as Laplace smoothing.

__Alphabet__: We tested this software with ASCII passwords only. Using non-ASCII passwords, likely requires to drop the support for Python 2 first. Hint: You can use the `info.py` script in the `utils` folder to determine the alphabet.

### Development
In early versions of this code, we made heavy use of Python's (Ordered)-Dictionary class. Fun fact: As of Python 3.7 [dictionaries are always ordered](https://mail.python.org/pipermail/python-dev/2017-December/151283.html) :)

```
cp_dict_full:
    key: "aaaa", value: 0.0071192...
    key: "aaab", value: 0.0034128...
    ...
```

A few months later, we optimized the memory consumption by only storing *n-grams* that really occur in the training corpus. If a rare *n-gram* like the 4-gram `o9py` does not occur in the training file, we used to return a very small default probability instead. This helped quite a lot to reduce the required memory, still, like Google Chrome, our solution easy occupied more than __20GB of RAM__. :poop:

```
cp_dict_sparse:
    key: "assw", value: 0.0838103...
    key: "sswo", value: 0.0954193...
    ...
```

Thus, we decided to refactor the code again to further limit the amount of required memory to nowadays approx. __16GB of RAM__.
Today, we use simple Python lists to store the *n-gram* probabilities in memory.
However, this forced us to come up with a `ngram-to-listindex` function(), which is different for CP in comparison with IP/EP.

```

_n2i(): ngram, e.g., "assw" to index in list, e.g., ngram_cp_list[87453]
_i2n(): index in list, e.g., ngram_cp_list[87453] to ngram, e.g., "assw"

cp_list_full:
    index:       0, value: 0.0071192... | ("aaaa")
    index:       1, value: 0.0034128... | ("aaab")
    ...
    index:   87453, value: 0.0838103... | ("assw")
    ...
    index: 8133135, value: 0.0954193... | ("sswo")
    ...
```

The current version of the code supports this operation for 2,3,4, and 5-grams.
Fortunately, while this approach achieves the desired memory savings, the additional function call does in comparison to the O(1) HashMap access (offered by Python dictionaries) not increase runtime significantly.

### Performance Testing

We highly recommended to replace Python with [PyPy](https://pypy.org/download.html) before using this software. :100: :thumbsup:
```
                 MEMORY  TIME
# PYTHON 2
CPython 2.7.10  15.36GB 53m 27s
PyPy2   7.1.1    5.88GB  3m  8s (based on Python 2.7.13) <- Highly recommended

# PYTHON 3
CPython 3.7.3   14.47GB 12m 34s
CPython 3.6.5   14.49GB 13m 13s
PyPy3   7.1.1    7.33GB  2m 13s (based on Python 3.6.1) <- Highly recommended
```

### Getting Started
#### Folder Structure

```
.
├── README.md
├── configs
│   ├── configure.py
│   ├── dev.json
│   └── main.json
├── input
├── log
│   └── multiprocessinglog.py
├── meter.py
├── ngram
│   └── ngram_creator.py
├── requirements.txt
├── results
├── train.py
├── trained
│   ├── training_cp_list_<ngram-size>_<pw-length>.pack
│   ├── training_ep_list_<ngram-size>_<pw-length>.pack
│   └── training_ip_list_<ngram-size>_<pw-length>.pack
└── utils
    ├── info.py
    └── sortresult.py
```

#### Installation

Install PyPy (for Python 2 or better Python 3), and create a virtual environment just to keep your system light and clean:

`$ virtualenv -p $(which pypy) nemo-venv`
```
Running virtualenv with interpreter /usr/local/bin/pypy
New pypy executable in /home/<username>/nemo-venv/bin/pypy
Installing setuptools, pip, wheel...
done.
```

Activate the new virtual environment:

`$ source nemo-venv/bin/activate`

Now clone the repo:

`(nemo-venv) $ git clone https://github.com/RUB-SysSec/NEMO.git`

Change into the newly cloned folder:

`(nemo-venv) $ cd NEMO`

Now install the requirements:

`(nemo-venv) $ pip install -r requirements.txt`

This includes:
- `tqdm` # for a fancy progress bar
- `u-msgpack-python` # required to store/load the trained model to/from disk
- `rainbow_logging_handler` # for colorful log messages

#### Dataset
While the Markov model can be used for a variety of things, in the following we focus on a simple **strength meter use case**.

For this, you will need two files:

- `input/training.txt`: Contains the passwords that you like to use to train your Markov model.
- `input/eval.txt`: Contains the passwords, which guessability you like to estimate.

I will not share any of those password files, but using "RockYou" or the "LinkedIn" password leak sounds like a great idea. Make sure to clean and (ASCII) filter the files to optimize the performance.

For optimal accuracy, consider to train with a password distribution that is similar to the one you like to evaluate (e.g., 90%/10% split). Please do not train a dictionary / word list, this won't work.  :stuck_out_tongue_winking_eye: You need a real password distribution, i.e., including duplicates.

- The file must be placed in the `input` folder.
- One password per line.
- File must be a real password distribution (not a dictionary / word list), i.e., must contain multiplicities.
- All passwords that are shorter or longer than the specified `lengths` will be ignored.
- All passwords that contain characters which are not in the specified `alphabet` will be ignored.
During development, we tested our code with a file that contained ~10m passwords.

#### Configuration
Before training, you need to provide a configuration file.
You can specify which configuration file to use by editing the following line in `configure.py` in the `configs` folder:

```
with open('./configs/dev.json', 'r') as configfile:
```

Here is the default content of `dev.json`, feel free to edit the file as you like.
```
{
    "name" : "Development",
    "eval_file" : "eval.txt",
    "training_file" : "training.txt",
    "alphabet" : "aeio1nrlst20mcuydh93bkgp84576vjfwzxAEqORLNISMTBYCP!.UGHDJ F-K*#V_\\XZW';Q],@&?~+$={^/%",
    "lengths" : [4,6,8],
    "ngram_size" : 4,
    "no_cpus" : 8,
    "progress_bar": true
}
```

Please note: You can use the `info.py` script in the `utils` folder to learn the alphabet of your training / evaluation file.

For example run:

`(nemo-venv) $ pypy utils/info.py input/eval.txt`

```
File: eval.txt
Min length: 3
Max length: 23
Observed password lengths: [3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,20,21,22,23]
Alphabet (escaped for Python, but watch out for the space char): "aeio1nrlst20mcuydh93bkgp84576vjfwzxAEqORLNISMTBYCP!.UGHDJ F-K*#V_\\XZW';Q],@&?~+$={^/%"
Alphabet length: 85
ASCII only: Yes
```

If you encounter any issues, go to `train.py` and change the `train()` function from multi to single processing. This way, it is easier to debug the actual problem.

#### Training

##### Training Requirements
* ~2-5 minutes
* ~8 threads (4 cores + hyper-threading)
* ~16GB of RAM
* ~6GB of disk space

##### How to Train the Model
To train the model run:

`(nemo-venv) $ pypy train.py`

Once the training is done, you should have multiple `*.pack` files in the `trained` folder. We use a lightweight [MessagePack](https://github.com/vsergeev/u-msgpack-python) implementation to serialize the model.

A successful training looks like this:

```
Start: 2019-07-06 15:54:13

Press Ctrl+C to shutdown
[15:54:13.239]     configure.py Line  30 __init__(): Constructor started for 'My Config'
[15:54:13.241]         train.py Line  76 train():    Training started ...
[15:54:13.242] ngram_creator.py Line  24 __init__(): Constructor started for 'NGramCreator, Session: Development, Length: 4, Progress bar: True'
[15:54:13.242] ngram_creator.py Line  33 __init__(): Used alphabet: ae10i2onrls9384t5m67cdyhubkgpjvfzwAxEONIRSLM.TC_DqBHYUKPJG!-*F @VWXZ/,#+&?$Q)<'=;^[(%\~]`:|">
[15:54:13.242] ngram_creator.py Line  35 __init__(): Model string length: 4
[15:54:13.242] ngram_creator.py Line  38 __init__(): NGram size: 4
[15:54:15.315] ngram_creator.py Line  48 __init__(): len(IP) theo: 804357
[15:54:15.315] ngram_creator.py Line  49 __init__(): len(CP) theo: 74805201 => 804357 * 93
[15:54:15.315] ngram_creator.py Line  50 __init__(): len(EP) theo: 804357

[15:54:15.315]         train.py Line  29 worker():   ip_list init() ...
[15:54:15.343]         train.py Line  32 worker():   ip_list count() ...
input/training.txt: 100%|███████████████████████████████████████████████████████████████████| 10000000/10000000 [00:03<00:00, 2916292.68pw/s]
[15:54:18.776]         train.py Line  35 worker():   ip_list prob() ...
[15:54:18.794] ngram_creator.py Line 213 _prob():    IP probability sum: 1.0000000000141687
[15:54:18.794]         train.py Line  38 worker():   ip_list save() ...
[15:54:18.794] ngram_creator.py Line 265 save():     Start: Writing result to disk, this gonna take a while ...
[15:54:19.022] ngram_creator.py Line 276 save():     Done! Everything stored on disk.
[15:54:19.023] ngram_creator.py Line 277 save():     Storing the data on disk took: 0:00:00.228256
[15:54:19.023]         train.py Line  41 worker():   Training IP done ...

[15:54:19.023]         train.py Line  44 worker():   cp_list init() ...
[15:54:21.722]         train.py Line  47 worker():   cp_list count() ...
input/training.txt: 100%|███████████████████████████████████████████████████████████████████| 10000000/10000000 [00:03<00:00, 2995344.77pw/s]
[15:54:25.063]         train.py Line  50 worker():   cp_list prob() ...
[15:54:25.893]         train.py Line  53 worker():   cp_list save() ...
[15:54:25.893] ngram_creator.py Line 265 save():     Start: Writing result to disk, this gonna take a while ...
[15:54:45.189] ngram_creator.py Line 276 save():     Done! Everything stored on disk.
[15:54:45.189] ngram_creator.py Line 277 save():     Storing the data on disk took: 0:00:19.295808
[15:54:45.190]         train.py Line  56 worker():   Training CP done ...

[15:54:45.190]         train.py Line  59 worker():   ep_list init() ...
[15:54:45.211]         train.py Line  62 worker():   ep_list count() ...
input/training.txt: 100%|███████████████████████████████████████████████████████████████████| 10000000/10000000 [00:03<00:00, 3005917.73pw/s]
[15:54:48.542]         train.py Line  65 worker():   ep_list prob() ...
[15:54:48.553] ngram_creator.py Line 242 _prob():    EP probability sum: 1.0000000000141684
[15:54:48.553]         train.py Line  68 worker():   ep_list save() ...
[15:54:48.554] ngram_creator.py Line 265 save():     Start: Writing result to disk, this gonna take a while ...
[15:54:48.781] ngram_creator.py Line 276 save():     Done! Everything stored on disk.
[15:54:48.782] ngram_creator.py Line 277 save():     Storing the data on disk took: 0:00:00.227519
[15:54:48.782]         train.py Line  71 worker():   Training EP done ...

[15:54:55.686] ngram_creator.py Line  53 __del__():  Destructor started for 'NGramCreator, Session: Development, Length: 4, Progress bar: True'
...
Done: 2019-07-06 15:56:11
```


#### Strength Estimation
After training, we can use the model for example to estimate the strength of a list of passwords that originate from a similar password distribution.
To do so, please double check that your `eval_file` is specified correctly in your configuration `.json`.

For the strength estimation, we will read the trained *n-gram* frequencies from disk and then evaluate all passwords from the specified `eval_file`.

`(nemo-venv) $ pypy meter.py`

The result of this strength estimation can be found in the `results` folder in a file called `eval_result.txt`.

```
...
1.7228127641947414e-13 funnygirl2
4.03572701534676e-13   single42
3.669804567773374e-16  silkk
3.345752850966769e-11  car345
6.9565427286338e-11    password1991
4.494395283171681e-12  abby28
3.1035094651948957e-13 1595159
7.936477209731241e-13  bhagwati
1.3319042593247044e-22 natt4evasexy
1.5909371909986554e-15 curbside
...
```

The values are `<TAB>` separated.
You can use `sortresult.py` from the `utils` folder to sort the passwords.

For example run:

`(nemo-venv) $ pypy utils/sortresult.py results/eval_result.txt > results/eval_result_sorted.txt`

A successful strength estimation looks like this:

```
Start: 2019-07-06 16:07:58

Press Ctrl+C to shutdown
[16:07:58.346]     configure.py Line  30 __init__(): Constructor started for 'My Config'
[16:07:58.349] ngram_creator.py Line  24 __init__(): Constructor started for 'Development'
[16:07:58.349] ngram_creator.py Line  33 __init__(): Used alphabet: ae10i2onrls9384t5m67cdyhubkgpjvfzwAxEONIRSLM.TC_DqBHYUKPJG!-*F @VWXZ/,#+&?$Q)<'=;^[(%\~]`:|">
[16:07:58.349] ngram_creator.py Line  35 __init__(): Model string length: 8
[16:07:58.349] ngram_creator.py Line  38 __init__(): NGram size: 4
[16:08:00.253] ngram_creator.py Line  48 __init__(): len(IP) theo: 804357
[16:08:00.253] ngram_creator.py Line  49 __init__(): len(CP) theo: 74805201 => 804357 * 93
[16:08:00.253] ngram_creator.py Line  50 __init__(): len(EP) theo: 804357

[16:08:00.253]         meter.py Line  23 worker():   Thread: 8 - ip_list load() ...
[16:08:00.438] ngram_creator.py Line 291 load():     Done! Everything loaded from disk.
[16:08:00.439] ngram_creator.py Line 292 load():     Loading the data from disk took: 0:00:00.184483

[16:08:00.439]         meter.py Line  25 worker():   Thread: 8 - cp_list load() ...
[16:08:14.075] ngram_creator.py Line 291 load():     Done! Everything loaded from disk.
[16:08:14.076] ngram_creator.py Line 292 load():     Loading the data from disk took: 0:00:13.635805

[16:08:14.076]         meter.py Line  27 worker():   Thread: 8 - ep_list load() ...
[16:08:14.224] ngram_creator.py Line 291 load():     Done! Everything loaded from disk.
[16:08:14.224] ngram_creator.py Line 292 load():     Loading the data from disk took: 0:00:00.148400

[16:08:14.224]         meter.py Line  29 worker():   Thread: 8 - Loading done ...
[16:08:14.225]         meter.py Line  55 eval():     Training loaded from disk ...
...

Info: No Markov model for this length: 13 jake1password
Info: No Markov model for this length: 16 marasalvatrucha3
...
Done: 2019-07-06 16:08:14

```

### FAQ

- Usage: ASCII pre-filter your input / eval files.

- Usage: Limit the alphabet `alphabet` (lower+upper+digits), *n-gram* size `ngram_size` (3 or 4-grams), password lengths `lengths` (6 or 8 character long passwords)

- Usage: Make sure you train a real password distribution, not a word list / dictionary, one normally uses with tools like Hashcat / John the Ripper.

- Debugging: If you encounter any issues, go to `train.py` and change the `train()` function from multi to single processing. This way, it is easier to debug the actual problem.

- Debugging: In `configure.py` you can change the verbosity of the `rainbow_logging_handler` from `DEBUG` to `INFO` or `CRITICAL`.


### License

**NEMO** is licensed under the MIT license. Refer to [docs/LICENSE](docs/LICENSE) for more information.

### Third-Party Libraries
* **tqdm** is a library that can be used to display a progress meter. It is a "*product of collaborative work*" from multiple authors and is using the MIT license. The license and the source code can be found
[here](https://tqdm.github.io/licence/).
* **u-msgpack-python** is a lightweight MessagePack serializer developed by Ivan (Vanya) A. Sergeev and is using the MIT license. The
source code and the license can be downloaded [here](https://github.com/vsergeev/u-msgpack-python#license).
* **rainbow_logging_handler** is a colorized logger developed by Mikko Ohtamaa and Sho Nakatani. The authors released it as "*free and unencumbered public domain software*". The source code and "license" can be found [here](https://github.com/laysakura/rainbow_logging_handler).

### Contact
Visit our [website](https://www.mobsec.rub.de) and follow us on [Twitter](https://twitter.com/hgi_bochum). If you are interested in passwords, consider to contribute and to attend the [International Conference on Passwords (PASSWORDS)](https://passwordscon.org).
