"""
numerictypes: Define the numeric type objects

This module is designed so "from numerictypes import \\*" is safe.
Exported symbols include:

  Dictionary with all registered number types (including aliases):
    typeDict

  Type objects (not all will be available, depends on platform):
      see variable sctypes for which ones you have

    Bit-width names

    int8 int16 int32 int64 int128
    uint8 uint16 uint32 uint64 uint128
    float16 float32 float64 float96 float128 float256
    complex32 complex64 complex128 complex192 complex256 complex512
    datetime64 timedelta64

    c-based names

    bool_

    object_

    void, str_, unicode_

    byte, ubyte,
    short, ushort
    intc, uintc,
    intp, uintp,
    int_, uint,
    longlong, ulonglong,

    single, csingle,
    float_, complex_,
    longfloat, clongfloat,

   As part of the type-hierarchy:    xx -- is bit-width

   generic
     +-> bool_                                  (kind=b)
     +-> number
     |   +-> integer
     |   |   +-> signedinteger     (intxx)      (kind=i)
     |   |   |     byte
     |   |   |     short
     |   |   |     intc
     |   |   |     intp            int0
     |   |   |     int_
     |   |   |     longlong
     |   |   \\-> unsignedinteger  (uintxx)     (kind=u)
     |   |         ubyte
     |   |         ushort
     |   |         uintc
     |   |         uintp           uint0
     |   |         uint_
     |   |         ulonglong
     |   +-> inexact
     |       +-> floating          (floatxx)    (kind=f)
     |       |     half
     |       |     single
     |       |     float_          (double)
     |       |     longfloat
     |       \\-> complexfloating  (complexxx)  (kind=c)
     |             csingle         (singlecomplex)
     |             complex_        (cfloat, cdouble)
     |             clongfloat      (longcomplex)
     +-> flexible
     |   +-> character
     |   |     str_     (string_, bytes_)       (kind=S)    [Python 2]
     |   |     unicode_                         (kind=U)    [Python 2]
     |   |
     |   |     bytes_   (string_)               (kind=S)    [Python 3]
     |   |     str_     (unicode_)              (kind=U)    [Python 3]
     |   |
     |   \\-> void                              (kind=V)
     \\-> object_ (not used much)               (kind=O)

"""
from __future__ import division, absolute_import, print_function

import types as _types
import sys
import numbers
import warnings

from numpy.compat import bytes, long
from numpy.core.multiarray import (
        typeinfo, ndarray, array, empty, dtype, datetime_data,
        datetime_as_string, busday_offset, busday_count, is_busday,
        busdaycalendar
        )
from numpy.core.overrides import set_module

# we add more at the bottom
__all__ = ['sctypeDict', 'sctypeNA', 'typeDict', 'typeNA', 'sctypes',
           'ScalarType', 'obj2sctype', 'cast', 'nbytes', 'sctype2char',
           'maximum_sctype', 'issctype', 'typecodes', 'find_common_type',
           'issubdtype', 'datetime_data', 'datetime_as_string',
           'busday_offset', 'busday_count', 'is_busday', 'busdaycalendar',
           ]

# we don't need all these imports, but we need to keep them for compatibility
# for users using np.core.numerictypes.UPPER_TABLE
from ._string_helpers import (
    english_lower, english_upper, english_capitalize, LOWER_TABLE, UPPER_TABLE
)

from ._type_aliases import (
    sctypeDict,
    sctypeNA,
    allTypes,
    bitname,
    sctypes,
    _concrete_types,
    _concrete_typeinfo,
    _bits_of,
)
from ._dtype import _kind_name

# we don't export these for import *, but we do want them accessible
# as numerictypes.bool, etc.
if sys.version_info[0] >= 3:
    from builtins import bool, int, float, complex, object, str
    unicode = str
else:
    from __builtin__ import bool, int, float, complex, object, unicode, str


# We use this later
generic = allTypes['generic']

genericTypeRank = ['bool', 'int8', 'uint8', 'int16', 'uint16',
                   'int32', 'uint32', 'int64', 'uint64', 'int128',
                   'uint128', 'float16',
                   'float32', 'float64', 'float80', 'float96', 'float128',
                   'float256',
                   'complex32', 'complex64', 'complex128', 'complex160',
                   'complex192', 'complex256', 'complex512', 'object']

