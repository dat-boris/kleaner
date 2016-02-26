## Kleaner

A set of simple utilities for cleaning up data frame.

## Install with pip

```
sudo pip install git+git://github.com/sketchytechky/kleaner.git
```

## Getting started

```
import pandas as pd
from kleaner.kleaner import Kleaner

df = pd.read_csv('kaggle.csv')

kdf = Kleaner(df)

# get the healthiness of the Kaggle
kdf.healthiness()
```
