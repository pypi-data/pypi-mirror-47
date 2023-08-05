Changelog
=========

0.2.0
-----

- :class:`pfsspy.Input` and :class:`pfsspy.Output` now take the optiona keyword
  argument *dtime*, which stores the datetime on which the magnetic field
  measurements were made. This is then propagated to the *obstime* attribute
  of computed field lines, allowing them to be transformed in to coordinate
  systems other than Carrignton frames.
- :class:`pfsspy.FieldLine` no longer overrrides the SkyCoord ``__init__``;
  this should not matter to users, as FieldLine objects are constructed
  internally by calling :meth:`pfsspy.Output.trace`

0.1.5
-----

- `Output.plot_source_surface` now accepts keyword arguments that are given to
  Matplotlib to control the plotting of the source surface.

0.1.4
-----

- Added more explanatory comments to the examples
- Corrected the dipole solution calculation
- Added :func:`pfsspy.coords.sph2cart` to transform from spherical to cartesian
  coordinates.

0.1.3
-----

- :meth:`pfsspy.Output.plot_pil` now accepts keyword arguments that are given
  to Matplotlib to control the style of the contour.
- :attr:`pfsspy.FieldLine.expansion_factor` is now cached, and is only
  calculated once if accessed multiple times.
