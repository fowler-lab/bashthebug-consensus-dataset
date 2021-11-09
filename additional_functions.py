#!#! /usr/bin/env python

import pandas,copy,numpy,math,pathlib

import matplotlib.pyplot as plt
import matplotlib.colors as colors

plt.rcParams.update({'font.size': 12})

def plot_heatmap(df,reading_day,type,dataset,n_classifications,growth,method,label,exclude_nr=False,vmax=100):

    df=numpy.array(df)
    df.resize((10,10))
    if exclude_nr:
        df=df[1:,1:]
        fig,ax=plt.subplots(1,1,figsize=(6,6))
    else:
        fig,ax=plt.subplots(1,1,figsize=(8,8))

    df=numpy.flipud(df)
    df=df*100

    if exclude_nr:
        # if numpy.sum(df)==0:
        #     print(df)
        df=df/numpy.sum(df)
        df=df*100
        xtics=[str("%i" % i) for i in range(1,10)]
        ytics=[str("%i" % i) for i in range(1,10)]
        ax.set_xticks(range(0,9))
        ax.set_yticks(range(8,-1,-1))
        ax.set_xlim([-0.5,8.5])
        ax.set_ylim([8.5,-0.5])
        max_xy=9

    else:
        # create lists for the x and ytics
        xtics=['NR']+[str("%i" % i) for i in range(1,10)]
        ytics=['NR']+[str("%i" % i) for i in range(1,10)]
        ax.set_xticks(range(0,10))
        ax.set_yticks(range(9,-1,-1))
        ax.set_xlim([-0.5,9.5])
        ax.set_ylim([9.5,-0.5])
        max_xy=10

    # set the x and ytics
    ax.set_xticklabels(xtics,size='large')
    ax.set_yticklabels(ytics,size='large')

    cmap = colors.LinearSegmentedColormap.from_list("", ["white","#9AB51E","#DC2D4C"])

    ax.imshow(df, interpolation='nearest',cmap=cmap,norm=colors.PowerNorm(gamma=4./5.,vmin=0,vmax=vmax))
    # ax.imshow(df, interpolation='nearest',cmap='RdPu',norm=colors.PowerNorm(gamma=2./5.,vmin=0,vmax=100))
    for i in range(max_xy):
        for j in range(max_xy-1,-1,-1):
            if df[(j,i)] > 10:
                ax.text(i,j,str("%.1f" % (df[(j,i)])),horizontalalignment='center',verticalalignment='center',color='white',size='large',weight="heavy")
            elif df[(j,i)] > 0.1:
                ax.text(i,j,str("%.1f" % (df[(j,i)])),horizontalalignment='center',verticalalignment='center',color='black',size='large')

    path=pathlib.Path.cwd() / 'pdf' / str(reading_day) / type / dataset / str(n_classifications) / growth
    if method is None:
        filename='map-'+str(reading_day)+"-"+type+'-'+str(dataset)+'-'+str(n_classifications)+'-'+growth+'-'+label+".pdf"
    else:
        filename='map-'+str(reading_day)+"-"+type+'-'+str(dataset)+'-'+str(n_classifications)+'-'+growth+'-'+method+'-'+label+".pdf"
    path.mkdir(parents=True,exist_ok=True)

    fig.savefig(path / filename,transparent=True)

    # filename=stem+".npy"
    # with open(path / filename,'wb') as f:
    #     numpy.save(f,df)

    plt.close()

#     return(row)

def plot_classifications_hist(series,reading_day,type,dataset,n_classifications,growth,label,color,orientation='vertical'):

    if orientation=='horizontal':
        figure,axes = plt.subplots(figsize=(8,3))
        hist,edges,rects=axes.hist(series,\
                  density=True,\
                  align='left',\
                  orientation='vertical',\
                  bins=range(0,11,1),\
                  color=color)

        for ix,iy in zip(edges,hist):
            axes.text(ix,iy+0.01,"%.1f%%" % (100*iy),color=color,horizontalalignment='center')

        axes.set_ylim([0,0.55])
        axes.set_yticks([])
        axes.spines['top'].set_visible(False)
        axes.spines['right'].set_visible(False)
        axes.spines['left'].set_visible(False)
        # axes.set_xlabel('dilution')
        axes.set_xticks(range(0,10,1))
        axes.set_xticklabels(['NR',1,2,3,4,5,6,7,8,9])

    else:
        figure,axes = plt.subplots(figsize=(3,8))
        hist,edges,rects=axes.hist(series,\
                  density=True,\
                  align='left',\
                  orientation='horizontal',\
                  bins=range(0,11,1),\
                  color=color)

        for iy,ix in zip(edges,hist):
            axes.text(ix+0.01,iy,"%.1f%%" % (100*ix),color=color,horizontalalignment='left')

        axes.set_xlim([0,0.55])
        axes.set_xticks([])
        axes.spines['top'].set_visible(False)
        axes.spines['right'].set_visible(False)
        axes.spines['bottom'].set_visible(False)
        axes.set_ylabel('dilution')
        axes.set_yticks(range(0,10,1))
        axes.set_yticklabels(['NR',1,2,3,4,5,6,7,8,9])

    path=pathlib.Path.cwd() / 'pdf' / str(reading_day) / type / dataset / str(n_classifications) / growth
    # path=pathlib.Path.cwd() / 'pdf' / str(reading_day) / str(truth_set.lower())
    path.mkdir(parents=True,exist_ok=True)
    filename='hist-'+label+'.pdf'

    figure.savefig(path / filename,transparent=True)
    plt.close()

def calculate_grid_metrics(df):

    df=numpy.array(df)

    assert df.shape==(10,10)
    # df.resize((10,10))
    # if numpy.sum(df)==0:
    #     print(df)

    row=[numpy.sum(df)]

    df=df/numpy.sum(df)
    df*=100    

    # diagonal, excluding (NR,NR)
    row.append(sum([df[i][i] for i in range(1,10)]))

    # upper diagonal, excluding (NR,NR)
    row.append(sum([df[i+1][i] for i in range(1,9)]))

    # lower diagonal, excluding (NR,NR)
    row.append(sum([df[i][i+1] for i in range(1,9)]))

    # upper triangle
    row.append(numpy.sum([numpy.sum(df[i+2:,i]) for i in range(1,8)]))

    # lower triangle
    row.append(numpy.sum([numpy.sum(df[i,i+2:]) for i in range(1,8)]))

    # both NR
    row.append(df[0,0])

    # method NR, truth ok
    row.append(numpy.sum(df[1:,0]))

    # method ok, truth NR
    row.append(numpy.sum(df[0,1:]))

    # inner square, not NR
    row.append(numpy.sum(df[1:,1:]))

    return(row)
