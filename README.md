## Another Wordle Solver

Resolving my urge of playing Wordle for once and for all.
## Solver short description

Every time we make a guess, we receive a *pattern* (green, yellow, grey boxes) which gives us information on what letters are present and/or missing. Ideally, we should choose such guesses which would minimize space of available words for the next rounds to come (hence less turns would be required to solve the puzzle). 

I guess the main approach is to use [Shannon Entropy](https://en.wikipedia.org/wiki/Entropy_(information_theory)) , which would help us to measure how effective each guess is. Entropy would tell us how *informative* the guess is, in other words it will tell us expected(average) number of information bits for this guess. For example if we have 1000 words and guess gives us 3 bit of information, then we have reduced our search space by factor of $2^3$ , so on average for the next round we would have 1000 / 8 = 125 words to choose from. Hence we want to find a word which would give us maximum Entropy. 

$H = -\sum_{x\in\chi} p\left(x\right) \log_2(p\left(x\right))$ where $\chi$ is a set of all *patterns* and $p(x)$ is the probability of a *pattern* occurring.

Solution:
- For every *valid word* we can calculate Entropy against all possible *accepted words*.
- Choose guess with the highest Entropy value
- Make Guess
- Based on returned *pattern* reduce set of *accepted words* 
- Repeat

If we want to play game more fairly, without access to set of accepted words,  then we would need to load dictionary of all 5 letter words and assign probability on how likely this word can be an answer.  For example word "lemon" is probably part of solution set while word "abohm" is likely not. But since we have set of accepted words we basically have $p(word) = 1.0$ if it's part of *accepted* word set and 0.0 otherwise.

## Benchmark Results

```bash
pypy3 benchmark.py
```
| Solver | Success Rate | Average Score (Success only) |
| --- | --- | --- |
| RandomSolver(all words) | 87.27% | 4.64 |
| RandomSolver(accepted words) | 98.40% | 4.00 |
| DistanceSolver(DistanceMetric.HAMMING_DISTANCE) | 98.96% | 3.89 |
| DistanceSolver(DistanceMetric.FREQ_DISTANCE) | 99.00% | 3.72 |
| EntropySolver | 99.52% | 3.55 |