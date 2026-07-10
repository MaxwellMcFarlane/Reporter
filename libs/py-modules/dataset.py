from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import yaml
import os
import warnings
import datetime as dt
import argparse
from utils import *

#### Global Functions ####
def is_valid_data(file_path:str, ext:str='.csv') -> bool:
    if not os.path.isfile(file_path):
        console_log(f'File not found : {file_path}',1,'error')
        return False
    elif ext not in file_path:
        console_log(f'File extension is not {ext} : {file_path}',1,'error')
        return False
    return True

#### Global Classes ####
# Single testcase or fpu in use (generic expression of a testcase type)
# A generic testcase that can display a 3 dimensional plot
## Or Dataset
class Dataset():

    def __init__(self, name:str='', dfile:str='', xname:str='', yname:str='', zname:str='', xmatch:str='', ymatch:str='', zmatch:str='', msglvl=0):
        # console_log(f'Testcase {dfile} contains {len(dfile)} name files.',msglvl,'info')
        self.name = name
        self.dfile = dfile
        self.cols = [xname, yname, zname]
        self.cols = [col for col in self.cols if col != ''] # Filter out empty column names

        self.df = pd.DataFrame(columns=self.cols)
        self.msglvl = msglvl

        # Check if data is valid
        if is_valid_data(dfile):
            self.df = self.read_data()

        # print(f"xmatch : {xmatch}, ymatch : {ymatch}, zmatch : {zmatch}")
        # Apply match filters to get index for each axis if specified
        if xmatch != '' and xmatch is not None:
            df_match = self.get_match_index(self.df, xname, xmatch)
        elif ymatch != '' and ymatch is not None:
            df_match = self.get_match_index(self.df, yname, ymatch)
        elif zmatch != '' and zmatch is not None:
            df_match = self.get_match_index(self.df, zname, zmatch)
        else:
            df_match = self.df

        self.x = df_match[xname] if xname != '' else pd.Series(dtype='float')
        self.y = df_match[yname] if yname != '' else pd.Series(dtype='float')
        self.z = df_match[zname] if zname != '' else pd.Series(dtype='float')
    
    def get_match_index(self,df:pd.DataFrame, col:str='A', match:str=None) -> pd.Series:

        if (match != '' or match is not None) and match in df.values:
            match = df[df[col] == match]
        else:
            match = df 
        
        return match

    def read_data(self) -> pd.DataFrame:
        if self.dfile == '' or '.csv' not in self.dfile:
            console_log(f'File path: {self.dfile} is invalid.', self.msglvl, status='error')
            return pd.DataFrame(columns=self.cols)
        else:
            try:
                # Read only expected columns, enforce core dtypes, and normalize amount at load time.
                df = pd.read_csv(
                    self.dfile,
                    engine = 'pyarrow',
                    usecols=self.cols,
                    parse_dates=[self.cols[0]] if self.cols[0] != '' else None,
                    dtype={'status': 'string', 'type': 'string', 'recurring': 'string'},
                    converters={
                        'amount': lambda x: float(str(x).replace('$', '').replace(',', '').strip())
                    },
                )
    
                return df
            except Exception as e:
                console_log(f'Error reading data: {e}', self.msglvl, status='error')
                return pd.DataFrame(columns=self.cols)
    
    def set_data(self, df: pd.DataFrame):
        if not isinstance(df, pd.DataFrame):
            console_log(f'Provided data is not a DataFrame.', self.msglvl, status='error')
            return
        
        # Check that the DataFrame has the expected columns
        if set(self.cols) > set(df.columns.to_list()):
            console_log(f'Invalid Columns : {df.columns.to_list()}', self.msglvl, status='error')
            return
        
        self.df = df
        self.x = df[self.cols[0]] if self.cols[0] != '' else pd.Series(dtype='float')
        self.y = df[self.cols[1]] if self.cols[1] != '' else pd.Series(dtype='float')
        self.z = df[self.cols[2]] if self.cols[2] != '' else pd.Series(dtype='float')
    
    def is_valid_tc(self,df:pd.DataFrame):
        # Check that data isn't empty and has expected columns
        if set(self.cols) > set(df.columns.to_list()):
            console_log(f'Invalid Columns : {df.columns.to_list()}')
            return False
        elif len(df) <= 1:
            console_log('No Data found in file.')
            return False
        return True

# # A kind of testcase that measures the functional latency of a block -> A testcase can be summarized as a csv file (data file) that is read and stored, with a name and calculation for this particular testcase
# class Latency_TC(TestCase):

#     def __init__(self,dfile:str='', msglvl=0):
#         self.name = name
#         self.data_name = dname
#         self.cols = ['Operation','Rounding_Mode','Latency','OperandA','OperandB','OperandC','Result','Golden']
#         self.outdir = outdir
#         self.msglvl = msglvl
#         self.x_label = 'Operation'
#         self.y_label = 'Latency'