def maximum_sctype(t):
    """
    Return the scalar type of highest precision of the same kind as the input.

    Parameters
    ----------
    t : dtype or dtype specifier
        The input data type. This can be a `dtype` object or an object that
        is convertible to a `dtype`.

    Returns
    -------
    out : dtype
        The highest precision data type of the same kind (`dtype.kind`) as `t`.

    See Also
    --------
    obj2sctype, mintypecode, sctype2char
    dtype

    Examples
    --------
    >>> np.maximum_sctype(int)
    <type 'numpy.int64'>
    >>> np.maximum_sctype(np.uint8)
    <type 'numpy.uint64'>
    >>> np.maximum_sctype(complex)
    <type 'numpy.complex192'>

    >>> np.maximum_sctype(str)
    <type 'numpy.string_'>

    >>> np.maximum_sctype('i2')
    <type 'numpy.int64'>
    >>> np.maximum_sctype('f4')
    <type 'numpy.float96'>

    """
    g = obj2sctype(t)
    if g is None:
        return t
    t = g
    base = _kind_name(dtype(t))
    if base in sctypes:
        return sctypes[base][-1]
    else:
        return t


@set_module('numpy')
def issctype(rep):
    """
    Determines whether the given object represents a scalar data-type.

    Parameters
    ----------
    rep : any
        If `rep` is an instance of a scalar dtype, True is returned. If not,
        False is returned.

    Returns
    -------
    out : bool
        Boolean result of check whether `rep` is a scalar dtype.

    See Also
    --------
    issubsctype, issubdtype, obj2sctype, sctype2char

    Examples
    --------
    >>> np.issctype(np.int32)
    True
    >>> np.issctype(list)
    False
    >>> np.issctype(1.1)
    False

    Strings are also a scalar type:

    >>> np.issctype(np.dtype('str'))
    True

    """
    if not isinstance(rep, (type, dtype)):
        return False
    try:
        res = obj2sctype(rep)
        if res and res != object_:
            return True
        return False
    except Exception:
        return False


@set_module('numpy')
def obj2sctype(rep, default=None):
    """
    Return the scalar dtype or NumPy equivalent of Python type of an object.

    Parameters
    ----------
    rep : any
        The object of which the type is returned.
    default : any, optional
        If given, this is returned for objects whose types can not be
        determined. If not given, None is returned for those objects.

    Returns
    -------
    dtype : dtype or Python type
        The data type of `rep`.

    See Also
    --------
    sctype2char, issctype, issubsctype, issubdtype, maximum_sctype

    Examples
    --------
    >>> np.obj2sctype(np.int32)
    <type 'numpy.int32'>
    >>> np.obj2sctype(np.array([1., 2.]))
    <type 'numpy.float64'>
    >>> np.obj2sctype(np.array([1.j]))
    <type 'numpy.complex128'>

    >>> np.obj2sctype(dict)
    <type 'numpy.object_'>
    >>> np.obj2sctype('string')
    <type 'numpy.string_'>

    >>> np.obj2sctype(1, default=list)
    <type 'list'>

    """
    # prevent abtract classes being upcast
    if isinstance(rep, type) and issubclass(rep, generic):
        return rep
    # extract dtype from arrays
    if isinstance(rep, ndarray):
        return rep.dtype.type
    # fall back on dtype to convert
    try:
        res = dtype(rep)
    except Exception:
        return default
    else:
        return res.type


@set_module('numpy')
def issubclass_(arg1, arg2):
    """
    Determine if a class is a subclass of a second class.

    `issubclass_` is equivalent to the Python built-in ``issubclass``,
    except that it returns False instead of raising a TypeError if one
    of the arguments is not a class.

    Parameters
    ----------
    arg1 : class
        Input class. True is returned if `arg1` is a subclass of `arg2`.
    arg2 : class or tuple of classes.
        Input class. If a tuple of classes, True is returned if `arg1` is a
        subclass of any of the tuple elements.

    Returns
    -------
    out : bool
        Whether `arg1` is a subclass of `arg2` or not.

    See Also
    --------
    issubsctype, issubdtype, issctype

    Examples
    --------
    >>> np.issubclass_(np.int32, int)
    True
    >>> np.issubclass_(np.int32, float)
    False

    """
    try:
        return issubclass(arg1, arg2)
    except TypeError:
        return False


