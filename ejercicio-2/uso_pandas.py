import pandas as pd
from scipy.sparse import csr_matrix

A = csr_matrix([[1, 0, 2], [0, 3, 0]])
df = pd.DataFrame.sparse.from_spmatrix(A, columns=['A', 'B', 'C'])
print(df)
