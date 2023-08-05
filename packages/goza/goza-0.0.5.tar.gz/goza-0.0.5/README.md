# Goza
A personal Python assistant library

## Overview
This is a working directory for Goza, my personal assistant Python library.  Goza provides me with tools to accomplish common tasks in my preferred manner.

## Installation
Goza is available on pip!

```python
pip install -U goza
```
## Modules
### Scatter
`Scatter` creates a pre-formatted scatter plot.  Title, axis labels, and figure size may be passed as arguments.
#### Usage
```python
import random
from goza import Scatter

x = random.sample(range(1, 100), 50)
y = random.sample(range(1, 100), 50)

scatter = Scatter(x, y,  title="Scatter Example")
```

![scatter](Scatter_Example.png "Scatter Example")