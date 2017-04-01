# -*- coding: utf-8 -*-

"""
Physical quantities.
"""

from __future__ import division

from sympy.core.compatibility import string_types
from sympy import sympify, Expr, Mul, Pow, S, Symbol, Add, AtomicExpr
from sympy.physics.units import Dimension
from sympy.physics.units import dimensions
from sympy.physics.units.prefixes import Prefix


class Quantity(AtomicExpr):
    """
    Physical quantity.
    """

    is_commutative = True
    is_real = True
    is_number = False
    is_nonzero = True
    _diff_wrt = True

    def __new__(cls, name, dimension, scale_factor=S.One, abbrev=None, **assumptions):

        if not isinstance(name, Symbol):
            name = Symbol(name)

        if not isinstance(dimension, dimensions.Dimension):
            if dimension == 1:
                dimension = Dimension(1)
            else:
                raise ValueError("expected dimension or 1")
        scale_factor = sympify(scale_factor)

        dimex = Quantity.get_dimensional_expr(scale_factor)
        if dimex != 1:
            if dimension != Dimension(dimex):
                raise ValueError("quantity value and dimension mismatch")

        # replace all prefixes by their ratio to canonical units:
        scale_factor = scale_factor.replace(lambda x: isinstance(x, Prefix), lambda x: x.scale_factor)
        # replace all quantities by their ratio to canonical units:
        scale_factor = scale_factor.replace(lambda x: isinstance(x, Quantity), lambda x: x.scale_factor)

        if abbrev is None:
            abbrev = name
        elif isinstance(abbrev, string_types):
            abbrev = Symbol(abbrev)

        obj = AtomicExpr.__new__(cls, name, dimension, scale_factor, abbrev)
        obj._name = name
        obj._dimension = dimension
        obj._scale_factor = scale_factor
        obj._abbrev = abbrev
        return obj

    @property
    def name(self):
        return self._name

    @property
    def dimension(self):
        return self._dimension

    @property
    def abbrev(self):
        """
        Symbol representing the unit name.

        Prepend the abbreviation with the prefix symbol if it is defines.
        """
        return self._abbrev

    @property
    def scale_factor(self):
        """
        Overall magnitude of the quantity as compared to the canonical units.
        """
        return self._scale_factor

    def _eval_is_positive(self):
       return self.scale_factor.is_positive

    def _eval_is_constant(self):
        return self.scale_factor.is_constant()

    @staticmethod
    def get_dimensional_expr(expr):
        if isinstance(expr, Mul):
            return Mul(*[Quantity.get_dimensional_expr(i) for i in expr.args])
        elif isinstance(expr, Pow):
            return Quantity.get_dimensional_expr(expr.base) ** expr.exp
        elif isinstance(expr, Add):
            # return get_dimensional_expr()
            raise NotImplementedError
        elif isinstance(expr, Quantity):
            return expr.dimension.name
        return 1

    @staticmethod
    def _collect_factor_and_dimension(expr):

        if isinstance(expr, Quantity):
            return expr.scale_factor, expr.dimension
        elif isinstance(expr, Mul):
            factor = 1
            dimension = 1
            for arg in expr.args:
                arg_factor, arg_dim = Quantity._collect_factor_and_dimension(arg)
                factor *= arg_factor
                dimension *= arg_dim
            return factor, dimension
        elif isinstance(expr, Pow):
            factor, dim = Quantity._collect_factor_and_dimension(expr.base)
            return factor ** expr.exp, dim ** expr.exp
        elif isinstance(expr, Add):
            raise NotImplementedError
        else:
            return 1, 1

    def convert_to(self, other):
        """
        Convert the quantity to another quantity of same dimensions.

        Examples
        ========

        >>> from sympy.physics.units import speed_of_light, meter, second
        >>> speed_of_light
        speed_of_light
        >>> speed_of_light.convert_to(meter/second)
        299792458*meter/second

        >>> from sympy.physics.units import liter
        >>> liter.convert_to(meter**3)
        meter**3/1000
        """
        from .util import convert_to
        return convert_to(self, other)

    @property
    def free_symbols(self):
        return set([])
