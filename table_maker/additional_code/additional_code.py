import pandas as pd
import os, re


def specimen_in_name(df):
    for idx, row in df.iterrows():
        definition = row['seqname']
        
        match_dict = {}

        for j in range(11,20):
            origin = str((df.iloc[idx][j]))
            
            if origin:
                if ':' in origin:
                    origin = origin.replace(":",' ')
                if f' {origin}' in definition:
                    match_dict[j] = origin
        if len(list(match_dict.keys())) >= 1:
            
            #중복제거 과정
            values = []
            values = {val: key for key, val in match_dict.items()}
            result = {val: key for key, val in values.items()}
                        
            if len(result) >1:
                name = ''
                key_list = []
                
                for key,value in result.items(): 
                    name += value + ' | '
                    name=name.strip()
                    key_list.append(key)
                del result[key]
                df.loc[idx,'specimen_name'] = name
                
            elif len(result) == 1:
                name = ''
                for key, value in result.items():
                    name += value
                    name =name.strip()
                df.loc[idx,'specimen_name'] = name
        else:
        
            if df.iloc[idx][11] != ' ': #voucher
                df.loc[idx,'specimen_name'] = df.loc[idx,'voucher']
                
            elif df.iloc[idx][12] != ' ': #specimen_vourcher
                df.loc[idx,'specimen_name'] = df.loc[idx,'specimen_vourcher']
                
            elif df.iloc[idx][13] != ' ': #strain
                df.loc[idx,'specimen_name'] = df.loc[idx,'strain']
                
            elif df.iloc[idx][14] != ' ': #isolate
                df.loc[idx,'specimen_name'] = df.loc[idx,'isolate']
                
            elif df.iloc[idx][15] != ' ': #clone
                df.loc[idx,'specimen_name'] = df.loc[idx,'clone']                

            elif df.iloc[idx][16] != ' ': #culture_collection
                df.loc[idx,'specimen_name'] = df.loc[idx,'culture_collection']

            elif df.iloc[idx][17] != ' ': #bio_material
                df.loc[idx,'specimen_name'] = df.loc[idx,'bio_material']
                
    df_Nan_delete = df.dropna(subset=['specimen_name'], how='any',axis =0)

    return df_Nan_delete



def decide_primer_region(df_name,index,region_dict):
    primer_region = df_name.loc[index,'primer']
    if "ITS" in primer_region:
        region_dict['ITS'].append(index)
    elif "LSU" in primer_region:
        region_dict['LSU'].append(index)
    elif "SSU" in primer_region:
        region_dict['SSU'].append(index)
    elif "EF" in primer_region:
        region_dict['EF'].append(index)
    elif "RPB2" in primer_region:
        region_dict['RPB2'].append(index)
        
    return region_dict



def ty_in_gen(df,idx):
    ty_re ='[a-z]*(type)'
    type_info = df.loc[idx,'type_material']

    tp_result = ''
    if (pd.notnull(type_info)):
        ty_result = (re.search(ty_re,type_info)).group()
        tp_result += f'[{ty_result}(from GenMine)]'

    return tp_result

def ty_in_def(df,idx):
    ncbi_defi = df.loc[idx,'seqname']
    tp_result = ''

    if 'TYPE material' in ncbi_defi:
        tp_result += f'[Type material(from definition)]'

    return tp_result




def fasta_parser():   
    path = os.getcwd()
    for file in os.listdir('./../Result'):
        if '.xlsx' in file:
            up_path = f'{path}/../Result/'
            file_path=(os.path.join(up_path,file))
            genus_name = (file.split('_'))[0]
            if not '~' in file:        
                if 'analysis' in file:
                    df_analysis = pd.read_excel(file_path,engine='openpyxl')       
                    print('Create the analysis data table complete')
                else:
                    pass
            else:
                pass
        
    seq_start = int((len(df_analysis.columns[4:]))/2)
    for column in df_analysis.columns[int(4+seq_start):]:
        f = open(f'{path}/../Result/{genus_name}_{column}.fasta','w')
        tmp = ''
        for idx, row in (df_analysis.iterrows()):
            seq_title =f'>{row["sp_name"].strip()} {row["specimen_name"].strip()}\n'
            seq = f'{row[column]}\n'
            if pd.notnull(row[column]):
                tmp += seq_title+seq
        f.write(tmp)        
        tmp = ''
        f.close()

    print('seq collecting finish')

