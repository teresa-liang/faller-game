def create_empty_state(rows: int, cols: int) -> list[list]:
    '''Creates a field where each square is empty'''
    field = []

    # create a field where each sublist represents a column
    for i in range(cols):
        col = []
        for j in range(rows):
            col.append('   ')
        field.append(col)
    
    return field