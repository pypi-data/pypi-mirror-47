## Fast Haversine distance evaluation

This package is a numpy version of [haversine](https://github.com/mapado/haversine). 
Compared with [haversine](https://github.com/mapado/haversine), our implementation is much more efficient when dealing with list-wise distance calculation.

### Usage

```python
from fasthaversine import haversine

haversine(points1, points2, unit='km')
``` 

where `points1` and `points2` are two list of tuples (lat, lon).
