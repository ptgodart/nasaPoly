nasaPoly
========

Python interface for thermodynamic properties based on NASA 9 polynomial format
[[source]](https://www.grc.nasa.gov/WWW/CEAWeb/TP-2002-211556.pdf).

Installation
------------

```bash
pip3 install git+https://github.com/ptgodart/nasaPoly.git
```

Usage
-----

```python
import nasaPoly

Water = nasaPoly.Species('H2O(L)')

T = 300 # K
h_0 = Water.h_0(T) # J/mol
s_0 = Water.s_0(T) # J/mol-K
g_0 = Water.g_0(T) # J/mol
cp_0 = Water.cp_0(T) # J/mol-K

# Print state
Water.printState(T)

print(Water.molecular_wt)
```
