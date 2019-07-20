# Pyrrho
Automated password composition policy selection.

![logo](assets/logo-text-h.svg)

## Overview
Pyrrho, named after the first Greek skeptic philosopher [Pyrrho of Elis](https://en.wikipedia.org/wiki/Pyrrho) makes up the core of the Skeptic password composition policy evaluation framework. Written in Python, it does a few things:

* Filters password probability distributions derived from large password datasets according to user-specified password composition policies (rules around password creation).
* Redistributes probability in these distributions in a number of different redistribution modes, with the aim of capturing a variety of broad user password selectiono behaviours.
* Fits power-law equations to the resulting distributions to permit selection of password composition policies based on the level of uniformity they induce under different redistribution modes.

The end result is automated password composition policy ranking.

## Redistribution Modes
It's easy to compute a password probability distribution from a large set of password frequencies, like those found in [SecLists](https://github.com/danielmiessler/seclists). We simply divide the password frequency by the total number of passwords in the dataset. For example, there are 35 passwords in this dataset (modelled as a frequency distribution):

```
password, frequency
"password", 25
"hunter2", 5
"matrix", 5
```

So their probability distribution looks like this:

```
password, probability
"password", 0.714285714
"hunter2", 0.142857143
"matrix", 0.142857143
```

If we add all the probabilities together, the result is 1. This is a property of probability distributions, specifically one of the probability axioms (number 2) which are as follows:

1. All values in a password probability distribution will bese greater than or equal to 0 and less than or equal to 1.
2. The sum of all values in the range of password probability distribution will be equal to 1.
3. The sum of any two distinct values in the domain of a password probability distribution will be equal to the probability of either of those events occurring.

Now, let's say we implement a password composition policy banning the password `hunter2` on the system. How does the above probability distribution change? The answer is that a depends on user behaviour (specifically, how users re-select their passwords), so we *don't know*. What we can do, though, is work out a best case, an average case and a worst case in a way that doesn't break our probability distribution by causing it to violate any of the probability axioms.

### Uniform Reselection (Best Case)
All users select another password completely uniformly. This means that the probability `0.142857143` that used to belong to the password `hunter2` will be divided equally between the remaining passwords. As we have two remaining passwords, that will mean adding `0.142857143 / 2 = 0.071428572` to each remaining probability, resulting in:

```
password, probability
"password", 0.785714286
"hunter2", 0
"matrix", 0.214285715
```

As it is now impossibe for our users to select `hunter2` as a password because it is forbidden by the policy, its probability is now `0`.

### Proportional Reselection (Average Case)
Most likely, when users are forced to select a password other than `hunter2`, they will do so proportionally to the remaining probabilities in the distribution. To model this, we can apply simple renormalization where for each password `p` its probability `P(p)` becomes `P(p) / 1 - P('hunter2')`. This constructs a distribution that preserves the proportions of remaining passwords:

```
password, probability
"password", 0.833333333
"hunter2", 0
"matrix", 0.166666667
```

### Convergent Reselection (Worse Case)
If we assume the worst, for every password we ban, all users who would previously have chosen that password will gravitate towards (i.e. *converge on*) the most common one. To simulate this, we simply add the probability of the banned password straight on to the most common remaining password in the distribution:

```
password, probability
"password", 0.857142857
"hunter2", 0
"matrix", 0.142857143
```

## Next Steps
This version of Pyrrho currently relies on a very basic Python implementation of password composition policies for proof-of-concept purposes. As a next step, we plan to integrate the tool properly into Skeptic by making it compatible with [Skeptic authorities](https://github.com/sr-lab/skeptic-authority-template). This will permit reasoning about software-specific password composition policy representations from within Coq and applying them to various password probability distributions.
