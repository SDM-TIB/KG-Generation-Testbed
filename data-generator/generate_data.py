#!/usr/bin/env python3
import pandas as pd
import subprocess


def sample(x, n):
    """
     Get n number of rows as a sample
    """
    # import random
    # print(random.sample(list(x.index), n))
    return x.iloc[list(range(n))]


def generate_table(nrows, IDstart=1, P1start=1):
    """
     Generate table which contain [ID,P1] columns
     - nrows: number of rows per table
     - IDstart: starting sequence for ID column
     - P1start: starting number for P1 column

     return generated table `table1`
    """
    subjID = range(IDstart, nrows+IDstart)
    P1 = ["V_" + str(i) for i in range(P1start, P1start + nrows)]
    data = {"ID": subjID, "P1": P1}
    table1 = pd.DataFrame(data)
    return table1


def low_selectivity(nrows=[1000]):
    """

    """
    def generate_low_selectivity(numrows):
        table1 = generate_table(numrows)
        table2 = generate_table(numrows)
        return table1, table2

    # Number of rows per table
    #nrows = [1000, 3000, 10000, 50000, 100000]

    for nrow in nrows:
        subprocess.check_call('mkdir -p ../data/joinselectivity/low_selectivity/'+ str(int(nrow/1000)) + 'k_rows', shell=True)
        table1, table2 = generate_low_selectivity(nrow)
        table1.to_csv('../data/joinselectivity/low_selectivity/'+ str(int(nrow/1000)) + 'k_rows/table1.csv', index=False )
        table2.to_csv('../data/joinselectivity/low_selectivity/'+ str(int(nrow/1000)) + 'k_rows/table2.csv', index=False )


def high_selectivity(nrows=[1000], percentages=[0.05]):
    """

    """
    def generate_high_selectivity(table1, table2, numrows, percentage):
        """
        Sample rows for percentage and update the sampled rows
        return: updated table2
        """
        prows = numrows * percentage

        tbl1_sample = sample(table1, int(prows))
        tbl2_sample = sample(table2, int(prows))

        for i, j in zip(list(tbl1_sample.index), list(tbl2_sample.index)):
            table2.loc[j, 'P1'] =  table1.loc[i, 'P1']

        return table2

    # Number of rows per table
    # nrows = [1000, 3000, 10000, 50000, 100000]
    # Percentage of data involved in the join condition
    # percentages = [0.05, 0.1, 0.2, 0.3, 0.5]

    for nrow in nrows:
        # Create folder
        subprocess.check_call('mkdir -p ../data/joinselectivity/high_selectivity/'+ str(int(nrow/1000)) + 'k_rows', shell=True)
        # generate table 1
        table1 = generate_table(nrow)
        table1.to_csv('../data/joinselectivity/high_selectivity/'+ str(int(nrow/1000)) + 'k_rows/table1.csv', index=False )
        for p in percentages:
            # generate table 2
            table2 = generate_table(nrow, P1start=nrow+1)
            table2 = generate_high_selectivity(table1, table2, nrow, p)
            table2.to_csv('../data/joinselectivity/high_selectivity/'+ str(int(nrow/1000)) + \
                          'k_rows/table2_' + str(int(100*p)) + '_percent.csv', index=False )


def update_joinable_rows(table1, table2, nrows, percentage):
    """
    Sample rows for percentage and update the sampled rows
    - table1:
    - table2:
    - nrows: number of rows in each table
    - percentage: ratio of rows in table1 that are involved in join condition to table2

    return: updated table2
    """
    prows = nrows * percentage

    tbl1_sample = sample(table1, int(prows))
    tbl2_sample = sample(table2, int(prows))

    for i, j in zip(list(tbl1_sample.index), list(tbl2_sample.index)):
        table2.loc[j, 'P1'] =  table1.loc[i, 'P1']

    return table2

def one_to_one(nrows, p=0.5):
    # Number of rows per table
    # nrows = [1000, 3000, 10000, 50000, 100000]

    for nrow in nrows:
        subprocess.check_call('mkdir -p ../data/relation_type/one-one/'+ str(int(nrow/1000)) + 'k_rows', shell=True)
        table1 = generate_table(nrow)
        table1.to_csv('../data/relation_type/one-one/'+ str(int(nrow/1000)) + 'k_rows/' + 'table1.csv', index=False )
        table2 = generate_table(nrow, P1start=nrow+1)
        # 50 % selectivity - ration of rows involved in join condition (mid in this case)
        # p = 0.5
        table2 = update_joinable_rows(table1, table2, nrow, p)
        table2.to_csv('../data/relation_type/one-one/'+ str(int(nrow/1000)) + 'k_rows/' + \
                      'table2_' + str(int(100*p)) + '_percent.csv', index=False )


