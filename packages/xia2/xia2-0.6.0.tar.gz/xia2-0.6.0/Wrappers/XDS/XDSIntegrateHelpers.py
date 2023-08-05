#!/usr/bin/env python
# XDSIntegrateHelpers.py
#   Copyright (C) 2006 CCLRC, Graeme Winter
#
#   This code is distributed under the BSD license, a copy of which is
#   included in the root directory of this package.
#
# Routines which help with working with XDS INTEGRATE - e.g. parsing the
# output INTEGRATE.LP.
#

from __future__ import absolute_import, division, print_function

import os
import sys


def _parse_integrate_lp_updates(filename):
    """Parse the integrate.lp file to get the values for any updated
    parameters."""

    if not os.path.split(filename)[-1] == "INTEGRATE.LP":
        raise RuntimeError("input filename not INTEGRATE.LP")

    file_contents = open(filename, "r").readlines()

    updates = {}

    for i, content in enumerate(file_contents):
        if " ***** SUGGESTED VALUES FOR INPUT PARAMETERS *****" in content:
            beam_parms = file_contents[i + 1].replace("=", "").split()
            reflecting_parms = file_contents[i + 2].replace("=", "").split()
            updates[beam_parms[0]] = float(beam_parms[1])
            updates[beam_parms[2]] = float(beam_parms[3])
            updates[reflecting_parms[0]] = float(reflecting_parms[1])
            updates[reflecting_parms[2]] = float(reflecting_parms[3])

    return updates


def _parse_integrate_lp(filename):
    """Parse the contents of the INTEGRATE.LP file pointed to by filename."""

    if not os.path.split(filename)[-1] == "INTEGRATE.LP":
        raise RuntimeError("input filename not INTEGRATE.LP")

    file_contents = open(filename, "r").readlines()

    per_image_stats = {}

    block_start_finish = (0, 0)

    oscillation_range = 0.0

    block_images = []

    for i, content in enumerate(file_contents):

        # check for the header contents - this is basically a duplicate
        # of the input data....

        if "OSCILLATION_RANGE=" in content:
            oscillation_range = float(content.split()[1])

        if "PROCESSING OF IMAGES" in content:
            lst = content.split()
            block_start_finish = (int(lst[3]), int(lst[5]))

            block_images = [j for j in range(int(lst[3]), int(lst[5]) + 1)]

        # look for explicitly per-image information
        if "IMAGE IER  SCALE" in content:
            j = i + 1
            while file_contents[j].strip():
                line = file_contents[j]
                assert len(line) == 71, len(line)
                image = int(line[0:6])
                status = int(line[6:10])
                scale = float(line[10:17])
                overloads = int(line[26:31])
                all = int(line[31:38])
                strong = int(line[38:46])
                rejected = int(line[46:52])

                if status == 0:

                    # trap e.g. missing images - need to be able to
                    # record this somewhere...

                    if all:
                        fraction_weak = 1.0 - (float(strong) / float(all))
                    else:
                        fraction_weak = 1.0

                    per_image_stats[image] = {
                        "scale": scale,
                        "overloads": overloads,
                        "strong": strong,
                        "all": all,
                        "fraction_weak": fraction_weak,
                        "rejected": rejected,
                    }

                else:
                    block_images.remove(image)

                j += 1

        # then look for per-block information - this will be mapped onto
        # individual images using the block_start_finish information

        if "CRYSTAL MOSAICITY (DEGREES)" in content:
            mosaic = float(content.split()[3])
            # for image in range(block_start_finish[0],
            # block_start_finish[1] + 1):
            for image in block_images:
                per_image_stats[image]["mosaic"] = mosaic

        if "OF SPOT    POSITION (PIXELS)" in content:
            rmsd_pixel = float(content.split()[-1])
            # for image in range(block_start_finish[0],
            # block_start_finish[1] + 1):
            for image in block_images:
                per_image_stats[image]["rmsd_pixel"] = rmsd_pixel

        if "UNIT CELL PARAMETERS" in content:
            unit_cell = tuple(map(float, content.split()[-6:]))
            for image in block_images:
                per_image_stats[image]["unit_cell"] = unit_cell

        if "OF SPINDLE POSITION (DEGREES)" in content:
            rmsd_phi = float(content.split()[-1])
            # for image in range(block_start_finish[0],
            # block_start_finish[1] + 1):
            for image in block_images:
                per_image_stats[image]["rmsd_phi"] = rmsd_phi / oscillation_range

        # want to convert this to mm in some standard setting!
        if "DETECTOR COORDINATES (PIXELS) OF DIRECT BEAM" in content:
            beam = map(float, content.split()[-2:])
            # for image in range(block_start_finish[0],
            # block_start_finish[1] + 1):
            for image in block_images:
                per_image_stats[image]["beam"] = beam

        if "CRYSTAL TO DETECTOR DISTANCE (mm)" in content:
            distance = float(content.split()[-1])
            # for image in range(block_start_finish[0],
            # block_start_finish[1] + 1):
            for image in block_images:
                per_image_stats[image]["distance"] = distance

    return per_image_stats


def _print_integrate_lp(integrate_lp_stats):
    """Print the contents of the integrate.lp dictionary."""

    images = sorted(integrate_lp_stats.keys())

    for i in images:
        data = integrate_lp_stats[i]
        print(
            "%4d %5.3f %5d %5d %5d %4.2f %6.2f"
            % (
                i,
                data["scale"],
                data["strong"],
                data["overloads"],
                data["rejected"],
                data["mosaic"],
                data["distance"],
            )
        )


if __name__ == "__main__":
    if len(sys.argv) > 1:
        integrate_lp = sys.argv[1]
    else:
        integrate_lp = os.path.join(
            os.environ["XIA2_ROOT"], "Wrappers", "XDS", "Doc", "INTEGRATE.LP"
        )

    stats = _parse_integrate_lp(integrate_lp)

    images = sorted(stats.keys())

    # these may not be present if only a couple of the
    # images were integrated...

    for i in images:
        print(stats[i]["rmsd_pixel"])

    stddev_pixel = [stats[i]["rmsd_pixel"] for i in images]

    # fix to bug # 2501 - remove the extreme values from this
    # list...

    stddev_pixel = sorted(set(stddev_pixel))
    stddev_pixel = stddev_pixel[1:-1]

    print(stddev_pixel)
