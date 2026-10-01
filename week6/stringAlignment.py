"""
Write code that builds the entire cost matrix P for two input strings and reports the optimal alignment cost, P(m,n).

Requirements:

1. A function that, given two strings, allocates a table of size ( m + 1 ) * ( n + 1 ) and fills in the base-case row and column.
2. A double loop — over i from 1 to m and j from 1 to n — that fills in the rest of the table using the recurrence above.
3. A way to retrieve both the full table and the final answer, P ( m , n ) , from your function.
"""

def alignment(stringA, stringB, match = 0, mismatch = 2, gap = 1):


    stringA = stringA.upper()
    stringB = stringB.upper()


    # Matrix for the values of the list.
    '''
    I couldn't figure out how to create the matrix, first opting to try with a dictionary, then couldn't create the 
    linked list I needed on my own. I prompted ChatGPT: "I am trying to create a matrix in python. I want the number 
    of rows to be m, the length of a string, and the number of columns to be n, the length of a second string"  

    This gave me the matrix variable I have listed below. 
    '''
    #switched rows and columns to make more sense
    m = len(stringA) # columns
    n = len(stringB) # rows
    matrix = [[0] * (m + 1) for _ in range(n + 1)]
    #1. Need two base cases for the first row and column of the matrix
    #   first column fill, walk down row
    for i in range(n+1):
        matrix[i][0] = i
    #   first row fill, walk across column
    for j in range(m+1):
        matrix[0][j] = j
    #2. double for loop, make sure to iterate after the first row and column 
    for i in range(1,n+1):
        for j in range(1,m+1):

            #call for i-1 and j-1 to compare to previous cell, compare for match, then fill left and above
            if stringB[i-1] == stringA[j-1]:
                replace = matrix[i-1][j-1] + match
            else:
                replace = matrix[i-1][j-1] + mismatch
            delete = matrix[i-1][j] + gap
            insert = matrix[i][j-1] + gap

            #out of all the choices from the 3 cells, find the cheapest
            matrix[i][j] = min(replace, delete, insert)

    return matrix, matrix[n][m]


def final_form(matrix, a, b):
    
    
    pass

'''
Printing the matrix and the optimal cost of the matrix 
'''
def P(a,b):
    matrix, optimalCost = alignment(a,b)
    print(f"x ={b}, y={a}")
    print(f"Optimal cost for switching is: {optimalCost}")
    for i in matrix:
        print(i)


P("cats", "cat")
P("dan","bigger")