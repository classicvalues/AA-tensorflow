# Copyright 2015 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Note: Elementwise binary operations in TensorFlow follow [numpy-style
broadcasting](http://docs.scipy.org/doc/numpy/user/basics.broadcasting.html).

## Arithmetic Operators

TensorFlow provides several operations that you can use to add basic arithmetic
operators to your graph.

@@add
@@subtract
@@multiply
@@scalar_mul
@@div
@@divide
@@truediv
@@floordiv
@@realdiv
@@truncatediv
@@floor_div
@@truncatemod
@@floormod
@@mod
@@cross

## Basic Math Functions

TensorFlow provides several operations that you can use to add basic
mathematical functions to your graph.

@@add_n
@@abs
@@negative
@@sign
@@reciprocal
@@square
@@round
@@sqrt
@@rsqrt
@@pow
@@exp
@@expm1
@@log
@@log1p
@@ceil
@@floor
@@maximum
@@minimum
@@cos
@@sin
@@lbeta
@@tan
@@acos
@@asin
@@atan
@@lgamma
@@digamma
@@erf
@@erfc
@@squared_difference
@@igamma
@@igammac
@@zeta
@@polygamma
@@betainc
@@rint

## Matrix Math Functions

TensorFlow provides several operations that you can use to add linear algebra
functions on matrices to your graph.

@@diag
@@diag_part
@@trace
@@transpose

@@eye
@@matrix_diag
@@matrix_diag_part
@@matrix_band_part
@@matrix_set_diag
@@matrix_transpose

@@matmul

@@norm
@@matrix_determinant
@@matrix_inverse
@@cholesky
@@cholesky_solve
@@matrix_solve
@@matrix_triangular_solve
@@matrix_solve_ls
@@qr
@@self_adjoint_eig
@@self_adjoint_eigvals
@@svd


## Tensor Math Function

TensorFlow provides operations that you can use to add tensor functions to your
graph.

@@tensordot


## Complex Number Functions

TensorFlow provides several operations that you can use to add complex number
functions to your graph.

@@complex
@@complex_abs
@@conj
@@imag
@@real

## Fourier Transform Functions

TensorFlow provides several operations that you can use to add discrete
Fourier transform functions to your graph.

@@fft
@@ifft
@@fft2d
@@ifft2d
@@fft3d
@@ifft3d

## Reduction

TensorFlow provides several operations that you can use to perform
common math computations that reduce various dimensions of a tensor.

@@reduce_sum
@@reduce_prod
@@reduce_min
@@reduce_max
@@reduce_mean
@@reduce_all
@@reduce_any
@@reduce_logsumexp
@@count_nonzero

@@accumulate_n

@@einsum

## Scan

TensorFlow provides several operations that you can use to perform scans
(running totals) across one axis of a tensor.

@@cumsum
@@cumprod

## Segmentation

TensorFlow provides several operations that you can use to perform common
math computations on tensor segments.
Here a segmentation is a partitioning of a tensor along
the first dimension, i.e. it  defines a mapping from the first dimension onto
`segment_ids`. The `segment_ids` tensor should be the size of
the first dimension, `d0`, with consecutive IDs in the range `0` to `k`,
where `k<d0`.
In particular, a segmentation of a matrix tensor is a mapping of rows to
segments.

For example:

```python
c = tf.constant([[1,2,3,4], [-1,-2,-3,-4], [5,6,7,8]])
tf.segment_sum(c, tf.constant([0, 0, 1]))
  ==>  [[0 0 0 0]
        [5 6 7 8]]
```

@@segment_sum
@@segment_prod
@@segment_min
@@segment_max
@@segment_mean

@@unsorted_segment_sum

@@sparse_segment_sum
@@sparse_segment_mean
@@sparse_segment_sqrt_n


## Sequence Comparison and Indexing

TensorFlow provides several operations that you can use to add sequence
comparison and index extraction to your graph. You can use these operations to
determine sequence differences and determine the indexes of specific values in
a tensor.

@@argmin
@@argmax

@@setdiff1d
@@where
@@unique

@@edit_distance

@@invert_permutation
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
from six.moves import xrange  # pylint: disable=redefined-builtin

from tensorflow.python.framework import common_shapes
from tensorflow.python.framework import constant_op
from tensorflow.python.framework import dtypes
from tensorflow.python.framework import graph_util
from tensorflow.python.framework import ops
from tensorflow.python.framework import sparse_tensor
from tensorflow.python.framework import tensor_shape
from tensorflow.python.ops import array_ops
from tensorflow.python.ops import gen_control_flow_ops
from tensorflow.python.ops import gen_data_flow_ops
from tensorflow.python.ops import gen_math_ops
from tensorflow.python.ops import gen_sparse_ops
from tensorflow.python.ops import gen_state_ops
from tensorflow.python.ops import state_ops
# go/tf-wildcard-import
# pylint: disable=wildcard-import
from tensorflow.python.ops.gen_math_ops import *
# pylint: enable=wildcard-import
from tensorflow.python.util import compat


# Aliases for some automatically-generated names.
linspace = gen_math_ops.lin_space


# pylint: disable=redefined-builtin
# TODO(aselle): deprecate arg_max
def argmax(input, axis=None, name=None, dimension=None):
  if dimension is not None:
    if axis is not None:
      raise ValueError("Cannot specify both 'axis' and 'dimension'")
    axis = dimension
  return gen_math_ops.arg_max(input, axis, name)


argmax.__doc__ = (gen_math_ops.arg_max.__doc__.replace(
    "dimensions", "axes").replace("dimension", "axis"))


# TODO(aselle:deprecate arg_min)
def argmin(input, axis=None, name=None, dimension=None):
  if dimension is not None:
    if axis is not None:
      raise ValueError("Cannot specify both 'axis' and 'dimension'")
    axis = dimension
  return gen_math_ops.arg_min(input, axis, name)


argmin.__doc__ = (gen_math_ops.arg_min.__doc__.replace(
    "dimensions", "axes").replace("dimension", "axis"))

# pylint: enable=redefined-builtin


# pylint: disable=anomalous-backslash-in-string,protected-access
def abs(x, name=None):
  """Computes the absolute value of a tensor.

  Given a tensor of real numbers `x`, this operation returns a tensor
  containing the absolute value of each element in `x`. For example, if x is
  an input element and y is an output element, this operation computes
  \\\\(y = |x|\\\\).

  Args:
    x: A `Tensor` or `SparseTensor` of type `float32`, `float64`, `int32`, or
      `int64`.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` or `SparseTensor` the same size and type as `x` with absolute
      values.
  """
  with ops.name_scope(name, "Abs", [x]) as name:
    if isinstance(x, sparse_tensor.SparseTensor):
      if x.values.dtype in (dtypes.complex64, dtypes.complex128):
        x_abs = gen_math_ops._complex_abs(
            x.values, Tout=x.values.dtype.real_dtype, name=name)
        return sparse_tensor.SparseTensor(
            indices=x.indices, values=x_abs, dense_shape=x.dense_shape)
      x_abs = gen_math_ops._abs(x.values, name=name)
      return sparse_tensor.SparseTensor(
          indices=x.indices, values=x_abs, dense_shape=x.dense_shape)
    else:
      x = ops.convert_to_tensor(x, name="x")
      if x.dtype in (dtypes.complex64, dtypes.complex128):
        return gen_math_ops._complex_abs(x, Tout=x.dtype.real_dtype, name=name)
      return gen_math_ops._abs(x, name=name)


def divide(x, y, name=None):
  """Computes Python style division of `x` by `y`."""
  with ops.name_scope(name, "Divide", [x]) as name:
    return x / y


# Make Python Aliases
multiply = gen_math_ops.mul
subtract = gen_math_ops.sub
negative = gen_math_ops.neg


def neg(x, name=None):
  """Computes numerical negative value element-wise.

  I.e., \\(y = -x\\).

  Args:
    x: A `Tensor` or `SparseTensor`. Must be one of the following types: `half`,
      `float32`, `float64`, `int32`, `int64`, `complex64`, `complex128`.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` or `SparseTensor`, respectively. Has the same type as `x`.
  """
  with ops.name_scope(name, "Neg", [x]) as name:
    if isinstance(x, sparse_tensor.SparseTensor):
      x_neg = gen_math_ops.neg(x.values, name=name)
      return sparse_tensor.SparseTensor(
          indices=x.indices, values=x_neg, dense_shape=x.dense_shape)
    else:
      return gen_math_ops.neg(x, name=name)


def sign(x, name=None):
  """Returns an element-wise indication of the sign of a number.

  `y = sign(x) = -1` if `x < 0`; 0 if `x == 0`; 1 if `x > 0`.

  For complex numbers, `y = sign(x) = x / |x|` if `x != 0`, otherwise `y = 0`.

  Args:
    x: A `Tensor` or `SparseTensor`. Must be one of the following types: `half`,
      `float32`, `float64`, `int32`, `int64`, `complex64`, `complex128`.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` or `SparseTensor`, respectively. Has the same type as `x`.
  """
  with ops.name_scope(name, "Sign", [x]) as name:
    if isinstance(x, sparse_tensor.SparseTensor):
      x_sign = gen_math_ops.sign(x.values, name=name)
      return sparse_tensor.SparseTensor(
          indices=x.indices, values=x_sign, dense_shape=x.dense_shape)
    else:
      return gen_math_ops.sign(x, name=name)


def square(x, name=None):
  """Computes square of x element-wise.

  I.e., \\(y = x * x = x^2\\).

  Args:
    x: A `Tensor` or `SparseTensor`. Must be one of the following types: `half`,
      `float32`, `float64`, `int32`, `int64`, `complex64`, `complex128`.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` or `SparseTensor`. Has the same type as `x`.
  """
  with ops.name_scope(name, "Square", [x]) as name:
    if isinstance(x, sparse_tensor.SparseTensor):
      x_square = gen_math_ops.square(x.values, name=name)
      return sparse_tensor.SparseTensor(
          indices=x.indices, values=x_square, dense_shape=x.dense_shape)
    else:
      return gen_math_ops.square(x, name=name)


def sqrt(x, name=None):
  """Computes square root of x element-wise.

  I.e., \\(y = \sqrt{x} = x^{1/2}\\).

  Args:
    x: A `Tensor` or `SparseTensor`. Must be one of the following types: `half`,
      `float32`, `float64`, `complex64`, `complex128`.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` or `SparseTensor`, respectively. Has the same type as `x`.
  """
  with ops.name_scope(name, "Sqrt", [x]) as name:
    if isinstance(x, sparse_tensor.SparseTensor):
      x_sqrt = gen_math_ops.sqrt(x.values, name=name)
      return sparse_tensor.SparseTensor(
          indices=x.indices, values=x_sqrt, dense_shape=x.dense_shape)
    else:
      return gen_math_ops.sqrt(x, name=name)


def erf(x, name=None):
  """Computes the Gauss error function of `x` element-wise.

  Args:
    x: A `Tensor` of `SparseTensor`. Must be one of the following types: `half`,
      `float32`, `float64`.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` or `SparseTensor`, respectively. Has the same type as `x`.
  """
  with ops.name_scope(name, "Erf", [x]) as name:
    if isinstance(x, sparse_tensor.SparseTensor):
      x_erf = gen_math_ops.erf(x.values, name=name)
      return sparse_tensor.SparseTensor(
          indices=x.indices, values=x_erf, dense_shape=x.dense_shape)
    else:
      return gen_math_ops.erf(x, name=name)


def complex_abs(x, name=None):
  r"""Computes the complex absolute value of a tensor.

  Given a tensor `x` of complex numbers, this operation returns a tensor of type
  `float32` or `float64` that is the absolute value of each element in `x`. All
  elements in `x` must be complex numbers of the form \\(a + bj\\). The
  absolute value is computed as \\( \sqrt{a^2 + b^2}\\).

  For example:

  ```
  # tensor 'x' is [[-2.25 + 4.75j], [-3.25 + 5.75j]]
  tf.complex_abs(x) ==> [5.25594902, 6.60492229]
  ```

  Args:
    x: A `Tensor` of type `complex64` or `complex128`.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` of type `float32` or `float64`.
  """
  return gen_math_ops._complex_abs(x, Tout=x.dtype.real_dtype, name=name)


def scalar_mul(scalar, x):
  """Multiplies a scalar times a `Tensor` or `IndexedSlices` object.

  Intended for use in gradient code which might deal with `IndexedSlices`
  objects, which are easy to multiply by a scalar but more expensive to
  multiply with arbitrary tensors.

  Args:
    scalar: A 0-D scalar `Tensor`. Must have known shape.
    x: A `Tensor` or `IndexedSlices` to be scaled.

  Returns:
    `scalar * x` of the same type (`Tensor` or `IndexedSlices`) as `x`.

  Raises:
    ValueError: if scalar is not a 0-D `scalar`.
  """
  scalar = ops.convert_to_tensor(
      scalar, dtype=x.dtype.base_dtype, name="scalar")
  shape = scalar.get_shape()
  if shape.ndims == 0:
    if isinstance(x, ops.IndexedSlices):
      return ops.IndexedSlices(scalar * x.values, x.indices, x.dense_shape)
    else:
      return scalar * x
  else:
    raise ValueError("Only scalar multiply works, got shape %s" % shape)


def pow(x, y, name=None):
  """Computes the power of one value to another.

  Given a tensor `x` and a tensor `y`, this operation computes \\\\(x^y\\\\) for
  corresponding elements in `x` and `y`. For example:

  ```
  # tensor 'x' is [[2, 2], [3, 3]]
  # tensor 'y' is [[8, 16], [2, 3]]
  tf.pow(x, y) ==> [[256, 65536], [9, 27]]
  ```

  Args:
    x: A `Tensor` of type `float32`, `float64`, `int32`, `int64`, `complex64`,
     or `complex128`.
    y: A `Tensor` of type `float32`, `float64`, `int32`, `int64`, `complex64`,
     or `complex128`.
    name: A name for the operation (optional).

  Returns:
    A `Tensor`.
  """
  with ops.name_scope(name, "Pow", [x]) as name:
    return gen_math_ops._pow(x, y, name=name)


# pylint: disable=redefined-builtin,redefined-outer-name
def complex(real, imag, name=None):
  r"""Converts two real numbers to a complex number.

  Given a tensor `real` representing the real part of a complex number, and a
  tensor `imag` representing the imaginary part of a complex number, this
  operation returns complex numbers elementwise of the form \\(a + bj\\), where
  *a* represents the `real` part and *b* represents the `imag` part.

  The input tensors `real` and `imag` must have the same shape.

  For example:

  ```
  # tensor 'real' is [2.25, 3.25]
  # tensor `imag` is [4.75, 5.75]
  tf.complex(real, imag) ==> [[2.25 + 4.75j], [3.25 + 5.75j]]
  ```

  Args:
    real: A `Tensor`. Must be one of the following types: `float32`,
      `float64`.
    imag: A `Tensor`. Must have the same type as `real`.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` of type `complex64` or `complex128`.
  """
  real = ops.convert_to_tensor(real, name="real")
  imag = ops.convert_to_tensor(imag, name="imag")
  with ops.name_scope(name, "Complex", [real, imag]) as name:
    input_types = (real.dtype, imag.dtype)
    if input_types == (dtypes.float64, dtypes.float64):
      Tout = dtypes.complex128
    elif input_types == (dtypes.float32, dtypes.float32):
      Tout = dtypes.complex64
    else:
      raise TypeError("real and imag have incorrect types: "
                      "{} {}".format(real.dtype.name,
                                     imag.dtype.name))
    return gen_math_ops._complex(real, imag, Tout=Tout, name=name)


def real(input, name=None):
  r"""Returns the real part of a complex number.

  Given a tensor `input` of complex numbers, this operation returns a tensor of
  type `float32` or `float64` that is the real part of each element in `input`.
  All elements in `input` must be complex numbers of the form \\(a + bj\\),
  where *a* is the real part returned by this operation and *b* is the
  imaginary part.

  For example:

  ```
  # tensor 'input' is [-2.25 + 4.75j, 3.25 + 5.75j]
  tf.real(input) ==> [-2.25, 3.25]
  ```

  If `input` is already real, it is returned unchanged.

  Args:
    input: A `Tensor`. Must have numeric type.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` of type `float32` or `float64`.
  """
  with ops.name_scope(name, "Real", [input]) as name:
    real_dtype = input.dtype.real_dtype
    if input.dtype.base_dtype == real_dtype:
      return input
    return gen_math_ops.real(input, Tout=real_dtype, name=name)


def imag(input, name=None):
  """Returns the imaginary part of a complex number.

  Given a tensor `input` of complex numbers, this operation returns a tensor of
  type `float32` or `float64` that is the imaginary part of each element in
  `input`. All elements in `input` must be complex numbers of the form \\(a +
  bj\\), where *a* is the real part and *b* is the imaginary part returned by
  this operation.

  For example:

  ```
  # tensor 'input' is [-2.25 + 4.75j, 3.25 + 5.75j]
  tf.imag(input) ==> [4.75, 5.75]
  ```

  Args:
    input: A `Tensor`. Must be one of the following types: `complex64`,
      `complex128`.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` of type `float32` or `float64`.
  """
  with ops.name_scope(name, "Imag", [input]) as name:
    return gen_math_ops.imag(input, Tout=input.dtype.real_dtype, name=name)


# pylint: enable=redefined-outer-name,redefined-builtin


def round(x, name=None):
  """Rounds the values of a tensor to the nearest integer, element-wise.

  Rounds half to even.  Also known as bankers rounding. If you want to round
  according to the current system rounding mode use tf::cint.
  For example:

  ```python
  # 'a' is [0.9, 2.5, 2.3, 1.5, -4.5]
  tf.round(a) ==> [ 1.0, 2.0, 2.0, 2.0, -4.0 ]
  ```

  Args:
    x: A `Tensor` of type `float32` or `float64`.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` of same shape and type as `x`.
  """
  x = ops.convert_to_tensor(x, name="x")
  if x.dtype.is_integer:
    return x
  else:
    return gen_math_ops.round(x, name=name)


def cast(x, dtype, name=None):
  """Casts a tensor to a new type.

  The operation casts `x` (in case of `Tensor`) or `x.values`
  (in case of `SparseTensor`) to `dtype`.

  For example:

  ```python
  # tensor `a` is [1.8, 2.2], dtype=tf.float
  tf.cast(a, tf.int32) ==> [1, 2]  # dtype=tf.int32
  ```

  Args:
    x: A `Tensor` or `SparseTensor`.
    dtype: The destination type.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` or `SparseTensor` with same shape as `x`.

  Raises:
    TypeError: If `x` cannot be cast to the `dtype`.
  """
  base_type = dtypes.as_dtype(dtype).base_dtype
  with ops.name_scope(name, "Cast", [x]) as name:
    if isinstance(x, sparse_tensor.SparseTensor):
      values_cast = cast(x.values, base_type, name=name)
      return sparse_tensor.SparseTensor(x.indices, values_cast, x.dense_shape)
    else:
      # TODO(touts): Handle what Josh said.
      #
      # Could return ops.convert_to_tensor(x, dtype=dtype, ...)  here, but that
      # allows some conversions that cast() can't do, e.g.  casting numbers to
      # strings.
      x = ops.convert_to_tensor(x, name="x")
      if x.dtype.base_dtype == base_type:
        return x
      return gen_math_ops.cast(x, base_type, name=name)


def saturate_cast(value, dtype, name=None):
  """Performs a safe saturating cast of `value` to `dtype`.

  This function casts the input to `dtype` without applying any scaling.  If
  there is a danger that values would over or underflow in the cast, this op
  applies the appropriate clamping before the cast.

  Args:
    value: A `Tensor`.
    dtype: The desired output `DType`.
    name: A name for the operation (optional).

  Returns:
    `value` safely cast to `dtype`.
  """
  # When casting to a type with smaller representable range, clamp.
  # Note that this covers casting to unsigned types as well.
  with ops.name_scope(name, "saturate_cast", [value]) as name:
    value = ops.convert_to_tensor(value, name="value")
    dtype = dtypes.as_dtype(dtype).base_dtype
    if value.dtype.min < dtype.min:
      value = gen_math_ops.maximum(
          value,
          ops.convert_to_tensor(
              dtype.min, dtype=value.dtype, name="min"))
    if value.dtype.max > dtype.max:
      value = gen_math_ops.minimum(
          value,
          ops.convert_to_tensor(
              dtype.max, dtype=value.dtype, name="max"))
    return cast(value, dtype, name=name)


def to_float(x, name="ToFloat"):
  """Casts a tensor to type `float32`.

  Args:
    x: A `Tensor` or `SparseTensor`.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` or `SparseTensor` with same shape as `x` with type `float32`.

  Raises:
    TypeError: If `x` cannot be cast to the `float32`.
  """
  return cast(x, dtypes.float32, name=name)


def to_double(x, name="ToDouble"):
  """Casts a tensor to type `float64`.

  Args:
    x: A `Tensor` or `SparseTensor`.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` or `SparseTensor` with same shape as `x` with type `float64`.

  Raises:
    TypeError: If `x` cannot be cast to the `float64`.
  """
  return cast(x, dtypes.float64, name=name)


def to_int32(x, name="ToInt32"):
  """Casts a tensor to type `int32`.

  Args:
    x: A `Tensor` or `SparseTensor`.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` or `SparseTensor` with same shape as `x` with type `int32`.

  Raises:
    TypeError: If `x` cannot be cast to the `int32`.
  """
  return cast(x, dtypes.int32, name=name)


def to_int64(x, name="ToInt64"):
  """Casts a tensor to type `int64`.

  Args:
    x: A `Tensor` or `SparseTensor`.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` or `SparseTensor` with same shape as `x` with type `int64`.

  Raises:
    TypeError: If `x` cannot be cast to the `int64`.
  """
  return cast(x, dtypes.int64, name=name)


def to_bfloat16(x, name="ToBFloat16"):
  """Casts a tensor to type `bfloat16`.

  Args:
    x: A `Tensor` or `SparseTensor`.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` or `SparseTensor` with same shape as `x` with type `bfloat16`.

  Raises:
    TypeError: If `x` cannot be cast to the `bfloat16`.
  """
  return cast(x, dtypes.bfloat16, name=name)


ops.Tensor._override_operator("__neg__", gen_math_ops.neg)
ops.Tensor._override_operator("__abs__", abs)
# __invert__ corresponds to the ~ operator.  Here we follow the numpy convention
# ~ marks an elementwise bit-wise inverse.  This is only implemented for boolean
# tensors and will throw a TypeError if used on nonboolean arrays
ops.Tensor._override_operator("__invert__", gen_math_ops.logical_not)


def _OverrideBinaryOperatorHelper(func, op_name, clazz_object=ops.Tensor):
  """Register operators with different tensor and scalar versions.

  If `clazz_object` is `SparseTensor`, assumes `func` takes `(sp_indices,
  sp_values, sp_shape, dense)` and outputs `(new_sp_values)`.

  Args:
    func: the operator
    op_name: name of the operator being overridden
    clazz_object: class to override for.  Either `Tensor` or `SparseTensor`.
  """

  def binary_op_wrapper(x, y):
    with ops.name_scope(None, op_name, [x, y]) as name:
      if not isinstance(y, sparse_tensor.SparseTensor):
        y = ops.convert_to_tensor(y, dtype=x.dtype.base_dtype, name="y")
      return func(x, y, name=name)

  def binary_op_wrapper_sparse(sp_x, y):
    with ops.name_scope(None, op_name, [sp_x, y]) as name:
      y = ops.convert_to_tensor(y, dtype=sp_x.dtype.base_dtype, name="y")
      return sparse_tensor.SparseTensor(
          sp_x.indices,
          func(
              sp_x.indices, sp_x.values, sp_x.dense_shape, y, name=name),
          sp_x.dense_shape)

  def r_binary_op_wrapper(y, x):
    with ops.name_scope(None, op_name, [x, y]) as name:
      x = ops.convert_to_tensor(x, dtype=y.dtype.base_dtype, name="x")
      return func(x, y, name=name)

  # Propagate func.__doc__ to the wrappers
  try:
    doc = func.__doc__
  except AttributeError:
    doc = None
  binary_op_wrapper.__doc__ = doc
  r_binary_op_wrapper.__doc__ = doc
  binary_op_wrapper_sparse.__doc__ = doc

  if clazz_object is ops.Tensor:
    clazz_object._override_operator("__%s__" % op_name, binary_op_wrapper)
    del binary_op_wrapper
    clazz_object._override_operator("__r%s__" % op_name, r_binary_op_wrapper)
    del r_binary_op_wrapper
  else:
    clazz_object._override_operator("__%s__" % op_name,
                                    binary_op_wrapper_sparse)
    del binary_op_wrapper_sparse


# Conversion table for __truediv__.  None entries mean no conversion required.
_TRUEDIV_TABLE = {
    dtypes.uint8: dtypes.float32,
    dtypes.int8: dtypes.float32,
    dtypes.uint16: dtypes.float32,
    dtypes.int16: dtypes.float32,
    dtypes.int32: dtypes.float64,
    dtypes.int64: dtypes.float64,
    dtypes.float16: None,
    dtypes.float32: None,
    dtypes.float64: None,
    dtypes.complex64: None,
    dtypes.complex128: None,
}


# NOTE: the support of "sparse (true)div dense" is currently not baked in into
# "tf.(true_)div()".  Until such an API decision is made, the supported usage is
# to explicitly use the "/" operator to invoke either truediv or div.
def _sparse_dense_truediv(sp_indices, sp_values, sp_shape, y, name=None):
  """Internal helper function for 'sp_t / dense_t'."""
  with ops.name_scope(name, "truediv",
                      [sp_indices, sp_values, sp_shape, y]) as name:
    sp_values = ops.convert_to_tensor(sp_values, name="sp_values")
    y = ops.convert_to_tensor(y, name="y")
    x_dtype = sp_values.dtype.base_dtype
    y_dtype = y.dtype.base_dtype
    if x_dtype != y_dtype:
      raise TypeError("x and y must have the same dtype, got %r != %r" %
                      (x_dtype, y_dtype))
    try:
      dtype = _TRUEDIV_TABLE[x_dtype]
    except KeyError:
      raise TypeError("Invalid dtype %r in __truediv__" % x_dtype)
    if dtype is not None:
      sp_values = cast(sp_values, dtype)
      y = cast(y, dtype)
    return gen_sparse_ops.sparse_dense_cwise_div(
        sp_indices, sp_values, sp_shape, y, name=name)


def _truediv_python3(x, y, name=None):
  with ops.name_scope(name, "truediv", [x, y]) as name:
    x = ops.convert_to_tensor(x, name="x")
    y = ops.convert_to_tensor(y, name="y")
    x_dtype = x.dtype.base_dtype
    y_dtype = y.dtype.base_dtype
    if x_dtype != y_dtype:
      raise TypeError("x and y must have the same dtype, got %r != %r" %
                      (x_dtype, y_dtype))
    try:
      dtype = _TRUEDIV_TABLE[x_dtype]
    except KeyError:
      raise TypeError("Invalid dtype %r in __truediv__" % x_dtype)
    if dtype is not None:
      x = cast(x, dtype)
      y = cast(y, dtype)
    return gen_math_ops._real_div(x, y, name=name)


def _div_python2(x, y, name=None):
  """Divide two values using Python 2 semantics. Used for Tensor.__div__.

  Args:
    x: `Tensor` numerator of real numeric type.
    y: `Tensor` denominator of real numeric type.
    name: A name for the operation (optional).
  Returns:
    `x / y` returns the quotient of x and y.
  """

  with ops.name_scope(name, "div", [x, y]) as name:
    x = ops.convert_to_tensor(x, name="x")
    y = ops.convert_to_tensor(y, name="y", dtype=x.dtype.base_dtype)
    x_dtype = x.dtype.base_dtype
    y_dtype = y.dtype.base_dtype
    if x_dtype != y_dtype:
      raise TypeError("x and y must have the same dtype, got %r != %r" %
                      (x_dtype, y_dtype))
    if x_dtype.is_floating or x_dtype.is_complex:
      return gen_math_ops._real_div(x, y, name=name)
    else:
      return gen_math_ops._floor_div(x, y, name=name)


def truediv(x, y, name=None):
  """Divides x / y elementwise (using Python 3 division operator semantics).

  NOTE: Prefer using the Tensor operator or tf.divide which obey Python
  division operator semantics.

  This function forces Python 3 division operator semantics where all integer
  arguments are cast to floating types first.   This op is generated by normal
  `x / y` division in Python 3 and in Python 2.7 with
  `from __future__ import division`.  If you want integer division that rounds
  down, use `x // y` or `tf.floordiv`.

  `x` and `y` must have the same numeric type.  If the inputs are floating
  point, the output will have the same type.  If the inputs are integral, the
  inputs are cast to `float32` for `int8` and `int16` and `float64` for `int32`
  and `int64` (matching the behavior of Numpy).

  Args:
    x: `Tensor` numerator of numeric type.
    y: `Tensor` denominator of numeric type.
    name: A name for the operation (optional).

  Returns:
    `x / y` evaluated in floating point.

  Raises:
    TypeError: If `x` and `y` have different dtypes.
  """
  return _truediv_python3(x, y, name)


def div(x, y, name=None):
  """Divides x / y elementwise (using Python 2 division operator semantics).

  NOTE: Prefer using the Tensor division operator or tf.divide which obey Python
  division operator semantics.

  This function divides `x` and `y`, forcing Python 2.7 semantics. That is,
  if one of `x` or `y` is a float, then the result will be a float.
  Otherwise, the output will be an integer type. Flooring semantics are used
  for integer division.

  Args:
    x: `Tensor` numerator of real numeric type.
    y: `Tensor` denominator of real numeric type.
    name: A name for the operation (optional).
  Returns:
    `x / y` returns the quotient of x and y.
  """
  return _div_python2(x, y, name)


# TODO(aselle): This should be removed
mod = gen_math_ops._floor_mod


# TODO(aselle): Deprecate this once all internal functionality uses
# tf.truncatediv
def floordiv(x, y, name=None):
  """Divides `x / y` elementwise, rounding toward the most negative integer.

  The same as `tf.div(x,y)` for integers, but uses `tf.floor(tf.div(x,y))` for
  floating point arguments so that the result is always an integer (though
  possibly an integer represented as floating point).  This op is generated by
  `x // y` floor division in Python 3 and in Python 2.7 with
  `from __future__ import division`.

  Note that for efficiency, `floordiv` uses C semantics for negative numbers
  (unlike Python and Numpy).

  `x` and `y` must have the same type, and the result will have the same type
  as well.

  Args:
    x: `Tensor` numerator of real numeric type.
    y: `Tensor` denominator of real numeric type.
    name: A name for the operation (optional).

  Returns:
    `x / y` rounded down (except possibly towards zero for negative integers).

  Raises:
    TypeError: If the inputs are complex.
  """
  with ops.name_scope(name, "floordiv", [x, y]) as name:
    return gen_math_ops._floor_div(x, y, name=name)


realdiv = gen_math_ops._real_div
truncatediv = gen_math_ops._truncate_div
# TODO(aselle): Rename this to floordiv when we can.
floor_div = gen_math_ops._floor_div
truncatemod = gen_math_ops._truncate_mod
floormod = gen_math_ops._floor_mod


def _mul_dispatch(x, y, name=None):
  """Dispatches cwise mul for "Dense*Dense" and "Dense*Sparse"."""
  is_tensor_y = isinstance(y, ops.Tensor)
  if is_tensor_y:
    return gen_math_ops.mul(x, y, name=name)
  else:
    assert isinstance(y, sparse_tensor.SparseTensor)  # Case: Dense * Sparse.
    new_vals = gen_sparse_ops.sparse_dense_cwise_mul(y.indices, y.values,
                                                     y.dense_shape, x, name)
    return sparse_tensor.SparseTensor(y.indices, new_vals, y.dense_shape)


# NOTE(aselle): When integer division is added for sparse_dense_cwise,
# div, truediv, and floordiv should be delegated appropriately for
# Python sematnics, analogous to dense cwise tensor operations.
_OverrideBinaryOperatorHelper(gen_sparse_ops.sparse_dense_cwise_div, "div",
                              sparse_tensor.SparseTensor)
_OverrideBinaryOperatorHelper(_sparse_dense_truediv, "truediv",
                              sparse_tensor.SparseTensor)
_OverrideBinaryOperatorHelper(gen_sparse_ops.sparse_dense_cwise_mul, "mul",
                              sparse_tensor.SparseTensor)

_OverrideBinaryOperatorHelper(gen_math_ops.add, "add")
_OverrideBinaryOperatorHelper(gen_math_ops.sub, "sub")
_OverrideBinaryOperatorHelper(_mul_dispatch, "mul")
_OverrideBinaryOperatorHelper(_div_python2, "div")
_OverrideBinaryOperatorHelper(_truediv_python3, "truediv")
_OverrideBinaryOperatorHelper(floordiv, "floordiv")
# TODO(aselle): Switch mod to floor_mod when ready
# _OverrideBinaryOperatorHelper(gen_math_ops.floor_mod, "mod")
_OverrideBinaryOperatorHelper(gen_math_ops._floor_mod, "mod")
_OverrideBinaryOperatorHelper(pow, "pow")


def logical_xor(x, y, name="LogicalXor"):
  """x ^ y = (x | y) & ~(x & y)."""
  # TODO(alemi) Make this a cwise op if people end up relying on it.
  return gen_math_ops.logical_and(
      gen_math_ops.logical_or(x, y),
      gen_math_ops.logical_not(gen_math_ops.logical_and(x, y)),
      name=name)


_OverrideBinaryOperatorHelper(gen_math_ops.logical_and, "and")
_OverrideBinaryOperatorHelper(gen_math_ops.logical_or, "or")
_OverrideBinaryOperatorHelper(logical_xor, "xor")

ops.Tensor._override_operator("__lt__", gen_math_ops.less)
ops.Tensor._override_operator("__le__", gen_math_ops.less_equal)
ops.Tensor._override_operator("__gt__", gen_math_ops.greater)
ops.Tensor._override_operator("__ge__", gen_math_ops.greater_equal)


def range(start, limit=None, delta=1, dtype=None, name="range"):
  """Creates a sequence of numbers.

  Creates a sequence of numbers that begins at `start` and extends by
  increments of `delta` up to but not including `limit`.

  The dtype of the resulting tensor is inferred from the inputs unless
  it is provided explicitly.

  Like the Python builtin `range`, `start` defaults to 0, so that
  `range(n) = range(0, n)`.

  For example:

  ```python
  # 'start' is 3
  # 'limit' is 18
  # 'delta' is 3
  tf.range(start, limit, delta) ==> [3, 6, 9, 12, 15]

  # 'start' is 3
  # 'limit' is 1
  # 'delta' is -0.5
  tf.range(start, limit, delta) ==> [3, 2.5, 2, 1.5]

  # 'limit' is 5
  tf.range(limit) ==> [0, 1, 2, 3, 4]
  ```

  Args:
    start: A 0-D `Tensor` (scalar). Acts as first entry in the range if
      `limit` is not None; otherwise, acts as range limit and first entry
      defaults to 0.
    limit: A 0-D `Tensor` (scalar). Upper limit of sequence,
      exclusive. If None, defaults to the value of `start` while the first
      entry of the range defaults to 0.
    delta: A 0-D `Tensor` (scalar). Number that increments
      `start`. Defaults to 1.
    dtype: The type of the elements of the resulting tensor.
    name: A name for the operation. Defaults to "range".

  Returns:
    An 1-D `Tensor` of type `dtype`.

  @compatibility(numpy)
  Equivalent to np.arange
  @end_compatibility
  """
  if limit is None:
    start, limit = 0, start

  with ops.name_scope(name, "Range", [start, limit, delta]) as name:
    start = ops.convert_to_tensor(start, dtype=dtype, name="start")
    limit = ops.convert_to_tensor(limit, dtype=dtype, name="limit")
    delta = ops.convert_to_tensor(delta, dtype=dtype, name="delta")

    # infer dtype if not explicitly provided
    if dtype is None:
      dtype_hierarchy = [
          dtypes.int32, dtypes.int64, dtypes.float32, dtypes.float64
      ]
      assert all(arg.dtype in dtype_hierarchy for arg in [start, limit, delta])
      inferred_dtype = max([arg.dtype for arg in [start, limit, delta]],
                           key=dtype_hierarchy.index)

      start = cast(start, inferred_dtype)
      limit = cast(limit, inferred_dtype)
      delta = cast(delta, inferred_dtype)

    return gen_math_ops._range(start, limit, delta, name=name)


# Reduction operations
def _ReductionDims(x, axis, reduction_indices):
  """Returns range(0, rank(x)) if reduction_indices is None."""
  # TODO(aselle): Remove this after deprecation
  if reduction_indices is not None:
    if axis is not None:
      raise ValueError("Can't specify both axis' and 'reduction_indices'.")
    axis = reduction_indices
  if axis is not None:
    return axis
  else:
    # Fast path: avoid creating Rank and Range ops if ndims is known.
    if isinstance(x, ops.Tensor) and x.get_shape().ndims is not None:
      return constant_op.constant(
          np.arange(x.get_shape().ndims), dtype=dtypes.int32)
    if (isinstance(x, sparse_tensor.SparseTensor) and
        x.dense_shape.get_shape().is_fully_defined()):
      rank = x.dense_shape.get_shape()[0].value  # sparse.dense_shape is 1-D.
      return constant_op.constant(np.arange(rank), dtype=dtypes.int32)

    # Otherwise, we rely on Range and Rank to do the right thing at run-time.
    return range(0, array_ops.rank(x))


def reduce_sum(input_tensor,
               axis=None,
               keep_dims=False,
               name=None,
               reduction_indices=None):
  """Computes the sum of elements across dimensions of a tensor.

  Reduces `input_tensor` along the dimensions given in `axis`.
  Unless `keep_dims` is true, the rank of the tensor is reduced by 1 for each
  entry in `axis`. If `keep_dims` is true, the reduced dimensions
  are retained with length 1.

  If `axis` has no entries, all dimensions are reduced, and a
  tensor with a single element is returned.

  For example:

  ```python
  # 'x' is [[1, 1, 1]
  #         [1, 1, 1]]
  tf.reduce_sum(x) ==> 6
  tf.reduce_sum(x, 0) ==> [2, 2, 2]
  tf.reduce_sum(x, 1) ==> [3, 3]
  tf.reduce_sum(x, 1, keep_dims=True) ==> [[3], [3]]
  tf.reduce_sum(x, [0, 1]) ==> 6
  ```

  Args:
    input_tensor: The tensor to reduce. Should have numeric type.
    axis: The dimensions to reduce. If `None` (the default),
      reduces all dimensions.
    keep_dims: If true, retains reduced dimensions with length 1.
    name: A name for the operation (optional).
    reduction_indices: The old (deprecated) name for axis.

  Returns:
    The reduced tensor.

  @compatibility(numpy)
  Equivalent to np.sum
  @end_compatibility
  """
  return gen_math_ops._sum(
      input_tensor,
      _ReductionDims(input_tensor, axis, reduction_indices),
      keep_dims,
      name=name)


def count_nonzero(input_tensor,
                  axis=None,
                  keep_dims=False,
                  dtype=dtypes.int64,
                  name=None,
                  reduction_indices=None):
  """Computes number of nonzero elements across dimensions of a tensor.

  Reduces `input_tensor` along the dimensions given in `axis`.
  Unless `keep_dims` is true, the rank of the tensor is reduced by 1 for each
  entry in `axis`. If `keep_dims` is true, the reduced dimensions
  are retained with length 1.

  If `axis` has no entries, all dimensions are reduced, and a
  tensor with a single element is returned.

  **NOTE** Floating point comparison to zero is done by exact floating point
  equality check.  Small values are **not** rounded to zero for purposes of
  the nonzero check.

  For example:

  ```python
  # 'x' is [[0, 1, 0]
  #         [1, 1, 0]]
  tf.count_nonzero(x) ==> 3
  tf.count_nonzero(x, 0) ==> [1, 2, 0]
  tf.count_nonzero(x, 1) ==> [1, 2]
  tf.count_nonzero(x, 1, keep_dims=True) ==> [[1], [2]]
  tf.count_nonzero(x, [0, 1]) ==> 3
  ```

  Args:
    input_tensor: The tensor to reduce. Should be of numeric type, or `bool`.
    axis: The dimensions to reduce. If `None` (the default),
      reduces all dimensions.
    keep_dims: If true, retains reduced dimensions with length 1.
    dtype: The output dtype; defaults to `tf.int64`.
    name: A name for the operation (optional).
    reduction_indices: The old (deprecated) name for axis.

  Returns:
    The reduced tensor (number of nonzero values).
  """
  with ops.name_scope(name, "count_nonzero", [input_tensor]):
    input_tensor = ops.convert_to_tensor(input_tensor, name="input_tensor")
    zero = input_tensor.dtype.as_numpy_dtype()
    return cast(
        reduce_sum(
            # int64 reduction happens on GPU
            to_int64(gen_math_ops.not_equal(input_tensor, zero)),
            axis=axis,
            keep_dims=keep_dims,
            reduction_indices=reduction_indices),
        dtype=dtype)


def reduce_mean(input_tensor,
                axis=None,
                keep_dims=False,
                name=None,
                reduction_indices=None):
  """Computes the mean of elements across dimensions of a tensor.

  Reduces `input_tensor` along the dimensions given in `axis`.
  Unless `keep_dims` is true, the rank of the tensor is reduced by 1 for each
  entry in `axis`. If `keep_dims` is true, the reduced dimensions
  are retained with length 1.

  If `axis` has no entries, all dimensions are reduced, and a
  tensor with a single element is returned.

  For example:

  ```python
  # 'x' is [[1., 1.]
  #         [2., 2.]]
  tf.reduce_mean(x) ==> 1.5
  tf.reduce_mean(x, 0) ==> [1.5, 1.5]
  tf.reduce_mean(x, 1) ==> [1.,  2.]
  ```

  Args:
    input_tensor: The tensor to reduce. Should have numeric type.
    axis: The dimensions to reduce. If `None` (the default),
      reduces all dimensions.
    keep_dims: If true, retains reduced dimensions with length 1.
    name: A name for the operation (optional).
    reduction_indices: The old (deprecated) name for axis.

  Returns:
    The reduced tensor.

  @compatibility(numpy)
  Equivalent to np.mean
  @end_compatibility
  """
  return gen_math_ops._mean(
      input_tensor,
      _ReductionDims(input_tensor, axis, reduction_indices),
      keep_dims,
      name=name)


def reduce_prod(input_tensor,
                axis=None,
                keep_dims=False,
                name=None,
                reduction_indices=None):
  """Computes the product of elements across dimensions of a tensor.

  Reduces `input_tensor` along the dimensions given in `axis`.
  Unless `keep_dims` is true, the rank of the tensor is reduced by 1 for each
  entry in `axis`. If `keep_dims` is true, the reduced dimensions
  are retained with length 1.

  If `axis` has no entries, all dimensions are reduced, and a
  tensor with a single element is returned.

  Args:
    input_tensor: The tensor to reduce. Should have numeric type.
    axis: The dimensions to reduce. If `None` (the default),
      reduces all dimensions.
    keep_dims: If true, retains reduced dimensions with length 1.
    name: A name for the operation (optional).
    reduction_indices: The old (deprecated) name for axis.

  Returns:
    The reduced tensor.

  @compatibility(numpy)
  Equivalent to np.prod
  @end_compatibility
  """
  return gen_math_ops._prod(
      input_tensor,
      _ReductionDims(input_tensor, axis, reduction_indices),
      keep_dims,
      name=name)


def reduce_min(input_tensor,
               axis=None,
               keep_dims=False,
               name=None,
               reduction_indices=None):
  """Computes the minimum of elements across dimensions of a tensor.

  Reduces `input_tensor` along the dimensions given in `axis`.
  Unless `keep_dims` is true, the rank of the tensor is reduced by 1 for each
  entry in `axis`. If `keep_dims` is true, the reduced dimensions
  are retained with length 1.

  If `axis` has no entries, all dimensions are reduced, and a
  tensor with a single element is returned.

  Args:
    input_tensor: The tensor to reduce. Should have numeric type.
    axis: The dimensions to reduce. If `None` (the default),
      reduces all dimensions.
    keep_dims: If true, retains reduced dimensions with length 1.
    name: A name for the operation (optional).
    reduction_indices: The old (deprecated) name for axis.

  Returns:
    The reduced tensor.

  @compatibility(numpy)
  Equivalent to np.min
  @end_compatibility
  """
  return gen_math_ops._min(
      input_tensor,
      _ReductionDims(input_tensor, axis, reduction_indices),
      keep_dims,
      name=name)


def reduce_max(input_tensor,
               axis=None,
               keep_dims=False,
               name=None,
               reduction_indices=None):
  """Computes the maximum of elements across dimensions of a tensor.

  Reduces `input_tensor` along the dimensions given in `axis`.
  Unless `keep_dims` is true, the rank of the tensor is reduced by 1 for each
  entry in `axis`. If `keep_dims` is true, the reduced dimensions
  are retained with length 1.

  If `axis` has no entries, all dimensions are reduced, and a
  tensor with a single element is returned.

  Args:
    input_tensor: The tensor to reduce. Should have numeric type.
    axis: The dimensions to reduce. If `None` (the default),
      reduces all dimensions.
    keep_dims: If true, retains reduced dimensions with length 1.
    name: A name for the operation (optional).
    reduction_indices: The old (deprecated) name for axis.

  Returns:
    The reduced tensor.

  @compatibility(numpy)
  Equivalent to np.max
  @end_compatibility
  """
  return gen_math_ops._max(
      input_tensor,
      _ReductionDims(input_tensor, axis, reduction_indices),
      keep_dims,
      name=name)


def reduce_all(input_tensor,
               axis=None,
               keep_dims=False,
               name=None,
               reduction_indices=None):
  """Computes the "logical and" of elements across dimensions of a tensor.

  Reduces `input_tensor` along the dimensions given in `axis`.
  Unless `keep_dims` is true, the rank of the tensor is reduced by 1 for each
  entry in `axis`. If `keep_dims` is true, the reduced dimensions
  are retained with length 1.

  If `axis` has no entries, all dimensions are reduced, and a
  tensor with a single element is returned.

  For example:

  ```python
  # 'x' is [[True,  True]
  #         [False, False]]
  tf.reduce_all(x) ==> False
  tf.reduce_all(x, 0) ==> [False, False]
  tf.reduce_all(x, 1) ==> [True, False]
  ```

  Args:
    input_tensor: The boolean tensor to reduce.
    axis: The dimensions to reduce. If `None` (the default),
      reduces all dimensions.
    keep_dims: If true, retains reduced dimensions with length 1.
    name: A name for the operation (optional).
    reduction_indices: The old (deprecated) name for axis.

  Returns:
    The reduced tensor.

  @compatibility(numpy)
  Equivalent to np.all
  @end_compatibility
  """
  return gen_math_ops._all(
      input_tensor,
      _ReductionDims(input_tensor, axis, reduction_indices),
      keep_dims,
      name=name)


def reduce_any(input_tensor,
               axis=None,
               keep_dims=False,
               name=None,
               reduction_indices=None):
  """Computes the "logical or" of elements across dimensions of a tensor.

  Reduces `input_tensor` along the dimensions given in `axis`.
  Unless `keep_dims` is true, the rank of the tensor is reduced by 1 for each
  entry in `axis`. If `keep_dims` is true, the reduced dimensions
  are retained with length 1.

  If `axis` has no entries, all dimensions are reduced, and a
  tensor with a single element is returned.

  For example:

  ```python
  # 'x' is [[True,  True]
  #         [False, False]]
  tf.reduce_any(x) ==> True
  tf.reduce_any(x, 0) ==> [True, True]
  tf.reduce_any(x, 1) ==> [True, False]
  ```

  Args:
    input_tensor: The boolean tensor to reduce.
    axis: The dimensions to reduce. If `None` (the default),
      reduces all dimensions.
    keep_dims: If true, retains reduced dimensions with length 1.
    name: A name for the operation (optional).
    reduction_indices: The old (deprecated) name for axis.

  Returns:
    The reduced tensor.

  @compatibility(numpy)
  Equivalent to np.any
  @end_compatibility
  """
  return gen_math_ops._any(
      input_tensor,
      _ReductionDims(input_tensor, axis, reduction_indices),
      keep_dims,
      name=name)


def reduce_logsumexp(input_tensor,
                     axis=None,
                     keep_dims=False,
                     name=None,
                     reduction_indices=None):
  """Computes log(sum(exp(elements across dimensions of a tensor))).

  Reduces `input_tensor` along the dimensions given in `axis`.
  Unless `keep_dims` is true, the rank of the tensor is reduced by 1 for each
  entry in `axis`. If `keep_dims` is true, the reduced dimensions
  are retained with length 1.

  If `axis` has no entries, all dimensions are reduced, and a
  tensor with a single element is returned.

  This function is more numerically stable than log(sum(exp(input))). It avoids
  overflows caused by taking the exp of large inputs and underflows caused by
  taking the log of small inputs.

  For example:

  ```python
  # 'x' is [[0, 0, 0]]
  #         [0, 0, 0]]
  tf.reduce_logsumexp(x) ==> log(6)
  tf.reduce_logsumexp(x, 0) ==> [log(2), log(2), log(2)]
  tf.reduce_logsumexp(x, 1) ==> [log(3), log(3)]
  tf.reduce_logsumexp(x, 1, keep_dims=True) ==> [[log(3)], [log(3)]]
  tf.reduce_logsumexp(x, [0, 1]) ==> log(6)
  ```

  Args:
    input_tensor: The tensor to reduce. Should have numeric type.
    axis: The dimensions to reduce. If `None` (the default),
      reduces all dimensions.
    keep_dims: If true, retains reduced dimensions with length 1.
    name: A name for the operation (optional).
    reduction_indices: The old (deprecated) name for axis.

  Returns:
    The reduced tensor.
  """
  with ops.name_scope(name, "ReduceLogSumExp", [input_tensor]) as name:
    my_max = array_ops.stop_gradient(
        reduce_max(
            input_tensor,
            axis=axis,
            reduction_indices=reduction_indices,
            keep_dims=True))
    result = gen_math_ops.log(
        reduce_sum(
            gen_math_ops.exp(input_tensor - my_max),
            axis,
            keep_dims=True,
            reduction_indices=reduction_indices)) + my_max
    if not keep_dims:
      if isinstance(axis, int):
        axis = [axis]
      result = array_ops.squeeze(result, axis)
    return result


def trace(x, name=None):
  """ Compute the trace of a tensor `x`.

  `trace(x)` returns the sum along the main diagonal of each inner-most matrix
  in x. If x is of rank `k` with shape `[I, J, K, ..., L, M, N]`, then output
  is a tensor of rank `k-2` with dimensions `[I, J, K, ..., L]` where

  `output[i, j, k, ..., l] = trace(x[i, j, i, ..., l, :, :])`

  For example:

  ```python
  # 'x' is [[1, 2],
  #         [3, 4]]
  tf.trace(x) ==> 5

  # 'x' is [[1,2,3],
  #         [4,5,6],
  #         [7,8,9]]
  tf.trace(x) ==> 15

  # 'x' is [[[1,2,3],
  #          [4,5,6],
  #          [7,8,9]],
  #         [[-1,-2,-3],
  #          [-4,-5,-6],
  #          [-7,-8,-9]]]
  tf.trace(x) ==> [15,-15]
  ```

  Args:
    x: tensor.
    name: A name for the operation (optional).

  Returns:
    The trace of input tensor.
  """
  with ops.name_scope(name, "Trace", [x]) as name:
    x = ops.convert_to_tensor(x, name="x")
    return reduce_sum(array_ops.matrix_diag_part(x), [-1], name=name)


def matmul(a,
           b,
           transpose_a=False,
           transpose_b=False,
           adjoint_a=False,
           adjoint_b=False,
           a_is_sparse=False,
           b_is_sparse=False,
           name=None):
  """Multiplies matrix `a` by matrix `b`, producing `a` * `b`.

  The inputs must be matrices (or tensors of rank > 2, representing batches of
  matrices), with matching inner dimensions, possibly after transposition.

  Both matrices must be of the same type. The supported types are:
  `float16`, `float32`, `float64`, `int32`, `complex64`, `complex128`.

  Either matrix can be transposed or adjointed (conjugated and transposed) on
  the fly by setting one of the corresponding flag to `True`. These are `False`
  by default.

  If one or both of the matrices contain a lot of zeros, a more efficient
  multiplication algorithm can be used by setting the corresponding
  `a_is_sparse` or `b_is_sparse` flag to `True`. These are `False` by default.
  This optimization is only available for plain matrices (rank-2 tensors) with
  datatypes `bfloat16` or `float32`.

  For example:

  ```python
  # 2-D tensor `a`
  a = tf.constant([1, 2, 3, 4, 5, 6], shape=[2, 3]) => [[1. 2. 3.]
                                                        [4. 5. 6.]]
  # 2-D tensor `b`
  b = tf.constant([7, 8, 9, 10, 11, 12], shape=[3, 2]) => [[7. 8.]
                                                           [9. 10.]
                                                           [11. 12.]]
  c = tf.matmul(a, b) => [[58 64]
                          [139 154]]


  # 3-D tensor `a`
  a = tf.constant(np.arange(1,13), shape=[2, 2, 3]) => [[[ 1.  2.  3.]
                                                         [ 4.  5.  6.]],
                                                        [[ 7.  8.  9.]
                                                         [10. 11. 12.]]]

  # 3-D tensor `b`
  b = tf.constant(np.arange(13,25), shape=[2, 3, 2]) => [[[13. 14.]
                                                          [15. 16.]
                                                          [17. 18.]],
                                                         [[19. 20.]
                                                          [21. 22.]
                                                          [23. 24.]]]
  c = tf.matmul(a, b) => [[[ 94 100]
                           [229 244]],
                          [[508 532]
                           [697 730]]]
  ```

  Args:
    a: `Tensor` of type `float16`, `float32`, `float64`, `int32`, `complex64`,
      `complex128` and rank > 1.
    b: `Tensor` with same type and rank as `a`.
    transpose_a: If `True`, `a` is transposed before multiplication.
    transpose_b: If `True`, `b` is transposed before multiplication.
    adjoint_a: If `True`, `a` is conjugated and transposed before
      multiplication.
    adjoint_b: If `True`, `b` is conjugated and transposed before
      multiplication.
    a_is_sparse: If `True`, `a` is treated as a sparse matrix.
    b_is_sparse: If `True`, `b` is treated as a sparse matrix.
    name: Name for the operation (optional).

  Returns:
    A `Tensor` of the same type as `a` and `b` where each inner-most matrix is
    the product of the corresponding matrices in `a` and `b, e.g. if all
    transpose or adjoint attributes are `False`:

    output[..., :, :] = a[..., :, :] * b[..., :, :] ,


  Raises:
    ValueError: If transpose_a and adjoint_a, or transpose_b and adjoint_b
      are both set to True.
  """
  with ops.name_scope(name, "MatMul", [a, b]) as name:
    if transpose_a and adjoint_a:
      raise ValueError("Only one of transpose_a and adjoint_a can be True.")
    if transpose_b and adjoint_b:
      raise ValueError("Only one of transpose_b and adjoint_b can be True.")

    a = ops.convert_to_tensor(a, name="a")
    b = ops.convert_to_tensor(b, name="b")
    a_shape = a.get_shape()
    b_shape = b.get_shape()
    if (not a_is_sparse and not b_is_sparse) and (
        (a_shape.ndims is None or a_shape.ndims > 2) and
        (b_shape.ndims is None or b_shape.ndims > 2)):
      # BatchMatmul does not support transpose, so we conjugate the matrix and
      # use adjoint instead. Conj() is a noop for real matrices.
      if transpose_a:
        a = conj(a)
        adjoint_a = True
      if transpose_b:
        b = conj(b)
        adjoint_b = True
      return gen_math_ops._batch_mat_mul(
          a, b, adj_x=adjoint_a, adj_y=adjoint_b, name=name)

    # Neither matmul nor sparse_matmul support adjoint, so we conjugate
    # the matrix and use transpose instead. Conj() is a noop for real
    # matrices.
    if adjoint_a:
      a = conj(a)
      transpose_a = True
    if adjoint_b:
      b = conj(b)
      transpose_b = True

    sparse_matmul_types = [dtypes.bfloat16, dtypes.float32]
    use_sparse_matmul = (a.dtype in sparse_matmul_types and
                         b.dtype in sparse_matmul_types and
                         (a_is_sparse or b_is_sparse))
    if dtypes.bfloat16 in (a.dtype, b.dtype):
      # matmul currently doesn't handle bfloat16 inputs.
      use_sparse_matmul = True
    if use_sparse_matmul:
      return sparse_matmul(
          a,
          b,
          transpose_a=transpose_a,
          transpose_b=transpose_b,
          a_is_sparse=a_is_sparse,
          b_is_sparse=b_is_sparse,
          name=name)
    else:
      return gen_math_ops._mat_mul(
          a, b, transpose_a=transpose_a, transpose_b=transpose_b, name=name)


sparse_matmul = gen_math_ops._sparse_mat_mul


@ops.RegisterStatistics("MatMul", "flops")
def _calc_mat_mul_flops(graph, node):
  """Calculates the compute resources needed for MatMul."""
  transpose_a = node.attr["transpose_a"].b
  a_shape = graph_util.tensor_shape_from_node_def_name(graph, node.input[0])
  a_shape.assert_is_fully_defined()
  if transpose_a:
    k = int(a_shape[0])
  else:
    k = int(a_shape[1])
  output_shape = graph_util.tensor_shape_from_node_def_name(graph, node.name)
  output_shape.assert_is_fully_defined()
  output_count = np.prod(output_shape.as_list())
  return ops.OpStats("flops", (k * output_count * 2))


def _as_indexed_slices(x, optimize=True):
  """Convert 'x' to IndexedSlices.

  Convert a dense Tensor to a block-sparse IndexedSlices.

  Args:
    x: Either a Tensor object, or an IndexedSlices object.
    optimize: if true, attempt to optimize the conversion of 'x'.

  Returns:
    An IndexedSlices object.

  Raises:
    TypeError: If 'x' is not a Tensor or an IndexedSlices object.
  """
  # TODO(touts): op_scope
  if not isinstance(x, (ops.Tensor, ops.IndexedSlices)):
    raise TypeError("Not a Tensor or IndexedSlices: %s" % type(x))
  if isinstance(x, ops.IndexedSlices):
    return x
  x_shape = array_ops.shape_internal(x, optimize=optimize)
  return ops.IndexedSlices(x, range(0, x_shape[0]), x_shape)


def _as_indexed_slices_list(inputs, optimize=True):
  """Convert all elements of 'inputs' to IndexedSlices.

  Additionally, homogenize the types of all the indices to
  either int32 or int64.

  Args:
    inputs: List containing either Tensor or IndexedSlices objects.
    optimize: if true, attempt to optimize the conversion of each input.

  Returns:
    A list of IndexedSlices objects.

  Raises:
    TypeError: If 'inputs' is not a list or a tuple.
  """
  if not isinstance(inputs, (list, tuple)):
    raise TypeError("Expected a list or tuple, not a %s" % type(inputs))
  outputs = [_as_indexed_slices(i, optimize=optimize) for i in inputs]
  with_int32_index = [
      o.indices for o in outputs if o.indices.dtype == dtypes.int32
  ]
  if not with_int32_index or len(with_int32_index) == len(outputs):
    return outputs
  casted_outputs = []
  for o in outputs:
    if o.indices.dtype == dtypes.int32:
      casted_outputs.append(
          ops.IndexedSlices(o.values,
                            cast(o.indices, dtypes.int64), o.dense_shape))
    else:
      casted_outputs.append(o)
  return casted_outputs


def add_n(inputs, name=None):
  """Adds all input tensors element-wise.

  Args:
    inputs: A list of `Tensor` objects, each with same shape and type.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` of same shape and type as the elements of `inputs`.

  Raises:
    ValueError: If `inputs` don't all have same shape and dtype or the shape
    cannot be inferred.
  """
  if not inputs or not isinstance(inputs, (list, tuple)):
    raise ValueError("inputs must be a list of at least one Tensor with the "
                     "same dtype and shape")
  inputs = ops.convert_n_to_tensor_or_indexed_slices(inputs)
  if not all(isinstance(x, ops.Tensor) for x in inputs):
    raise ValueError("inputs must be a list of at least one Tensor with the "
                     "same dtype and shape")

  if len(inputs) == 1:
    if name:
      return array_ops.identity(inputs[0], name=name)
    return inputs[0]
  return gen_math_ops._add_n(inputs, name=name)


def accumulate_n(inputs, shape=None, tensor_dtype=None, name=None):
  """Returns the element-wise sum of a list of tensors.

  Optionally, pass `shape` and `tensor_dtype` for shape and type checking,
  otherwise, these are inferred.

  NOTE: This operation is not differentiable and cannot be used if inputs depend
  on trainable variables. Please use `tf.add_n` for such cases.

  For example:

  ```python
  # tensor 'a' is [[1, 2], [3, 4]]
  # tensor `b` is [[5, 0], [0, 6]]
  tf.accumulate_n([a, b, a]) ==> [[7, 4], [6, 14]]

  # Explicitly pass shape and type
  tf.accumulate_n([a, b, a], shape=[2, 2], tensor_dtype=tf.int32)
    ==> [[7, 4], [6, 14]]
  ```

  Args:
    inputs: A list of `Tensor` objects, each with same shape and type.
    shape: Shape of elements of `inputs`.
    tensor_dtype: The type of `inputs`.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` of same shape and type as the elements of `inputs`.

  Raises:
    ValueError: If `inputs` don't all have same shape and dtype or the shape
    cannot be inferred.
  """
  if not inputs or not isinstance(inputs, (list, tuple)):
    raise ValueError("inputs must be a list of at least one Tensor with the "
                     "same dtype and shape")
  inputs = ops.convert_n_to_tensor_or_indexed_slices(inputs)
  if not all(isinstance(x, ops.Tensor) for x in inputs):
    raise ValueError("inputs must be a list of at least one Tensor with the "
                     "same dtype and shape")
  if not all(x.dtype == inputs[0].dtype for x in inputs):
    raise ValueError("inputs must be a list of at least one Tensor with the "
                     "same dtype and shape")
  if shape is not None:
    shape = tensor_shape.as_shape(shape)
  else:
    shape = tensor_shape.unknown_shape()
  for input_tensor in inputs:
    if isinstance(input_tensor, ops.Tensor):
      shape = shape.merge_with(input_tensor.get_shape())
  if len(inputs) == 1:
    return inputs[0]
  if tensor_dtype is None:
    tensor_dtype = inputs[0].dtype
  with ops.name_scope(name, "AccumulateN", inputs) as name:
    var = gen_state_ops._temporary_variable(
        shape=tensor_shape.vector(0), dtype=tensor_dtype)
    with ops.colocate_with(var):
      zeros = array_ops.zeros_like(gen_control_flow_ops._merge(inputs)[0])
      zeros.set_shape(shape)
      ref = state_ops.assign(var, zeros, validate_shape=False)
      update_ops = [
          state_ops.assign_add(
              ref, input_tensor, use_locking=True) for input_tensor in inputs
      ]
      with ops.control_dependencies(update_ops):
        return gen_state_ops._destroy_temporary_variable(
            ref, var_name=var.op.name, name=name)


def sigmoid(x, name=None):
  """Computes sigmoid of `x` element-wise.

  Specifically, `y = 1 / (1 + exp(-x))`.

  Args:
    x: A Tensor with type `float32`, `float64`, `int32`, `complex64`, `int64`,
      or `qint32`.
    name: A name for the operation (optional).

  Returns:
    A Tensor with the same type as `x` if `x.dtype != qint32`
      otherwise the return type is `quint8`.

  @compatibility(numpy)
  Equivalent to np.scipy.special.expit
  @end_compatibility
  """
  with ops.name_scope(name, "Sigmoid", [x]) as name:
    x = ops.convert_to_tensor(x, name="x")
    return gen_math_ops._sigmoid(x, name=name)


def tanh(x, name=None):
  """Computes hyperbolic tangent of `x` element-wise.

  Args:
    x: A Tensor or SparseTensor with type `float`, `double`, `int32`,
      `complex64`, `int64`, or `qint32`.
    name: A name for the operation (optional).

  Returns:
    A Tensor or SparseTensor respectively with the same type as `x` if
    `x.dtype != qint32` otherwise the return type is `quint8`.
  """
  with ops.name_scope(name, "Tanh", [x]) as name:
    if isinstance(x, sparse_tensor.SparseTensor):
      x_tanh = gen_math_ops._tanh(x.values, name=name)
      return sparse_tensor.SparseTensor(
          indices=x.indices, values=x_tanh, dense_shape=x.dense_shape)
    else:
      return gen_math_ops._tanh(x, name=name)


def cumsum(x, axis=0, exclusive=False, reverse=False, name=None):
  """Compute the cumulative sum of the tensor `x` along `axis`.

  By default, this op performs an inclusive cumsum, which means that the first
  element of the input is identical to the first element of the output:
  ```prettyprint
  tf.cumsum([a, b, c]) ==> [a, a + b, a + b + c]
  ```

  By setting the `exclusive` kwarg to `True`, an exclusive cumsum is performed
  instead:
  ```prettyprint
  tf.cumsum([a, b, c], exclusive=True) ==> [0, a, a + b]
  ```

  By setting the `reverse` kwarg to `True`, the cumsum is performed in the
  opposite direction:
  ```prettyprint
  tf.cumsum([a, b, c], reverse=True) ==> [a + b + c, b + c, c]
  ```
  This is more efficient than using separate `tf.reverse` ops.

  The `reverse` and `exclusive` kwargs can also be combined:
  ```prettyprint
  tf.cumsum([a, b, c], exclusive=True, reverse=True) ==> [b + c, c, 0]
  ```

  Args:
    x: A `Tensor`. Must be one of the following types: `float32`, `float64`,
       `int64`, `int32`, `uint8`, `uint16`, `int16`, `int8`, `complex64`,
       `complex128`, `qint8`, `quint8`, `qint32`, `half`.
       axis: A `Tensor` of type `int32` (default: 0).
       reverse: A `bool` (default: False).
       name: A name for the operation (optional).

  Returns:
    A `Tensor`. Has the same type as `x`.
  """
  with ops.name_scope(name, "Cumsum", [x]) as name:
    x = ops.convert_to_tensor(x, name="x")
    return gen_math_ops.cumsum(
        x, axis, exclusive=exclusive, reverse=reverse, name=name)


def cumprod(x, axis=0, exclusive=False, reverse=False, name=None):
  """Compute the cumulative product of the tensor `x` along `axis`.

  By default, this op performs an inclusive cumprod, which means that the
  first
  element of the input is identical to the first element of the output:
  ```prettyprint
  tf.cumprod([a, b, c]) ==> [a, a * b, a * b * c]
  ```

  By setting the `exclusive` kwarg to `True`, an exclusive cumprod is
  performed
  instead:
  ```prettyprint
  tf.cumprod([a, b, c], exclusive=True) ==> [1, a, a * b]
  ```

  By setting the `reverse` kwarg to `True`, the cumprod is performed in the
  opposite direction:
  ```prettyprint
  tf.cumprod([a, b, c], reverse=True) ==> [a * b * c, b * c, c]
  ```
  This is more efficient than using separate `tf.reverse` ops.

  The `reverse` and `exclusive` kwargs can also be combined:
  ```prettyprint
  tf.cumprod([a, b, c], exclusive=True, reverse=True) ==> [b * c, c, 1]
  ```

  Args:
    x: A `Tensor`. Must be one of the following types: `float32`, `float64`,
       `int64`, `int32`, `uint8`, `uint16`, `int16`, `int8`, `complex64`,
       `complex128`, `qint8`, `quint8`, `qint32`, `half`.
    axis: A `Tensor` of type `int32` (default: 0).
    reverse: A `bool` (default: False).
    name: A name for the operation (optional).

  Returns:
    A `Tensor`. Has the same type as `x`.
  """
  with ops.name_scope(name, "Cumprod", [x]) as name:
    x = ops.convert_to_tensor(x, name="x")
    return gen_math_ops.cumprod(
        x, axis, exclusive=exclusive, reverse=reverse, name=name)


def conj(x, name=None):
  r"""Returns the complex conjugate of a complex number.

  Given a tensor `input` of complex numbers, this operation returns a tensor of
  complex numbers that are the complex conjugate of each element in `input`. The
  complex numbers in `input` must be of the form \\(a + bj\\), where *a* is the
  real part and *b* is the imaginary part.

  The complex conjugate returned by this operation is of the form \\(a - bj\\).

  For example:

      # tensor 'input' is [-2.25 + 4.75j, 3.25 + 5.75j]
      tf.conj(input) ==> [-2.25 - 4.75j, 3.25 - 5.75j]

  If `x` is real, it is returned unchanged.

  Args:
    x: `Tensor` to conjugate.  Must have numeric type.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` that is the conjugate of `x` (with the same type).

  Raises:
    TypeError: If `x` is not a numeric tensor.
  """
  with ops.name_scope(name, "Conj", [x]) as name:
    x = ops.convert_to_tensor(x, name="x")
    if x.dtype.is_complex:
      return gen_math_ops._conj(x, name=name)
    elif x.dtype.is_floating or x.dtype.is_integer:
      return x
    else:
      raise TypeError("Expected numeric tensor, got dtype %r" % x.dtype)


def _BroadcastShape(op):
  """Common shape function for binary operators that broadcast their inputs."""
  return [
      common_shapes.broadcast_shape(op.inputs[0].get_shape(),
                                    op.inputs[1].get_shape())
  ]


def reduced_shape(input_shape, axes):
  """Helper function for reduction ops.

  Args:
    input_shape: 1-D Tensor, the shape of the Tensor being reduced.
    axes: 1-D Tensor, the reduction axes.
  Returns:
    A 1-D Tensor, the output shape as if keep_dims were set to True.
  """
  # Example:
  # cast needed for SparseTensor reductions
  input_shape = to_int32(input_shape)  # [2, 3, 5, 7]
  axes = to_int32(axes)  # [1, 2]

  input_rank = array_ops.size(input_shape)  # 4
  axes = (axes + input_rank) % input_rank
  axes_shape = array_ops.shape(axes)  # [2]
  return gen_data_flow_ops.dynamic_stitch(  # [2, 1, 1, 7]
      [
          range(input_rank),  # [0, 1, 2, 3]
          axes
      ],  # [1, 2]
      [
          input_shape,  # [2, 3, 5, 7]
          array_ops.fill(axes_shape, 1)
      ])  # [1, 1]


def tensordot(a, b, axes, name=None):
  r"""Tensor contraction of a and b along specified axes.

  Tensordot (also known as tensor contraction) sums the product of elements
  from `a` and `b` over the indices specified by `a_axes` and `b_axes`.
  The lists `a_axes` and `b_axes` specify those pairs of axes along which to
  contract the tensors. The axis `a_axes[i]` of `a` must have the same dimension
  as axis `b_axes[i]` of `b` for all `i` in `range(0, len(a_axes))`. The lists
  `a_axes` and `b_axes` must have identical length and consist of unique
  integers that specify valid axes for each of the tensors.

  This operation corresponds to `numpy.tensordot(a, b, axes)`.

  Example 1: When `a` and `b` are matrices (order 2), the case `axes = 1`
  is equivalent to matrix multiplication.

  Example 2: When `a` and `b` are matrices (order 2), the case
  `axes = [[1], [0]]` is equivalent to matrix multiplication.

  Example 3: Suppose that \\(a_ijk\\) and \\(b_lmn\\) represent two
  tensors of order 3. Then, `contract(a, b, [0], [2])` is the order 4 tensor
  \\(c_{jklm}\\) whose entry
  corresponding to the indices \\((j,k,l,m)\\) is given by:

  \\( c_{jklm} = \sum_i a_{ijk} b_{lmi} \\).

  In general, `order(c) = order(a) + order(b) - 2*len(axes[0])`.

  Args:
    a: `Tensor` of type `float32` or `float64`.
    b: `Tensor` with the same type as `a`.
    axes: Either a scalar `N`, or a list or an `int32` `Tensor` of shape [2, k].
     If axes is a scalar, sum over the last N axes of a and the first N axes
     of b in order.
     If axes is a list or `Tensor` the first and second row contain the set of
     unique integers specifying axes along which the contraction is computed,
     for `a` and `b`, respectively. The number of axes for `a` and `b` must
     be equal.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` with the same type as `a`.

  Raises:
    ValueError: If the shapes of `a`, `b`, and `axes` are incompatible.
    IndexError: If the values in axes exceed the rank of the corresponding
      tensor.
  """

  def _tensordot_reshape(a, axes, flipped=False):
    """Helper method to perform transpose and reshape for contraction op.

    This method is helpful in reducing `math_ops.tensordot` to `math_ops.matmul`
    using `array_ops.transpose` and `array_ops.reshape`. The method takes a
    tensor and performs the correct transpose and reshape operation for a given
    set of indices. It returns the reshaped tensor as well as a list of indices
    necesary to reshape the tensor again after matrix multiplication.

    Args:
      a: `Tensor`.
      axes: List or `int32` `Tensor` of unique indices specifying valid axes of
       `a`.
      flipped: An optional `bool`. Defaults to `False`. If `True`, the method
        assumes that `a` is the second argument in the contraction operation.

    Returns:
      A pair `(reshaped_a, free_dims)` where `reshaped_a` is the tensor `a`
      reshaped to allow contraction via `matmul` and `free_dims` is either a
      list of integers or an `int32` `Tensor`, depending on if `axes` is a list
      and the shape of `a`  is fully defined.
    """
    # TODO(b/33084409): Implement partial shape inference.
    if a.get_shape().is_fully_defined() and isinstance(axes, (list, tuple)):
      shape_a = a.get_shape().as_list()
      axes = [i if i >= 0 else i + len(shape_a) for i in axes]
      free = [i for i in xrange(len(shape_a)) if i not in axes]
      free_dims = [shape_a[i] for i in free]
      prod_free = int(np.prod([shape_a[i] for i in free]))
      prod_axes = int(np.prod([shape_a[i] for i in axes]))
      perm = list(axes) + free if flipped else free + list(axes)
      new_shape = [prod_axes, prod_free] if flipped else [prod_free, prod_axes]
      reshaped_a = array_ops.reshape(array_ops.transpose(a, perm), new_shape)
      return reshaped_a, free_dims
    else:
      shape_a = array_ops.shape(a)
      rank_a = array_ops.rank(a)
      axes = ops.convert_to_tensor(axes, dtype=dtypes.int32, name="axes")
      axes = cast(axes >= 0, dtypes.int32) * axes + cast(
          axes < 0, dtypes.int32) * (axes + rank_a)
      free, _ = array_ops.setdiff1d(range(rank_a), axes)
      free_dims = array_ops.gather(shape_a, free)
      axes_dims = array_ops.gather(shape_a, axes)
      prod_free_dims = reduce_prod(free_dims)
      prod_axes_dims = reduce_prod(axes_dims)
      perm = array_ops.concat(0, [axes_dims, free_dims])
      if flipped:
        perm = array_ops.concat(0, [axes, free])
        new_shape = array_ops.stack([prod_axes_dims, prod_free_dims])
      else:
        perm = array_ops.concat(0, [free, axes])
        new_shape = array_ops.stack([prod_free_dims, prod_axes_dims])
      reshaped_a = array_ops.reshape(array_ops.transpose(a, perm), new_shape)
      return reshaped_a, free_dims

  def _tensordot_axes(a, axes):
    """Generates two sets of contraction axes for the two tensor arguments."""
    a_shape = a.get_shape()
    if isinstance(axes, compat.integral_types):
      if axes < 1:
        raise ValueError("'axes' must be at least 1.")
      if a_shape.ndims is not None:
        return range(a_shape.ndims - axes, a_shape.ndims), range(axes)
      else:
        rank = array_ops.rank(a)
        return (array_ops.range(
            rank - axes, rank, dtype=dtypes.int32), array_ops.range(
                rank, dtype=dtypes.int32))
    elif isinstance(axes, (list, tuple)):
      if len(axes) != 2:
        raise ValueError("'axes' must be an integer or have length 2.")
      a_axes = axes[0]
      b_axes = axes[1]
      if len(a_axes) != len(b_axes):
        raise ValueError(
            "Different number of contraction axes 'a' and 'b', %s != %s.",
            len(a_axes), len(b_axes))
      return a_axes, b_axes
    else:
      axes = ops.convert_to_tensor(axes, name="axes", dtype=dtypes.int32)
      return axes[0], axes[1]

  with ops.name_scope(name, "Tensordot", [a, b, axes]) as name:
    a = ops.convert_to_tensor(a, name="a")
    b = ops.convert_to_tensor(b, name="b")
    a_axes, b_axes = _tensordot_axes(a, axes)
    a_reshape, a_free_dims = _tensordot_reshape(a, a_axes)
    b_reshape, b_free_dims = _tensordot_reshape(b, b_axes, True)
    ab_matmul = matmul(a_reshape, b_reshape)
    if isinstance(a_free_dims, list) and isinstance(b_free_dims, list):
      return array_ops.reshape(ab_matmul, a_free_dims + b_free_dims, name=name)
    else:
      a_free_dims = ops.convert_to_tensor(a_free_dims)
      b_free_dims = ops.convert_to_tensor(b_free_dims)
      return array_ops.reshape(
          ab_matmul, array_ops.concat(0, [a_free_dims, b_free_dims]), name=name)
