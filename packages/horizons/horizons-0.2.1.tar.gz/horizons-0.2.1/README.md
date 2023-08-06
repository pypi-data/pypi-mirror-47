# horizons

A python client for the [JPL HORIZONS System](https://ssd.jpl.nasa.gov/?horizons).

This is an ugly regex fueled API. JPL has a much cleaner [SSD/CNEOS API Service](https://ssd-api.jpl.nasa.gov/) that overlaps with HORIZONS in some places. HORIZONS' orbital element data on "Major Bodies" (i.e. planets, moons, and some others) are not available yet in this other collection of APIs. This project only aims to cover those features.

Only getting position and velocity vectors of major bodies is supported. This project could be extended to pull from other features of HORIZONS, like retrieving orbital elements.

## Usage

```python
from horizons import Horizons

with Horizons() as h:
    bodies = h.get_major_bodies() # equivalent to 'MB' in HORIZONS
    print(bodies)
    # [
    #   ...,
    #   horizons.BodyResult(
    #     id='301',
    #     name='Moon',
    #     designation='',
    #     other='Luna'
    #   ),
    #   ...
    # ]

    moon_vectors = h.get_vectors('301', center='399')
    print(moon_vectors)
    # horizons.VectorsResult(
    #   epoch_jd_tdb=2458642.5,
    #   calendar_date_tdb='A.D. 2019-Jun-08 00:00:00.0000',
    #   pos_km=(
    #     -268370.0664760619,
    #     252047.1714898835,
    #     16377.37006983293
    #   ),
    #   vel_kmps=(
    #     -0.7239795957732902,
    #     -0.7759062564667508,
    #     0.08457449888090685
    #   )
    # )
```