def one_to_many(nrows=[1000], N=5, percentages=[0.025], p=0.5):
    """

    """

    def update_joinable_relation_rows(table1, nrows, selecivity_percentage, \
                                      N, relation_from_percentage=-1, \
                                      relation_to_percentage=-1):
        """
        Sample rows for percentage and update the sampled rows
        return: updated table 1, table2
        """
        prows = nrows * selecivity_percentage
        tbl1_sample = sample(table1, int(prows))
        rpercentage = nrows

        if relation_to_percentage > 0:
            rpercentage = nrows * relation_to_percentage

        NumOfP1s = rpercentage / N
        # print(NumOfP1s, prows, rpercentage)
        tbl1_sample = tbl1_sample.reset_index(drop=True)
        P1ForJoin = sample(tbl1_sample, int(NumOfP1s+0.7))
        values = list(set([row[1]['P1'] for  row in P1ForJoin.iterrows()]))
        values = values * N
        if len(values) > nrows:
            values = values[:nrows]

        table2 = generate_table(nrows, P1start=nrows+1)
        tbl2_sample = sample(table2, len(values))
        # print(len(values), len(list(set((tbl2_sample.index)))))
        for i, j in zip(values, list(tbl2_sample.index)):
            table2.loc[j, 'P1'] =  i

        return table1, table2

    # Number of rows per table
    # nrows = [1000, 3000, 10000, 50000, 100000]

    # value of N (relation size)
    # N = [5, 10, 15]
    # 50 % selectivity - percentage of rows, overall, involvd in join from table1 to table2
    #p = 0.5
    # percentage of rows that are involved in 1-N relation
    # percentages = [0.25 , 0.5]

    for nrow in nrows:
        subprocess.check_call('mkdir -p ../data/relation_type/one-N/'+ str(int(nrow/1000)) + 'k_rows', shell=True)
        table1 = generate_table(nrow)
        table1.to_csv('../data/relation_type/one-N/'+ str(int(nrow/1000)) + 'k_rows/table1.csv', index=False )
        for rp in percentages:
            for n in N:
                table1, table2 = update_joinable_relation_rows(table1, nrow, p, n, -1, rp)
                table2.to_csv('../data/relation_type/one-N/'+ str(int(nrow/1000)) + 'k_rows/table2_' + \
                              str(int(100*p)) + "_" + str(n) + "_" + str(int(100*rp)) + '_percent.csv', index=False )



def many_to_one(nrows=[1000], N=5, percentages=[0.025], p=0.5):
    """

    """

    def update_joinable_relation_rows(table1, nrows, selecivity_percentage, \
                                      N, relation_from_percentage=-1, \
                                      relation_to_percentage=-1):
        """
        Sample rows for percentage and update the sampled rows
        return: updated table 1, table2
        """
        prows = nrows * selecivity_percentage
        tbl1_sample = sample(table1, int(prows))
        rpercentage = nrows

        if relation_to_percentage > 0:
            rpercentage = nrows * relation_to_percentage

        NumOfP1s = rpercentage / N
        # print(NumOfP1s, prows, rpercentage)
        tbl1_sample = tbl1_sample.reset_index(drop=True)
        P1ForJoin = sample(tbl1_sample, int(NumOfP1s+0.7))
        values = list(set([row[1]['P1'] for  row in P1ForJoin.iterrows()]))
        values = values * N
        if len(values) > nrows:
            values = values[:nrows]

        table2 = generate_table(nrows, P1start=nrows+1)
        tbl2_sample = sample(table2, len(values))
        # print(len(values), len(list(set((tbl2_sample.index)))))
        for i, j in zip(values, list(tbl2_sample.index)):
            table2.loc[j, 'P1'] =  i

        return table1, table2

    # Number of rows per table
    # nrows = [1000, 3000, 10000, 50000, 100000]

    # value of N (relation size)
    # N = [5, 10, 15]
    # 50 % selectivity - percentage of rows, overall, involvd in join from table1 to table2
    # p = 0.5
    # percentage of rows that are involved in 1-N relation
    # percentages = [0.25 , 0.5]

    for nrow in nrows:
        subprocess.check_call('mkdir -p ../data/relation_type/N-one/'+ str(int(nrow/1000)) + 'k_rows', shell=True)
        table1 = generate_table(nrow)
        table1.to_csv('../data/relation_type/N-one/'+ str(int(nrow/1000)) + 'k_rows/table2.csv', index=False )
        for rp in percentages:
            for n in N:
                table1, table2 = update_joinable_relation_rows(table1, nrow, p, n, -1, rp)
                table2.to_csv('../data/relation_type/N-one/'+ str(int(nrow/1000)) + 'k_rows/table1_' + \
                              str(int(100*p)) + "_" + str(n) + "_" + str(int(100*rp)) + '_percent.csv', index=False )