#         self.df = self.read_data(dcc_realpath(infile,msglvl+1),msglvl+1)

#         # Convert necessary columns to floats
#         self.df[['Latency','OperandA','OperandB','OperandC','Result','Golden']] = self.df[['Latency','OperandA','OperandB','OperandC','Result','Golden']].astype('float32')

#         self.operations = self.df['Operation'].unique()
#         self.operation_operands = []
#         self.stats = self.get_stats()

#         if not self.is_valid_tc(self.df):
#             print(f'Provided testcase is in an invalid format {self.name}')

#         self.operand_a = [ ]
#         self.operand_b = [ ]
#         self.operand_c = [ ] # Some occassions it may not be filled
#         self.result = [ ]
#         self.result = [ ]

# # TestCase for synthesis v. area 
# class Synthesis_Area_TC(TestCase):

#     def __init__(self, name:str='', dname:str='', infile:str='', blocks:list=[], outdir:str='', msglvl=0, xlabel:str='Clock Edge',ylabel:str='Cell Area', filter:dict={}):
#         super().__init__(name,infile,msglvl,xlabel,ylabel)

#         # Data Handles
#         self.name = name
#         self.data_name = dname
#         self.cols = ['Instance','Cell Count','Cell Area','Net Area','Total Area','Clock Edge']
        
#         # Plot & Print Handles
#         self.outdir = outdir
#         self.msglvl = msglvl
#         self.x_label = 'Clock Frequency'
#         self.y_label = 'Cell Area'

#         # Initialize Dataframes
#         self.df = None
#         self.df_slack = None
#         if ('timing' in infile) and ('area' in infile) : 
#             print('timing found')
#             self.df = self.read_data(dcc_realpath(infile['area']),msglvl)
#             self.df_slack = self.read_data(dcc_realpath(infile['timing']),msglvl)
#         elif 'area' in infile : 
#             self.df = self.read_data(dcc_realpath(infile['area']),msglvl)
#         else: console_log('No Data to create TC')

#         self.blocks = blocks 

#         ### Post-Processing
#         self.df['Clock Frequency'] = 1/(self.df['Clock Edge']/1e12) # Convert to (ns)

#         if self.df_slack is not None :
#             fail_times = self.df_slack['Clock Edge'][self.df_slack['Slack'] < 0].to_list()
#             console_log(f'Fail Times Found {fail_times}')
#             # df_filtered = df[~df['City'].isin(drop_cities)]
#             self.df = self.df[~self.df['Clock Edge'].isin(fail_times)] 

#         self.df_cell_area = self.df[[self.x_label,self.y_label,'Instance','Clock Edge']]

#         if not self.is_valid_tc(self.df):
#             print(f'Provided testcase is in an invalid format {self.name}')

# class Synthesis_Slack_TC(TestCase):

#     def __init__(self, name:str='', dname:str='', infile:str='', blocks:list=[], outdir:str='', msglvl=0):
#         # super().__init__(name,infile,msglvl,xlabel,ylabel)

#         self.x_label = 'Clock Frequency'
#         self.y_label = 'Slack'
#         self.data_name = dname
#         self.blocks = blocks 
#         self.cols = ['Operation','Rounding_Mode','Latency','OperandA','OperandB','OperandC','Result','Golden']

#         # Get Data
#         if infile != '': self.df = self.read_data(dcc_realpath(infile),msglvl)
#         else: console_log('No Data to create TC')

#         self.df['Clock Frequency'] = 1/(self.df['Clock Edge']/1e12) # Convert to (ns)
#         self.df_setup_slack = self.df[[self.x_label,self.y_label]]

#         if not self.is_valid_tc(self.df):
#             print(f'Provided testcase is in an invalid format {self.name}')


if __name__ == '__main__':
    console_log('Dataset module loaded successfully.',0,'info')
    dfile = 'data/sample.csv'
    # Load dataset and print summary
    dataset = Dataset(name='Sample Dataset', dfile=dfile, xname='Time (ns)', yname='X Value', zname='Y Value', msglvl=1)
    df = dataset.read_data()
    if dataset.is_valid_tc(df):
        console_log('Dataset loaded successfully. Here is a summary:',1,'success')
        print(df.describe())
    else:
        console_log('Failed to load dataset. Please check the file and format.',1,'error')
    
    console_log('Demo XData Correctly Loaded:',1,'info')
    console_log(f'X Data: {dataset.x}',1,'debug')
    console_log('Demo YData Correctly Loaded:',1,'info')
    console_log(f'Y Data: {dataset.y}',1,'debug')
    console_log('Demo ZData Correctly Loaded:',1,'info')
    console_log(f'Z Data: {dataset.z}',1,'debug')