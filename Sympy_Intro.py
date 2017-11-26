# coding: utf-8

# # Warmup - Introduction to SymPy
# This lab exercise uses the [SymPy](http://www.sympy.org/en/index.html) symbolic math library to model constraints in the problem.  To do that, we will use symbols (`sympy.Symbol`), functions (`sympy.Function`), and expressions (`sympy.Expr`) from sympy, and then we'll combine the function and expression classes to make constraints -- evaluatable symbolic functions.
# 
# In this warmup, you will be introduced to the syntax and functionality of SymPy:
# - [Example 1](#Example-1:-Symbols): Creating [symbols](http://docs.sympy.org/dev/modules/core.html#module-sympy.core.symbol)
# - [Example 2](#Example-2:-Expressions): Creating & manipulating [expressions](http://docs.sympy.org/dev/modules/core.html#id16) with [arithmetic & logical operators](http://docs.sympy.org/dev/modules/core.html#sympy-core)
# - [Example 3](#Example-3:-Symbolic-substitution-and-expression-evaluation): Symbolic [substitution & evaluation](http://docs.sympy.org/dev/modules/core.html#subs)
# - [Exercises](#SymPy-Exercises): Creating & manipulating constraints & [functions](http://docs.sympy.org/dev/modules/functions/index.html)
# 
# (See a list of common "gotchas" for sympy in their documentation: http://docs.sympy.org/dev/gotchas.html)
# 
# Start by reading and running the example cells, then complete the steps in the warmup cell.

# In[1]:

import matplotlib as mpl
import matplotlib.pyplot as plt

from util import constraint
from IPython.display import display
from sympy import *

init_printing()

# ## Example 1: Symbols
# **Sympy provides the `Symbol` class to create symbolic variables.  Create individual symbols by calling the constructor with a symbol name.**  (Tip: Use the `display()` function to pretty-print symbolic terms.)

# In[3]:

x = Symbol('x')
display(x)

# **You can also create symbols from an iterable sequence using the `symbols()` function.**

# In[4]:

i, j, k = symbols(['i', 'j', 'k'])  # use implicit unpacking to associate multiple symbols with variables
display((i, j, k))

# **`symbols()` can also create subscripted sequences of symbolic variables.**

# In[5]:

X = symbols("X:3")
display(X)

# ## Example 2: Expressions
# 
# **A symbol is the most basic expression.**  (Tip: Jupyter notebooks show information about objects
# using the `?` magic function)

# In[7]:

x = Symbol('x')
# get_ipython().magic('pinfo x')
display(x)

# **You can also define expressions with relations between symbols.** (However, notice that expressions have no _names_...)

# In[8]:

x, y = symbols('x y')
or_relation = x | y
# get_ipython().magic('pinfo or_relation')
display(or_relation)

# **Also, not all operators can be used in expressions.  The equal sign (=) performs assignment in python, so it cannot be used to make expressions.  Using `=` assigns a new python variable to an existing reference.**

# In[9]:

x, y = symbols("x y")
y = x  # now y references the same symbolic object as x
display(y)  # display(y) == x  ??!

# **Use `sympy.Eq` for symbolic equality expressions:** (Tip: there are lots of expressions in the [sympy docs](http://docs.sympy.org/dev/modules/core.html#sympy-core))

# In[10]:

x, z = symbols("x z")
display(Eq(z, x))

# **Sympy overloads standard python operators so that arithmetic and logical expressions can be constructed directly between symbolic objects.**

# In[11]:

x, y, z = symbols("x y z")
display([x ** 2, x - y, Ne(x, y), (~x & y & z)])

# ## Example 3: Symbolic substitution and expression evaluation
# 
# **Given an original expression...**

# In[12]:

x, y, z = symbols("x y z")
relation = Eq(x, y)
display(relation)

# **Symbolic variables can be replaced by other variables, or by concrete values.** (Tip: use positional arguments in the `subs()` method to replace one symbol)

# In[13]:

display(relation.subs(x, z))  # Use positional arguments to substitute a single symbol

