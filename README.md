# Vincenty formula geodesic
#
### Python Code of the Geodesic Vincenty formula

Calculate the geographical distance (in meters, kilometers, millimeters, miles, nautical miles, feet, inches and yards) between 2 points with extreme accuracy.

This code implements Vincenty's formula to the inverse geodetic problem. It is based on the WGS 84 reference ellipsoid and is accurate to within 1 mm (!) or better.

### Example to use

```
coord1 = [40.670265648245696, -73.82879452057598]
coord2 = [40.6702786191182, -73.8287890775083]
vincenty = Vincenty(coord1, coord2)
print(vincenty.meters)
```
### Options measure

* .meters = output distance in meters
* .km = output distance in kilometers
* .mm = output distance in milimeters
* .ml = output distance in miles
* .n_miles = output distance in nautical miles
* .feet = output distance in feet
* .inches = output distance in inches
* .yards = output distance in yards

### More Information

[Vincenty formulae - Wikipedia](https://en.wikipedia.org/wiki/Vincenty's_formulae)
