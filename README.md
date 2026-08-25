# Raindrops on roses

Raindrops on roses and whiskers on kittens<br>
[...]<br>
These are a few of my favorite things

## Installation

### Default

To install default, use:
> uv add raindrops-on-roses

## Usage

Just use the module name `favs` ("favourites") to `import` directly, e.g. 
> import favs

To access `<function>` in `<submodule>` within `favs`, then use `favs.<submodule>.<function>`, e.g.
> favs.repr.args_kwargs_repr(1, 'two', y=25, z='last)

There's no need (or option) for (lengthy) ~~`import raindrops_on_roses`~~ or ~~`import raindrops_on_roses as favs`~~.


## Contents
* dicttools
  * map_mapping_keys()
  * map_mapping_values()
* itertools
  * mark_first()
  * mark_last()
* repr
  * function_repr()
  * function_call_repr()
  * function_param_repr()
  * function_signature_repr()
  * function_header_repr()
  * args_kwargs_repr()
  * call_repr()
* types
  * EndoFunction
  * sentinel (for Python versions <= 3.14)