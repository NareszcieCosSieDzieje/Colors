#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from __future__ import division             # Division in Python 2.7
import matplotlib
import os
matplotlib.use('Agg')                       # So that we can render files without GUI
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
import math

from matplotlib import colors

def plot_color_gradients(gradients, names):
    # For pretty latex fonts (commented out, because it does not work on some machines)
    #rc('text', usetex=True)
    #rc('font', family='serif', serif=['Times'], size=10)
    rc('legend', fontsize=10)

    column_width_pt = 400         # Show in latex using \the\linewidth
    pt_per_inch = 72
    size = column_width_pt / pt_per_inch

    fig, axes = plt.subplots(nrows=len(gradients), sharex=True, figsize=(size, 0.75 * size))
    fig.subplots_adjust(top=1.00, bottom=0.05, left=0.25, right=0.95)

    for ax, gradient, name in zip(axes, gradients, names):
        # Create image with two lines and draw gradient on it
        img = np.zeros((2, 1024, 3))
        for i, v in enumerate(np.linspace(0, 1, 1024)):
            img[:, i] = gradient(v)

        im = ax.imshow(img, aspect='auto')
        im.set_extent([0, 1, 0, 1])
        ax.yaxis.set_visible(False)

        pos = list(ax.get_position().bounds)
        x_text = pos[0] - 0.25
        y_text = pos[1] + pos[3]/2.
        fig.text(x_text, y_text, name, va='center', ha='left', fontsize=10)

    if os.path.exists('my-gradients.pdf'):
        os.remove('my-gradients.pdf')
    else:
        print("The file does not exist")
    fig.savefig('my-gradients.pdf')
    os.startfile('my-gradients.pdf')


def hsv2rgb(h, s, v):
    #TODO
    return (h, s, v)


def gradient_rgb_bw(v):
    return (v, v, v)


def gradient_rgb_gbr(v):
    if v < 0.5:
        return (0,1-v*2.0,v*2.0)
    else:
        return ((v-0.5)*2.0,0.0,1-((v-0.5)*2.0))


def gradient_rgb_gbr_full(v):
    if v < 0.25:
        return (0.0, 1.0, 4.0*v)
    elif v < 0.5:
        return (0.0, 1.0-(v-0.25)*4.0, 1.0)
    elif v < 0.75:
        return (4.0*(v-0.5), 0.0, 1.0)
    else:
        return (1.0, 0.0, 1.0-(v-0.75)*4.0 )


def gradient_rgb_wb_custom(v):
    if v < 0.14:
        return (1.0, max(0,1.0 - 14.3*v), 1.0 )
    elif v < 0.28:
        return (1.0, 0.0, max(0,1.0 - 14.3*(v-0.14)))
    elif v < 0.42:
        return (1.0, min(1.0,0.0 + 14.3*(v-0.28)), 0.0)
    elif v < 0.56:
        return ( max(0,1.0 - 14.3*(v-0.42)), 1.0 , 0.0)
    elif v < 0.70:
        return ( 0.0, 1.0, min(1.0, 0.0 + 14.3*(v-0.56)))
    elif v < 0.84:
        return ( 0.0, max(0.0,1.0 - 14.3*(v-0.70)), 1.0)
    elif v < 0.95:
        return ( min(1.0, 0.0 + 14.3*(v-0.84)), min(1.0, 0.0 + 14.3*(v-0.84)), max(0.0, 1.0 - 14.3*(v-0.84)))
    else:
        return (max(0.0,1.0 - 14.3*(v-0.95)) , max(0.0,1.0 - 14.3*(v-0.95)), 0.0)


def gradient_hsv_bw(v):
    return hsv2rgb(1.0, 0, v)


def gradient_hsv_gbr(v): #100-360
    return hsv2rgb( 115 + v * 245, 1, 1)


def gradient_hsv_unknown(v):
    return hsv2rgb( 100 - v*100, 0.6, 1)


def gradient_hsv_custom(v):
    return hsv2rgb(0 + v * 315, 1-v, 1)


def hsv2rgb(H, S, V): #0-360, 0-1, 0-1
    RGB = list()
    if H == 360:
        H = 0
    else:
        H/=60.0
    fract = H - math.floor(H)
    P = V * (1. - S)
    Q = V * (1. - S * fract)
    T = V * (1. - S * (1. - fract))
    if (0. <= H) and (H < 1.):
        RGB = (V, T, P)
    elif (1. <= H) and (H < 2.):
        RGB = (Q, V, P)
    elif (2. <= H) and (H < 3.):
        RGB = (P, V, T)
    elif (3. <= H) and (H < 4.):
        RGB = (P, Q, V)
    elif (4. <= H) and (H < 5.):
        RGB = (T, P, V)
    elif (5. <= H) and (H < 6.):
        RGB = (V, P, Q)
    else:
        RGB = (0., 0., 0.)
    return RGB



if __name__ == '__main__':
    def toname(g):
        return g.__name__.replace('gradient_', '').replace('_', '-').upper()

    gradients = (gradient_rgb_bw, gradient_rgb_gbr, gradient_rgb_gbr_full, gradient_rgb_wb_custom,
                 gradient_hsv_bw, gradient_hsv_gbr, gradient_hsv_unknown, gradient_hsv_custom)

    plot_color_gradients(gradients, [toname(g) for g in gradients])