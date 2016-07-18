#!/usr/bin/env python

#script to draw a heatmap from counts data, i.e. PFAM, InterPro, or even OTU table

import sys, warnings, argparse
import pandas as pd
import numpy as np
with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    import matplotlib.pyplot as plt
    import seaborn as sns
    

#setup menu with argparse
class MyFormatter(argparse.ArgumentDefaultsHelpFormatter):
    def __init__(self,prog):
        super(MyFormatter,self).__init__(prog,max_help_position=48)
parser=argparse.ArgumentParser(prog='csv2heatmap.py', usage="%(prog)s [options] -i input.csv -o output.pdf",
    description='''Script that creates heatmap(s) from csv data, column 1 is the row name, csv file has headers.''',
    epilog="""Written by Jon Palmer (2016) nextgenusfs@gmail.com""",
    formatter_class = MyFormatter)
parser.add_argument('-i','--input', required=True, help='Input file (csv)')
parser.add_argument('-o','--output', required=True, help='Output file (pdf)')
parser.add_argument('-m','--method', default='clustermap', choices = ['clustermap', 'heatmap'], help='Type of heatmap')
parser.add_argument('--distance_metric', default='braycurtis', help='Distance metric for clustermap')
parser.add_argument('--cluster_method', default='single', choices=['single', 'complete', 'average', 'weighted'], help='Clustering method for clustermap')
parser.add_argument('--cluster_columns', default='False', choices = ['True', 'False'], help='Cluster columns')
parser.add_argument('--yaxis_fontsize', default='5', help='Font size for y-axis')
parser.add_argument('--xaxis_fontsize', default='8', help='Font size for x-axis')
parser.add_argument('--font', default='arial', help='Font set')
parser.add_argument('--color', default='gist_gray_r', help='Color palette')
parser.add_argument('--figsize', default='2x8', help='Figure size (3x5, 2x10, etc)')
parser.add_argument('--annotate', action='store_true', help='Annotate heatmap with values')
parser.add_argument('--scaling', default='None', choices= ['z_score', 'standard', 'None'], help='Scale the data by row')
parser.add_argument('--debug', action='store_true', help='Print the data table to terminal')
args=parser.parse_args()

#parse the figure size and get it into a tuple
dim = args.figsize.split('x')
figSize = (int(dim[0]),int(dim[1]))

if args.cluster_columns == 'False':
    cluster = False
else:
    cluster = True    

def drawHeatmap(df, output):
    #get size of table
    width = len(df.columns) / 2
    height = len(df.index) / 4
    fig, ax = plt.subplots(figsize=(width,height))
    cbar_ax = fig.add_axes(shrink=0.4)
    if args.annotate:
        sns.heatmap(df,linewidths=0.5, cmap=args.color, ax=ax, fmt="d", annot_kws={"size": 4}, annot=True)
    else:
        sns.heatmap(df,linewidths=0.5, cmap=args.color, ax=ax, annot=False)
    plt.yticks(rotation=0)
    plt.xticks(rotation=90)
    for item in ax.get_xticklabels():
        item.set_fontsize(int(args.xaxis_fontsize))
    for item in ax.get_yticklabels():
        item.set_fontsize(int(args.yaxis_fontsize))
    fig.savefig(output, format='pdf', dpi=1000, bbox_inches='tight')
    plt.close(fig)
    
def drawClustermap(df, output):
    if args.scaling == 'z_score':
        g = sns.clustermap(df, method=args.cluster_method, metric=args.distance_metric, linewidths=0.5, cmap=args.color, col_cluster=cluster, z_score=0, figsize=figSize)
    elif args.scaling == 'standard':
        g = sns.clustermap(df, method=args.cluster_method, metric=args.distance_metric, linewidths=0.5, cmap=args.color, col_cluster=cluster, standard_scale=0, figsize=figSize)
    else:
        g = sns.clustermap(df, method=args.cluster_method, metric=args.distance_metric, linewidths=0.5, cmap=args.color, col_cluster=cluster, figsize=figSize)
    plt.setp(g.ax_heatmap.get_yticklabels(), rotation=0, size=int(args.yaxis_fontsize), family=args.font)
    plt.setp(g.ax_heatmap.get_xticklabels(), rotation=90, size=int(args.xaxis_fontsize), family=args.font, weight='bold')
    g.savefig(output, format='pdf', dpi=1000, bbox_inches='tight')


#lets open up file and convert to dataframe
data = pd.read_csv(args.input, index_col=0)
if args.debug:
    print data

#run heatmap
if args.method == 'clustermap':
    drawClustermap(data, args.output)
else:
    drawHeatmap(data, args.output)