# **But keep in mind that substitution returns a _copy_ of the expression -- it doesn't operate in-place.**  (Tip: as a result, you can use substitution on one expression bound to generic variables to generate new instances bound to specific variables.)
# 
# Look at what happens when we bind new variables to our equality relation:

# In[14]:

a = symbols("a:5")
b = symbols("b:5")
display([relation.subs({x: _a, y: _b}) for _a, _b in zip(a, b)])

# **Symbol substitution returns an expression.** (Recall that Symbols _are_ expressions).

# In[15]:

print(type(relation), type(relation.subs(x, z)))
print(type(relation) == type(relation.subs(x, z)))

# **But substituting values for all symbols returns a value type.** (Tip: You can substitute multiple symbols in the `subs()` command by providing a mapping (dict) from current symbols to new symbols or values.)

# In[16]:

print(type(relation), type(relation.subs({x: 0, y: 1})))
print(type(relation) != type(relation.subs({x: 0, y: 1})))

# ## Example 4: Constraints
# 
# **Constraints are a construct of this lab exercise (not part of sympy) that combine symbolic Functions with Expressions for evaluation. The `constraint()` function (defined in the `util` module) takes a name and an expression and returns a "named expression" -- a constraint.**

# In[17]:

x, y = symbols(['x', 'y'])
sameAs = constraint("SameAs", Eq(x, y))
display(sameAs)

# **Constraints are evaluated using the .subs method, just like an expression. If the resulting
# expression has unbound (free) symbols, then the result is a new constraint.**

# In[ ]:

display(sameAs.subs(x, 0), type(sameAs.subs(x, 0)))

# **If the resulting expression has no free symbols, then the result is only the evaluated expression.**

# In[ ]:

display(sameAs.subs({x: 0, y: 0}), type(sameAs.subs({x: 0, y: 0})))

# ## SymPy Exercises
# Complete the following exercises to check your understanding of sympy symbols, expressions, and constraints:

# **Question 1:** Create an array of subscripted symbols A0, A1, A2 stored in a variable named `A`

# In[18]:

A = symbols('A:3')

# test for completion
assert (len(A) == 3)
assert (all([type(v) == Symbol for v in A]))
print("All tests passed!")

# **Question 2:** Create an expression E with two generic symbols (e.g., "a" and "b", etc.) that represents logical XOR

# In[20]:

E = symbols('a') ^ symbols('b')

# test for completion
_vars = E.free_symbols
assert (len(_vars) == 2)
xor_table = {(0, 0): False, (0, 1): True, (1, 0): True, (1, 1): False}
assert (all(E.subs(zip(_vars, vals)) == truth for vals, truth in xor_table.items()))
print("All tests passed!")

# **Question 3:** Create a constraint MaxAbsDiff with three generic arguments to test abs(a - b) < c, and create a copy of the constraint such that it tests abs(A[0] - A[1]) < A[2] from Q1

# In[51]:

var('a b c')
maxAbsDiff = Abs(a - b) < c
maxAbsDiff_copy = maxAbsDiff.subs({a: A[0], b: A[1], c: A[2]})

display(maxAbsDiff_copy)

inputs = {(0, 6, 7): True, (6, 0, 7): True, (7, 6, 0): False}
items = list(inputs.items())
v1,t1 = items[0]

subs = list(zip(A[:3], v1))
t = maxAbsDiff_copy.subs(subs)
print(t)

items_ = (maxAbsDiff_copy.subs(zip(A[:3], vals)) == truth for vals, truth in inputs.items())

# test for completion
assert (maxAbsDiff.free_symbols != maxAbsDiff_copy.free_symbols)
assert (len(maxAbsDiff_copy.free_symbols) == len(maxAbsDiff_copy.args))
assert (all(items_))
print("All tests passed!")

# **(Optional) Question 4:** Create a constraint AllDiff accepting the symbols in A as arguments, returning True if they are all different, and False if any pair is the same

# In[ ]:

allDiff = None

inputs = (([0, 1, 2], True), ([1, 1, 1], False), ([0, 1, 1], False))
assert (all(allDiff.subs(zip(A, vals)) == truth for vals, truth in inputs))
print("All tests passed!")
