import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib

import matplotlib.pyplot as plt
from matplotlib import cm
import re
from time import sleep
from sympy import numer
import sympy
from sympy.parsing.latex import parse_latex
from sympy.plotting import plot, plot3d

# plt.rcParams.update({"text.usetex": True, "xtick.labelsize": 16, "ytick.labelsize": 16})
plt_color = ["#0025b8", "#820303", "#02630f", "#460263", "#018c75"]




def plot_eq(equations, ax, fig):

    ax.clear()

    ax, fig = check_axis(equations[0], ax, fig)

    for idx, eq in enumerate(equations):
   
        eq = eq.replace("\\cdot", "*")
        if "z" in eq:
            dim = 3
            eq = eq.replace("z", "")
            eq = eq.replace("=", "")
        else:
            dim = 2
            eq = eq.replace("y", "")
            eq = eq.replace("=", "")

        
        # plot equations
        sympy_eq = parse_latex(eq)

        
        if dim == 2:
            p = plot(sympy_eq,show=False)
            eq_latex = (
                r"$y="
                + sympy.latex(sympy_eq)
                + "$"
            )
            x,y =p[0].get_data()
            ax.plot(
                x,
                y,
                label=eq_latex,
                color=plt_color[idx],
                linewidth=2,
            )
        else:
            p = plot3d(sympy_eq,show=False)
           
            x,y,z =p[0].get_meshes()
            eq_latex = (
                r"$z="
                + sympy.latex(sympy_eq)
                + "$"
            )
            surf = ax.plot_surface(
                x,
                y,
                z,
                label=eq_latex,
                cmap=cm.coolwarm,
                linewidth=0,
                antialiased=False,
            )
            surf._facecolors2d = surf._facecolor3d
            surf._edgecolors2d = surf._edgecolor3d

    ax.legend(fontsize=12)
    plt.pause(0.0001)
    plt.show(block=False)
    plt.pause(0.0001)

    return ax, fig


def check_axis(eq, ax, fig):

    if "z" in eq:
        if ax.name != "3d":
            ax.remove()
            plt.pause(0.0001)
            ax = fig.add_subplot(projection="3d")
            plt.pause(0.0001)
    else:
        if ax.name == "3d":
            ax.remove()
            plt.pause(0.0001)
            ax = fig.add_subplot()
            plt.pause(0.0001)

    return ax, fig


if __name__ == "__main__":
    plt.ion()
    fig = plt.figure(figsize=(8, 5), tight_layout=True)
    ax = fig.gca()
    plt.pause(0.0001)

    equations = ["y=\\sqrt{\\sqrt{x^2}}+\\sqrt{1-x^2}", "y=\\sqrt{\\sqrt{x^2}}-\\sqrt{1-x^2}"]
    ax, fig = plot_eq(equations, ax, fig)
    sleep(2)
    equations = [r"z=x^2-y^2"]
    ax, fig = plot_eq(equations, ax, fig)
    sleep(2)

    # equations = ["z=x+y"]
    # ax, fig = plot_eq(equations, ax, fig)
    # sleep(2)

    # equations = ["y=x^2", "y=2*x"]
    # ax, fig = plot_eq(equations, ax, fig)
    # sleep(2)
