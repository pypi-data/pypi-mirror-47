import torch
from torch import autograd

# noinspection PyUnreachableCode
if False:
    from typing import Any, Tuple, Union

from ._impl import (_signature_channels,
                    _signature_forward,
                    _signature_backward)


# It would be lovely to do all of this at the C++ level. (In particular sigspec is really a struct that has no
# business being passed around at the Python level.) But unfortunately the documentation for how to create autograd
# Functions in C++ is nonexistent. Presumably that means it's all still subject to change, so we're just going to stick
# to the Python way of doings things for now.
class _SignatureFunction(autograd.Function):
    @staticmethod
    def forward(ctx, path, depth, basepoint, stream, flatten):
        # type: (Any, torch.Tensor, int, bool, bool, bool) -> Union[torch.Tensor, Tuple[torch.Tensor, ...]]
        result, result_as_vector, path_increments, sigspec = _signature_forward(path, depth, basepoint, stream, flatten)
        ctx._call_info = (result_as_vector, path_increments, sigspec, depth, basepoint, stream, flatten)
        if flatten:
            result = result[0]
        else:
            result = tuple(result)  # okay to return tuples, not okay to return lists. For some reason.
        return result

    @staticmethod
    def backward(ctx, *grad_outputs):
        # type: (Any, Tuple[torch.Tensor]) -> Tuple[torch.Tensor, None, None, None, None]
        return _signature_backward(grad_outputs, *ctx._call_info), None, None, None, None


def signature(path, depth, basepoint=False, stream=False, flatten=True):
    # type: (torch.Tensor, int, bool, bool, bool) -> Union[torch.Tensor, Tuple[torch.Tensor, ...]]
    r"""Applies the signature transform to a stream of data.

    The input :attr:`path` is expected to be a three-dimensional tensor, with dimensions :math:`(N, C, L)`, where
    :math:`N` is the batch size, :math:`C` denotes the number of channels, and :math:`L` is the length of the input
    sequence. Thus each batch element is interpreted as a stream of data :math:`(x_1, \ldots, x_L)`, where each
    :math:`x_i \in \mathbb{R}^C`. (This is the same as :class:`torch.nn.Conv1d`, for example.)

    If :attr:`basepoint` is True then an additional point :math:`x_0 = 0 \in \mathbb{R}^C` is prepended to the path.

    Each path is then lifted to a piecewise constant path :math:`X \colon [0, 1] \to \mathbb{R}^C`, and the signature
    transform of this path is then computed. This (by the definition of the signature transform) gives a sequence of
    tensors of shape

    .. math::
        (N, C), (N, C, C), \ldots (N, C, \ldots, C),

    where the final tensor has :attr:`depth` many dimensions of size :math:`C`. If :attr:`flatten` is True then these
    are then flattened down and concatenated to give a single tensor of shape

    .. math::
        (N, C + C^2 + \cdots + C^\text{depth}).

    (This value may be computed via the :func:`signatory.signature_channels` function.)

    If :attr:`stream` is True then  the signatures of all paths :math:`(x_1, \ldots, x_j)`, for :math:`j=2, \ldots, L`,
    are computed. (Or :math:`(x_0, \ldots, x_j)`, for :math:`j=1, \ldots, L` if :attr:`basepoint` is True. In neither
    case is the signature of the path of a single element computed, as that is just zero.)

    Examples:
        If :attr:`stream` is False and :attr:`flatten` is True then the returned tensor will have shape

        .. math::
            (N, C + C^2 + \cdots + C^d).

        If :attr:`basepoint` is True, :attr:`stream` is True and :attr:`flatten` is True then the returned tensor will
        have shape

        .. math::
            (N, C + C^2 + \cdots + C^d, L),

        as the stream dimension is now preserved. See also the 'Returns' section below.

    Arguments:
        path (:class:`torch.Tensor`): The input path to apply the signature transform to.

        depth (int): The depth to truncate the signature at.

        basepoint (bool, optional): Defaults to False. If True, then the path will have an additional point prepended to
            the start corresponding to the origin. If this is False then the signature transform is invariant to
            translations of the path. (Which may or may not be desirable.)

        stream (bool, optional): Defaults to False. If False then the signature transform of the whole path is computed.
            If True then the signature of all intermediate paths are also computed.

        flatten (bool, optional): Defaults to True. Whether to flatten the sequence of tensors resulting from the
            signature transform.

    Returns:
        A :class:`torch.Tensor` or a tuple of :class:`torch.Tensor` s.
        Given an input :class:`torch.Tensor` of shape :math:`(N, C, L)`, and input arguments :attr:`depth`,
        :attr:`basepoint`, :attr:`stream`, :attr:`flatten`, then the return value is, in pseudocode:

        .. code-block:: python

            if flatten:
                if stream:
                    if basepoint:
                        return torch.Tensor of shape (N, C + C^2 + ... + C^(depth), L)
                    else:
                        return torch.Tensor of shape (N, C + C^2 + ... + C^(depth), L - 1)
                else:
                    return torch.Tensor of shape (N, C + C^2 + ... + C^(depth))
            else:
                if stream:
                    if basepoint:
                        out = []
                        for i in range(1, depth + 1):
                            out.append(torch.Tensor of shape (N, C^i, L))
                        return tuple(out)
                    else:
                        out = []
                        for i in range(1, depth + 1):
                            out.append(torch.Tensor of shape (N, C^i, L - 1))
                        return tuple(out)
                else:
                    out = []
                    for i in range(1, depth + 1):
                        out.append(torch.Tensor of shape (N, C^i))
                    return tuple(out)

    """

    return _SignatureFunction.apply(path, depth, basepoint, stream, flatten)


# A wrapper for the sake of consistent documentation on signatures
def signature_channels(in_channels, depth):
    # type: (int, int) -> int
    """Computes the number of output channels from a signature call.

    Arguments:
        in_channels (int): The number of channels in the input; that is, the dimension of the space that the input path
            resides in.

        depth (int): The depth of the signature that is being computed.

    Returns:
        An int specifying the number of channels in the signature of the path.
    """

    return _signature_channels(in_channels, depth)
