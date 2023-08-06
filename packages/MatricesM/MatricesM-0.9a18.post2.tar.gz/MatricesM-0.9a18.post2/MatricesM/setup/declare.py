def declareDim(mat):
    """
    Set new dimension 
    """
    try:
        rows=[1 for i in mat._matrix].count(1)
        cols = len(mat._matrix[0])
        for i in range(rows):
            if not cols == len(mat._matrix[i]):
                raise IndexError
            
    except IndexError:
        print("Matrix has different length rows")
        return None
    else:
        return [rows,cols]
    
def declareRange(mat,lis):
    """
    Finds and returns the range of the elements in a given list
    """
    c={}
    mat.setFeatures()
    mat.setcoldtypes()
    if mat._dfMat:
        valid_feats_inds = [t for t in range(len(mat.coldtypes)) if mat.coldtypes[t] in [float,int]]
        for cols in valid_feats_inds:
            temp=[lis[rows][cols] for rows in range(mat.dim[0]) if isinstance(lis[rows][cols],(int,float))]
            c[mat.features[cols]]=[min(temp),max(temp)]
    elif mat._cMat:
        for i in range(mat.dim[1]):
            temp=[]
            for rows in range(mat.dim[0]):
                temp.append(lis[rows][i].real)
                temp.append(lis[rows][i].imag)
            c[mat.features[i]]=[min(temp),max(temp)]
    else:
        for cols in range(mat.dim[1]):
            temp=[lis[rows][cols] for rows in range(mat.dim[0])]
            c[mat.features[cols]]=[min(temp),max(temp)]
    return c
