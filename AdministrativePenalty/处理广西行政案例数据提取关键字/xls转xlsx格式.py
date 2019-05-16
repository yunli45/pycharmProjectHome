import sys
import pandas as pd

x = pd.read_excel('P020180208396770079220.xls')
x.to_excel('P020180208396770079220.xlsx', index=False)