# Pyrrho
Automated password composition policy selection.

![logo](assets/logo-text-h.svg)

## Overview
Pyrrho, named after the first Greek skeptic philosopher [Pyrrho of Elis](https://en.wikipedia.org/wiki/Pyrrho) makes up the core of the Skeptic password composition policy evaluation framework. Written in Python, it does a few things:

* Filters password probability distributions derived from large password datasets according to user-specified password composition policies (rules around password creation).
* Redistributes probability in these distributions in a number of different redistribution modes, with the aim of capturing a variety of broad user password selectiono behaviours.
* Fits power-law equations to the resulting distributions to permit selection of password composition policies based on the level of uniformity they induce under different redistribution modes.

The end result is automated password composition policy ranking.
