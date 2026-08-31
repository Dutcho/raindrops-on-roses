# Raindrops on roses
Collection of **classes and functions** to stop repeating myself.

## Background
### Situation
I noted I came back to repetitively coding the same/similar utility functions and classes in various projects.
Often, they were trivial, so I just repeated the development effort (sometimes introducing bugs).
At other times, I copied snippets across projects (and forgot dependencies). 

Now, I decided to put in the effort to come [DRY](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself).

### Name
Obviously, this package's name comes
from the <cite>[Sound of Music](https://en.wikipedia.org/wiki/The_Sound_of_Music)</cite> 
song <cite>[My Favorite Things](https://en.wikipedia.org/wiki/My_Favorite_Things_(song))</cite>:
<blockquote>
Raindrops on roses and whiskers on kittens<br>
[...]<br>
These are a few of my favorite things
</blockquote>
<img src="https://i1.pickpik.com/photos/955/929/102/rose-bud-pink-green-preview.jpg" alt="Raindrops on roses" height="250"/>

There's _no_ connection whatsoever to similarly named packages like `raindrop-ai` or `raindrop-io-py`.

## Installation
### Default
To install default, use:
```shell
uv add raindrops-on-roses
```

## Usage
Just use the module name `favs` ("favourites") to `import` directly, e.g.
```python
import favs
```

Then, to access `<function>` in `<submodule>` within `favs`, use `favs.<submodule>.<function>`, e.g.
```python
favs.repr.args_kwargs_repr(1, 'two', y=25, z='last)
```

There's no need (or option) for (lengthy) 
~~`import raindrops_on_roses`~~ or ~~`import raindrops_on_roses as favs`~~.

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
