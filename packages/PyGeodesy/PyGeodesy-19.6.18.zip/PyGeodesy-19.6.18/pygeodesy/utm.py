
# -*- coding: utf-8 -*-

u'''Universal Transverse Mercator (UTM) classes L{Utm} and L{UTMError}
and functions L{parseUTM5}, L{toUtm8} and L{utmZoneBand5}.

Pure Python implementation of UTM / WGS-84 conversion functions using
an ellipsoidal earth model, transcribed from JavaScript originals by
I{(C) Chris Veness 2011-2016} published under the same MIT Licence**, see
U{UTM<http://www.Movable-Type.co.UK/scripts/latlong-utm-mgrs.html>} and
U{Module utm<http://www.Movable-Type.co.UK/scripts/geodesy/docs/module-utm.html>}.

The U{UTM<http://WikiPedia.org/wiki/Universal_Transverse_Mercator_coordinate_system>}
system is a 2-dimensional Cartesian coordinate system providing another way
to identify locations on the surface of the earth.  UTM is a set of 60
transverse Mercator projections, normally based on the WGS-84 ellipsoid.
Within each zone, coordinates are represented as I{easting}s and I{northing}s,
measured in metres.

This module includes some of Charles Karney's U{'Transverse Mercator with an
accuracy of a few nanometers'<http://Arxiv.org/pdf/1002.1417v3.pdf>}, 2011
(building on Krüger's U{'Konforme Abbildung des Erdellipsoids in der Ebene'
<http://bib.GFZ-Potsdam.DE/pub/digi/krueger2.pdf>}, 1912) and C++ class
U{TransverseMercator
<http://GeographicLib.SourceForge.io/html/classGeographicLib_1_1TransverseMercator.html>}.

Some other references are U{Universal Transverse Mercator coordinate system
<http://WikiPedia.org/wiki/Universal_Transverse_Mercator_coordinate_system>},
U{Transverse Mercator Projection<http://GeographicLib.SourceForge.io/tm.html>}
and Henrik Seidel U{'Die Mathematik der Gauß-Krueger-Abbildung'
<http://Henrik-Seidel.GMXhome.DE/gausskrueger.pdf>}, 2006.

@newfield example: Example, Examples
'''

from bases import _Based, _xattrs, _xnamed
from datum import Datums
from dms import degDMS, parseDMS2, _parseUTMUPS, RangeError
from ellipsoidalBase import LatLonEllipsoidalBase as _LLEB, \
                            _hemi, _to4lldn, _to3zBhp, _to3zll, \
                            _UTM_LAT_MAX, _UTM_LAT_MIN, \
                            _UTM_ZONE_MIN, _UTM_ZONE_MAX, \
                            _UTM_ZONE_OFF_MAX
from fmath import EPS, fdot3, fStr, Fsum, hypot, hypot1, len2, map2
from lazily import _ALL_LAZY
from utily import degrees90, degrees180, property_RO, sincos2  # splice

from math import asinh, atan, atanh, atan2, cos, cosh, \
                 degrees, radians, sin, sinh, tan, tanh
from operator import mul

# all public contants, classes and functions
__all__ = _ALL_LAZY.utm
__version__ = '19.04.24'

# Latitude bands C..X of 8° each, covering 80°S to 84°N with X repeated
# for 80-84°N
_Bands         = 'CDEFGHJKLMNPQRSTUVWXX'  #: (INTERNAL) Latitude bands.
_FalseEasting  =   500e3  #: (INTERNAL) False (C{meter}).
_FalseNorthing = 10000e3  #: (INTERNAL) False (C{meter}).
_K0            = 0.9996   #: (INTERNAL) UTM scale central meridian.


class UTMError(ValueError):
    '''UTM parse or other error.
    '''
    pass


