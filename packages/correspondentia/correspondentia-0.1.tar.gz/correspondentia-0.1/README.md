# Correspondentia

[![Build Status](https://travis-ci.org/BONSAMURAIS/correspondentia.svg?branch=master)](https://travis-ci.org/BONSAMURAIS/correspondentia) [![Build status](https://ci.appveyor.com/api/projects/status/2ktjyy6bn8vao95k?svg=true)](https://ci.appveyor.com/project/cmutel/correspondentia)

Python library to map correspondence tables in different formats to data structures.

A quick example:

```python

from correspondentia import match_fields

numbers_to_names = {
    1: [{"value": "one", "type": "exact"}],
    2: [{"value": "two", "weight": 0.5, "type": "disaggregation"},
        {"value": "deux", "weight": 0.5, "type": "disaggregation"}],
}

my_data = [{
    'count': 1,
    'name': 'foo'
}, {
    'count': 2,
    'name': 'bar'
}]

list(match_fields(my_data, numbers_to_names, "count"))
> [{'count': 'one', 'name': 'foo'},
   {'count': 'two', 'name': 'bar', 'correspondentia_allocation': 0.5},
   {'count': 'deux', 'name': 'bar', 'correspondentia_allocation': 0.5}]

```

`match_fields` return a generator.

## Input data

Input data should be an iterable of objects supporting the dictionary interface.

## Input tables

`correspondentia` currently can import the following formats:

* CSVs following the simple schema

We plan to also eventually support the following:

* RDF (Turtle) correspondence tables following the BONSAI spec
* CSVs with BONSAI ontology predicates

You can also write custom importers, or define correspondence tables manually. In either case, the correspondence table data should include at least the following fields (additional fields are also allowed):

```python

{
    "label in origin schema (usually str, but can be int or float)": {
        "value": "label in destination schema (usually str, but can be int or float)",
        "type": one of ["exact", "disaggregation"],
        "weight": float, # optional
    }
}

```

## Simple CSV schema for input tables

A CSV with two required and one optional columns.

* First column: Label in origin schema
* Second column: Label in destination schema
* Third column (optional): Weight used for disaggregation.

If matching is 1-N or N-1, just use multiple rows with redundant labels.

CSVs should follow the Open Knowledge CSV spec. Do not use column headers.

## Installation

Installation via normal pathways; currently has no dependencies.

## Contributing

Follow standard fork/pull-request procedure.
