import pandas as pd
import re

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