class _Kseries(object):
    '''(INTERNAL) Alpha or Beta Krüger series.

       Krüger series summations for I{eta}, I{ksi}, I{p} and I{q},
       caching the C{cos}, C{cosh}, C{sin} and C{sinh} values for
       the given I{eta} and I{ksi} angles (in C{radians}).
    '''
    def __init__(self, AB, x, y):
        '''(INTERNAL) New Alpha or Beta Krüger series

           @param AB: Krüger Alpha or Beta series coefficients
                      (C{4-, 6- or 8-tuple}).
           @param x: Eta angle (C{radians}).
           @param y: Ksi angle (C{radians}).
        '''
        n, j2 = len2(range(2, len(AB) * 2 + 1, 2))

        self._ab = AB
        self._pq = map2(mul, j2, self._ab)
#       assert len(self._ab) == len(self._pq) == n

        x2 = map2(mul, j2, (x,) * n)
        self._chx = map2(cosh, x2)
        self._shx = map2(sinh, x2)
#       assert len(x2) == len(self._chx) == len(self._shx) == n

        y2 = map2(mul, j2, (y,) * n)
        self._cy = map2(cos, y2)
        self._sy = map2(sin, y2)
        # self._sy, self._cy = splice(sincos2(*y2))  # PYCHOK false
#       assert len(y2) == len(self._cy) == len(self._sy) == n

    def xs(self, x0):
        '''(INTERNAL) Eta summation (C{float}).
        '''
        return fdot3(self._ab, self._cy, self._shx, start=x0)

    def ys(self, y0):
        '''(INTERNAL) Ksi summation (C{float}).
        '''
        return fdot3(self._ab, self._sy, self._chx, start=y0)

    def ps(self, p0):
        '''(INTERNAL) P summation (C{float}).
        '''
        return fdot3(self._pq, self._cy, self._chx, start=p0)

    def qs(self, q0):
        '''(INTERNAL) Q summation (C{float}).
        '''
        return fdot3(self._pq, self._sy, self._shx, start=q0)


def _cmlon(zone):
    '''(INTERNAL) Central meridian longitude (C{degrees180}).
    '''
    return (zone * 6) - 183


def _to3zBlat(zone, band, mgrs=False):  # imported by .mgrs.Mgrs
    '''(INTERNAL) Check and return zone, Band and band latitude.

       @param zone: Zone number or string.
       @param band: Band letter.
       @param mgrs: Optionally, raise UTMError (C{bool}).

       @return: 3-Tuple (zone, Band, latitude).
    '''
    try:
        z, B, _ = _to3zBhp(zone, band=band)  # in .ellipsoidalBase
        if _UTM_ZONE_MIN > z or z > _UTM_ZONE_MAX:
            raise ValueError
    except ValueError:
        raise UTMError('%s invalid: %r' % ('zone', zone))

    b = None
    if B:
        b = _Bands.find(B)
        if b < 0:
            raise UTMError('%s invalid: %r' % ('band', band or B))
        b = (b << 3) - 80
    elif mgrs:
        raise UTMError('%s missing: %r' % ('band', band))

    return z, B, b


def _to3zBll(lat, lon, cmoff=True):
    '''(INTERNAL) Return zone, Band and lat- and (central) longitude in degrees.

       @param lat: Latitude (C{degrees}).
       @param lon: Longitude (C{degrees}).
       @keyword cmoff: Offset I{lon} from zone's central meridian.

       @return: 4-Tuple (zone, Band, lat, lon).
    '''
    z, lat, lon = _to3zll(lat, lon)  # in .ellipsoidalBase

    if _UTM_LAT_MIN > lat or lat >= _UTM_LAT_MAX:  # [-80, 84)
        x = '%s [%s, %s)' % ('range', _UTM_LAT_MIN, _UTM_LAT_MAX)
        raise RangeError('%s outside UTM %s: %s' % ('lat', x, degDMS(lat)))
    B = _Bands[int(lat + 80) >> 3]

    x = lon - _cmlon(z)  # z before Norway/Svaldbard
    if abs(x) > _UTM_ZONE_OFF_MAX:
        x = '%s %d by %s' % ('zone', z, degDMS(x, prec=6))
        raise RangeError('%s outside UTM %s: %s' % ('lon', x, degDMS(lon)))

    if B == 'X':  # and 0 <= int(lon) < 42: z = int(lon + 183) // 6 + 1
        x = {32: 9, 34: 21, 36: 33}.get(z, None)
        if x:  # Svalbard
            z += 1 if lon >= x else -1
    elif B == 'V' and z == 31 and lon >= 3:
        z += 1  # SouthWestern Norway

    if cmoff:  # lon off central meridian
        lon -= _cmlon(z)  # z after Norway/Svaldbard
    return z, B, lat, lon


