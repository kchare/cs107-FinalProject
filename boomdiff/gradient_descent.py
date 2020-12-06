"""
Interface for Gradient Descent (GD)
"""

__all__ = ['GD']

import numpy as np

from autodiff import AD
from optimizer import Optimizer

class GD(Optimizer):
    """
    Gradient descent (GD) optimizer subclass

    Usage:
    ```python
    >>> # Instantiate a GD optimizer
    >>> opt = GD(learning_rate=0.1)

    >>> # loss is the objective function that we want to minimize
    >>> # 'loss' should be a callable that takes no arguments and output an AD instance
    >>> # should only use operations supported by AD class
    >>> loss = lambda: var1**2 + var2**2

    >>> # initialize the variables for the objective function
    >>> # make sure the name string in the dict is corresponding with the variable name
    >>> var1 = AD(100, {'var1': 1})
    >>> var2 = AD(1, {'var2': 1})

    >>> # Call step method, update the variables for one step, to minimize the loss value
    >>> # var_list are the variable lists that you want to update
    >>> # It can be part of the variables in loss callable.
    >>> # The step method will update the variables defined before
    >>> opt.step(loss, var_list=[var1, var2])

    >>> # The var1 and var2 will be updated by -learning_rate * grad(loss)
    >>> print(var1, var2)
    >>> 80.0 ({'var1': 1}) 0.8 ({'var2': 1})

    >>> # Or you can call minimize method, to update multiple steps
    >>> # With user-specified learning_rate series
    >>> opt.minimize(loss, [var1, var2], steps=100)

    >>> # This will give some final optimization results if converged
    >>> print(var1, var2)
    1.6296287810675902e-08 ({'var1': 1}) 1.6296287810675902e-10 ({'var2': 1})
    ```
    """

    def __init__(self, learning_rate=0.1, **kwargs):

        super().__init__(learning_rate)

    def _apply_gradient(self, loss, var_list, grad_dict):
        """
        Apply the gradient to update variables GD algorithm

        x_i = x_i - learning_rate * grad(loss(x_i))
        """
        for var in var_list:
            grad = grad_dict[var.name()[0]]
            print("grad: ", grad)
            if grad > var.func_val * 10**6:
                raise ValueError("Gradient is too large: potential numerical instability")
            var.func_val -= self.lr * grad
            print("var.func_val: ", var.func_val)




# opt = GD(learning_rate=0.1)
# var1 = AD(9, {'var1': 1})
# var2 = AD(4, {'var2': 1})
# loss = lambda: var1**2 +var2**2
# opt.step(loss, var_list=[var1, var2])
# print(var1, var2)
#
# opt.minimize(loss, [var1, var2], steps=100)
# # #
# # # # opt.step(loss, [var1])
# # # # print(var1, var2)
# # # # opt.step(loss, [var1])
# # # # print(var1, var2)
# # # # opt.step(loss, [var1])
# print(var1, var2)
# print(opt.loss_val_for_step)
# print(opt.iterations)
# opt.plot_loss_func()
