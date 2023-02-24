import os
import pandas as pd


path = os.getcwd()
def fasta_parser():   
    for file in os.listdir('../Result'):

        if '.xlsx' in file:
            up_path = f'{path}/../Result/'
            file_path=(os.path.join(up_path,file))
            genus_name = (file.split('_'))[0]
            if not '~' in file:        
                if 'analysis' in file:
                    df_table = pd.read_excel(file_path,engine='openpyxl')       
                    print('Create the analysis data table complete')

    seq_start = int((len(df_table.columns[4:]))/2)

    for column in df_table.columns[int(4+seq_start):]:
        f = open(f'{path}/../Result/{column}.fasta','w')
        tmp = ''
        for idx, row in (df_table.iterrows()):
            seq = f'{row[column]}\n'
            seq_title =f'>{row["sp_name"].strip()} {row["specimen_name"].strip()}\n'
            sp_name = row['sp_name']
            specimen = row["specimen_name"]
            if pd.notnull(seq):
                tmp += seq_title+seq
        f.write(tmp)        
        tmp = ''
        f.close()

    print('seq collecting finish')

fasta_parser()