class Utm(_Based):
    '''Universal Transverse Mercator (UTM) coordinate.
    '''
    _band        = ''    #: (INTERNAL) Latitude band letter ('C..X').
    _convergence = None  #: (INTERNAL) Meridian conversion (C{degrees}).
    _datum       = Datums.WGS84  #: (INTERNAL) L{Datum}.
    _easting     = 0     #: (INTERNAL) Easting from false easting (C{meter}).
    _epsg        = None  #: (INTERNAL) toEpsg cache (L{Epsg}).
    _falsed      = True  #: (INTERNAL) Falsed easting and northing (C{bool}).
    _hemisphere  = ''    #: (INTERNAL) Hemisphere ('N' or 'S').
    # _latlon also set by ellipsoidalBase.LatLonEllipsoidalBase.toUtm
    _latlon      = None  #: (INTERNAL) toLatLon cache (C{LatLon}).
    _latlon_eps  = EPS   #: (INTERNAL) eps from _latlon (C{float}).
    _mgrs        = None  #: (INTERNAL) toMgrs cache (L{Mgrs}).
    _northing    = 0     #: (INTERNAL) Northing from false northing (C{meter}).
    _scale       = None  #: (INTERNAL) Grid scale factor (C{scalar}) or C{None}.
    _ups         = None  #: (INTERNAL) toUps cache (L{Ups}).
    _utm         = None  #: (INTERNAL) toUtm cache (L{Utm}).
    _zone        = 0     #: (INTERNAL) Longitudinal zone, zero always.

    def __init__(self, zone, hemisphere, easting, northing, band='',  # PYCHOK expected
                             datum=Datums.WGS84, falsed=True,
                             convergence=None, scale=None, name=''):
        '''New UTM coordinate.

           @param zone: Longitudinal UTM zone (C{int}, 1..60) or zone
                        with/-out (latitudinal) Band letter (C{str},
                        '01C'..'60X').
           @param hemisphere: Northern or southern hemisphere (C{str},
                              C{'N[orth]'} or C{'S[outh]'}).
           @param easting: Easting from false easting (C{meter}, -500km
                           from central meridian).
           @param northing: Northing from equator (C{meter}, N or from
                            false northing -10,000km S).
           @keyword band: Optional, (latitudinal) band (C{str}, 'C'..'X').
           @keyword datum: Optional, this coordinate's datum (L{Datum}).
           @keyword falsed: Both I{easting} and I{northing} are falsed (C{str}).
           @keyword convergence: Optional meridian convergence, bearing
                                 off grid North, clockwise from true
                                 North (C{degrees}) or C{None}.
           @keyword scale: Optional grid scale factor (C{scalar}) or C{None}.
           @keyword name: Optional name (C{str}).

           @raise RangeError: If I{easting} or I{northing} outside the
                              valid UTM range.

           @raise UTMError: Invalid I{zone}, I{hemishere} or I{band}.

           @example:

           >>> import pygeodesy
           >>> u = pygeodesy.Utm(31, 'N', 448251, 5411932)
        '''
        if name:
            self.name = name

        self._zone, B, _ = _to3zBlat(zone, band)

        h = str(hemisphere)[:1].upper()
        if h not in ('N', 'S'):
            raise UTMError('%s invalid: %r' % ('hemisphere', hemisphere))

        e, n = float(easting), float(northing)
        if not falsed:
            e += _FalseEasting  # relative to central meridian
            if h == 'S':  # relative to equator
                n += _FalseNorthing
        # check easting/northing (with 40km overlap
        # between zones) - is this worthwhile?
        if 120e3 > e or e > 880e3:
            raise RangeError('%s invalid: %r' % ('easting', easting))
        if 0 > n or n > _FalseNorthing:
            raise RangeError('%s invalid: %r' % ('northing', northing))

        self._band        = B
        self._convergence = convergence
        self._datum       = datum
        self._easting     = e
        self._hemisphere  = h
        self._northing    = n
        self._scale       = scale

    def __repr__(self):
        return self.toStr2(B=True)

    def __str__(self):
        return self.toStr()

    def _xcopy(self, *attrs):
        '''(INTERNAL) Make copy with add'l, subclass attributes.
        '''
        return _xattrs(self.classof(self.zone, self.hemisphere,
                                    self.easting, self.northing,
                                    band=self.band, datum=self.datum),
                       self, *attrs)

    @property_RO
    def band(self):
        '''Get the (latitudinal) band (C{str}, 'C'..'X' or '').
        '''
        return self._band

    @property_RO
    def convergence(self):
        '''Get the meridian convergence (C{degrees}) or C{None}.
        '''
        return self._convergence

    def copy(self):
        '''Copy this UTM coordinate.

           @return: The copy (L{Utm} or subclass thereof).
        '''
        return self._xcopy()

    @property_RO
    def datum(self):
        '''Get the datum (L{Datum}).
        '''
        return self._datum

    @property_RO
    def easting(self):
        '''Get the easting (C{meter}).
        '''
        return self._easting

    @property_RO
    def falsed(self):
        '''Get the easting and northing falsing (C{bool}).
        '''
        return self._falsed

    @property_RO
    def hemisphere(self):
        '''Get the hemisphere (C{str}, 'N'|'S').
        '''
        return self._hemisphere

    @property_RO
    def northing(self):
        '''Get the northing (C{meter}).
        '''
        return self._northing

    def parseUTM(self, strUTM):
        '''Parse a string to a UTM coordinate.

           @return: The coordinate (L{Utm}).

           @see: Function L{parseUTM5} in this module L{utm}.
        '''
        return parseUTM5(strUTM, datum=self.datum, Utm=self.classof)

    @property_RO
    def scale(self):
        '''Get the grid scale (C{scalar}) or C{None}.
        '''
        return self._scale

    def toEpsg(self):
        '''Determine the I{EPSG (European Petroleum Survey Group)} code.

           @return: C{EPSG} code (C{int}).

           @raise EPSGError: See L{Epsg}.
        '''
        if self._epsg is None:
            from epsg import Epsg  # PYCHOK circular import
            self._epsg = Epsg(self)
        return self._epsg

    def toLatLon(self, LatLon=None, eps=EPS, unfalse=True):
        '''Convert this UTM coordinate to an (ellipsoidal) geodetic point.

           @keyword LatLon: Optional, ellipsoidal (sub-)class to return
                            the point (C{LatLon}) or C{None}.
           @keyword eps: Optional convergence limit, L{EPS} or above
                         (C{float}).
           @keyword unfalse: Unfalse I{easting} and I{northing} if falsed
                             (C{bool}).

           @return: This UTM coordinate as (I{LatLon}) or 5-tuple
                    (lat, lon, datum, convergence, scale) if I{LatLon}
                    is C{None}.

           @raise TypeError: If I{LatLon} is not ellipsoidal.

           @raise UTMError: Invalid meridional radius or H-value.

           @example:

           >>> u = Utm(31, 'N', 448251.795, 5411932.678)
           >>> from pygeodesy import ellipsoidalVincenty as eV
           >>> ll = u.toLatLon(eV.LatLon)  # 48°51′29.52″N, 002°17′40.20″E
        '''
        if eps < EPS:
            eps = EPS  # less doesn't converge

        if self._latlon and self._latlon_eps == eps:
            return self._latlon5(LatLon)

        E = self._datum.ellipsoid  # XXX vs LatLon.datum.ellipsoid

        x = self._easting
        y = self._northing
        if unfalse and self._falsed:
            x -= _FalseEasting  # relative to central meridian
            if self._hemisphere == 'S':  # relative to equator
                y -= _FalseNorthing

        # from Karney 2011 Eq 15-22, 36
        A0 = _K0 * E.A
        if A0 < EPS:
            raise UTMError('%s invalid: %r' % ('meridional', E.A))
        x /= A0  # η eta
        y /= A0  # ξ ksi

        Ks = _Kseries(E.BetaKs, x, y)  # Krüger series
        y = -Ks.ys(-y)  # ξ'
        x = -Ks.xs(-x)  # η'

        shx = sinh(x)
        sy, cy = sincos2(y)

        H = hypot(shx, cy)
        if H < EPS:
            raise UTMError('%s invalid: %r' % ('H', H))

        d = 1.0 + eps
        q = 1.0 / E.e12
        T = t0 = sy / H  # τʹ
        sd = Fsum(T)
        while abs(d) > eps:
            h = hypot1(T)
            s = sinh(E.e * atanh(E.e * T / h))
            t = T * hypot1(s) - s * h
            d = (t0 - t) / hypot1(t) * ((q + T**2) / h)
            T, d = sd.fsum2_(d)  # τi, (τi - τi-1)

        a = atan(T)  # lat
        b = atan2(shx, cy) + radians(_cmlon(self._zone))
        ll = _LLEB(degrees90(a), degrees180(b), datum=self._datum, name=self.name)

        # convergence: Karney 2011 Eq 26, 27
        p = -Ks.ps(-1)
        q =  Ks.qs(0)
        ll._convergence = degrees(atan(tan(y) * tanh(x)) + atan2(q, p))

        # scale: Karney 2011 Eq 28
        ll._scale = E.e2s(sin(a)) * hypot1(T) * H * (A0 / E.a / hypot(p, q))

        self._latlon, self._latlon_eps = ll, eps
        return self._latlon5(LatLon)

    def _latlon5(self, LatLon):
        '''(INTERNAL) Convert cached LatLon
        '''
        ll = self._latlon
        if LatLon is None:
            return ll.lat, ll.lon, ll.datum, ll.convergence, ll.scale
        elif issubclass(LatLon, _LLEB):
            return _xnamed(_xattrs(LatLon(ll.lat, ll.lon, datum=ll.datum),
                                   ll, '_convergence', '_scale'), ll.name)
        raise TypeError('%s not ellipsoidal: %r' % ('LatLon', LatLon))

    def toMgrs(self):
        '''Convert this UTM coordinate to an MGRS grid reference.

           See function L{toMgrs} in module L{mgrs} for more details.

           @return: The MGRS grid reference (L{Mgrs}).
        '''
        if self._mgrs is None:
            from mgrs import toMgrs  # PYCHOK recursive import
            self._mgrs = toMgrs(self, name=self.name)
        return self._mgrs

    def toStr(self, prec=0, sep=' ', B=False, cs=False):  # PYCHOK expected
        '''Return a string representation of this UTM coordinate.

           To distinguish from MGRS grid zone designators, a
           space is left between the zone and the hemisphere.

           Note that UTM coordinates are rounded, not truncated
           (unlike MGRS grid references).

           @keyword prec: Optional number of decimals, unstripped (C{int}).
           @keyword sep: Optional separator to join (C{str}).
           @keyword B: Optionally, include latitudinal band (C{bool}).
           @keyword cs: Optionally, include meridian convergence and
                        grid scale factor (C{bool}).

           @return: This UTM as a string with I{zone[band], hemisphere,
                    easting, northing, [convergence, scale]} in
                    C{"00 N|S meter meter"} plus C{" degrees float"} if
                    I{cs} is C{True} (C{str}).

           @example:

           >>> u = Utm(3, 'N', 448251, 5411932.0001)
           >>> u.toStr(4)  # 03 N 448251.0 5411932.0001
           >>> u.toStr(sep=', ')  # 03 N, 448251, 5411932
        '''
        z = '%02d%s' % (self.zone, self.band if B else '')
        t = (z, self.hemisphere, fStr(self.easting,  prec=prec),
                                 fStr(self.northing, prec=prec))
        if cs:
            t += ('n/a' if self.convergence is None else
                    degDMS(self.convergence, prec=8, pos='+'),
                  'n/a' if self.scale is None else
                      fStr(self.scale, prec=8))
        return sep.join(t)

    def toStr2(self, prec=0, fmt='[%s]', sep=', ', B=False, cs=False):  # PYCHOK expected
        '''Return a string representation of this UTM coordinate.

           Note that UTM coordinates are rounded, not truncated
           (unlike MGRS grid references).

           @keyword prec: Optional number of decimals, unstripped (C{int}).
           @keyword fmt: Optional, enclosing backets format (C{str}).
           @keyword sep: Optional separator between name:value pairs (C{str}).
           @keyword B: Optionally, include latitudinal band (C{bool}).
           @keyword cs: Optionally, include meridian convergence and
                        grid scale factor (C{bool}).

           @return: This UTM as a string C{"[Z:09[band], H:N|S, E:meter,
                    N:meter]"} plus C{", C:degrees, S:float"} if I{cs} is
                    C{True} (C{str}).
        '''
        t = self.toStr(prec=prec, sep=' ', B=B, cs=cs).split()
        return fmt % (sep.join('%s:%s' % t for t in zip('ZHENCS', t)),)

    def toUps(self, pole='', eps=EPS, **unused):
        '''Convert this UTM coordinate to a UPS coordinate.

           @keyword pole: Optional top/center of the UPS projection,
                          (C{str}, 'N[orth]'|'S[outh]').
           @keyword eps: Optional convergence limit, L{EPS} or above
                         (C{float}), see method L{Utm.toLatLon}.

           @return: The UPS coordinate (L{Ups}).
        '''
        u = self._ups
        if u is None or u.pole != (pole or u.pole):
            from ups import toUps8  # PYCHOK recursive import
            ll = self.toLatLon(LatLon=_LLEB, eps=eps)
            self._ups = u = toUps8(ll, pole=pole, strict=False)
        return u

    def toUtm(self, zone, eps=EPS, **unused):
        '''Convert this UTM coordinate to a different one.

           @param zone: New UTM zone (C{int}).
           @keyword eps: Optional convergence limit, L{EPS} or above
                         (C{float}), see method L{Utm.toLatLon}.

           @return: The UTM coordinate (L{Utm}).
        '''
        if zone == self.zone:
            return self.copy()
        elif zone:
            u = self._utm
            if u is None or u.zone != zone:
                ll = self.toLatLon(LatLon=_LLEB, eps=eps)
                self._utm = u = toUtm8(ll, name=self.name, zone=zone)
            return u
        raise UTMError('%s invalid: %r' % ('zone', zone))

    @property_RO
    def zone(self):
        '''Get the (longitudinal) zone (C{int}, 1..60).
        '''
        return self._zone


