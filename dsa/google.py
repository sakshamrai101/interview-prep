

def findQueens(n: int) -> list[list[str]]:

    cols = set() # c
    pos_diag = set() # r + c
    neg_diag = set() # r - c

    res = []
    board_state = []

    def backtrack(r):

        # Base Case: all rows are done:
        if r == n:
            copy = ['.' * (i) + 'Q' + '.' * (n - i - 1) for i in board_state]
            res.append(copy)
            return 
        
        # Try every col in range of r
        for c in range(n):

            if c in cols or (r + c) in pos_diag or (r - c) in neg_diag:
                continue
            
            # visit
            cols.add(c)
            pos_diag.add(r + c)
            neg_diag.add(r - c)
            board_state.append(c)

            # recurse 
            backtrack(r + 1)

            # backtrack:
            cols.remove(c)
            pos_diag.remove(r + c)
            neg_diag.remove(r - c)
            board_state.pop()

    backtrack(0)
    return res


print(findQueens(4))

