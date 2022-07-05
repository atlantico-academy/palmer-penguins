import seaborn as sns
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import patches
import pandas as pd


colors = ['#6892b1', '#282625', '#c9bfaf']#, '#9199a2', '#626c74']

sns.set_theme(style="whitegrid")
sns.set_palette(sns.color_palette(colors))

def group_graph(df, list_vars):
    query_data = (
        df
        .groupby(list_vars)
        .aggregate('count')
        .reset_index()
    )
    # display(query_data)
    query_data = (
        query_data.assign(Quantidade = query_data.bill_length_mm)
        .sort_values(by='Quantidade', ascending=False)
    )
    query_data = query_data
    x_order = list(query_data[list_vars[2]].unique())
    no_info = 'Não informado'
    if x_order.count(no_info):
        x_order.remove(no_info)
        x_order.append(no_info)
    catp = sns.catplot(
        x=list_vars[1],
        y="Quantidade",
        hue=list_vars[0],
        col=list_vars[2],
        data=query_data,
        kind="bar",
        height=4,
        aspect=.7, 
        col_order=x_order,
        palette=colors
    ).set_titles("{col_name}")
    for x, y, z in [ax[0] for ax in catp.facet_data()]:
        ax = catp.facet_axis(x, y, z)
        for c in ax.containers:
            labels = [f'{(v.get_height() / len(df) * 100):.1f} %' for v in c]
            ax.bar_label(c, labels=labels, label_type='edge', fontsize=9)
    plt.suptitle(f"Distribuição de {list_vars[0]} por {'IDH' if list_vars[2] == 'idh_label' else list_vars[2].replace('_', ' ').capitalize()}\n",  y=1.1, fontweight='bold')
    plt.show()


def cat_graph(df, var_name, axe):
    query_data = df.groupby(var_name).aggregate('count').reset_index()
    ax = sns.barplot(y=var_name, x='paciente_id', data=query_data, color=colors[0], ax=axe)
    labels = [f'{(v.get_width() / len(df) * 100):.1f} %' for v in ax.containers[0]]
    graph = ax.bar_label(ax.containers[0], labels=labels, label_type='edge', fontsize=12)
    ax.set(
        xlabel='Quantidade',
        title=f"{var_name}"
    )
    sns.despine(left=True, bottom=False)
    return ax

def histogram(df, var_name, axe=None):
    ax = sns.histplot(data=df, x=var_name, alpha=1, color=colors[0], ax=axe)
    labels = [f'{(v.get_height() / len(df) * 100):.1f} %' for v in ax.containers[0]]
    graph = ax.bar_label(ax.containers[0], labels=labels, label_type='edge', fontsize=8)
    ax.xaxis.grid(False)
    ax.set(
        ylabel='Quantidade',
        title=f"{var_name}"
    )
    sns.despine(left=True, bottom=False)
    return ax

def correlation(df, title, annot=False):
    for i in 
    corr = df.corr()

    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # Set up the matplotlib figure
    f, ax = plt.subplots(figsize=(6, 6))

    # Generate a custom diverging colormap
    cmap = sns.diverging_palette(0, 255, as_cmap=True)

    # Draw the heatmap with the mask and correct aspect ratio
    sns.heatmap(corr, mask=mask, cmap=cmap, center=0, square=True, linewidths=.5, cbar_kws={"shrink": .5}, annot=annot, fmt=".2f")
    plt.suptitle(f"Correlação ({title})", fontweight='bold')
    plt.show()

def correlation_between(df, var_list_1, var_list_2, title, annot=False):
    corr = (
        df.replace(["Não", "Sim"], [0, 1])
        .corr()
        .query('index in @var_list_1')[var_list_2]
    )
    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # Set up the matplotlib figure
    f, ax = plt.subplots(figsize=(6, 6))

    # Generate a custom diverging colormap
    cmap = sns.diverging_palette(0, 255, sep=77, as_cmap=True)

    # Draw the heatmap with the mask and correct aspect ratio
    sns.heatmap(corr, cmap=cmap, center=0, square=True, linewidths=.5, cbar_kws={"shrink": .5}, annot=annot, fmt=".2f")
    plt.suptitle(f"Correlação ({title})", fontweight='bold')
    plt.show()


def results_plot(df, title):
    catp = (
        sns
        .catplot(x='model', y='mean', col='metric', data=df, kind="bar")#, col_wrap=2)
        .set_titles("{col_name}")
        .set_ylabels("Média")
    )
    for x, y, z in [ax[0] for ax in catp.facet_data()]:
        ax = catp.facet_axis(x, y, z)
        for c in ax.containers:
            labels = [f'{v.get_height():.2f}' for v in c]
            ax.bar_label(c, labels=labels, label_type='edge', fontsize=12)
    plt.suptitle(title,  y=1.1, fontweight='bold')
    plt.show()