def many_to_many(nrows, N, M, NP, MP, p=0.5):
    """

    """
    def update_joinable_n_m_relation_rows(table1,
                                      table2,
                                      nrows=1000,
                                      selecivity_percentage=0.5,
                                      N = 3,
                                      M = 5,
                                      relation_from_percentage=0.1,
                                      relation_to_percentage=0.1):
        """
        Sample rows for percentage and update the sampled rows
        return: updated table 1, table2
        """
        prows = nrows * selecivity_percentage
        # Sample selecivity_percentage of rows in the first table
        tbl1_sample = sample(table1, int(prows))
        # Sample selecivity_percentage of rows from second table to make them joinable (pudate P1 same values as frist table)
        tbl2_sample = sample(table2, int(prows))

        rpercentagen = nrows
        rpercentagem = nrows

        if relation_from_percentage > 0:
            rpercentagen = nrows * relation_from_percentage

        if relation_to_percentage > 0:
            rpercentagem = nrows * relation_to_percentage

        NumOfP1sN = rpercentagen / N
        NumOfP1sM = rpercentagem / M

        tbl1_sample_v = tbl1_sample.reset_index(drop=True)

        # Sample relation_to_percentage of rows
        P1ForJoinM = sample(tbl1_sample_v, int(NumOfP1sM+0.7))
        # Extract unique values of P1 from table1, only those sampled for percentage to table 2
        values = list(set([row[1]['P1'] for  row in P1ForJoinM.iterrows()]))

        # Select values that are not in rows that participate in the many relations
        # restvalues = tbl1_sample[~tbl1_sample.isin(values)]

        # Repeat them M times
        values = values * M
        if len(values) > nrows:
            values = values[:nrows]
        # Sample as much as the repeated values of P1 from table 2
        tbl2_sample = sample(table2, len(values))
        # Update values of P1 based on the samples for repeated values on table 2
        for i, j in zip(values, list(tbl2_sample.index)):
            table2.loc[j, 'P1'] =  i

        tbl2_sample_v = tbl2_sample.reset_index(drop=True)

        # Sample relation_from_percentage of rows
        P1ForJoinN = sample(tbl2_sample_v, int(NumOfP1sN+0.7))
        # Extract unique values of P1 from table2, only those sampled from percentage to table 1
        values = list(set([row[1]['P1'] for  row in P1ForJoinN.iterrows()]))
        # Repeat them N times (relation is N-M)
        values = values * N
        if len(values) > nrows:
            values = values[:nrows]
        # Sample as much as the repeated values of P1 from table 1
        tbl1_sample = sample(table1, len(values))
        # Update values of P1 based on the samples for repeated values on table 1
        for i, j in zip(values, list(tbl1_sample.index)):
            table1.loc[j, 'P1'] =  i


        return table1, table2

    # 50 %
    # p = 0.5
    # value of N (relation size)
    # N = [3, 5, 10]
    # value of M (relation size)
    # M = [3, 5, 10]

    # percentage of rows that are involved in relation from table2 to table1
    # NP = [0.1, 0.25, 0.5]
    # percentage of rows that are involved in relation from table1 to table2
    # MP = [0.1, 0.25, 0.5]

    # number of rows per table
    # nrows = [1000, 3000, 10000, 50000, 100000]

    for nrow in nrows:
        subprocess.check_call('mkdir -p ../data/relation_type/N-M/'+ str(int(nrow/1000)) + 'k_rows', shell=True)
        for np, mp in zip(NP, MP):
            for n in N:
                for m in M:
                    table1 = generate_table(nrow)
                    table2 = generate_table(nrow, P1start=nrow+1)
                    table1, table2 = update_joinable_n_m_relation_rows(table1, table2, nrow, p, n, m, np, mp)
                    table1.to_csv('../data/relation_type/N-M/'+ str(int(nrow/1000)) + 'k_rows/table1_' + \
                                  str(int(100*p)) + "_" + str(n)+ "_" + str(m) + "_" + str(int(100*np)) + '_percent.csv', index=False )
                    table2.to_csv('../data/relation_type/N-M/'+ str(int(nrow/1000)) + 'k_rows/table2_' + \
                                  str(int(100*p)) + "_" +  str(n)+ "_" + str(m) + "_" + str(int(100*mp)) + '_percent.csv', index=False )


