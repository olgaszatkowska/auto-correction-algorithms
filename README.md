# auto-correction-algorithms

How to run:
1) Create virtual environment

```
python3 -m venv venv
```

2) Activate virtual environment

```
source venv/bin/activate
```

3) Run prepare to download packages and dataset

```
make prepare
```

4) Run research, where N is the number of samples

```
make run-research N=3
```

5) Implement algorithm

Context based algorithms should inherit from ContextAutoCorrect and single world lookup should inherit from SingleWordLookup.

```
class LevenshteinAutoCorrect(SingleWordLookup):
```


```
class MarkovAutoCorrect(ContextAutoCorrect):
```

They should implement def `fix_word(self, word: str) -> str:` which takes in either entire sentence or one world and returns the same string but with corrected errors. They should also implement `def name(self) -> str:` property which is needed to run research script.

```
def fix_word(self, sentence: str) -> str:
    return self._fix(sentence)

@property
def name(self) -> str:
    return "My algorithm"
```

To test implemented algorithm add it to `auto_correct_classes` in `src/research`.

```
auto_correct_classes = [
    MarkovAutoCorrect(),
    MyAlgorithm()
]
```

Inheritance will inject proper dataset for tests. Then, run command

```
make run-research N=3
```