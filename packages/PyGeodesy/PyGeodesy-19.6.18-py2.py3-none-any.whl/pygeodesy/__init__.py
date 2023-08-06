
# -*- coding: utf-8 -*-

u'''A pure Python implementation of geodesy tools for various ellipsoidal
and spherical earth models using precision trigonometric, vector-based and
approximate methods for geodetic (lat-/longitude) and geocentric cartesian
(x/y/z) coordinates.

Transcribed from U{JavaScript originals<http://GitHub.com/ChrisVeness/geodesy>}
by I{Chris Veness (C) 2005-2016} and several U{C++ classes
<http://GeographicLib.SourceForge.io/html/annotated.html>} by I{Charles Karney
(C) 2008-2017} and published under the same U{MIT License
<http://OpenSource.org/licenses/MIT>}**.

There are three modules for ellipsoidal earth models, I{ellipsoidalKarney},
I{-Vincenty} and I{-Nvector} and two for spherical ones, I{sphericalTrigonometry}
and I{-Nvector}.  Each module provides a I{attributes-LatLon-html} class
with methods and functions to compute distance, initial and final bearing,
intermediate and nearest points, area, perimeter, conversions and unrolling,
among other things.  For more information and further details see the
U{documentation<http://mrJean1.GitHub.io/PyGeodesy>}, the descriptions of
U{Latitude/Longitude<http://www.Movable-Type.co.UK/scripts/latlong.html>},
U{Vincenty<http://www.Movable-Type.co.UK/scripts/latlong-vincenty.html>} and
U{Vector-based<http://www.Movable-Type.co.UK/scripts/latlong-vectors.html>}
geodesy, the original U{JavaScript source<http://GitHub.com/ChrisVeness/geodesy>} or
U{docs<http://www.Movable-Type.co.UK/scripts/geodesy/docs>} and the Python
U{GeographicLib<http://PyPI.org/project/geographiclib>}.

Also included are modules for conversions to and from U{Cassini-Soldner
<http://GeographicLib.SourceForge.io/html/classGeographicLib_1_1CassiniSoldner.html>},
U{UTM<http://www.Movable-Type.co.UK/scripts/latlong-utm-mgrs.html>}
(Universal Transverse Mercator),
U{UPS<http://WikiPedia.org/wiki/Universal_polar_stereographic_coordinate_system>}
(Universal Polar Stereographic) and U{Web Mercator
<http://WikiPedia.org/wiki/Web_Mercator>} (Pseudo-Mercator) coordinates,
U{MGRS<http://www.Movable-Type.co.UK/scripts/latlong-utm-mgrs.html>}
(NATO Military Grid Reference System) and
U{OSGR<http://www.Movable-Type.co.UK/scripts/latlong-os-gridref.html>}
(British Ordinance Survery Grid Reference) grid references and a module for
encoding and decoding U{EPSG<http://www.EPSG-Registry.org>},
U{Geohashes<http://www.Movable-Type.co.UK/scripts/geohash.html>},
U{Georefs (WGRS)<http://WikiPedia.org/wiki/World_Geographic_Reference_System>}
and U{Garefs (GARS)<http://WikiPedia.org/wiki/Global_Area_Reference_System>}.

Other modules provide Lambert conformal conic projections and positions
(from U{John P. Snyder, "Map Projections -- A Working Manual", 1987, pp 107-109
<http://pubs.er.USGS.gov/djvu/PP/PP_1395.pdf>}), functions to clip a path or
polygon of C{LatLon} points using the U{Cohen–Sutherland
<http://WikiPedia.org/wiki/Cohen-Sutherland_algorithm>} and the
U{Sutherland-Hodgman<http://WikiPedia.org/wiki/Sutherland-Hodgman_algorithm>}
methods, functions to U{simplify<http://Bost.Ocks.org/mike/simplify>} or
linearize a path of C{LatLon} points (or a U{NumPy array
<http://docs.SciPy.org/doc/numpy/reference/generated/numpy.array.html>}),
including implementations of the U{Ramer-Douglas-Peucker
<http://WikiPedia.org/wiki/Ramer-Douglas-Peucker_algorithm>} the
U{Visvalingam-Whyatt<http://hydra.Hull.ac.UK/resources/hull:8338>} and
U{Reumann-Witkam<http://psimpl.SourceForge.net/reumann-witkam.html>}
the algorithms and modified versions of the former and classes to
U{interpolate<http://docs.SciPy.org/doc/scipy/reference/interpolate.html>}
the height of C{LatLon} points and several C{Geoid} models.

Testing
=======

All Python source code has been statically U{checked
<http://GitHub.com/ActiveState/code/tree/master/recipes/Python/546532_PyChecker_postprocessor>}
with U{PyChecker<http://PyPI.org/project/pychecker>},
U{PyFlakes<http://PyPI.org/project/pyflakes>},
U{PyCodeStyle<http://PyPI.org/project/pycodestyle>} (formerly Pep8) and
U{McCabe<http://PyPI.org/project/mccabe>} using Python 2.7.16 and with
U{Flake8<http://PyPI.org/project/flake8>} using Python 3.7.3, both in
64-bit on macOS 10.13.6 High Sierra.

The tests have been run with Python 2.7.16 and 3.7.3 (both with
U{geographiclib <http://PyPI.org/project/geographiclib>} 1.49,
U{numpy<http://PyPI.org/project/numpy>} 1.16.1 and U{scipy
<http://Scipy.org/scipylib/download.html>} 1.2.1) and with
U{PyPy<http://PyPy.org>} 6.0.0 (Python 2.7.13 and 3.5.3) on macOS
10.13.6 High Sierra.  The results of those tests are included in the
distribution files.

The tests also run with Python 2.6.9, 2.7.14, 3.5.6 and 3.6.3 (and
U{geographiclib<http://PyPI.org/project/geographiclib>} 1.49) on
U{Ubuntu 14.04<http://Travis-CI.org/mrJean1/PyGeodesy>} and with Python
3.7.3 (and U{geographiclib<http://PyPI.org/project/geographiclib>} 1.49)
on U{Debian 9<http://Cirrus-CI.com/github/mrJean1/PyGeodesy/master>}
I{all in 64-bit only} and with Python 2.7.15, 3.6.8 and 3.7.2 (all with
U{geographiclib<http://PyPI.org/project/geographiclib>} 1.49) on
U{Windows Server 2012R2<http://CI.AppVeyor.com/project/mrJean1/pygeodesy>}
I{in both 32- and 64-bit}.

On Python 3.7+, the tests run with and without C{lazy import}.

Previously, the tests were run with Python 2.6.9 (and numpy 1.6.2), 2.7.10
(and numpy 1.8.0rc1), 2.7.13, 2.7.14, 2.7.15 (and numpy 1.13.1, 1.14.0 or
1.15.2), 3.5.3, 3.6.2, 3.6.3, 3.6.4, 3.6.5, 3.7.0, 3.7.2 and U{Intel-Python
<http://software.Intel.com/en-us/distribution-for-python>} 3.5.3 (and
U{numpy<http://PyPI.org/project/numpy>} 1.11.3) on MacOS X 10.10 Yosemite,
MacOS X 10.11 El Capitan, macOS 10.12 Sierra, macOS 10.13.5 High Sierra and
macOS 10.14 Mojave, with U{Pythonista 3.1<http://OMZ-Software.com/pythonista>}
on iOS 10.3.3, 11.0.3, 11.1.2 and 11.3 on iPad4, with U{Pythonista 3.2
<http://OMZ-Software.com/pythonista>} on iOS 11.4.1 and 12.0 on iPad4,
iPhone7 and/or iPhone10, all in 64-bit only and with 32-bit Python 2.6.6
on Windows XP SP3 and with 32-bit Python 2.7.14 on Windows 10 Pro.

Documentation
=============

In addition to the U{PyGeodesy<http://PyPI.org/project/PyGeodesy>}
package, the distribution files contain the tests, the test results (on
macOS only) and the complete U{documentation<http://mrJean1.GitHub.io/PyGeodesy>}
(generated by U{Epydoc<http://PyPI.org/project/epydoc>} using command line:
C{epydoc --html --no-private --no-source --name=PyGeodesy --url=... -v pygeodesy}).

Installation
============

To install PyGeodesy, type C{pip install PyGeodesy} or C{easy_install
PyGeodesy} in a terminal or command window.  Alternatively, download
C{PyGeodesy-yy.m.d.zip} from U{PyPI<http://PyPI.org/project/PyGeodesy>}
or U{GitHub<http://GitHub.com/mrJean1/PyGeodesy>}, C{unzip} the downloaded
file, C{cd} to directory C{Pygeodesy-yy.m.d} and type C{python setup.py
install}.  To run all PyGeodesy tests, type C{python setup.py test}
before installation.

Installation of U{GeographicLib<http://PyPI.org/project/geographiclib>},
U{NumPy<http://www.NumPy.org>} and U{SciPy<http://SciPy.org>} is optional.
However, the former is required for module L{css} classes L{CassiniSoldner}
and L{Css} and function L{toCss} and for module L{ellipsoidalKarney} classes
C{LatLon} and C{Cartesian} and functions C{areaOf} and C{perimeterOf}.  The
latter are needed for the C{Geoid...} and C{Height...} interpolators, except
L{GeoidKarney}, L{HeightIDW}, L{HeightIDW2} and L{HeightIDW3}.

Notes
=====

Some function and method names differ from the JavaScript version. In such
cases documentation tag B{JS name:} shows the original JavaScript name.

Copyright and License
=====================

**) U{Copyright (C) 2016-2019 -- mrJean1 at Gmail dot com
<http://OpenSource.org/licenses/MIT>}

C{Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:}

C{The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.}

C{THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.}

@newfield example: Example, Examples
@newfield JSname: JS name, JS names

@var EPS:    System's M{epsilon} ≈2.22e-16 (C{float}).
@var EPS_2:  Half system's M{epsilon} ≈1.11e-16 (C{float}).
@var EPS1:   M{1 - EPS} ≈0.9999999999999998 (C{float}).
@var EPS1_2: M{1 - EPS_2} ≈0.9999999999999999 (C{float}).

@var F_D:   Format degrees as "deg°" (C{str}).
@var F_DM:  Format degrees as "deg°min′" (C{str}).
@var F_DMS: Format degrees as "deg°min′sec″" (C{str}).
@var F_DEG: Format degrees as "[D]DD" without symbol (C{str}).
@var F_MIN: Format degrees as "[D]DDMM" without symbols (C{str}).
@var F_SEC: Format degrees as "[D]DDMMSS" without symbols (C{str}).
@var F_RAD: Convert degrees to radians and format as "RR" (C{str}).

@var INF:    Infinity (C{float}), see C{isinf}, C{isfinite}.
@var MANTIS: System's M{mantissa bits} ≈53 (C{int}).
@var MAX:    System's M{float max} ≈1.798e+308 (C{float}).
@var MIN:    System's M{float min} ≈2.225e-308 (C{float}).
@var NAN:    Not-A-Number (C{float}), see C{isnan}.
@var NEG0:   Negative 0.0 (C{float}), see C{isneg0}.

@var OK:   Unique OK object (C{str}).

@var PI:   Constant M{math.pi} (C{float}).
@var PI2:  Two PI, M{math.pi * 2} (C{float}).
@var PI_2: Half PI, M{math.pi / 2} (C{float}).
@var PI_4: Quarter PI, M{PI / 4} (C{float}).

@var R_M:  Mean (spherical) earth radius (C{meter}).
@var R_MA: Major (equatorial) earth radius (C{meter}) WGS84, EPSG:3785.
@var R_MB: Minor (polar) earth radius (C{meter}) WGS84, EPSG:3785.
@var R_KM: Mean (spherical) earth radius (C{km}, kilometer).
@var R_NM: Mean (spherical) earth radius (C{NM}, nautical miles).
@var R_SM: Mean (spherical) earth radius (C{SM}, statute miles).
@var R_FM: Former FAI Sphere earth radius (C{meter}).
@var R_VM: Aviation/Navigation earth radius (C{meter}).

@var S_DEG: Degrees symbol "°" (C{str}).
@var S_MIN: Minutes symbol "′" (C{str}).
@var S_SEC: Seconds symbol "″" (C{str}).
@var S_RAD: Radians symbol "" (C{str}).
@var S_SEP: Separator between deg°, min′ and sec″ "" (C{str}).

@var Conics:     Registered conics (C{enum-like}).
@var Datums:     Registered datums (C{enum-like}).
@var Ellipsoids: Registered ellipsoids (C{enum-like}).
@var Transforms: Registered transforms (C{enum-like}).

@var pygeodesy_abspath: Fully qualified C{pygeodesy} directory name (C{str}).

@var version: Normalized C{PyGeodesy} version (C{str}).

'''

