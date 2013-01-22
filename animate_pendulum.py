#!/usr/bin/env python
# -*- coding: utf-8 -*

"""Basic animation of the n pendulum.

In IPython you can type:

run n_pend.py
from animate_pendulum import animate_pendulum
animate_pendulum(t, y, link_l)

This will show a graph on screen and also create a video.
"""
from numpy import zeros, cos, sin, arange
from matplotlib import pyplot as plt
from matplotlib import animation

def animate_pendulum(t, states, link_l):
    # First set up the figure, the axis, and the plot element we want to animate
    fig = plt.figure()
    ax = plt.axes(xlim=(-0.2, 0.2), ylim=(-1, 0), aspect='equal')
    line, = ax.plot([], [], lw=2, marker='o', markersize=12)

    # initialization function: plot the background of each frame
    def init():
        line.set_data([], [])
        return line,

    # animation function.  This is called sequentially
    def animate(i):
        x = zeros((5))
        y = zeros((5))
        for j in arange(1, 5):
            x[j] = link_l * sin(states[i, j]) + x[j - 1]
            y[j] = -link_l * cos(states[i, j]) + y[j - 1]
        line.set_data(x, y)
        return line,

    # call the animator.  blit=True means only re-draw the parts that have changed.
    anim = animation.FuncAnimation(fig, animate, frames=len(t), init_func=init,
            interval=10, blit=True, repeat=False)

    # save the animation as an mp4.  This requires ffmpeg or mencoder to be
    # installed.  The extra_args ensure that the x264 codec is used, so that
    # the video can be embedded in html5.  You may need to adjust this for
    # your system: for more information, see
    # http://matplotlib.sourceforge.net/api/animation_api.html
    anim.save('pendulum_animation.mp4', fps=30)
    #, extra_args=['-vcodec', 'libx264'] #for html5 video
    plt.show()
