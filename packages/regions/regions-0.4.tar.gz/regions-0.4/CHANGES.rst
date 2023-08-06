0.4 (2019-06-17)
================

New Features
------------

- Add region copy methods [#269]
- Add pixel region rotate method [#265]
- Added ``union`` and ``intersection`` methods to the ``BoundingBox``
  class. [#277]
- Add support for BOX in FITS regions [#255]
- Add PixCoord.xy [#247]

Bug Fixes
---------

- Fixed a corner-case issue where ``RegionMask.multiply()`` would not set
  non-finite data values outside of the mask but within the bounding box
  to zero. [#278]
- Fix 'text' renamed to 'label' [#234]


Other
-----

- Remove astropy-healpix dependency [#258]
- Use standalone six to avoid deprecation warnings [#235]
- Change CRTF writer to match CASA implementation [#226]
- Simplify annulus regions [#279]

See also: `regions v0.4 merged pull requests list on Github <https://github.com/astropy/regions/pulls?q=is%3Apr+milestone%3A0.4+>`__.

0.3 (2018-09-09)
================


New features
------------

- Changed ``as_patch`` to ``as_artist`` to accommodate non-patch artists [#218]

- Implemented ``to_pixel`` for ``regions.CompoundSkyRegions``,
  ``to_mask`` for ``regions.CompoundPixelRegion`` and ``to_pixel`` for
  ``regions.CircleSkyRegion``. [#137]

- Handling dimension and broadcast of `x` and `y` in ``regions.PixCoord``.
  [#172]

- Deserialization of ``CRTF`` file format is possible. [#173]

- Added ``regions.TextPixelRegion`` and ``regions.TextSkyRegion``. [#177]

- Added ``Shape`` layer in the serialization of ``DS9`` format. Also,
  implemented ``RegionMeta`` and ``RegionVisual`` to validate
  the meta parameters. [#179]

- Serialization of ``regions.Region`` object to ``CRTF`` format
  is possible. [#186]

- Fix mask bug for regions with negative indices. [#190]

- Improved the ``plot`` methods for several regions. Added ``as_patch`` for
  annulus regions. Now, uses the parameters in the ``visual`` attributes of
  regions in the matplotlib plotting. Also, added ``mpl_properties_default``
  method in ``regions.PixelRegion`` to set the visual parameters to that of
  ``DS9`` by default. [#194]

- Now, ``to_mask`` in ``regions.CompoundPixelRegion`` handles negative
  bounding box. [#195]

- Added ``regions.RectangleAnnulusPixelRegion``,
  ``regions.RectangleAnnulusSkyRegion``, ``regions.EllipseAnnulusPixelRegion``
  and ``regions.RectangleAnnulusSkyRegion``. Also, implemented custom descriptor
  classes for attribute validation. [#196]

- Implemented FITS Region Binary Table reader and writer. [#198]

- Renamed ``Mask`` class to ``RegionMask`` and added ``origin`` arg to
  ``as_patch`` and ``plot`` methods in ``regions.Region`` class. [#203]

- Support for explicit formatting directives in ``DS9``. [#204]

See also: `regions v0.3 merged pull requests list on Github <https://github.com/astropy/regions/pulls?q=is%3Apr+milestone%3A0.3+>`__.

0.2 (2017-02-16)
================

Changelog wasn't filled.

See also: `regions v0.2 merged pull requests list on Github <https://github.com/astropy/regions/pulls?q=is%3Apr+milestone%3A0.2+>`__.

0.1 (2016-07-26)
================

Changelog wasn't filled.

See also: `regions v0.1 merged pull requests list on Github <https://github.com/astropy/regions/pulls?q=is%3Apr+milestone%3A0.1+>`__.
