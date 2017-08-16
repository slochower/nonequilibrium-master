"""
General functions for controlling the aesthetics of figures and
ensuring consistency.
"""

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.colors import colorConverter
import seaborn as sns


def prepare_plot():
    """
    Set up general plot aesthetics to be used for including figures in a manuscript or talk.
    These defaults are possibly too large for interactive use.
    This function should be called before `paper_plot`.
    """
    sns.set()
    # Increase font size and linewidth
    sns.set_context("notebook", font_scale=2, rc={"lines.linewidth": 5})
    sns.set_style("white")
    # Use LaTeX, setup to use Helvetica. This can be safely commented to make
    # the installation footprint of running this code smaller -- for example,
    # in Docker.
    mpl.rc('text', usetex=True)
    mpl.rcParams['text.latex.preamble'] = [
        r'\usepackage{amsmath}',
        r'\usepackage{helvet}',
        r'\usepackage[EULERGREEK]{sansmath}',
        r'\sansmath',
        r'\renewcommand{\familydefault}{\sfdefault}',
        r'\usepackage[T1]{fontenc}',
        r'\usepackage{graphicx}'
    ]


def paper_plot(fig, adjustment=0, scientific=False, save=False, filename=None,
               raster=False, label_pad=True):
    """
    Take a prepared figure and make additional adjustments for inclusion in manuscript:
    mostly tick thickness, length, and label padding, and include only the left and the bottom
    axis spines. It would be nice to force the axes to end on a major tick, but I haven't
    figured out how to do that yet.
    :param fig:
    :param adjustment:
    :param scientific:
    """
    for ax in fig.axes:
        # Increase padding
        ax.tick_params(which='major', direction='out', length=10, pad=10)
        ax.tick_params(which='minor', direction='out', length=5)
        # If plotting with pi, increase the x tick size specifically
        # ax.tick_params(axis='x', labelsize=40, pad=-10)
        # Increase tick thickness
        ax.xaxis.set_tick_params(width=2)
        ax.yaxis.set_tick_params(width=2)
        ax.yaxis.set_ticks_position('left')
        ax.xaxis.set_ticks_position('bottom')
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        if label_pad:
            # Increase padding
            ax.xaxis.labelpad = 15
            ax.yaxis.labelpad = 15
        # Make the background color white
        facecolor = 'white'
        if facecolor is False:
            facecolor = fig.get_facecolor()
        alpha = 1
        color_with_alpha = colorConverter.to_rgba(facecolor, alpha)
        fig.patch.set_facecolor(color_with_alpha)
        # Stick the scientific notation into the axis label, instead of the
        # default position which in the corner, which really makes no sense.
        if ax.xaxis.get_scale() == 'linear':
            if scientific:
                pretty_label(ax)
            ax.get_xaxis().set_minor_locator(mpl.ticker.AutoMinorLocator())
            ax.get_yaxis().set_minor_locator(mpl.ticker.AutoMinorLocator())
        elif ax.xaxis.get_scale() == 'log':
            pass
        # For scatter plots, where points get cut off
        if adjustment != 0:
            x0, x1, y0, y1 = ax.axis()
            ax.xaxis((x0 - adjustment,
                      x1 + adjustment,
                      y0,
                      y1
                      ))
        # Make axes thicker
        for axis in ['top', 'bottom', 'left', 'right']:
            ax.spines[axis].set_linewidth(2)
    if save:
        plt.savefig(filename + '.png', dpi=300, bbox_inches='tight')
        plt.savefig(filename + '.svg', dpi=300, bbox_inches='tight')


