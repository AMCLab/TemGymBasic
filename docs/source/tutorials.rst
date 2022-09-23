========
Examples
========

Lens & Rotation Centre Guide
----------------------------

Beam Tilt/Shift Guide
---------------------
In this basic model of the beam shift/tilt alignment, we use a pair of deflectors, a lens,
and a detector to bring the alignment diagram to life. 
For the beam shift and beam tilt alignment, the goal is to find the "deflector ratio" setting
such that the beam purely shifts or purely tilts in the detector plane. The deflector ratio value is a 
multiplier which dictates how the lower deflector responds to a deflection provided by the upper deflector. 
For example, if the upper deflector adds a deflection of 0.5 radians to the beam, and the deflector ratio 
is set to -1, the lower deflector will add a deflection of -0.5 radians to the beam, cancelling out the 
deflection from the upper deflector. This will then shift the beam over the sample and keep the beam paralell to
the optic axis. 

Another layer of complication is added because alignment manuals actually explain this alignment
in terms of "Pivot Points", and there is a seperate pivot point for both beam tilt and beam shift. 
Pivot points are simply where the beam pivots before or after going through lens. 
For beam shift the beam needs to go over the sample and into the lens paralell to the optic axis, 
and this will cause all rays to converge or "pivot" on the focal point of this lens (a.k.a the back focal plane).
For beam tilt, the beam needs to pivot about a point on the sample before the lens, and this requires that 
our deflector ratio is set so that all rays go through the front focal plane, which is where the pivot point
for beam tilt is located. For the proceeding alignments it is important to mention that the deflector ratio 
that we need to find is a function of the distances between each component. When creating this model, 
we placed the components at convenient distances so that the deflector ratio is a nice even value.

Beam Shift Alignment
--------------------
Run the basic Beam Shift/Tilt model and click the "Wobble Def Ratio X Button". 
Set the deflector ratio to -1 and see that the spot on the detector is now stationary.
You have correctly aligned the beam shift pivot point.

Beam Tilt Alignment
---------------------
Now adjust the deflector ratio so that it is set to -2, and see that the beam tilts about a single point 
in the sample plane on the 3D viewer. 

Condenser Astigmatism
---------------------

Condenser Aperture
------------------

Biprism
-------

Model TEM
---------

Model SEM
---------
