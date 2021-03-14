def shallow_2d_copy(matrix): # matrix: 2d array
  copy = []

  for row in matrix:
    row_copy = []

    for cell in row:
      row_copy.append(cell)

    copy.append(row_copy)
  
  return copy

def splitstr( string_to_split ):
  return [char for char in string_to_split]

# matrix 90deg clockwise Code by Arnab Chakraborty 
def rot90(matrix):
  temp_matrix = []
  column = len(temp_matrix) - 1
  for column in range(len(matrix)):
    temp = []
    for row in range(len(matrix)-1, -1, -1):
      temp.append(matrix[row][column])
    
    temp_matrix.append(temp)
  for i in range(len(matrix)):
     for j in range(len(matrix)):
        matrix[i][j] = temp_matrix[i][j]
  return matrix
  
def rotate(matrix):
  return rot90( rot90( matrix ) )