def generate_table_multi_col(nrows, ncols, IDstart=1, P1start=1):
    subjID = range(IDstart, nrows+IDstart)
    data = {"ID": subjID}
    for j in range(1, ncols+1):
        P = ["V_"  + str(j) + "-" + str(i) for i in range(P1start, P1start + nrows)]
        if j < 10:
            data["P0" + str(j) ] =  P
        else:
            data["P" + str(j) ] =  P

    table1 = pd.DataFrame(data)
    return table1

def virtical_partitioning(nrows):
    # nrows = [1000, 3000, 10000, 50000, 100000]
    # without duplicates  - best case
    for nrow in nrows:
        subprocess.check_call('mkdir -p ../data/partitioning/vertical_without_dup_best_case/'+ str(int(nrow/1000)) + 'k_rows', shell=True)
        table1 = generate_table_multi_col(nrow, 30)
        columns = list(table1.columns)
        columns = sorted(columns)
        columns.remove("ID")

        part1 = table1[["ID"] + columns[:int(len(columns)/2)]]
        part2 = table1[["ID"] + columns[int(len(columns)/2):]]

        part1.to_csv('../data/partitioning/vertical_without_dup_best_case/'+ str(int(nrow/1000)) + 'k_rows/table1.csv', index=False )
        part2.to_csv('../data/partitioning/vertical_without_dup_best_case/'+ str(int(nrow/1000)) + 'k_rows/table2.csv', index=False )

    # nrows = [1000, 3000, 10000, 50000, 100000]
    # worst case
    for nrow in nrows:
        subprocess.check_call('mkdir -p ../data/partitioning/vertical_without_dup_worst_case/'+ str(int(nrow/1000)) + 'k_rows', shell=True)
        table1 = generate_table_multi_col(nrow, 30)
        columns = list(table1.columns)
        columns = sorted(columns)
        columns.remove("ID")
        for i in range(0, len(columns)):
            part1 = table1[["ID", columns[i]]]
            part1.to_csv('../data/partitioning/vertical_without_dup_worst_case/'+ str(int(nrow/1000)) + 'k_rows/table'+str(i) + '.csv', index=False )

    # with duplicates - best case
    for nrow in nrows:
        subprocess.check_call('mkdir -p ../data/partitioning/vertical_with_dup_best_case/'+ str(int(nrow/1000)) + 'k_rows', shell=True)
        table1 = generate_table_multi_col(nrow, 30)
        columns = list(table1.columns)
        columns = sorted(columns)
        columns.remove("ID")

        part1 = table1[["ID"] + columns[:int(len(columns)/2)+1]]
        part2 = table1[["ID"] + columns[int(len(columns)/2)-1:]]

        part1.to_csv('../data/partitioning/vertical_with_dup_best_case/'+ str(int(nrow/1000)) + 'k_rows/table1.csv', index=False )
        part2.to_csv('../data/partitioning/vertical_with_dup_best_case/'+ str(int(nrow/1000)) + 'k_rows/table2.csv', index=False )

    # with duplicates - worst case
    # nrows = [1000, 3000, 10000, 50000, 100000]
    for nrow in nrows:
        subprocess.check_call('mkdir -p ../data/partitioning/vertical_with_dup_worst_case/'+ str(int(nrow/1000)) + 'k_rows', shell=True)
        table1 = generate_table_multi_col(nrow, 30)
        columns = list(table1.columns)
        columns = sorted(columns)
        columns.remove("ID")
        for i in range(0, len(columns)):
            if i+1 < len(columns):
                part1 = table1[["ID", columns[i], columns[i+1]]]
            else:
                part1 = table1[["ID", columns[0], columns[i]]]

            part1.to_csv('../data/partitioning/vertical_with_dup_worst_case/'+ str(int(nrow/1000)) + 'k_rows/table'+str(i) + '.csv', index=False )