def generic_plot(x, y, xlabel=None, ylabel=None, scientific=False,
                 c=None, panel_label=None, panel_xoffset=-0.24, panel_yoffset=0.95):
    """
    Quickly plot some data in a consistent style, useful for interactive explorations.
    :param x: List or array of data
    :param y: List or array of data
    :param xlabel: Label for $x$ axis
    :param ylabel: Label for $y$ axis
    :param scientific: Scientific notation boolean
    :param c: Color
    :param panel_label: Figure label (top left)
    :param panel_xoffset: Figure label $x$ position fine tuning
    :param panel_yoffset: Figure label $y$ position fine tuning
    :return:
    """
    fig = plt.figure(figsize=(6 * 1.2, 6))
    grid = GridSpec(1, 1, wspace=0.2, hspace=0.5)
    ax = plt.subplot(grid[0, 0])
    if c:
        ax.plot(x, y, 'o', markersize=10, markeredgecolor='k',
                markeredgewidth=0.8, alpha=0.5, mfc=c)
    else:
        ax.plot(x, y, 'o', markersize=10, markeredgecolor='k',
                markeredgewidth=0.8, alpha=0.5, mfc='b')
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    if scientific:
        pretty_label(ax)
    if panel_label:
        ax.annotate(r'\textbf{{ {} }}'.format(panel_label), xy=(0, 0),
                    xytext=(panel_xoffset, panel_yoffset),
                    xycoords='axes fraction', fontsize=24, fontweight='bold')
    ax.margins(None)
    paper_plot(fig)
    return ax


def setup_plot(y_label, x_label, axis_padding=0.06):
    # https://stackoverflow.com/questions/31928209/matplotlib-fixed-spacing-between-left-edge-of-figure-and-y-axis
    fig_width = 6 * 1.2
    fig_height = 6
    fig = plt.figure(figsize=(fig_width, fig_height))
    left_margin = 0.95 / fig_width
    right_margin = 0.20 / fig_width
    bottom_margin = 0.50 / fig_height
    top_margin = 0.25 / fig_height
    x = left_margin + axis_padding   # horizontal position of bottom-left corner
    y = bottom_margin                # vertical position of bottom-left corner
    w = 1 - (left_margin + right_margin)  # width of axes
    h = 1 - (bottom_margin + top_margin)  # height of axes
    ax = fig.add_axes([x, y, w, h])
    y_label_x = 0
    y_label_y = y + h / 2.0
    ax.set_ylabel(y_label, verticalalignment='top',
                  horizontalalignment='center')
    # Horizontally, the "top" of the y axis label is `label_padding` from
    # from the left edge of the figure, no matter what.
    ax.yaxis.set_label_coords(y_label_x, y_label_y, transform=fig.transFigure)
    ax.set_xlabel(x_label)
    return fig, ax


def update_label(old_label, exponent_text):
    """
    Update an axis label with scientific notation using LaTeX formatting for the
    order of magnitude.
    :param old_label:
    :param exponent_text:
    :return:
    """
    if exponent_text == "":
        return old_label
    try:
        units = old_label[old_label.index("(") + 1:old_label.rindex(")")]
    except ValueError:
        units = ""
    label = old_label.replace("({})".format(units), "")
    exponent_text = exponent_text.replace(r"$\times$", "")
    return "{} ({} {})".format(label, exponent_text, units)


def pretty_label(ax, axis='both'):
    """
    Format the label string with the exponent from the ScalarFormatter.
    :param ax:
    :param axis:
    """
    try:
        ax.xaxis
    except:
        ax = plt.gca()

    ax.ticklabel_format(axis=axis, style='sci')
    axes_instances = []
    if axis in ['x', 'both']:
        axes_instances.append(ax.xaxis)
    if axis in ['y', 'both']:
        axes_instances.append(ax.yaxis)
    for ax in axes_instances:
        ax.major.formatter._useMathText = True
        plt.draw()  # Update the text
        exponent_text = ax.get_offset_text().get_text()
        label = ax.get_label().get_text()
        ax.offsetText.set_visible(False)
        ax.set_label_text(update_label(label, exponent_text))


def panel_label(label=None,
                panel_xoffset=-0.24, panel_yoffset=0.95):
    """
    Add a small label to the top left region of a figure.
    :param label: Figure label string
    :param panel_xoffset: Figure label $x$ position fine tuning
    :param panel_yoffset: Figure label $y$ position fine tuning
    """
    ax = plt.gca()
    ax.annotate(r'\textbf{{ {} }}'.format(label), xy=(0, 0),
                xytext=(panel_xoffset, panel_yoffset),
                xycoords='axes fraction', fontsize=24, fontweight='bold')
