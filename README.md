# Pyrrho
Automated password composition policy selection.

![logo](assets/logo-text-h.svg)

## Overview
Pyrrho, named after the first Greek skeptic philosopher [Pyrrho of Elis](https://en.wikipedia.org/wiki/Pyrrho) makes up the core of the Skeptic password composition policy evaluation framework. Written in Python, it does a few things:

* Filters password probability distributions derived from large password datasets according to user-specified password composition policies (rules around password creation). Policy naming in this project mostly follows the Shay/Komanduri conventions \[1\].
* Redistributes probability in these distributions in a number of different redistribution modes, with the aim of capturing a variety of broad user password selectiono behaviours.
* Fits power-law equations to the resulting distributions to permit selection of password composition policies based on the level of uniformity they induce under different redistribution modes. This draws on research by Malone and Maher \[2\] and Wang et al. \[3\] into [Zipf's law](https://en.wikipedia.org/wiki/Zipf%27s_law) in passwords.

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

### Convergent Reselection (Worst Case)
If we assume the worst, for every password we ban, all users who would previously have chosen that password will gravitate towards (i.e. *converge on*) the most common one. To simulate this, we simply add the probability of the banned password straight on to the most common remaining password in the distribution:

```
password, probability
"password", 0.857142857
"hunter2", 0
"matrix", 0.142857143
```

## Running
To run the demo, first take a look at the file in `/tasks/sample.json`:

```json
{
  "out": "../results",
  "modes": [1, 2, 3],
  "files": ["../data/singles.probs"],
  "authority": "./authority.native",
  "policies": ["basic8", "basic7", "basic6"]
}
```

This is a very simple file format, understood by Pyrrho, called a *task*. For every file listed in `files` (see `/data/singles.probs` to get an idea about formatting), redistribution will take places in each mode listed in `modes` under each policy listed in `policies` \[1\]. Actual password composition policy enforcement is carried out by a [Skeptic authority](https://github.com/sr-lab/skeptic-authority-template), which must be compiled and referenced from the `authority` field. All specified policies must be understood by the authority, for more instructions consult [the Skeptic authority template repository](https://github.com/sr-lab/skeptic-authority-template). Modes are as follows:

1. Proportional Reselection
2. Uniform Reselection
3. Convergent Reselection

For testing purposes, a probability distribution derived from passwords in the relatively small *singles.org* dataset from [SecLists](https://github.com/danielmiessler/seclists) is included under `/data`. To see the tool in action, run the following and take a look in the `/results` directory:

```bash
cd src
python3 pyrrho.py ../tasks/sample.json
```

You'll notice probability distributions under each redistribution mode and corresponding JSON files containing fitted power-law curves in the `/results` directory when the tool has finished running.

## References
1. Saranga Komanduri, Richard Shay, Patrick Gage Kelley, Michelle L. Mazurek, Lujo Bauer, Nicolas Christin, Lorrie Faith Cranor, and Serge Egelman. 2011. Of passwords and people: measuring the effect of password-composition policies. In Proceedings of the SIGCHI Conference on Human Factors in Computing Systems (CHI '11). ACM, New York, NY, USA, 2595-2604. DOI: https://doi.org/10.1145/1978942.1979321 \[[PDF](https://www.guanotronic.com/~serge/papers/chi11b.pdf)\]
2. David Malone and Kevin Maher. 2012. Investigating the distribution of password choices. In Proceedings of the 21st international conference on World Wide Web (WWW '12). ACM, New York, NY, USA, 301-310. DOI: https://doi.org/10.1145/2187836.2187878 \[[PDF](https://www.maths.tcd.ie/~dwmalone/p/www2012.pdf)\]
3. D. Wang, H. Cheng, P. Wang, X. Huang and G. Jian, "Zipf’s Law in Passwords," in IEEE Transactions on Information Forensics and Security, vol. 12, no. 11, pp. 2776-2791, Nov. 2017. DOI: https://doi.org/10.1109/TIFS.2017.2721359 \[[PDF](http://wangdingg.weebly.com/uploads/2/0/3/6/20366987/passwordzipf_v8.pdf)\]
