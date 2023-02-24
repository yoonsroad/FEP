import pandas as pd


#df = pd.read_excel('G:/내 드라이브/Coding/python_env/paper_coding/in_develop/fuscoporia_transformed.xlsx')

def specimen_in_name(df):
    for idx, row in df.iterrows():
        definition = row['seqname']
        
        match_dict = {}

        for j in range(11,20): #9voucher	10strain	11isolate	12clone	13culture_collection	14bio_material	15isolation_source	16isolation_material
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
#specimen_in_name(df)

def decide_primer(df_name,index,primer_list,seq_list): #중복되는 표본에 관하여 처리 방법 생각
    primer = df_name.loc[index,'primer']
    acc = df_name.loc[index,'acc']
    seq = df_name.loc[index,'seq']
    if "ITS" in primer:
        primer_list[0]= acc
        seq_list[0] = seq
        print(index, primer)
    elif "LSU" in primer:
        primer_list[1] = acc
        seq_list[1] = seq
        print(index, primer)
    elif "SSU" in primer:
        primer_list[2] = acc
        seq_list[2] = seq
        print(index, primer)
    elif "EF" in primer:
        primer_list[3] = acc
        seq_list[3] = seq
        print(index, primer)
    elif 'RPB2' in primer:
        primer_list[4] = acc
        seq_list[4] = seq
        print(index, primer)
    
    return primer_list, seq_list