
BPG is a template engine with expression support.
A BPG template is a YAML file. The values in a template
can be an expression.

A template can be instantiated to a configulation which
is a set of key-value pairs. The values are not expression,
but concrete values evaluated from template expressions.


Template
Each template has an identifying name. The name is 
specified in yml template file.

Template Library

BPG mainatins a repository of  templates loaded from yaml
files. This repository is created during module
initialization. All *.yml files in BPG_TEMPLATES_DIR 
are loaded as template. 

A template can be retrieved from this repository by name.


Usage:

from bpg import Template, TemplateLibrary
# assuming BPG_TEMPLATES_DIR is set as an environment
$ variable
# all *.yml are loaded as template

template = TemplateLibary.find


