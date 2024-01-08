# Corporate Clash Egg Tools

**eggtools** is a library that provides access to managing egg files through the use of EggMan.

**EggMan** is a docile robust egg manager for installing & maintaining models. 
It allows you to do bulk/individual modifications to a set of egg files,

## Installation
If you are using Devtools, then Poetry should automatically install Eggtools.

However, to install this as a standalone package, you can run the following:
```
pip install git+https://github.com/CorporateClash/eggtools
```


## Utilities
If you installed Eggtools as a global package, then a few utilities are available:

### Egg Aggregator
Aggregates a set of egg files into one. Requires at least two input egg files.
```
python -m eggtools.scripts.EggAggregator
```

### Egg Prepper
Prepares eggs for cooking by removing defined UV names, converting <ObjectTypes> into their literal equivalents, and
fixing TRef names.
```
python -m eggtools.scripts.EggPrepper
```

### Egg UV Remover
Removes UV names off a given egg file.
```
python -m eggtools.scripts.UVNameRemover
```
