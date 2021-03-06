# boomdiff: Software for optimization of objective functions

**Authors**: Minhuan Li, Oksana Makarova, Timothy Williamson, Kevin Hare *(Group #19)*


## Introduction
#### Overview
This software package `boomdiff` implements an optimization of a user-supplied or pre-set objective function. Many scientific and social scientific fields rely on probabilistic and statistical methodologies, of which function optimization is an integral part. This function, often called an objective function or a cost function, can take many arbitrary functional forms. Intuitively, the user observes some data and wishes to fit a model to the data subject to some constraint. Deviations from the constraint (i.e. the accuracy) can be viewed as the 'cost'. In minimizing this cost, the user retains the best model.

Two common point estimators in data-driven fields are Maximum Likelihood Estimator (MLE) from Frequentist's view and Maximum A Posterior (MAP) from Bayesian's view. In each case, the optimum points are identified by the stationary condition (first order derivative equals 0) and convexity check by higher order derivatives. Generally, a major branch of modern optimization methods, like Stochastic Gradient Descent (SGD) and Broyden–Fletcher–Goldfarb–Shanno algorithm (BFGS), are established via the first or higher order gradient of target function, thus heavily relies on an efficient gradient computation.

Auto Differentiation (AD) is one highly effective method for calculation of the gradient function at some arbitrary point. The method, which balances the efficiency of numeric computation and the precision of symbolic derivatives, is commonly used for optimization applications. Our library solves the optimization problem described above for users via gradient descent, a generalized class of algorithms that exploit the first derivative of a function. The optimization is implemented via forward-mode autodifferentiation, a computing technique that  can effectively and efficiently compute the Jacobian matrix. For the optimization problems we consider, the multidimensional nature of the challenge necessarily lends itself to the use of AD.

While the provided description of *boomdiff* primarily concerns the case where the user has some set of data and wishes to optimize a model against that data, the functionality of this package is not limited to that setting. Rather, *boomdiff* will suffice as a general optimization tool as well for an arbitrary function defined by the user.

#### Gradient-methods supported
- Gradient descent (also known as batch gradient descent)
- Stochastic gradient descent
- Mini-batch gradient descent
- TBD

## Background
#### Optimization
As briefly described in the introduction, nearly all scientific and social scientific fields rely require the optimization of objective (or cost) functions. Even realtively straightforward data analysis techniques such as ordinary least squares regression proceed by specifying a cost function ($(y-\hat{y})^2$ in the canoncial regression task), and then minimizing this cost function. The relative simplicity of this idea, however, belies the true difficulty of estimation of this function minimum. The case of OLS regression has a closed form [solution](https://en.wikipedia.org/wiki/Ordinary_least_squares); more computationally complex models such as neural networks do not. The most general approach for solving these complex sets of equations in lieu of an analytical solution is gradient descent. This iterative methodology operates in the following two general steps:
1. Evaluate the gradient of the objective function while fixing the parameters to be optimized.
2. Update the parameters based on the direction and magnitude of the gradient.

This procedure is continued until the parameters are optimized, which will intuitively occur when the gradient with respect to the parameter is equal to zero. Algorithmically, when the gradient is zero, the magnitude will be as well, and the parameters will terminate updates. Speaking mathematically, this occurs exactly when the stationarity condition has been satisfied (i.e. the first derivative, or gradient) is equal to zero.

This methodology, however, is quite [generalizable and flexible](https://ruder.io/optimizing-gradient-descent/). Two particular problems faced in practice revolve around computational cost and saddle points. When optimization involves significant quantities of data -- as is often the case for MLE or MAP procedures -- the [log-likelihood function](https://en.wikipedia.org/wiki/Likelihood_function), which we hope to minimize, may have hundreds or thousands of data points to be summed over. Doing so can be computationally overwhelming and expensive. To account for this, many techniques randomly select some subset of data, and iteratively optimize over each subset of data. In doing so, the optimization proceeds with smaller magnitude updates, but may more quickly realize the appropriate direction. This technique is commonly known as Stochastic Gradient Descent (SGD) or Mini-Batch Gradient Descent (MBGD) (see [here](https://developers.google.com/machine-learning/crash-course/reducing-loss/stochastic-gradient-descent) for more information). 

Second, for highly complex and non-convex functions, the gradient descent may become 'stuck' at a specific point, or a local minimum, rather than the desired global minimum. Overcoming this challenge once again requires the introduction of randomness. While SGD may be able to eventually overcome this challenge via selecting a subset of data with a gradient with sufficient magnitude to escape the point, a second general approach is to update the parameters using not only the single previous estimate, but many previous estimates. This concept is often referred to as 'momentum' (see [here](https://distill.pub/2017/momentum/) for a more detailed tutorial on the specific mechanics underlying momentum-based gradient descent algorithms).

In all of these methodologies, however, there is the notion of calculation of the gradient. For highly non-convex functions, analytically writing the gradient, or writing a function to evaluate it, may be impossible or highly time-consuming. One approach for solving this issue is to use automatic differentiation, which

#### Automatic Differentiation
At it’s heart, automatic differentiation (AD) seeks to calculate the derivative of some function, and evaluate both the function and the derivative, at a given point by iteratively applying the chain rule to a composition of elementary functions whose derivatives are well-known. This application of the [chain rule](https://en.wikipedia.org/wiki/Chain_rule) is essential. By viewing a more complex function as simply the composition of many elementary functions, the calculation of the derivative becomes a series of steps, starting from the innermost function in the forward mode of AD. In each step, the chain rule is applied. For $z(y(x))$:

$$ \frac{dz}{dx} = \frac{dz}{dy} \frac{dy}{dx} $$

Importantly, because $z(y)$ will be an elementary function (e.g. addition, subtraction, sine, cosine), its derivative can be easily calculated. As we have begun at the innermost derivative, that function $\frac{dy}{dx}$ is known and can be used to iteratively calculate the derivative of the composition. For the simple example above, there are only two elementary operations, but this method can be extended to cover many elementary operations. One only needs to keep track of the derivative of each ‘running’ piece.

The method can be implemented through a graph structure (see below for a simple example), with each node in the graph, which represents a single elementary operation. This computational graph is especially important when the function of interest relies on multiple elements (e.g. $f(x,y) = x^2 + \sin(y)$). One particular advantage of the elementary operations in this method is that each type of operation has a known derivative that can be calculated systematically and efficiently. At each step in the forward mode, the algorithm only needs to maintain the status of the derivative (potentially multiple partial derivatives in the case of multiple elements) as well as the current value of the function.

These storage requirements and iterative nature take advantage of a computer’s ability to store many values and perform many simple operations very quickly. One challenge for computers in calculating complex, symbolic derivatives is that symbolic differentiation may lead to enormous equations and syntactical rules that are highly complex to apply. For humans with a pen and paper, the AD approach may take too much time. The number of calculations, albeit simple, would certainly overwhelm the ability of most people to simply calculate the symbolic derivatives and implement a single evaluation. That concern is severely attenuated by computers. Additionally, AD is superior to the finite differences method of differentiation due to the fact that it is able to keep track of derivatives and functions at the level of machine precision. In scientific applications, this feature is incredibly important, as the sensitive systems measured or engineered will not be successful with only generalities.


## Installation of boomdiff
Below are instructions for the download and installation of the *boomdiff* package. The instructions below are all designed to be run on a command-line interface (Windows, macOS, Linux). Please note that steps (2) and (3) assume that the user has installed [Python](https://www.python.org/). If the user has not installed Python, please see instructions [below](#installation_py)

**Method #1: Installation via PyPi**
Note: this is the preferred method for installing the most up-to-date release of *boomdiff*.
1. In a command-line interface, run the following command:

` pip install boomdiff`

** Method #2: Installation via GitHub**
If installation via PyPi is insufficient, we have provided the instructions below, desgined to download and install the development version of *boomdiff*, available through our GitHub repository.
1. **Download package**: 

    The boomdiff package is available at the GitHub address (https://github.com/team-boomeraang/cs107-FinalProject). To download, navigate on the command line to the desired installation location and run:

    `git clone https://github.com/team-boomeraang/cs107-FinalProject.git`
    
2. **Installation of dependencies**: 

    There are two ways to install dependencies, depending on the package manager used. If using `pip`, then run:

    `pip install -r requirements.txt`
    
    Else, if using Conda or Miniconda for package management, run:
    
    `conda install --file requirements.txt`
    
    Finally, if the desired use is to use `pip` to install the package through Conda or Miniconda, run the following sequence of commands:
    
    `conda install pip`
    
    `which pip`
    
    Ensure that the directory of pip to be used falls below 'anaconda' or 'miniconda' in the directory structure.
    
    `pip install -r requirements.txt`
    
3. **Set-up and install packages**: 
   
    Next, the `setup.py` file must be run to install boomdiff [boomdiff_optimizer not currently available, see Future Features section below]. Navigate to the newly cloned directory and run:

    `python setup.py install`
    
    

<a id='installation_py'></a>

#### Installation of Python
We recommend two possible methods for installation of Python.


1. [Anaconda](https://www.anaconda.com/products/individual) is a package manager that can install Python as well as a variety of common packages (e.g. NumPy, Pandas, scipy). If installed with Anaconda, the instructions below describing `conda install` will be most relevant.


2. Python can also be installed directly (see [here](https://www.python.org/downloads/)). This installation mode will require use of an outside text editor, but may offer more flexibility for installation. If installed via the Python documentation directly, please follow instructions for `pip`.

## Use of *boomdiff*
### Generalized autodifferentiation
In order to take advantage of the ability of *boomdiff*, all objects for optimization must be instantiated as automatic differentiation objects. This section provides a brief introduction and example to instantiation of AD objects. The following section, on objective functions, details how to combine these AD objects into an objective function.

#### Example 0: Instantiate a variable 

As a forward AD mode, we mostly have to instantiate input variables with value and derivative values as a starting point. This process can be easily done with `x1 = AD(*value,**derivate_dict)`. Value is a necessary argument and derivative dictionary are defaulted to be `{'x1': 1}`, you can set as you like. Currently, we only support single input, single scalar output.

The value of the variable will be stored in an attribute `func_val` and the partial derivative dictionary (for now, only one key-value pair) will be stored as `partial_dict`. Then you can use this defined varaible for constructing following complex functions.

```python
>>> from boomdiff import AD
>>> # Step1: Instantiate a variable called x1, with value 10, derivative to be default 1
>>> x1 = AD(10)
>>> # Step2: Demonstrate the information
>>> print(x1)
10 ({'x1': 1})
```

You can name the variable and set the derivative value as you like. There are two options for specifying the variable name and partial derivative. First, the desired name of the variable can be passed directly, and *boomdiff* will use a default seed value of 1 for the partial derivative.
```python
>>> x = AD(10, 'x')
>>> print(x)
10.0 ({'x': 1})
```
Second, the entire partial derivative dictionary can be passed through to the constructor:

```python
>>> # Step1: Instantiate a variable called a, with value 4.9, derivative to be 3.4
>>> a = AD(4.9, {'a': 3.4})

>>> # Step2: Demonstrate the information
>>> print(a)
4.9 ({'a': 3.4})
```
#### Example 1: Constructing an arbitrary function $f(x) = 3x + 4$
We use this example as a demonstration of overloaded primary function in our package. Currently, we support `+`(add), `-`(subtract & negation), `*`(multiply), `/`(divide) and `**`(power)

We will evaluate this function and its derivative at the point $x = 10$. From analytical derivation, we can ascertain that $f(10) = 34$ and $f'(10) = 3$. The tutorial below demonstrates how to calculate this result using *boomdiff*. Before beginning, one important note is that because *boomdiff* only supports scalar functions of one variable, the default behavior is to label the variable `x1`. While the variable name may be any variable name supported by Python, *boomdiff* will report a derivative associated with `x1` unless otherwise specified.

The value of the function will be stored in an attribute `func_val` and the partial derivative dictionary (for now, only one key-value pair) will be stored as `partial_dict`.

```python
>>> # Step 1: Instantiate AD object, as a variable x, at evaluation point (10)
>>> x = AD(10, {'x': 1})

>>> # Step 2: Construct function f(x) = 3x + 4
>>> f = 3*x + 4

>>> # Step 3: Evaluate function and derivative
>>>print(f.func_val)
34
>>> print(f.partial_dict)
{'x': 3}
```

#### Example 2: Static method functions, $f(x) = \sin(x^2)$
We use this example as a demonstration of static method primary functions in our package. Currently, we support `AD.sin()`(sine), `AD.cos()`(cosine), `AD.tan()`(tangent), `AD.log()`(natural log) and `AD.exp()`(exponential). 

We will evaluate this function and its derivative at the value 3. Analytically, the derivative of this function, $f'(x) = 2x \cos(2x)$. Unlike the first function, this one is not so easily evaluated simply by inspection. For *boomdiff*, however, this remains computationally easy. Additionally, in this example, we directly instantiate the function. Note that this functionality assumes that there is only one variable, and thus, $x + y$ will be treated as $x1 + x1$.

```python
>>> # Step 1: Instantiate AD object, as a variable x, at evaluation point (3)
>>> x = AD(10, {'x': 1})
>>> # Step 2: Instantiate function f = sin(x**2)
>>> f = AD.sin(x**2)
>>> # Step 2: Evaluate function and derivative
>>>print(f.func_val)
-0.5063656411097588
>>>print(f.partial_dict)
{'x': 17.24637744575368}
```

#### Example 3: Functions of many variables
```python
>>> from boomdiff import AD
  
>>> # Step1: instantiate multiple variables, x1, x2 here
>>> x1 = AD(10, {'x1': 1})
>>> x2 = AD(4.9, {'x2': 1})
    
>>> # Step2: Define a multivariant function, f = x1+x2
>>> f = x1 + x2
    
>>> # Step3: Show the information of f
>>> f.func_val
14.9   
    
>>> # Now we have multiple partial derivatives in the dictionary
>>> f.partial_dict
{'x1': 1, 'x2': 1}
```

### Optimization of objective functions
From these objects, users may instantiate more complex and arbitrary functions. Using the *boomdiff.optimize* framework, those functions can be efficiently minimzied to machine precision. In terms of structure, *boomdiff* relies on an `Optimizer()` superclass structure, with each gradient descent method taking being a subclass. More details regarding implementation and use can be found in the Implementation section below. In this section, we demonstrate the optimization of two functions: first, an arbirary function, $-x$, and second, an objective function given some data.

#### Example 1: Minimize $f(x_1, x_2) = x_1^2 + x_2^2$
Example:
```python
>>> # Instantiate an SGD optimizer
>>> opt = boomdiff.optimize.SGD(learning_rate=0.1)
```
In this case, `loss` should be a callable that takes no arguments and output an AD instance that only uses operations supported by AD class
```python
>>> loss = lambda: var1**2 + var2**2
```
Initialize the variables for the objective function. Make sure the name string in the dict is corresponds to the variable names instantiated in the lamda function.
```python
>>> var1 = AD(1, {'var1': 1})
>>> var2 = AD(2, {'var2': 1})
```
Call step method, update the variables for one step, to minimize the loss value. `var_list` are the variable lists to update, which can be part of the variables in the callable loss function defined above. This step method will update the underlying variables previously defined.
```python
>>> opt.step(loss, var_list=[var1, var2])
```
For each step, `var1` and `var2` will be updated. the magnitude of the update will be `learning_rate * grad` where `grad` corresponds to the multi-dimensional gradient (i.e. the partial derivative of `var1` and `var2` found in the `partial_dict` attribute of `loss`).
```python
>>> var1
0.8 ({'var1': 1})
>>> var2
1.6 ({'var2': 1})
```
Alternatively, a user can call the `minimize()` method to update multiple steps. As specified in the documentation for `minimize()`, the user may specify a series of learning rates to vary with each step.
```python
>>> opt.miminize(loss, var_list[var1, var2], learning_rates=np.linspace(0.1,0.01,100), steps=100)
```
If converged after `steps` steps, this will yield the optimziation results. If this has not converged, a warning will be raised to the user.
```python
>>> var1
0.0 ({'var1': 1})
>>> var2
0.0 ({'var2': 1})
```

#### Example 2: Optimization for regression


## Software organization
The software implementation for Version 2.0 of our software is presented below.  Thus, this organization is subject to change in future released versions of *boomdiff*.

```
cs107-FinalProject/
	LICENSE.txt
    setup.py
    requirements.txt
	boomdiff/
		__init__.py
		autodiff.py
        optimizer/
            __init__.py
            gradient_descent.py
	docs/
	    milestone1.ipynb
	    milestone2.ipynb
	    documentation.md
	tests/
		__init__.py
		test_unit.py
        test_suite.py
```

There are two main modules, both of which sit within the *boomdiff* package structure. The main functionality is encapsulated in the `optimize` subpackage, as this provides full access to our suite of optimization tools. Those tools, which are described in detail above and through the details on implementation below,, will not be reviewed here.  Additonally, the implemented module, `autodiff.py` provides support for automatic differentiation of a scalar functions of a many variables of elementary functions and operations (detailed in the 'Implementation' section below). 

Our test suite lives in the `tests` directory of the main directory structure. These unit tests currently cover 99% of the *boomdiff* functionality. Additionally, each of the overloaded operations and static methods implemented in the AD class have docstring tests to support additional testing and usability. Our repository is currently being tracked by Travis CI, integrated with CodeCov, to provide support for continuous integration of our library.

As described above, our package is distributed through two separate avenues. First, the package is installable via PyPi. Second, our packaging is distributed via a clone of this GitHub repository. We’re not planning to use the framework since our package is not going to be a web application. Also, the package should be basic enough and contain all required documentation. 

## Implementation
#### optimize
*Summary*: The *optimize* subpackage of *boomdiff* performs optimization of arbitrary objective functions, according to the user's specifications. This section reviews the superclass, `Optimizer`, as well as the important methods. Following that, we review the subclasses, which inherit from this `Optimizer` superclass. Unless users wish to implement additional optimization methods not included at this time in *boomdiff*, these subclasses will provide full functionality to optimize the objective function. Developers who wish to create additional methods should inherit from the superclass. Please contact Team Boomeraang if you wish to contibute additional optimizations or have suggestions for additional methodologies! The landscape of optimization algorithms is ever-changing, and we would love your feedback and contributions.




class `Optimizer(learning_rate=0.1)`: This is the base class for all optimizers. *This class should only be called by developers who wish to implement optimization algorithms not included in boomdiff*. Instead of instantiating this class directly, users should call specific subclasses, e.g. `boomdiff.optimize.SGD` or `boomdiff.optimize.BGD`.

| Arguments | Type        | Status              | Description                                                  |
| --------- | ----------- | ------------------- | ------------------------------------------------------------ |
| `learning_rate`     | float, int  | optional, default 0.1| Learning rate of the optimizer, controlling the step size. Smaller learning rates imply smaller steps in each direction |

| Attribute      | Type  | Description                                                  |
| -------------- | ----- | ------------------------------------------------------------ |
| `lr`     | float | Learning rate at current step; comes from constructor method              |
| `iterations` | dict  | Number of iterations of the optimization algorithm. Please note that this attribute has been left public, but is not intended to be widely used. The primary intended use is developers who encounter issues with the package and wish to debug the specific algorithm |

- `step(loss, var_list, learning_rate=None)`: Implements a single step of the optimization algorithm. Since each methodology included here is an iterative method, this will be called within the application of the gradient. *Developer note: this function may be used for debugging purposes, especially as it relates to application of a pre-specified gradient. Second, if the gradient is calculated outside of the optimization library, this step method may be useful for singular updates*.
| Arguments | Type        | Status              | Description                                                  |
| --------- | ----------- | ------------------- | ------------------------------------------------------------ |
| `loss` | callable   | required | Objective function to be optimized, takes no arguments and must output an AD object. |
| `var_list` | list       | required | List of variables to be updated. Each element in list must be a pre-instantiated AD instance. Prevents accidental, nonsensical calls as non-AD objects cannot be optimized. |
| `learning_rate` | int; float | optional | Learning rate can be re-specified here; alternatively, advanced users can specify a learning rate schedule as a sequence structure. |

- `minimize(loss, var_list, steps=100, learning_rates=None)`: Minimizes the supplied loss function relative to the user-designated `var_list`. At default, optimization will be performed over a maximum of 100 steps. This can be changed by the user, but is set relatively low to avoid unintentional computational time without specific direction from the user.

| Arguments | Type        | Status              | Description                                                  |
| --------- | ----------- | ------------------- | ------------------------------------------------------------ |
| `loss` | callable   | required | Objective function to be optimized, takes no arguments and must output an AD object. |
| `var_list` | list       | required | List of variables to be updated. Each element in list must be a pre-instantiated AD instance. Prevents accidental, nonsensical calls as non-AD objects cannot be optimized. |
| `steps` | int | optional; default 100 | Number of gradient steps to apply within optimization algorithm |
|`learning_rate` | int; float | optional | Learning rate can be re-specified here; alternatively, advanced users can specify a learning rate schedule as a sequence structure. |

#### autodiff
*Summary*: The automatic differentiation module for *boomdiff* is implemented through an object oriented class, AD. This class represents the object to be differentiated, and can be combined in functions. While the actual object must be called separately, e.g. AD(2.0), this can be wrapped into a single line characterized by either a function or lambda function in Python. The remainder of this section reviews the attributes and methods associated with this class. Please note, while we have added all operations that work for this class via operator overloading, those methods have not been entirely enumerated here. For more information, please see the [Python Data Model](https://docs.python.org/3/reference/datamodel.html), which describes the desired function of each of these operations.

class `AD(eval_pt, der_dict)`:

| Arguments  | Type       | Status   | Description                                                  |
| ---------- | ---------- | -------- | ------------------------------------------------------------ |
| `eval_pt`  | float, int | Required | Point to evaluate the object at; raises error if not float or int. |
| `der_dict` | str, dict  | Optional | f string, this should be the name of the variable for the associated `eval_pt`. Otherwise, should be a dictionary in format `{'x1': 2.0}` where 'x1' is the name of the variable and 2.0 is the partial derivative. Default behavior for string is to set partial derivative seed vector to be 1. If not passed at all, sets variable to 'x1' and partial derivative to one. |
The attributes and methods associated with the class are as follows:

| Attribute      | Type  | Description                                                  |
| -------------- | ----- | ------------------------------------------------------------ |
| `func_val`     | float | Current value of the AD object as a real number              |
| `partial_dict` | dict  | This dictionary will store the partial derivatives. Each key corresponds to the variable (in a multiple variable function). Note that the multiple variable functionality has not been fully implemented and tested |

The methods for this class can be broadly grouped into three subsets: helper methods, operator overloading, and static methods.

**Helper instance methods**

- `name()`: This function returns the name of all variables contained within the AD object. Equivalent to returning the keys of the partial dictionary
	
- ` value()`: Returns the current function value of an AD object.
	
- `ders()`:  Returns the partial derivative dictionary of the specified object.
	
- `evaluate()`: Returns the function value and derivative dictionary as a tuple, in that order.
	
- `set_params(att, val)`: Set a given attribute for the AD object. May be used to reset the partial derivative dictionary to zero or to otherwise clear the function.

| Arguments | Type             | Status   | Description                                                  |
| --------- | ---------------- | -------- | ------------------------------------------------------------ |
| `att`     | string           | required | Must be one of 'func_val' or a dictionary. If `func_val`, will reset the function value at a given time. Otherwise will overwrite the partial derivative dictionary. |
| `val`     | float, int, dict | required | If `func_val`, must be one of float or int. Otherwise must be dictionary specified according to conditions in constructor. |

**Overloaded operations**
- `__add__(self, other)`: Performs addition between AD objects and AD object and non-AD object (must be int or float).
	- `func_val` for `self` and `other` are added. If `other` not an AD object, float or int added to `func_val`.
	- `partial_dict`: Partial derivatives are added within a common key. If one key does not exist in the other dictionary, the returned object will contain both.
```python
>>> print(AD(3.0, {'x1':1}) + AD(2.0, {'x2':1}))
5.0 ({'x1': 1, 'x2': 1''})
```
- `__radd__(self, other)`: See documentation for `__add__`.
- `__sub__(self, other)`: Like addition, if both objects are AD objects, will subtract function values arithmetically, and will substract partial derivatives for elements of each `partial_dict` with the same key.
```python
>>> print(AD(3.0, {'x1':1}) - AD(2.0, {'x2':1}))
1.0 ({'x1': 1, 'x2': -1''})
```
- `__rsubb__(self, other)`: See documentation for `__sub__`.
- `__mul__(self, other)`: Overload multiplication operation (`*`). For AD objects, multiplies function values and applies product rule to partial derivatives. Thus, for each key, the new partial derivative is:
	- `self.partial_dict[key]*other.func_val + other.partial_dict[key]*self.func_val`
```python
>>> print(AD(2.0, {'x1':1}) * AD(2.0, {'x2':1}))
4.0 ({'x1': 1, 'x2': 1''})
```
-`__rmul__(self, other)`: See documentation for `__mul__`.
- `__truediv__(self, other)`: Operation overloading for (`/`). Divides function values and applies quotient rule within a partial dictionary key. Note that if function_val for `other` is zero, will raise a `DivideZeroError`. If `other` not an AD object, will treat value as function value, dividing function value for self as well as partial dictionary entries.
```python
>>> print(AD(6.0, {'x1':2}) / AD(2.0, {'x1':1}))
3.0 ({'x1': -0.5})
```
- `__rtruediv__(self, other)`: See documentatio for `__truediv__`.
- `__pow__(self, other)`: Implements operator overloading for power symbol (`**`). For `other` AD objects, will apply power within `func_val`. Partial derivatives will be calculated according to the [generalized power rule](https://en.wikipedia.org/wiki/Differentiation_rules#Generalized_power_rule). If `other` int or float, will apply simple power rule, though this is implemented as special case of generalized rule. 
```python
>>> a = AD(2, {'a': 1})
>>> b = AD(4, {'b': 1})
>>> f3 = a**b
>>> print(f3.func_val, f3.partial_dict)
16 {'a': 32.0, 'b': 11.090354888959125}
```
- `__rpow__(self, other)`: See documentation for `__pow__`.
- `__neg__(self)`: Applies negation to AD objects. Calls `-1*self`.

**Static methods**
-`sin(x)`: Accessed via `AD.sin(x)`. Calls sine function on `x`. If `x` is AD object, will apply sine to function value and return partial derivative of `cos(x)`. Otherwise, performs similarly to `numpy.sin` for int and float types.
```python
>>> x2 = AD.sin(np.pi)
>>> print(x2)
1.2246467991473532e-16
```
-`cos(x)`: Accessed via `AD.cos(x)`. Calls cosine function on `x`. Like `sin(x)`, if `x` is an AD object, will apply cosine to function value and `-sin(p)` to each partial derivative `p`. If `x` not an AD object, will perform similarly to `numpy.cos()`.
```python
>>> x = AD.cos(np.pi)
>>> print(x)
-1.0
```
- `tan(x)`: Accessed via `AD.tan(x)`. Calls tangent function on `x`, applying to function value and partial derivative of tangent fuction. If `x` not an AD object, will perform similarly to `numpy.tan(x)`.
```python
>>> y = AD.tan(np.pi)
>>> print(y.round(1))
-0.0
```
- `arcsin(x)`: Accessed via `AD.arcsin(x)`. Applies inverse sine function to `x` function value and partial derivatives. See [here](https://ocw.mit.edu/courses/mathematics/18-01sc-single-variable-calculus-fall-2010/1.-differentiation/part-b-implicit-differentiation-and-inverse-functions/session-15-implicit-differentiation-and-inverse-functions/MIT18_01SCF10_Ses15c.pdf) for more information.
```python
>>> x = AD(0.25, {'x1': 1.})
>>> print(AD.arcsin(x))
0.25268025514207865 ({'x1': 1.0327955589886444})
```
-`arccos(x)`: Accessed via `AD.arccos(x)`. Applies inverse cosine function to `x` function value and partial derivatives. See [here](https://math.berkeley.edu/~peyam/Math1AFa10/Arccos.pdf) for more information.
```python
>>> x = AD(0.25, {'x1': 1.})
>>> print(AD.arccos(x))
1.318116071652818 ({'x1': -1.0327955589886444})
```
-`arctan(x)`: Accessed via `AD.arctan(x)`. Applies inverse tangent function to `x` function value and partial derivatives. See [here](https://math.berkeley.edu/~peyam/Math1AFa10/Arccos.pdf) for more information on calculation of partial derivatives. If `x` not an AD object, performs operation as `numpy.arctan(x)`.
```python
>>> x = AD(0.25, {'x1': 1.})
>>> print(AD.arctan(x))
0.24497866312686414 ({'x1': 0.9411764705882353})
```
-`sqrt(x)`: Applies square root to `x` object. Please note that this is not a fully flexible operation and thus cannot take any root. For other roots, `r`, please apply via `** (1/r)`.
```python
>>> x1 = AD(1.0, {'x1': 1.0})
>>> f1 = AD.sqrt(x1)
>>> print(f1.func_val, f1.partial_dict)
1.0 {'x1': 0.5}
```
-`log(x, base-numpy.e)`: Applies logarithm of `base` to `x`. Note that by default, will apply natural logarithm. If `x` is not an AD object, will perform similarly to `numpy.log`.
```python
>>> x1 = AD(np.e**2, {'x1': 1.})
>>> f0 = AD.log(x1)
>>> print(f0)
2.0 ({'x1': 0.1353352832366127})
```
- `sinh(x)`: Applies hyperbolic sine function to `x`. If `x` not an AD object, then performs similarly to `numpy.sinh`. For more information on derivative of `sinh(x)`, see [here](https://www.math24.net/derivatives-hyperbolic-functions/).
```python
>>> x1 = AD(0.0, {'x1': 1.0})
>>> f1 = AD.sinh(x1)
>>> print(f1)
0.0 ({'x1': 1.0})
```
-`cosh(x)`: Applies hyperbolic cosine transformation to `x`. If `x` is not an AD object, then performs similarly to `numpy.cosh`. For more information on the calculation of partial derivatives of `sinh(x)`, please see [here](https://www.math24.net/derivatives-hyperbolic-functions/).
```python
>>> x1 = AD(0.0, {'x1': 1.0})
>>> f1 = AD.cosh(x1)
>>> print(f1)
1.0 ({'x1': -0.0})
```
-`tanh(x)`: Applies hyperbolic tangent transformation to `x`. If `x` is not an AD object, performs similarly to `numpy.tanh`. For more information on the calculation of partial derivatives of `tanh(x)`, please see [here](https://www.math24.net/derivatives-hyperbolic-functions/).
```python
>>> x1 = AD(0.0, {'x1': 1.0})
>>> f1 = AD.tanh(x1)
>>> print(f1)
0.0 ({'x1': 1.0})
```
- `exp(x)`: Applies exponential function to `x`, in a similar fashion to calling `numpy.e ** x`. Function constructed using `numpy.e` and `__rpow__`. Please see documentation of those functions for futher details.
```python
>>> x = AD(2, {'x1': 1.})
>>> print(AD.exp(x))
7.3890560989306495 ({'x1': 7.3890560989306495})
```
- `logistic(x, x_0=0, k=1, L=1)`: Calls logistic function (also known as sigmoid function) on x in the fully general case (see [here](https://en.wikipedia.org/wiki/Logistic_function) for distinction). Default values produce $\frac{1}{1+ e^{-x}}$, fully general case is: $\frac{L}{1+ e^{-k(x-x_0)}}$.
| Arguments | Type        | Status              | Description                                                  |
| --------- | ----------- | ------------------- | ------------------------------------------------------------ |
| `x_0`     | float, int  | optional, default 0 | Value of the midpoint of the logistic function, which will be set to zero by default. In the case of regression tasks, this is commonly set to be the center of the distribution for a certain set of predictors. |
| `k`       | float, int, | optional; default 1 | Logistic growth rate of curve. Lower values of `k` imply a steeper curve. |
| `L`       | float, int  | optional, default 0 | Maximum value for the entirety of the logistic function.     |
```python
>>> x = AD(1.5)
>>> print(AD.logistic(x))
0.8175744761936437 ({'x1': 0.14914645207033284})
```
- External dependencies:
    - [NumPy](https://numpy.org/)
    - [itertools](https://docs.python.org/3/library/itertools.html)

## Future
We see two primary directions for continued development on this project: implementing a user-friendly approach and/or targeting a specific scientific community.  While these directions are not necessarily mutually exclusive (both could be built on the same optimization package), the next steps and direction of the development process are likely fairly separate. In terms of usability, we believe that one promising direction would be to include a class or set of functions meant to parse string versions of common functions, which would likely significantly increase the accessibility of our package. We believe this could be a particular comaprative advantage of our package to currently existing optimization libraries, namely the general functionality of major libraries such as PyTorch and TensorFlow. As a small team without any specialists in either automatic differentiation or optimization, our package will likely not compete with the performance of a PyTorch or TensorFlow. That being said, one particular weakness of those packages is that the optimized performance and object-oriented structure may be confusing to users less familiar with Python. Less familiarity with Python should not stop users from efficiently performing optimization, though -- these tasks are too central to too much reasearch for that.

A second direction our package could plausibly go would be to adapt the first proposal into a subfield-specific optimization library. This may go hand-in-hand with the user-friendly nature of the package, but would likely be more targeted in terms of application and functionality. For example, there may be less utility in adapting the package to address the needs of machine learning practitioners, as most are likely comfortable with an existing optimization library. For social and physical sciences less traditionally connected to computing, however, we believe that this could be a promising direction. One example of a feature that we might add if, for example, our package was targeted at  statiscians is the ability to perform importance sampling within the application of a gradient. For mode-finding algorithms that feature intractable integrals which cannot be discarded. To optimize complex likelihood and posterior distributions, this functionality may facilitate ease of use for that particular 'client'. As noted, one advantage of our object-oriented structure is modularity, which may allow us to pursue both of these avenues. In the interest of limited resources, though, they may not both be feasible over the medium-term.