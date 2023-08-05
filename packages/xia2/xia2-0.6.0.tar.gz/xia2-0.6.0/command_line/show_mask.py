# LIBTBX_SET_DISPATCHER_NAME dev.xia2.show_mask
# LIBTBX_PRE_DISPATCHER_INCLUDE_SH export BOOST_ADAPTBX_FPE_DEFAULT=1
from __future__ import absolute_import, division, print_function


def main(filename):
    """Show a mask from create_mask."""

    from dials.array_family import flex
    import six.moves.cPickle as pickle
    from matplotlib import pylab

    with open(filename, "rb") as fh:
        m = pickle.load(fh)

    pylab.imshow(m[0].as_numpy_array())
    pylab.show()


if __name__ == "__main__":
    import sys

    main(sys.argv[1])
