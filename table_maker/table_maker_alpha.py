import os, re
import pandas as pd
import time
from add.specimen_name import *
from add.decide_primer import *
from add.about_ty import *
path = os.getcwd()

for file in os.listdir('../'):
    
    if '.xlsx' in file:
        up_path = f'{path}/../'
        file_path=(os.path.join(up_path,file))
        genus_name = (file.split('_'))[0]
        if not '~' in file:        
            if 'transformed' in file:
                df_table = pd.read_excel(file_path,engine='openpyxl')       
                print('Create the transformed data table complete')

if not os.path.isdir('../Result'):
    os.mkdir('../Result') 
    print('directory 생성 완료')

df_name = specimen_in_name(df_table) #specimen_name column을 채움

mt_idx = df_name[df_name['primer'].str.contains('mt')].index #mitocondri or other region index 
df_name = df_name.drop(mt_idx) #해당 index 제거

#데이터 프레임 수정
other_idx = df_name[df_name['primer'].str.contains('others')].index
keyword={'28S':'LSU','small subunit ribosomal':'SSU','RNA polymerase II second largest subunit':'RPB2',
         'RPB2':'RPB2', 'ITS':'ITS'}
for idx in other_idx: 
    sq_name = (df_name.loc[idx,'seqname'])
    for key in keyword.keys():
        if key in sq_name:
            df_name.loc[idx,'primer'] = keyword[key]
            break


def name_control(spname):
    spname_list = spname.split(' ')
    
    if 'uncultured' in spname_list:
        spname_list.remove('uncultured')
        
    elif 'sp.' in spname_list:
        del spname_list[2:]
    elif 'aff.' or 'cf.' in spname_list:
        del spname_list[3:]

    if len(spname_list) ==1:
        spname_list.append('sp.')

    name = ''
    for i in spname_list:
        name += i+' '
    
    name.strip()
    return name


    df_name.insert(6,'fin_name','')




    species_name = {}
for idx, row in (df_name.iterrows()):
    seq_name = row['seqname']
    taxonomy = row['taxonomy']
    species = row['spname']

    
    if not 'genome' in seq_name:
        if 'Fungi' in taxonomy:
            result_name = name_control(species)
            df_name.loc[idx,'fin_name'] = result_name
    
            con_name = df_name.index[df_name['fin_name']== result_name].tolist()
    
            species_name[result_name]=con_name
        else:
            pass
    else:
        pass


final_df = pd.DataFrame(columns=['sp_name','specimen_name','type_info(GenMine)','type_info(dis)','ITS','LSU','SSU','EF','RPB2','ITS_seq','LSU_seq','SSU_seq','EF_seq','RPB2_seq'])
out_list = [] 
for sp, value in species_name.items(): #sp는 학명, value는 index
    specimen_name_list = []
    for idx in value:
        sp_name = (df_name.loc[idx,"specimen_name"]) #학명 별로 해당되는 표본을 리스트로 정리
        sp_name = sp_name.strip()
        specimen_name_list.append(sp_name)
    specimen_name_list = list(set(specimen_name_list))
    for sm in specimen_name_list: #sm은 표본 이름

        con_sample = df_name.index[df_name['specimen_name']== sm].tolist() #같은 표본을 갖는 시퀀스를 리스트로
        
        specimen_df = pd.DataFrame(columns=['sp_name','specimen_name','type_info(GenMine)','type_info(dis)',
                                            'ITS','LSU','SSU','EF','RPB2','ITS_seq','LSU_seq','SSU_seq','EF_seq','RPB2_seq']) #new data frame

        region_dict = {'ITS':[],'LSU':[],'SSU':[],'EF':[],'RPB2':[]}
        
        for i in con_sample: #동일 표본의 index를 출력함
            index_in_region = decide_primer_region(df_name,i,region_dict) #region마다 index담아줌
            for region, value in index_in_region.items(): #value가 index의 list형태
                if len(value) == 1:
                    specimen_df.loc[1,'sp_name'] = sp #학몀
                    specimen_df.loc[1,'specimen_name'] = sm #표본이름
                    specimen_df.loc[1,'type_info(GenMine)'] = ty_in_gen(df_name,value[0])
                    specimen_df.loc[1,'type_info(dis)'] = ty_in_gen(df_name,value[0])
                    specimen_df.loc[1,region]=df_name.loc[value[0],'acc'] #primer region에 accession을 넣어줌
                    specimen_df.loc[1,f'{region}_seq']  = df_name.loc[value[0],'seq'] #primer region에 맞추어 seq 넣어줌
            
                elif len(value) >1:
                    for i in range(1,len(value)+1):
                        specimen_df.loc[i,'sp_name'] = sp
                        specimen_df.loc[i,'specimen_name'] = sm
                        specimen_df.loc[i,'type_info(GenMine)'] = ty_in_gen(df_name,value[i-1])
                        specimen_df.loc[i,'type_info(dis)'] = ty_in_gen(df_name,value[i-1])
                        specimen_df.loc[i,region]=df_name.loc[value[i-1],'acc'] #primer region에 accession을 넣어줌
                        specimen_df.loc[i,f'{region}_seq']  = df_name.loc[value[i-1],'seq']
                    
        final_df = pd.concat([final_df,specimen_df])


save_time =time.strftime('%Y%m%d_%H%M',time.localtime(time.time())) 
excel_dir = f'../Result/{genus_name}_analysis_Result({save_time}).xlsx'
final_df.to_excel(excel_dir,index=False)
print('finish')