def horizontal_partitioning(nrows):

    # without duplicates - best case
    for nrow in nrows:
        subprocess.check_call('mkdir -p ../data/partitioning/horizontal_without_dup_best_case/'+ str(int(nrow/1000)) + 'k_rows', shell=True)
        table1 = generate_table_multi_col(nrow, 30)

        part1 = table1.head(int(nrow/2))
        part2 = table1.tail(int(nrow/2))

        part1.to_csv('../data/partitioning/horizontal_without_dup_best_case/'+ str(int(nrow/1000)) + 'k_rows/table1.csv', index=False )
        part2.to_csv('../data/partitioning/horizontal_without_dup_best_case/'+ str(int(nrow/1000)) + 'k_rows/table2.csv', index=False )

    # without duplicates - worst case
    for nrow in nrows:
        subprocess.check_call('mkdir -p ../data/partitioning/horizontal_without_dup_worst_case/'+ str(int(nrow/1000)) + 'k_rows', shell=True)
        table1 = generate_table_multi_col(nrow, 30)
        part_rows = 0.1 * nrow  # 10%
        nfiles = nrow/part_rows
        for i in range(0, int(nfiles)):
            part1 = table1.iloc[list(range(i,int(i+part_rows)))]
            part1.to_csv('../data/partitioning/horizontal_without_dup_worst_case/'+ str(int(nrow/1000)) + 'k_rows/table'+str(i) + '.csv', index=False )

    # with duplicates - best case
    for nrow in nrows:
        subprocess.check_call('mkdir -p ../data/partitioning/horizontal_with_dup_best_case/'+ str(int(nrow/1000)) + 'k_rows', shell=True)
        table1 = generate_table_multi_col(nrow, 30)

        part1 = table1.head(int(nrow/2 + nrow * 0.15))
        part2 = table1.tail(int(nrow/2 + nrow * 0.15))

        part1.to_csv('../data/partitioning/horizontal_with_dup_best_case/'+ str(int(nrow/1000)) + 'k_rows/table1.csv', index=False )
        part2.to_csv('../data/partitioning/horizontal_with_dup_best_case/'+ str(int(nrow/1000)) + 'k_rows/table2.csv', index=False )

    # with duplicates - worst case
    for nrow in nrows:
        subprocess.check_call('mkdir -p ../data/partitioning/horizontal_with_dup_worst_case/'+ str(int(nrow/1000)) + 'k_rows', shell=True)
        table1 = generate_table_multi_col(nrow, 30)
        part_rows = 0.1 * nrow  # 10%
        nfiles = nrow/part_rows
        for i in range(0, int(nfiles)):
            if i+part_rows + part_rows * 0.1 > nrow: # 10% duplicate
                part1 = table1.iloc[list(range(i,nrow))]
            else:
                part1 = table1.iloc[list(range(i,int(i+part_rows)))]
            part1.to_csv('../data/partitioning/horizontal_with_dup_worst_case/'+ str(int(nrow/1000)) + 'k_rows/table'+str(i) + '.csv', index=False )


if __name__ == "__main__":
    nrows = [1000, 3000, 10000, 50000] #, 100000
    low_selectivity(nrows)

    percentages = [0.05, 0.1, 0.2, 0.3, 0.5]
    high_selectivity(nrows, percentages)

    p = 0.5
    one_to_one(nrows, p)

    N = [5, 10, 15]
    percentages = [0.25 , 0.5]
    p = 0.5
    one_to_many(nrows, N, percentages, p)

    N = [5, 10, 15]
    percentages = [0.25 , 0.5]
    p = 0.5
    many_to_one(nrows, N, percentages, p)

    p = 0.5
    # value of N (relation size)
    N = [3, 5, 10]
    # value of M (relation size)
    M = [3, 5, 10]
    # percentage of rows that are involved in relation from table2 to table1
    NP = [0.1, 0.25, 0.5]
    # percentage of rows that are involved in relation from table1 to table2
    MP = [0.1, 0.25, 0.5]
    many_to_many(nrows, N, M, NP, MP, p)

    virtical_partitioning(nrows)
    horizontal_partitioning(nrows)

    print("Data generated!")
