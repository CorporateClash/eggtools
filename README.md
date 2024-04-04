# Toontown: Corporate Clash Egg Tools

**eggtools** is a library that provides access to managing egg files through the use of EggMan.

**EggMan** is a docile robust egg manager for installing & maintaining models. 
It allows you to do bulk/individual modifications to a set of egg files,

## Installation

### Standalone Package
To install and use as a standalone package, you can run the following in your developer environment:
```
pip install git+https://github.com/CorporateClash/eggtools
```

### Development

For working directly with the codebase, you have the option to use a virtual environment or a Poetry environment

#### Quickstart

1. Clone this repository

```
git clone https://github.com/CorporateClash/eggtools
cd eggtools
```

2. Optional: Create a Poetry or virtual environment
```
python -m venv env
./env/Scripts/activate
```

*or*

```
poetry init
poetry shell
```

3. Install required dependencies

```
python -m pip install -r requirements.txt
```

*or*

```
poetry install
```

4. Validate components

```
python -m tests.test_attrs
```

Note: You should see a warning for a missing dummy_test.egg model. This is intended.

### Optional: Configuring Environment Variables

There are a few optional environment variables that can be defined to autocomplete certain paths:

| Variable Name     | Description                                                                            | Default Value |
|-------------------|----------------------------------------------------------------------------------------|---------------|
| GAMEASSETS_SRC    | Currently used for developing TexturePrefixRefactorTool; reserved for future use.      | ./            |
| GAMEASSETS_MAPS   | Optionally used to declare a default directory when searching for textures.            | ./maps/       |
| GAMEASSETS_MODELS | Used to declare the default directory when searching for external egg file references. | ./models/     |

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
