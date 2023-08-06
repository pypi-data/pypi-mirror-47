# pybemolle
PyBemolle is a [pygments](http://pygments.org/) library plugin made to colorize guitar chords

This is an example of how this library works:

![pybemolle](pybemolle.png "pybemolle")

### Quickstart

Install pygments and pybemolle lib into your python environment:

```bash
pip install pygments && pip install pybemolle
```

Make test.bemolle file:

```bemolle
;;  A                            Asus4   A
    Deep down Louisiana close to New   Orleans
;;                                     Asus4 A
    Way back up in the woods among the ever  greens
;;        D
    There stood a log cabin made of earth and wood
;;        A                         Asus4     A
    Where lived a country boy named Johnny B. Goode
;;      E                             E7*      E
    Who never ever learned to read or write so well
;;               A                           Asus4     A
    But he could play the guitar just like a ringing a bell
 
;;  A
    Go go, Go Johnny go go, Go Johnny go
;;  D
    Go, Go Johnny go
;;  A
    Go, Go Johnny go
;;  E  E7          A
    Go,Johnny B. Goode
```

Compile it to html code using pygments tool:

```bash
pygmentize -f html -O full -o test.html test.bemolle
```

Enjoy!


### Advanced usage

The same example using python code:

```python
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import get_formatter_by_name


song = '''
;;  A                            Asus4   A
    Deep down Louisiana close to New   Orleans
;;                                     Asus4 A
    Way back up in the woods among the ever  greens
;;        D
    There stood a log cabin made of earth and wood
;;        A                         Asus4     A
    Where lived a country boy named Johnny B. Goode
;;      E                             E7*      E
    Who never ever learned to read or write so well
;;               A                           Asus4     A
    But he could play the guitar just like a ringing a bell
 
;;  A
    Go go, Go Johnny go go, Go Johnny go
;;  D
    Go, Go Johnny go
;;  A
    Go, Go Johnny go
;;  E  E7          A
    Go,Johnny B. Goode
'''

lexer = get_lexer_by_name('bemolle', stripall=True)
formatter = get_formatter_by_name('html')
result = highlight(song, lexer, formatter)
```
