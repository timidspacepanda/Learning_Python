import matplotlib.pyplot as plt

def indep_hist_plot(group1, group2, nbins=10):
    fig, ax = plt.subplots()
    ax.hist(group1, bins=nbins, alpha=0.7, label='Group 1', color='blue')
    ax.hist(group2, bins=nbins, alpha=0.7, label='Group 2', color='orange')

    ax.set_title("Historgram of Group 1 and Group 2")
    ax.set_xlabel('Value')
    ax.set_ylabel('Frequency')
    ax.legend()

    return fig

def indep_hist_subplot(ax, group1, group2, nbins=10):
    ax.hist(group1, bins=nbins, alpha=0.7, label='Group 1', color='blue')
    ax.hist(group2, bins=nbins, alpha=0.7, label='Group 2', color='orange')

    ax.set_title("Historgram of Group 1 and Group 2")
    ax.set_xlabel('Value')
    ax.set_ylabel('Frequency')
    ax.legend()


def dual_boxplot(group1, group2):
    fig, ax = plt.subplots()
    ax.boxplot([group1, group2], label=['Group 1', 'Group 2'])
    ax.set_title("Boxplot of Group 1 andd Group 2")
    ax.set_ylabel('Value')
    
    return fig

def dual_boxplot_sub(ax, group1, group2):
    ax.boxplot([group1, group2], label=['Group 1', 'Group 2'])
    ax.set_title("Boxplot of Group 1 andd Group 2")
    ax.set_ylabel('Value')