def parseUTM(strUTM, datum=Datums.WGS84, Utm=Utm, name=''):
    '''DEPRECATED, use function L{parseUTM5}.

       @return: The UTM coordinate (L{Utm}) or 4-tuple (C{zone,
                hemisphere, easting, northing}) if I{Utm} is C{None}.
    '''
    r = parseUTM5(strUTM, datum=datum, Utm=Utm, name=name)
    if isinstance(r, tuple):
        r = r[:4]  # remove band
    return r


def parseUTM5(strUTM, datum=Datums.WGS84, Utm=Utm, name=''):
    '''Parse a string representing a UTM coordinate, consisting
       of I{"zone[band] hemisphere easting northing"}.

       @param strUTM: A UTM coordinate (C{str}).
       @keyword datum: Optional datum to use (L{Datum}).
       @keyword Utm: Optional (sub-)class to return the UTM
                     coordinate (L{Utm}) or C{None}.
       @keyword name: Optional I{Utm} name (C{str}).

       @return: The UTM coordinate (L{Utm}) or 5-tuple (C{zone,
                hemisphere, easting, northing, band}) if I{Utm}
                is C{None}.

       @raise UTMError: Invalid I{strUTM}.

       @example:

       >>> u = parseUTM('31 N 448251 5411932')
       >>> u.toStr2()  # [Z:31, H:N, E:448251, N:5411932]
       >>> u = parseUTM('31 N 448251.8 5411932.7')
       >>> u.toStr()  # 31 N 448252 5411933
    '''
    try:
        z, h, e, n, B = _parseUTMUPS(strUTM)
        if _UTM_ZONE_MIN > z or z > _UTM_ZONE_MAX \
                             or (B and B not in _Bands):
            raise ValueError
    except ValueError:
        raise UTMError('%s invalid: %r' % ('strUTM', strUTM))

    return (z, h, e, n, B) if Utm is None else _xnamed(Utm(
            z, h, e, n, band=B, datum=datum), name)