from os.path import abspath, basename, dirname
import sys

_init_abspath     = abspath(__file__)
pygeodesy_abspath = dirname(_init_abspath)
# <http://PyInstaller.ReadTheDocs.io/en/stable/runtime-information.html>
_isfrozen   = getattr(sys, 'frozen', False)
__version__ = '19.06.18'
# see setup.py for similar logic
version = '.'.join(map(str, map(int, __version__.split('.'))))

# setting __path__ should make ...
__path__ = [pygeodesy_abspath]
try:  # ... this import work, ...
    import bases as _  # PYCHOK expected
    del _
except ImportError:  # ... if it doesn't, extend
    # sys.path to include this very directory such
    # that all public and private sub-modules can
    # be imported (and checked by PyChecker, etc.)
    sys.path.insert(0, pygeodesy_abspath)  # XXX __path__[0]
del sys

try:  # MCCABE 13
    # lazily requires Python 3.7+, see lazily.__doc__
    from lazily import LazyImportError, _lazy_import2
    _, __getattr__ = _lazy_import2('pygeodesy')
except (LazyImportError, NotImplementedError):

    # keep ellipsoidal, spherical and vector modules as sub-modules
    import ellipsoidalKarney  # PYCHOK false
    import ellipsoidalNvector  # PYCHOK false
    import ellipsoidalVincenty  # PYCHOK false
    import epsg
    import gars
    import geohash
    import nvector  # PYCHOK false
    import sphericalNvector  # PYCHOK false
    import sphericalTrigonometry  # PYCHOK false
    import vector3d  # PYCHOK false
    import wgrs

    CrossError    = vector3d.CrossError
    crosserrors   = vector3d.crosserrors
    Epsg          = epsg.Epsg
    EPSGError     = epsg.EPSGError
    Garef         = gars.Garef
    Geohash       = geohash.Geohash
    Georef        = wgrs.Georef
    VincentyError = ellipsoidalVincenty.VincentyError

    # all public sub-modules, contants, classes and functions
    __all__ = ('bases', 'clipy', 'css', 'datum', 'dms', 'elevations',  # modules
               'ellipsoidalKarney', 'ellipsoidalNvector', 'ellipsoidalVincenty',
               'epsg', 'fmath', 'formy', 'gars', 'geohash', 'geoids', 'heights',
               'lazily', 'lcc', 'mgrs', 'nvector', 'osgr', 'points',
               'simplify', 'sphericalNvector', 'sphericalTrigonometry',
               'ups', 'utily', 'utm', 'utmups', 'vector3d', 'webmercator', 'wgrs',
               'CrossError', 'Epsg', 'EPSGError',  # classes
               'Garef', 'Geohash', 'Georef', 'VincentyError',
               'R_M',  # to avoid duplicates from .datum.py and .utily.py
               'pygeodesy_abspath',
               'version',
               'crosserrors')  # extended below

    # lift all public classes, constants, functions, etc. but
    # only from the following sub-modules ... (see also David
    # Beazley's <http://DaBeaz.com/modulepackage/index.html>)
    from bases       import *  # PYCHOK __all__
    from clipy       import *  # PYCHOK __all__
    from css         import *  # PYCHOK __all__
    from datum       import *  # PYCHOK __all__
    from dms         import *  # PYCHOK __all__
    from elevations  import *  # PYCHOK __all__
    from fmath       import *  # PYCHOK __all__
    from formy       import *  # PYCHOK __all__
    from geoids      import *  # PYCHOK __all__
    from heights     import *  # PYCHOK __all__
    from lazily      import *  # PYCHOK __all__
    from lcc         import *  # PYCHOK __all__
    from mgrs        import *  # PYCHOK __all__
    from osgr        import *  # PYCHOK __all__
    from points      import *  # PYCHOK __all__
    from simplify    import *  # PYCHOK __all__
    from ups         import *  # PYCHOK __all__
    from utily       import *  # PYCHOK __all__
    from utm         import *  # PYCHOK __all__
    from utmups      import *  # PYCHOK __all__
    from webmercator import *  # PYCHOK __all__

    import bases        # PYCHOK expected
    import clipy        # PYCHOK expected
    import css          # PYCHOK expected
    import datum        # PYCHOK expected
    import dms          # PYCHOK expected
    import elevations   # PYCHOK expected
    import fmath        # PYCHOK expected
    import formy        # PYCHOK expected
    import geoids       # PYCHOK expected
    import heights      # PYCHOK expected
    import lazily       # PYCHOK expected
    import lcc          # PYCHOK expected
    import mgrs         # PYCHOK expected
    import osgr         # PYCHOK expected
    import points       # PYCHOK expected
    import simplify     # PYCHOK expected
    import ups          # PYCHOK expected
    import utily        # PYCHOK expected
    import utm          # PYCHOK expected
    import utmups       # PYCHOK expected
    import webmercator  # PYCHOK expected

    # for backward compatibility with previous, DEPRECATED names
    def areaof(*args, **kwds):
        '''DEPRECATED, use function C{areaOf}.
        '''
        return points.areaOf(*args, **kwds)

    def bounds(*args, **kwds):
        '''DEPRECATED, use function C{boundsOf}.
        '''
        return points.boundsOf(*args, **kwds)

    def decodeEPSG2(arg):
        '''DEPRECATED, use function L{epsg.decode2}.
        '''
        return epsg.decode2(arg)

    def encodeEPSG(zone, hemipole='', band=''):
        '''DEPRECATED, use function L{epsg.encode}.
        '''
        return int(epsg.encode(zone, hemipole=hemipole, band=band))

    def isenclosedby(*args, **kwds):
        '''DEPRECATED, use function C{isenclosedBy}.
        '''
        return points.isenclosedBy(*args, **kwds)

    def perimeterof(*args, **kwds):
        '''DEPRECATED, use function C{perimeterOf}.
        '''
        return points.perimeterOf(*args, **kwds)

    __all__ += ('areaof', 'bounds', 'decodeEPSG2', 'encodeEPSG',
                'isenclosedby', 'perimeterof')  # DECPRECATED

    def _ismodule(m):
        p = abspath(m.__file__)  # PYCHOK undefined?
        if dirname(p) != pygeodesy_abspath:  # PYCHOK undefined?
            raise ImportError('foreign module %r from %r' % (m.__name__, p))

    # check that all modules are from this very package, pygeodesy
    # (only check when package is not bundled with PyInstaller or
    # Py2Exe, since the file-layout is different.  Courtesy of
    # GilderGeek <http://GitHub.com/mrJean1/PyGeodesy/issues/31>)
    if not _isfrozen:
        for m in (ellipsoidalKarney, ellipsoidalNvector, ellipsoidalVincenty,
                  epsg, gars, geohash, nvector,
                  sphericalNvector, sphericalTrigonometry,
                  vector3d, wgrs):
            _ismodule(m)

    # concat __all__ with the public classes, constants,
    # functions, etc. from the sub-modules mentioned above
    for m in (bases, clipy, css, datum, dms, elevations,
              fmath, formy, geoids, heights, lazily, lcc, mgrs,
              osgr, points, simplify, ups, utily, utm, utmups,
              webmercator):
        __all__ += m.__all__
        # GilderGeek <http://GitHub.com/mrJean1/PyGeodesy/issues/31>)
        if not _isfrozen:
            _ismodule(m)

    # remove any duplicates, only R_M?
    __all__ = tuple(set(__all__))

    del _ismodule, m

if __name__ == '__main__':

    from lazily import _all_missing2, isLazy  # PYCHOK expected

    a = ['.%s=%r' % a for a in (('version',           version),
                                ('isLazy',            isLazy),
                                ('pygeodesy_abspath', pygeodesy_abspath))]
    print('%s%s' % (basename(pygeodesy_abspath), ', '.join(a)))
    # double check that __all__ and _all_imports match
    for a, m in _all_missing2(__all__):
        if m:
            print('missing in %s: %s' % (a, m))

# XXX del ellipsoidalBase, sphericalBase  # PYCHOK expected
del abspath, basename, dirname, _init_abspath, _lazy_import2

# **) MIT License
#
# Copyright (C) 2016-2019 -- mrJean1 at Gmail dot com
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
