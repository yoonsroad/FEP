def decide_primer_region(df_name,index,region_dict): #중복되는 표본에 관하여 처리 방법 생각
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

#def region(df,region):
    #for key in 



def decide_primer(df_name,index,primer_list,seq_list): #중복되는 표본에 관하여 처리 방법 생각
    primer = df_name.loc[index,'primer']
    acc = df_name.loc[index,'acc']
    seq = df_name.loc[index,'seq']
    len = df_name.loc[index,'length']
    if "ITS" in primer:
        primer_list[0]= f'{acc}({len})'
        seq_list[0] = seq
        
    elif "LSU" in primer:
        primer_list[1] = f'{acc}({len})'
        seq_list[1] = seq
        
    elif "SSU" in primer:
        primer_list[2] = f'{acc}({len})'
        seq_list[2] = seq
        
    elif "EF" in primer:
        primer_list[3] = f'{acc}({len})'
        seq_list[3] = seq
        
    elif 'RPB2' in primer:
        primer_list[4] = f'{acc}({len})'
        seq_list[4] = seq
        
    
    return primer_list, seq_list