def toUtm(latlon, lon=None, datum=None, Utm=Utm, name='', cmoff=True):
    '''DEPRECATED, use function L{toUtm8}.

       @return: The UTM coordinate (L{Utm}) or a 6-tuple (zone,
                easting, northing, band, convergence, scale) if
                I{Utm} is C{None} or I{cmoff} is C{False}.
    '''
    r = toUtm8(latlon, lon=lon, datum=datum, Utm=Utm, name=name, cmoff=cmoff)
    if isinstance(r, tuple):
        # remove hemisphere and datum
        z, _, x, y, B, _, c, s = r
        r = z, x, y, B, c, s
    return r


def toUtm8(latlon, lon=None, datum=None, Utm=Utm, cmoff=True, name='', zone=None):
    '''Convert a lat-/longitude point to a UTM coordinate.

       @param latlon: Latitude (C{degrees}) or an (ellipsoidal)
                      geodetic C{LatLon} point.
       @keyword lon: Optional longitude (C{degrees}) or C{None}.
       @keyword datum: Optional datum for this UTM coordinate,
                       overriding I{latlon}'s datum (C{Datum}).
       @keyword Utm: Optional (sub-)class to return the UTM
                     coordinate (L{Utm}) or C{None}.
       @keyword cmoff: Offset longitude from zone's central meridian,
                       apply false easting and false northing (C{bool}).
       @keyword name: Optional I{Utm} name (C{str}).
       @keyword zone: Optional zone to enforce (C{int} or C{str}).

       @return: The UTM coordinate (L{Utm}) or a 8-tuple (C{zone, hemisphere,
                easting, northing, band, datum, convergence, scale}) if
                I{Utm} is C{None} or I{cmoff} is C{False}.

       @raise TypeError: If I{latlon} is not ellipsoidal.

       @raise RangeError: If I{lat} outside the valid UTM bands or if
                          I{lat} or I{lon} outside the valid range and
                          I{rangerrrors} set to C{True}.

       @raise UTMError: Invlid I{zone}.

       @raise ValueError: If I{lon} value is missing or if I{latlon}
                          is invalid.

       @note: Implements Karney’s method, using 8-th order Krüger series,
              giving results accurate to 5 nm (or better) for distances
              up to 3900 km from the central meridian.

       @example:

       >>> p = LatLon(48.8582, 2.2945)  # 31 N 448251.8 5411932.7
       >>> u = toUtm(p)  # 31 N 448252 5411933
       >>> p = LatLon(13.4125, 103.8667) # 48 N 377302.4 1483034.8
       >>> u = toUtm(p)  # 48 N 377302 1483035
    '''
    lat, lon, d, name = _to4lldn(latlon, lon, datum, name)
    z, B, lat, lon = _to3zBll(lat, lon, cmoff=cmoff)
    if zone:  # re-zone for UTM
        r, _, _ = _to3zBhp(zone, band=B)
        if r != z:
            if not _UTM_ZONE_MIN <= r <= _UTM_ZONE_MAX:
                raise UTMError('%s invalid: %r' % ('zone', zone))
            if cmoff:  # re-offset from central meridian
                lon += _cmlon(z) - _cmlon(r)
            z = r

    E = d.ellipsoid

    a, b = radians(lat), radians(lon)
    # easting, northing: Karney 2011 Eq 7-14, 29, 35
    sb, cb = sincos2(b)

    T = tan(a)
    T12 = hypot1(T)
    S = sinh(E.e * atanh(E.e * T / T12))

    T_ = T * hypot1(S) - S * T12
    H = hypot(T_, cb)

    y = atan2(T_, cb)  # ξ' ksi
    x = asinh(sb / H)  # η' eta

    A0 = _K0 * E.A

    Ks = _Kseries(E.AlphaKs, x, y)  # Krüger series
    y = Ks.ys(y) * A0  # ξ
    x = Ks.xs(x) * A0  # η

    if cmoff:
        # Charles Karney, "Test data for the transverse Mercator projection (2009)"
        # <http://GeographicLib.SourceForge.io/html/transversemercator.html>
        # and <http://Zenodo.org/record/32470#.W4LEJS2ZON8>
        x += _FalseEasting  # make x relative to false easting
        if y < 0:
            y += _FalseNorthing  # y relative to false northing in S

    # convergence: Karney 2011 Eq 23, 24
    p_ = Ks.ps(1)
    q_ = Ks.qs(0)
    c = degrees(atan(T_ / hypot1(T_) * tan(b)) + atan2(q_, p_))

    # scale: Karney 2011 Eq 25
    s = E.e2s(sin(a)) * T12 / H * (A0 / E.a * hypot(p_, q_))

    h = _hemi(a)
    if Utm is None or not cmoff:
        r = z, h, x, y, B, d, c, s
    else:
        r = _xnamed(Utm(z, h, x, y, band=B, datum=d,
                                    convergence=c, scale=s), name)
    return r


