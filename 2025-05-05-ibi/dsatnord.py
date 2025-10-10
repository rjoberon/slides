#!/usr/bin/python3
# -*- coding: utf-8 -*-

#
#
#
# Usage:
#
# Author: rja
#
# Changes:
# 2025-04-16 (rja)
# - initial version

import subprocess
import numpy as np
import matplotlib.pyplot as plt

parts = [
    (2, "red", 16, "header", "3"),
    (3, "blue", 20 * 4 + 169 * 4 + 2280 + 30*4 + 844 + 2990*4 + 41245 * 4 + 135064, "offsets", "4"),
    (5, "#267d40", 754077, "tiles0", "6"),
    (6, "#31a354", 9056940, "tiles1", "6/3"),
    (10, "#3182bd", 567760, "paths", "8"),
    (11, "#fd8d3c", 975894 + 994802, "topware", "9"),
    (1, "#974ea3", 13394 * 64, "places", "1/3"),
    (12, "#666666", 24 * 16, "unknown", "10/0/0"),
    (9, "#e6550d", 4878 * 201, "citysigns", "7"),
    (4, "#6baed6", 1691200, "paths", "5"),
    (7, "#73c475", 70627806, "tiles2", "6/5"),
    (8, "#a1d99b", 644804703 + 936 - 86822577, "tiles3", "6/6"),
    (12, "#666666", 644824916 - 644804703 - 936, "unknown", "10/0/1"),
    (12, "#666666", 8995, "unknown", "10/0/2")
]

fname = "images/dsatnord"
baseurl = "/2025-05-05-ibi/#/"


if __name__ == '__main__':
    # https://github.com/matplotlib/matplotlib/issues/25567#issuecomment-1487258247
    plt.rcParams['svg.fonttype'] = 'none'

    sizes = np.array([size for pos, color, size, name, href in parts])
    total_size = sum(sizes)

    done = 0
    for i in range(max([pos for pos, color, size, name, href in parts]) + 2):
        fig, ax = plt.subplots(figsize=(15.15, 1))
        ax.xaxis.set_visible(False)
        ax.yaxis.set_visible(False)
        for d in ['top', 'right', 'left']:
            ax.spines[d].set_visible(False)
        ax.set_xlim(0, sizes.sum())

        size_cum = 0
        for pos, color, size, name, href in parts:
            c = color if pos <= i else "white" # switch parts (in)visible
            b = "black" if pos == i else c
            if pos == i:
                done += size
            ax.barh(0, size, left=size_cum, height=0.1, label=name, color=c, edgecolor=b)
            size_cum += size
        legend = ax.legend(ncols=len(parts), bbox_to_anchor=(0, 1), loc='lower left',
                           fontsize="small", frameon=False, labelcolor="linecolor",
                           title=f"dsatnord.mp: {done: >11,}  of  {total_size:,}  bytes  known  ({done/total_size*100:2.2f}%)")
        for ta in legend.texts:
            t = ta.get_text()
            for pos, color, size, name, href in parts:
                if name == t:
                    ta.set_url(baseurl + href)

        plt.tight_layout()
        plt.setp(legend.get_title(), fontfamily="Eurostile Extended", fontsize=13)

        outfile = f"{fname}_{i:02}.svg"
        plt.savefig(outfile, bbox_inches='tight')

        # add target="_parent" attribute to all <a xlink:href
        subprocess.run(["sed", "-i", "-e", "s/<a xlink:href/<a target='_parent' xlink:href/g", outfile])