@set_module('numpy')
def issubsctype(arg1, arg2):
    """
    Determine if the first argument is a subclass of the second argument.

    Parameters
    ----------
    arg1, arg2 : dtype or dtype specifier
        Data-types.

    Returns
    -------
    out : bool
        The result.

    See Also
    --------
    issctype, issubdtype,obj2sctype

    Examples
    --------
    >>> np.issubsctype('S8', str)
    True
    >>> np.issubsctype(np.array([1]), int)
    True
    >>> np.issubsctype(np.array([1]), float)
    False

    """
    return issubclass(obj2sctype(arg1), obj2sctype(arg2))


@set_module('numpy')
def issubdtype(arg1, arg2):
    """
    Returns True if first argument is a typecode lower/equal in type hierarchy.

    Parameters
    ----------
    arg1, arg2 : dtype_like
        dtype or string representing a typecode.

    Returns
    -------
    out : bool

    See Also
    --------
    issubsctype, issubclass_
    numpy.core.numerictypes : Overview of numpy type hierarchy.

    Examples
    --------
    >>> np.issubdtype('S1', np.string_)
    True
    >>> np.issubdtype(np.float64, np.float32)
    False

    """
    if not issubclass_(arg1, generic):
        arg1 = dtype(arg1).type
    if not issubclass_(arg2, generic):
        arg2_orig = arg2
        arg2 = dtype(arg2).type
        if not isinstance(arg2_orig, dtype):
            # weird deprecated behaviour, that tried to infer np.floating from
            # float, and similar less obvious things, such as np.generic from
            # basestring
            mro = arg2.mro()
            arg2 = mro[1] if len(mro) > 1 else mro[0]

            def type_repr(x):
                """ Helper to produce clear error messages """
                if not isinstance(x, type):
                    return repr(x)
                elif issubclass(x, generic):
                    return "np.{}".format(x.__name__)
                else:
                    return x.__name__

            # 1.14, 2017-08-01
            warnings.warn(
                "Conversion of the second argument of issubdtype from `{raw}` "
                "to `{abstract}` is deprecated. In future, it will be treated "
                "as `{concrete} == np.dtype({raw}).type`.".format(
                    raw=type_repr(arg2_orig),
                    abstract=type_repr(arg2),
                    concrete=type_repr(dtype(arg2_orig).type)
                ),
                FutureWarning, stacklevel=2
            )

    return issubclass(arg1, arg2)


# This dictionary allows look up based on any alias for an array data-type
class _typedict(dict):
    """
    Base object for a dictionary for look-up with any alias for an array dtype.

    Instances of `_typedict` can not be used as dictionaries directly,
    first they have to be populated.

    """

    def __getitem__(self, obj):
        return dict.__getitem__(self, obj2sctype(obj))

nbytes = _typedict()
_alignment = _typedict()
_maxvals = _typedict()
_minvals = _typedict()
def _construct_lookups():
    for name, info in _concrete_typeinfo.items():
        obj = info.type
        nbytes[obj] = info.bits // 8
        _alignment[obj] = info.alignment
        if len(info) > 5:
            _maxvals[obj] = info.max
            _minvals[obj] = info.min
        else:
            _maxvals[obj] = None
            _minvals[obj] = None

_construct_lookups()


@set_module('numpy')
def sctype2char(sctype):
    """
    Return the string representation of a scalar dtype.

    Parameters
    ----------
    sctype : scalar dtype or object
        If a scalar dtype, the corresponding string character is
        returned. If an object, `sctype2char` tries to infer its scalar type
        and then return the corresponding string character.

    Returns
    -------
    typechar : str
        The string character corresponding to the scalar type.

    Raises
    ------
    ValueError
        If `sctype` is an object for which the type can not be inferred.

    See Also
    --------
    obj2sctype, issctype, issubsctype, mintypecode

    Examples
    --------
    >>> for sctype in [np.int32, float, complex, np.string_, np.ndarray]:
    ...     print(np.sctype2char(sctype))
    l
    d
    D
    S
    O

    >>> x = np.array([1., 2-1.j])
    >>> np.sctype2char(x)
    'D'
    >>> np.sctype2char(list)
    'O'

    """
    sctype = obj2sctype(sctype)
    if sctype is None:
        raise ValueError("unrecognized type")
    if sctype not in _concrete_types:
        # for compatibility
        raise KeyError(sctype)
    return dtype(sctype).char

# Create dictionary of casting functions that wrap sequences
# indexed by type or type character
cast = _typedict()
for key in _concrete_types:
    cast[key] = lambda x, k=key: array(x, copy=False).astype(k)