def utmZoneBand2(lat, lon):
    '''DEPRECATED, use function L{utmZoneBand5}.
    '''
    return utmZoneBand5(lat, lon)[:2]


def utmZoneBand5(lat, lon, cmoff=False):
    '''Return the UTM zone number, Band letter, hemisphere and
       clipped lat- and longitude for a given location.

       @param lat: Latitude in degrees (C{scalar} or C{str}).
       @param lon: Longitude in degrees (C{scalar} or C{str}).
       @keyword cmoff: Offset longitude from zone's central meridian
                       (C{bool}).

       @return: 5-Tuple (C{zone, Band, hemisphere, lat, lon}) as
                (C{int, str, 'N'|'S', degrees90, degrees180}) where
                C{zone} is C{1..60} and C{Band} is C{'C'|'D'..'W'|'X'}
                for UTM.

       @raise RangeError: If I{lat} outside the valid UTM bands or if
                          I{lat} or I{lon} outside the valid range and
                          I{rangerrrors} set to C{True}.

       @raise ValueError: Invalid I{lat} or I{lon}.
    '''
    lat, lon = parseDMS2(lat, lon)
    z, B, lat, lon = _to3zBll(lat, lon, cmoff=cmoff)
    return z, B, _hemi(lat), lat, lon

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
