def _setInstance(mat):
    if mat.dtype=="complex":
        mat._dfMat=0
        mat._fMat=1
        mat._cMat=1
    elif mat.dtype=="float":
        mat._dfMat=0
        mat._fMat=1
        mat._cMat=0
    elif mat.dtype=="integer":
        mat._dfMat=0
        mat._fMat=0
        mat._cMat=0
    elif mat.dtype=="dataframe":
        mat._dfMat=1
        mat._fMat=0
        mat._cMat=0
    else:
        raise ValueError("dtype should be one of the following: 'integer', 'float', 'complex', 'dataframe'")