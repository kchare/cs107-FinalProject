import numpy as np
import itertools

class AD():

    def __init__(self, eval_pt, der_dict={'x1':1}):
        """Initializes class structure
        Parameters
        ----------
        eval_pt : float
            Value of the current function/variable
        der_dict : dict
            derivative value dictionary of all variables
        Returns
        -------
        None.
        Examples
        --------
        >>> x1 = AD(3.6, {'x1':1})
        >>> x1.func_val
        3.6
        >>> x1.partial_dict
        {'x1': 1}
        """
        # Set function value if int or float; else raise error
        if isinstance(eval_pt, (int, float)):
            self.func_val = eval_pt
        else:
            raise ValueError('All valuess should be real float or integer numbers!')

        # Set partial derivative dictionary
        # Will assume form of x_1, ..., x_n
        if not isinstance(der_dict, dict):
            raise ValueError('der_dict must be type dict!')
        try:
            for key, val in der_dict.items():
                assert isinstance(der_dict[key], (int, float))
            self.partial_dict = der_dict
        except:
            raise ValueError('All derivatives must be type int or float, to make the expression real and valid!')

    def set_params(self, att, val):
        """Set parameters for class; to be used in selective cases only
        Parameters
        ----------
        att: string
            Must be passed as a string. One of func_val or partial_dict.
        val: float, int, dictionary
            If att == 'func_val', must be int or float. Else must be dictionary.
        Returns
        -------
        None
        
        Examples
        --------
        >>> x = AD(1)
        >>> x.set_params('func_val', 3.4)
        >>> x.set_params('partial_dict', {'x1': 2})
        >>> print(x.func_val, x.partial_dict)
        3.4 {'x1': 2}
        """
        if att == 'func_val':
            # Implement same check as constructor
            if not isinstance(val, (float, int)):
                raise ValueError("val must be type float or int")
            self.func_val = val
        elif att == 'partial_dict':
            if not isinstance(val, dict):
                raise ValueError("If att='partial_dict', val must be type dictionary")
            # Check that all values of passed dictionary are integers or floats
            try:
                for k, v in val.items():
                    assert isinstance(val[k], (int, float))
                self.partial_dict = val
            except:
                raise ValueError('All values of partial_dict must be int or float')
        else:
            raise ValueError("att must be either 'func_val' or 'partial_dict'")

    def __repr__(self):
        return f'{self.func_val} ({self.partial_dict})'

    def __add__(self, other):
        """Overload addition operation '+'
        Parameters
        ----------
        other : AD class instance or float
            Elements to be added from self. Can be a AD class instance, which
            will update function value and partial derivative dictionary; Or a con-
            -stant, which will only update function value.
        Returns
        -------
        A new AD class instance with updated information
        Examples
        --------
        >>> x1 = AD(3.6, {'x1': 1})
        >>> x2 = AD(5.2, {'x2': 1.5})
        >>> f1 = x1 + x2
        >>> print(f1.func_val, f1.partial_dict)
        8.8 {'x1': 1, 'x2': 1.5}
        >>> f2 = f1 + x1
        >>> print(f2.func_val, f2.partial_dict)
        12.4 {'x1': 2, 'x2': 1.5}
        """
        try:
            # First try as other is an AD class instance
            # Combine the partial_dict of self and other, for common keys, add the value; else, append the dictionary
            new_der_dict = {}
            for k in itertools.chain(self.partial_dict.keys(), other.partial_dict.keys()):
                new_der_dict[k] = self.partial_dict.get(k,0) + other.partial_dict.get(k,0)
            return AD(self.func_val+other.func_val, new_der_dict)
        except AttributeError:
            # If other is not an AD class instance, treat as a constant
            return AD(self.func_val+other, self.partial_dict)

    def __radd__(self, other):
        """Overload to make sure commutativity of addition '+'
        Parameters
        ----------
        other : AD class instance or float
            Elements to be subtracted on the left, from self. Can be a AD class instance, which
            will update function value and partial derivative dictionary; Or a con-
            -stant, which will only update function value.
        Returns
        -------
        A new AD class instance with updated information
        Examples
        --------
        >>> x1 = AD(3.6, {'x1': 1})
        >>> f1 = 10 + x1
        >>> print(f1.func_val, f1.partial_dict)
        13.6 {'x1': 1}
        >>> f0 = AD(3.6, {'x1': 1, 'x2': 4})
        >>> f1 = 10 + f0
        >>> print(f1.func_val, f1.partial_dict)
        13.6 {'x1': 1, 'x2': 4}
        """
        assert isinstance(other,(int, float)), "All values should be real float or int values!"
        # treat as a constant
        # just return the partial dictionary of the self instance 
        new_der_dict = dict(self.partial_dict)
        return AD(other+self.func_val, new_der_dict)

    def __sub__(self, other):
        """Overload subtraction operation '-'
        Parameters
        ----------
        other : AD class instance or float
            Elements to be subtracted from self. Can be a AD class instance, which
            will update function value and partial derivative dictionary; Or a con-
            -stant, which will only update function value.
        Returns
        -------
        A new AD class instance with updated information
        Examples
        --------
        >>> x1 = AD(3.6, {'x1': 1})
        >>> f1 = x1 - 10
        >>> print(f1.func_val, f1.partial_dict)
        -6.4 {'x1': 1}
        >>> x2 = AD(2.0, {'x2': 3.4})
        >>> f2 = x1 - x2
        >>> print(f2.func_val, f2.partial_dict)
        1.6 {'x1': 1, 'x2': -3.4}
        """
        try:
            # First try as other is an AD class instance
            # Combine the partial_dict of self and other, for common keys, subtract the value; else, append the dictionary
            new_der_dict = {}
            for k in itertools.chain(self.partial_dict.keys(), other.partial_dict.keys()):
                new_der_dict[k] = self.partial_dict.get(k,0) - other.partial_dict.get(k,0)
            return AD(self.func_val-other.func_val, new_der_dict)
        except AttributeError:
            # If other is not an AD class instance, treat as a constant
            return AD(self.func_val-other, self.partial_dict)

    def __rsub__(self, other):
        """Overload to make sure commutativity of subtraction '-'
        Parameters
        ----------
        other : AD class instance or float
            Elements to be subtracted on the left, from self. Can be a AD class instance, which
            will update function value and partial derivative dictionary; Or a con-
            -stant, which will only update function value.
        Returns
        -------
        A new AD class instance with updated information
        Examples
        --------
        >>> x1 = AD(3.6, {'x1': 1})
        >>> f1 = 10 - x1
        >>> print(f1.func_val, f1.partial_dict) 
        6.4 {'x1': -1}
        >>> f0 = AD(3.6, {'x1': 1, 'x2': 3})
        >>> f1 = 10 - f0
        >>> print(f1.func_val, f1.partial_dict)
        6.4 {'x1': -1, 'x2': -3}
        """
        assert isinstance(other,(int, float)), "All values should be real float or int values!"
        # If other is not an AD class instance, treat as a constant
        new_der_dict = {}
        for key, value in self.partial_dict.items():
            new_der_dict[key] = -value
        return AD(other-self.func_val, new_der_dict)

    def __mul__(self, other):
        """Overload multiplication operation '*'
        Parameters
        ----------
        other : AD class instance or float
            Elements to be multiplied to self. Can be a AD class instance, which
            will update function value and partial derivative dictionary; Or a con-
            -stant, which will only update function value.
        Returns
        -------
        A new AD class instance with updated information
        Examples
        --------
        >>> x1 = AD(1, {'x1': 1})
        >>> f1 = x1*10.0
        >>> print(f1.func_val, f1.partial_dict)
        10.0 {'x1': 10.0}
        >>> x2 = x1*3.4 - 1.4
        >>> print(x2.func_val, x2.partial_dict)
        2.0 {'x1': 3.4}
        >>> f2 = f1 * x2
        >>> print(f2.func_val, f2.partial_dict)
        20.0 {'x1': 54.0}
        >>> a = AD(2, {'a': 1})
        >>> b = AD(4, {'b': 1})
        >>> f3 = a*b
        >>> print(f3.func_val, f3.partial_dict)
        8 {'a': 4, 'b': 2}
        >>> f4 = f3*b
        >>> print(f4.func_val, f4.partial_dict)
        32 {'a': 16, 'b': 16}
        """
        try:
            # First try as other is an AD class instance
            new_der_dict = {}
            for k in itertools.chain(self.partial_dict.keys(), other.partial_dict.keys()):
                new_der_dict[k] = self.partial_dict.get(k,0)*other.func_val + other.partial_dict.get(k,0)*self.func_val
            #print(new_der_dict)
            #print(self.partial_dict)
            return AD(self.func_val*other.func_val, new_der_dict)
        except AttributeError:
            # If other is not an AD class instance, treat as a constant
            new_der_dict = {}
            for key, value in self.partial_dict.items():
                new_der_dict[key] = value*other
            return AD(self.func_val*other, new_der_dict)

    def __rmul__(self, other):
        """Overload to make sure commutativity of operation '*'
        Parameters
        ----------
        other : AD class instance or float
            Elements to be multiplied to self. Can be a AD class instance, which
            will update function value and partial derivative dictionary; Or a con-
            -stant, which will only update function value.
        Returns
        -------
        A new AD class instance with updated information
        Examples
        --------
        >>> x1 = AD(1, {'x1': 1})
        >>> f1 = 10.0*x1
        >>> print(f1.func_val, f1.partial_dict)
        10.0 {'x1': 10.0}
        >>> x2 = 3.4*x1 - 1.4
        >>> print(x2.func_val, x2.partial_dict)
        2.0 {'x1': 3.4}
        >>> f2 = f1 * x2
        >>> print(f2.func_val, f2.partial_dict)
        20.0 {'x1': 54.0}
        >>> a = AD(2, {'a': 1})
        >>> b = AD(4, {'b': 1})
        >>> f3 = (4*a + 6*b)*a
        >>> print(f3.func_val, f3.partial_dict)
        64 {'a': 40, 'b': 12}
        """
        assert isinstance(other,(int, float)), "All values should be real float or int values!"
        # if other is not an AD class instance, treat as a constant
        new_der_dict = {}
        for key, value in self.partial_dict.items():
            new_der_dict[key] = value*other
        return AD(other*self.func_val, new_der_dict)

    def __truediv__(self, other):
        """Overload division operation '/'
        Parameters
        ----------
        other: AD class instance or float
            Elements to be divided from self. Can be an AD class instance, which
            will update function value and partial derivative dictionary; Or a con-
            -stant, which will only update function value.
        Returns
        -------
        A new AD class instance with updated information
        Examples
        --------
        >>> x1 = AD(1., {'x1':1})
        >>> f1 = x1/10.
        >>> print(f1.func_val, f1.partial_dict)
        0.1 {'x1': 0.1}
        >>> x2 = 3.4*x1
        >>> f2 = x2/x1
        >>> print(f2.func_val, f2.partial_dict)
        3.4 {'x1': 0.0}
        >>> a = AD(2, {'a': 1})
        >>> b = AD(4, {'b': 1})
        >>> f3 = a/b
        >>> print(f3.func_val, f3.partial_dict)
        0.5 {'a': 0.25, 'b': -0.125}
        """
        try:
            # first try as other is an ad class instance
            new_der_dict = {}
            for k in itertools.chain(self.partial_dict.keys(), other.partial_dict.keys()):
                new_der_dict[k] = (self.partial_dict.get(k,0)*other.func_val - other.partial_dict.get(k,0)*self.func_val)/(other.func_val**2)
            return AD(self.func_val/other.func_val, new_der_dict)
        except AttributeError:
            # If other is not an AD class instance, treat as a constant
            new_der_dict = {}
            for key, value in self.partial_dict.items():
                new_der_dict[key] = value/other
            return AD(self.func_val/other, new_der_dict)

    def __rtruediv__(self, other):
        """Overload to make right version of operation '/' works
        Parameters
        ----------
        other : AD class instance or float
            Elements to be multiplied to self. Can be a AD class instance, which
            will update function value and partial derivative dictionary; Or a con-
            -stant, which will only update function value.
        Returns
        -------
        A new AD class instance with updated information
        Examples
        --------
        >>> x1 = AD(1., {'x1':1})
        >>> f1 = 10.0/x1
        >>> print(f1.func_val, f1.partial_dict)
        10.0 {'x1': -10.0}
        >>> x2 = 3.4*x1 - 1.4
        >>> f2 = x2/x1
        >>> print(f2.func_val, f2.partial_dict)
        2.0 {'x1': 1.4}
        >>> a = AD(2, {'a': 1})
        >>> b = AD(4, {'b': 1})
        >>> f3 = 16./(a*b)
        >>> print(f3.func_val, f3.partial_dict)
        2.0 {'a': -1.0, 'b': -0.5}
        """
        assert isinstance(other,(int, float)), "All values should be real float or int values!"
        # if other is not an AD class instance, treat as a constant
        new_der_dict = {}
        for key, value in self.partial_dict.items():
            new_der_dict[key] = -other*value/(self.func_val**2)
        return AD(other/self.func_val, new_der_dict)

    def __pow__(self, other):
        """Overload power operation '**'
        Parameters
        ----------
        other : AD class instance or float
            Elements to be powered to self. Can be a AD class instance, which
            will update function value and partial derivative dictionary; Or a con-
            -stant, which will only update function value.
        Returns
        -------
        A new AD class instance with updated information
        Examples
        --------
        >>> x = AD(2, {'x1': 1})
        >>> print(x**3)
        8 ({'x1': 12})
        >>> x = AD(2, {'x1': 1.})
        >>> f1 = AD.sin(x**3)
        >>> print(f1**3)
        0.9684132754691923 ({'x1': -5.127111370310495})
        >>> x = AD(2, {'x': 1})
        >>> f2 = x**x
        >>> print(f2.func_val, f2.partial_dict)
        4 {'x': 6.772588722239782}
        >>> a = AD(2, {'a': 1})
        >>> b = AD(4, {'b': 1})
        >>> f3 = a**b
        >>> print(f3.func_val, f3.partial_dict)
        16 {'a': 32.0, 'b': 11.090354888959125}
        """
        try:
            # First try as other is an AD class instance
            new_der_dict = {}
            for k in itertools.chain(self.partial_dict.keys(), other.partial_dict.keys()):
                new_der_dict[k] = self.func_val**other.func_val *\
                                    (self.partial_dict.get(k,0)*other.func_val/self.func_val +\
                                     other.partial_dict.get(k,0)*np.log(self.func_val))
            return AD(self.func_val**other.func_val, new_der_dict)
        except AttributeError:
            # If other is not an AD class instance, treat as a constant
            new_der_dict = {}
            for key, value in self.partial_dict.items():
                new_der_dict[key] = other * self.func_val**(other-1) * value
            return AD(self.func_val**other, new_der_dict)
        
        
    def __rpow__(self, other):
        """Overload right power operation '**'
        Parameters
        ----------
        other : AD class instance or float
            Elements to be powered to self. Can be a AD class instance, which
            will update function value and partial derivative dictionary; Or a con-
            -stant, which will only update function value.
        Returns
        -------
        A new AD class instance with updated information
        Examples
        --------
        >>> x = AD(2, {'x1': 1})
        >>> print(3**x)
        9 ({'x1': 9.887510598012987})
        >>> x = AD(2, {'x1': 1.})
        >>> f1 = AD.sin(3**x)
        >>> print(f1**3)
        0.06999488183019169 ({'x1': -4.5902134148312985})
        >>> a = AD(2, {'a': 1})
        >>> b = AD(3, {'b': 1})
        >>> f2 = 2**(a+b)
        >>> print(f2.func_val, f2.partial_dict)
        32 {'a': 22.18070977791825, 'b': 22.18070977791825}
        """
        assert isinstance(other,(int, float)), "All values should be real float or int values!"
        # if other is not an AD class instance, treat as a constant
        new_der_dict = {}
        for key, value in self.partial_dict.items():
            new_der_dict[key] = other**self.func_val * np.log(other) * value
        return AD(other**self.func_val, new_der_dict)

    def __neg__(self):
        """Overload '-' to return the negative of an object
        
        Parameters
        ----------
        self: AD class instance or float
             Current AD instance
        Returns
        -------
        A new AD class instance with opposite function value and derivative
        
        Examples
        --------
        >>> x1 = AD(1., {'x1':1})
        >>> f_x1 = -x1
        >>> print(f_x1.func_val, f_x1.partial_dict)
        -1.0 {'x1': -1}
        >>> x2 = 3*x1
        >>> f_x2_x1 = -x2 + x1
        >>> print(f_x2_x1.func_val, f_x2_x1.partial_dict)
        -2.0 {'x1': -2}
        >>> f2 = AD(2, {'a': 1}) + AD(4, {'b': 1})
        >>> print(-f2)
        -6 ({'a': -1, 'b': -1})
        """
        # Pass to __rmul__ via multiply by float
        return self.__rmul__(-1)


    @staticmethod
    def sin(x):
        """A static method to calculate the sine function of a AD instance, or a float
        Parameters
        ----------
        x: AD class instance or float, in radians
           Elements to be operated a sin operator. Can be an AD class instance, whichi
           will update function value and partial derivative dictionary; or a constant, whi-
           -ch will give a constant output
        Returns
        -------
        A new AD class with updated information
        Examples
        --------
        >>> x1 = AD(np.pi/2, {'x1': 1.})
        >>> f1 = AD.sin(x1)
        >>> print(f1.func_val, f1.partial_dict)
        1.0 {'x1': 6.123233995736766e-17}
        >>> x2 = AD.sin(np.pi)
        >>> print(x2)
        1.2246467991473532e-16
        """
        try:
            # First try as x is an AD instance
            new_der_dict = x.partial_dict.copy()
            for var in new_der_dict.keys():
                new_der_dict[var] = np.cos(x.func_val)*new_der_dict[var]
            return AD(np.sin(x.func_val), new_der_dict)
        except AttributeError:
            # if x is not an AD class instance, treat as a constant
            return np.sin(x)


    @staticmethod
    def cos(x):
        """A static method to calculate the cosine function of a AD instance, or a float
        Parameters
        ----------
        x: AD class instance or float, in radians
           Elements to be operated a cosine operator. Can be an AD class instance, which
           will update function value and partial derivative dictionary; or a constant, whi-
           -ch will give a constant output
        Returns
        -------
        A new AD class with updated information
        Examples
        --------
        >>> x1 = AD(np.pi/2, {'x1': 1.})
        >>> f1 = AD.cos(x1)
        >>> print(f1.func_val.round(1), f1.partial_dict)
        0.0 {'x1': -1.0}
        >>> x2 = AD.cos(np.pi)
        >>> print(x2)
        -1.0
        """
        try:
            # First try as x is an AD instance
            new_der_dict = x.partial_dict.copy()
            for var in new_der_dict.keys():
                new_der_dict[var] = -np.sin(x.func_val)*new_der_dict[var]
            return AD(np.cos(x.func_val), new_der_dict)
        except AttributeError:
            # if x is not an AD class instance, treat as a constant
            return np.cos(x)

    @staticmethod
    def tan(x):
        """A static method to calculate the tangent function of a AD instance, or a float
        Parameters
        ----------
        x: AD class instance or float, in radians
           Elements to be operated a tangent operator. Can be an AD class instance, which
           will update function value and partial derivative dictionary; or a constant, whi-
           -ch will give a constant output
        Returns
        -------
        A new AD class with updated information
        Examples
        --------
        >>> x1 = AD(np.pi, {'x1': 1.})
        >>> f1 = AD.tan(x1)
        >>> print(f1.func_val.round(1), f1.partial_dict)
        -0.0 {'x1': 1.0}
        >>> x2 = AD.tan(np.pi)
        >>> print(x2.round(1))
        -0.0
        """
        try:
            # First try as x is an AD instance
            new_der_dict = x.partial_dict.copy()
            for var in new_der_dict.keys():
                new_der_dict[var] = new_der_dict[var]/(np.cos(x.func_val)**2)
            return AD(np.tan(x.func_val), new_der_dict)
        except AttributeError:
            # if x is not an AD class instance, treat as a constant
            return np.tan(x)
        
    @staticmethod
    def sqrt(x):
        """Overload power operation 'sqrt'
        Parameters
        ----------
        other : AD class instance or float
            Elements to be put to 1/2 power. Can be a AD class instance, which
            will update function value and partial derivative dictionary; Or a con-
            -stant, which will only update function value.
        Returns
        -------
        A new AD class instance with updated information
        
        Examples
        --------
        >>> x1 = AD(1.0, {'x1': 1.0})
        >>> f1 = AD.sqrt(x1)
        >>> print(f1.func_val, f1.partial_dict)
        1.0 {'x1': 0.5}
        >>> f2 = AD.sqrt(1.0)
        >>> print(f2)
        1.0
        >>> x2 = AD(0, {'x2': 1})
        >>> f3 = AD.sqrt(AD.cos(x2))
        >>> print(f3.func_val, f3.partial_dict)
        1.0 {'x2': -0.0}
        """
        try:
            # First try as x is an AD instance
            new_der_dict = x.partial_dict.copy()
            for var in new_der_dict.keys():
                new_der_dict[var] = new_der_dict[var]/(2 * (x.func_val**(1/2)))
            return AD(np.sqrt(x.func_val), new_der_dict)
        except AttributeError:
            # if x is not an AD class instance, treat as a constant
            return np.sqrt(x)
        
    @staticmethod
    def log(x,base = np.e):
        """A static method to calculate the logrithmic function of a AD instance, 
            or a float for multiple bases, with the default being e. 
        Parameters
        ----------
        x: AD class instance or float, in radians
           Elements to be operated on a logrithm. Can be an AD class instance, which
           will update function value and partial derivative dictionary; or a constant, whi-
           -ch will give a constant output. 
        Base : Constant integer or float to be used as base in logarithm. 
            Base is a default of e, but can be changed by entering in after x in log
            method.
        Returns
        -------
        A new AD class with updated information
        Examples
        --------
        >>> x1 = AD(np.e**2, {'x1': 1.})
        >>> f0 = AD.log(x1)
        >>> print(f0.func_val.round(1), f0.partial_dict)
        2.0 {'x1': 0.1353352832366127}
        >>> f1 = AD.log(x1, np.e**2)
        >>> print(f1.func_val.round(1), f1.partial_dict)
        2.0 {'x1': 0.06766764161830635}
        >>> x2 = AD.log(np.e)
        >>> print(x2)
        1.0
        >>> x3 = AD.log(4, 2)
        >>> print(x3)
        2.0
        >>> x4 = AD.log(2, 32)
        >>> print(x4.round(1))
        0.2
        """
        if base == 0 or not (isinstance(base, int) or isinstance(base,float)):
            raise Exception("Base Must be a constant integer or a float not equal to 0")
        try:
            # First try as x is an AD instance
            new_der_dict = x.partial_dict.copy()
            for var in new_der_dict.keys():
                new_der_dict[var] = new_der_dict[var]/(x.func_val * np.log(base))
            return AD(np.log(x.func_val), new_der_dict)
        except AttributeError:
            # if x is not an AD class instance, treat as a constant
            return np.log(x) / np.log(base)
        
    @staticmethod
    def sinh(x):
        """A static method to calculate the hyperbolic sine function of a AD instance, or a float
        Parameters
        ----------
        x: AD class instance or float, in radians
           Elements to be operated a sinh operator. Can be an AD class instance, whichi
           will update function value and partial derivative dictionary; or a constant, whi-
           -ch will give a constant output
        Returns
        -------
        A new AD class with updated information
        Examples
        --------
        >>> x1 = AD(0.0, {'x1': 1.0})
        >>> f1 = AD.sinh(x1)
        >>> print(f1.func_val, f1.partial_dict)
        0.0 {'x1': 1.0}
        >>> x2 = AD.sinh(0)
        >>> print(x2)
        0.0
        """

        try:
            # First try as x is an AD instance
            new_der_dict = x.partial_dict.copy()
            for var in new_der_dict.keys():
                new_der_dict[var] = np.cosh(x.func_val)*new_der_dict[var]
            return AD(np.sinh(x.func_val), new_der_dict)
        except AttributeError:
            # if x is not an AD class instance, treat as a constant
            return np.sinh(x)


    @staticmethod
    def cosh(x):
        """A static method to calculate the hyperbolic cosine function of a AD instance, or a float
        Parameters
        ----------
        x: AD class instance or float, in radians
           Elements to be operated a cosine operator. Can be an AD class instance, which
           will update function value and partial derivative dictionary; or a constant, whi-
           -ch will give a constant output
        Returns
        -------
        A new AD class with updated information
        Examples
        --------
        >>> x1 = AD(0.0, {'x1': 1.0})
        >>> f1 = AD.cosh(x1)
        >>> print(f1.func_val.round(1), f1.partial_dict)
        1.0 {'x1': -0.0}
        >>> x2 = AD.cosh(0)
        >>> print(x2)
        1.0
        """
        try:
            # First try as x is an AD instance
            new_der_dict = x.partial_dict.copy()
            for var in new_der_dict.keys():
                new_der_dict[var] = -np.sinh(x.func_val)*new_der_dict[var]
            return AD(np.cosh(x.func_val), new_der_dict)
        except AttributeError:
            # if x is not an AD class instance, treat as a constant
            return np.cosh(x)

    @staticmethod
    def tanh(x):
        """A static method to calculate the hyperbolic tangent function of a AD instance, or a float
        Parameters
        ----------
        x: AD class instance or float, in radians
           Elements to be operated a hyperbolic tangent operator. Can be an AD class instance, which
           will update function value and partial derivative dictionary; or a constant, whi-
           -ch will give a constant output
        Returns
        -------
        A new AD class with updated information
        Examples
        --------
        >>> x1 = AD(0.0, {'x1': 1.0})
        >>> f1 = AD.tanh(x1)
        >>> print(f1.func_val.round(1), f1.partial_dict)
        0.0 {'x1': 1.0}
        >>> x2 = AD.tanh(np.pi)
        >>> print(x2.round(1))
        1.0
        """
        try:
            # First try as x is an AD instance
            new_der_dict = x.partial_dict.copy()
            for var in new_der_dict.keys():
                new_der_dict[var] = new_der_dict[var]/(np.cosh(x.func_val)**2)
            return AD(np.tanh(x.func_val), new_der_dict)
        except AttributeError:
            # if x is not an AD class instance, treat as a constant
            return np.tanh(x)
          
    @staticmethod
    def exp(x):
        """A static method to calculate the natrual an exponent function of a AD instance, or a float
        Parameters
        ----------
        x: AD class instance or float, in radians
           Elements to be operated an exponent. Can be an AD class instance, which
           will update function value and partial derivative dictionary; or a constant, whi-
           -ch will give a constant output
        Returns
        -------
        A new AD class with updated information
        Examples
        --------
        >>> x = AD(2, {'x1': 1.})
        >>> print(AD.exp(x))
        7.3890560989306495 ({'x1': 7.3890560989306495})
        >>> x2 = 2
        >>> print(AD.exp(x2))
        7.3890560989306495
        """
        return np.e**x
    
    
    
    @staticmethod
    def logistic(x, x_0=0, k=1, L=1):
        """A static method to calculate the logistic function of an AD instance or
        float. Logistic function L/(1+e^(-k(x-x_0))). More commonly used as 1/(1+e^(-x))
        Parameters
        ----------
        x: AD class instance of float
            Elements to be used as base of logistic function. Can be an AD class instance,
            which will update both the function value and partial derivative dictionary; or
            a constant, which will return a constant output
        x_0: int or float 
            This represents the center of logistic function; default set to zero, i.e.
            logistic function centered at zero 0.
        k: int or float
            Logistic growth rate of function; default set to 1. Larger values of k imply
            steeper logistic growth rate
        L: int or float
            Maximum value of logistic function; default set to 1.
        Returns
        -------
        A new AD class with updated information; otherwise a float value.
        
        Examples
        --------
        >>> x = AD(1.5)
        >>> print(AD.logistic(x))
        0.8175744761936437 ({'x1': 0.14914645207033284})
        >>> f = x + AD(-0.5, {'x2': 1})
        >>> print(AD.logistic(f))
        0.7310585786300049 ({'x1': 0.19661193324148188, 'x2': 0.19661193324148188})
        """
        return L/(1 + AD.exp(-k * (x - x_0)))

if __name__ == '__main__':
    import doctest
    doctest.testmod()