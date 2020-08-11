nasaPoly
========

Python interface for thermodynamic properties based on NASA 9 polynomial format
([source])[https://www.grc.nasa.gov/WWW/CEAWeb/TP-2002-211556.pdf].

Usage
-----

```python
import nasaPoly

Water = nasaPoly.Species('H2O(L)')
T = 300 # K
h_0 = Water.H_0(T)
s_0 = Water.S_0(T)
g_0 = Water.G_0(T)
cp_0 = Water.Cp_0(T)
```
