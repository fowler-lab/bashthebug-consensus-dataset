#! /usr/bin/env python

import argparse, pandas, numpy, time, copy

from scipy import stats

from tqdm import tqdm

def custom_aggregate(series):

    classifications=numpy.array(series).astype(int)

    if numpy.sum(classifications<0) >= len(classifications)/2:
        return(0,0,0,None)
    else:
        classifications=classifications[classifications>0]

        # note that if there are two modes, the smallest is returned
        mode,count=stats.mode(classifications)

        return(numpy.mean(classifications),numpy.median(classifications),float(mode[0]),numpy.std(classifications))


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--reading_days",nargs='+',type=int,required=True,help="which reading days to consider. Must be one or more of 7,10,14 or 21")
    parser.add_argument("--classifications",nargs='+',type=int,required=True,help="how many classifications to pick, can be list")
    parser.add_argument("--bootstraps",default=20,type=int,help="how many boostraps to do")
    parser.add_argument("--output_name",required=True,help="the name of the dataframe to save the results in")
    options = parser.parse_args()

    for i in options.reading_days:
        assert i in [7,10,14,21], 'not valid!'

    assert (options.bootstraps>0 and options.bootstraps<=100)

    start=time.time()

    CLASSIFICATIONS=pandas.read_pickle("tables/CLASSIFICATIONS.pkl.gz")
    CLASSIFICATIONS.reset_index(inplace=True)
    CLASSIFICATIONS.set_index(['PLATE','DRUG'],inplace=True)

    PHENOTYPES=pandas.read_pickle('tables/PHENOTYPES.pkl.gz')
    # remove some odd duplicates
    PHENOTYPES=PHENOTYPES.loc[~((PHENOTYPES.STRAIN.str[:3]=='CRY') & (PHENOTYPES.REPLICATE.isin(['0003','0004'])))]
    PHENOTYPES.reset_index(inplace=True)
    PHENOTYPES.set_index(['PLATE','DRUG'],inplace=True)

    table=[]

    for READINGDAY in options.reading_days:

        PHENOTYPES_SUBSET=PHENOTYPES.loc[PHENOTYPES.READINGDAY==READINGDAY]
        CLASSIFICATIONS_SUBSET=CLASSIFICATIONS.loc[CLASSIFICATIONS.READINGDAY==READINGDAY]

        for N_CLASSIFICATIONS in tqdm(options.classifications):

                # identify the drug images that we can sample from
                drug_images=PHENOTYPES_SUBSET.loc[(PHENOTYPES_SUBSET.N_TOTAL>=N_CLASSIFICATIONS)].index

                # subset down the classifications table
                CLASSIFICATIONS_SUBSET2=copy.deepcopy(CLASSIFICATIONS_SUBSET.loc[(CLASSIFICATIONS_SUBSET.index.isin(drug_images))])
                CLASSIFICATIONS_SUBSET2.reset_index(inplace=True)

                TOTAL_DRUG_IMAGES=len(drug_images)

                for boot in tqdm(range(options.bootstraps)):

                    # randomly sample
                    CLASSIFICATIONS_SAMPLE=CLASSIFICATIONS_SUBSET2[['PLATE','DRUG','BASHTHEBUG_DILUTION']].groupby(['PLATE','DRUG']).sample(n=N_CLASSIFICATIONS,replace=True)

                    # form consensus BB readings
                    df=CLASSIFICATIONS_SAMPLE.groupby(['PLATE','DRUG']).agg(custom_aggregate)

                    df=pandas.DataFrame(df['BASHTHEBUG_DILUTION'].tolist(),index=df.index)
                    df.columns=['MEAN','MEDIAN','MODE','STDDEV']
                    df['BOOTSTRAP_RUN']=boot
                    df['N_CLASSIFICATIONS']=N_CLASSIFICATIONS
                    df['N_DRUG_IMAGES']=TOTAL_DRUG_IMAGES
                    df['READINGDAY']=READINGDAY
                    table.append(df)

    CONSENSUS_DATASET=pandas.concat(table)
    CONSENSUS_DATASET=CONSENSUS_DATASET[['READINGDAY','N_DRUG_IMAGES','N_CLASSIFICATIONS','BOOTSTRAP_RUN','MEAN','MEDIAN','MODE','STDDEV']]
    CONSENSUS_DATASET.to_pickle('bootstraps/'+options.output_name+".pkl")
    # CONSENSUS_DATASET.to_csv('bootstraps/'+options.output_name+'.csv')
