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

import numpy as np
import matplotlib.pyplot as plt

parts = [
    (2, "red", 16, "header"),
    (3, "blue", 20 * 4 + 169 * 4 + 2280 + 30*4 + 844 + 2990*4 + 41245 * 4 + 135064, "offsets"),
    (5, "#267d40", 754077, "tiles0"),
    (6, "#31a354", 9056940, "tiles1"),
    (10, "#3182bd", 567760, "paths"),
    (11, "#fd8d3c", 975894 + 994802, "topware"),
    (1, "#974ea3", 13394 * 64, "places"),
    (12, "#666666", 24 * 16, "unknown"),
    (9, "#e6550d", 4878 * 201, "citysigns"),
    (4, "#6baed6", 1691200, "paths"),
    (7, "#73c475", 70627806, "tiles2"),
    (8, "#a1d99b", 644804703 + 936 - 86822577, "tiles3"),
    (12, "#666666", 644824916 - 644804703 - 936, "unknown"),
    (12, "#666666", 8995, "unknown")
]

fname = "images/dsatnord"

if __name__ == '__main__':
    sizes = np.array([size for pos, color, size, _ in parts])
    total_size = sum(sizes)

    done = 0
    for i in range(max([pos for pos, color, size, _ in parts]) + 2):
        fig, ax = plt.subplots(figsize=(15.15, 1))
        ax.xaxis.set_visible(False)
        ax.yaxis.set_visible(False)
        for d in ['top', 'right', 'left']:
            ax.spines[d].set_visible(False)
        ax.set_xlim(0, sizes.sum())

        size_cum = 0
        for pos, color, size, name in parts:
            c = color if pos <= i else "white" # switch parts (in)visible
            b = "black" if pos == i else c
            if pos == i:
                done += size
            ax.barh(0, size, left=size_cum, height=0.1, label=name, color=c, edgecolor=b)
            size_cum += size
        legend = ax.legend(ncols=len(parts), bbox_to_anchor=(0, 1), loc='lower left',
                           fontsize="small", frameon=False, labelcolor="linecolor",
                           title=f"dsatnord.mp: {done: >11,}  of  {total_size:,}  bytes  known  ({done/total_size*100:2.2f}%)")

        plt.tight_layout()
        plt.setp(legend.get_title(), fontfamily="Eurostile Extended", fontsize=13)
        plt.savefig(f"{fname}_{i:02}.svg", bbox_inches='tight')