try:
    ScalarType = [_types.IntType, _types.FloatType, _types.ComplexType,
                  _types.LongType, _types.BooleanType,
                   _types.StringType, _types.UnicodeType, _types.BufferType]
except AttributeError:
    # Py3K
    ScalarType = [int, float, complex, int, bool, bytes, str, memoryview]

ScalarType.extend(_concrete_types)
ScalarType = tuple(ScalarType)


# Now add the types we've determined to this module
for key in allTypes:
    globals()[key] = allTypes[key]
    __all__.append(key)

del key

typecodes = {'Character':'c',
             'Integer':'bhilqp',
             'UnsignedInteger':'BHILQP',
             'Float':'efdg',
             'Complex':'FDG',
             'AllInteger':'bBhHiIlLqQpP',
             'AllFloat':'efdgFDG',
             'Datetime': 'Mm',
             'All':'?bhilqpBHILQPefdgFDGSUVOMm'}

# backwards compatibility --- deprecated name
typeDict = sctypeDict
typeNA = sctypeNA

# b -> boolean
# u -> unsigned integer
# i -> signed integer
# f -> floating point
# c -> complex
# M -> datetime
# m -> timedelta
# S -> string
# U -> Unicode string
# V -> record
# O -> Python object
_kind_list = ['b', 'u', 'i', 'f', 'c', 'S', 'U', 'V', 'O', 'M', 'm']

__test_types = '?'+typecodes['AllInteger'][:-2]+typecodes['AllFloat']+'O'
__len_test_types = len(__test_types)

# Keep incrementing until a common type both can be coerced to
#  is found.  Otherwise, return None
def _find_common_coerce(a, b):
    if a > b:
        return a
    try:
        thisind = __test_types.index(a.char)
    except ValueError:
        return None
    return _can_coerce_all([a, b], start=thisind)

# Find a data-type that all data-types in a list can be coerced to
def _can_coerce_all(dtypelist, start=0):
    N = len(dtypelist)
    if N == 0:
        return None
    if N == 1:
        return dtypelist[0]
    thisind = start
    while thisind < __len_test_types:
        newdtype = dtype(__test_types[thisind])
        numcoerce = len([x for x in dtypelist if newdtype >= x])
        if numcoerce == N:
            return newdtype
        thisind += 1
    return None

def _register_types():
    numbers.Integral.register(integer)
    numbers.Complex.register(inexact)
    numbers.Real.register(floating)
    numbers.Number.register(number)

_register_types()


@set_module('numpy')
def find_common_type(array_types, scalar_types):
    """
    Determine common type following standard coercion rules.

    Parameters
    ----------
    array_types : sequence
        A list of dtypes or dtype convertible objects representing arrays.
    scalar_types : sequence
        A list of dtypes or dtype convertible objects representing scalars.

    Returns
    -------
    datatype : dtype
        The common data type, which is the maximum of `array_types` ignoring
        `scalar_types`, unless the maximum of `scalar_types` is of a
        different kind (`dtype.kind`). If the kind is not understood, then
        None is returned.

    See Also
    --------
    dtype, common_type, can_cast, mintypecode

    Examples
    --------
    >>> np.find_common_type([], [np.int64, np.float32, complex])
    dtype('complex128')
    >>> np.find_common_type([np.int64, np.float32], [])
    dtype('float64')

    The standard casting rules ensure that a scalar cannot up-cast an
    array unless the scalar is of a fundamentally different kind of data
    (i.e. under a different hierarchy in the data type hierarchy) then
    the array:

    >>> np.find_common_type([np.float32], [np.int64, np.float64])
    dtype('float32')

    Complex is of a different type, so it up-casts the float in the
    `array_types` argument:

    >>> np.find_common_type([np.float32], [complex])
    dtype('complex128')

    Type specifier strings are convertible to dtypes and can therefore
    be used instead of dtypes:

    >>> np.find_common_type(['f4', 'f4', 'i4'], ['c8'])
    dtype('complex128')

    """
    array_types = [dtype(x) for x in array_types]
    scalar_types = [dtype(x) for x in scalar_types]

    maxa = _can_coerce_all(array_types)
    maxsc = _can_coerce_all(scalar_types)

    if maxa is None:
        return maxsc

    if maxsc is None:
        return maxa

    try:
        index_a = _kind_list.index(maxa.kind)
        index_sc = _kind_list.index(maxsc.kind)
    except ValueError:
        return None

    if index_sc > index_a:
        return _find_common_coerce(maxsc, maxa)
    else:
        return maxa
