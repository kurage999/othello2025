# Generation ID: Hutch_1765945221079_jjbnfyfvl (前半)

def myai(board, color):
    """
    オセロAI: 3手先を読んで最適な手を決定
    board: 8x8のオセロ盤 (0=空, 1=黒, 2=白)
    color: 自分の色 (1=黒, 2=白)
    return: (column, row) の置き位置
    """
    
    EVAL_TABLE = [
        [100, -40,  20,   5,   5,  20, -40, 100],
        [-40, -80,  -1,  -1,  -1,  -1, -80, -40],
        [ 20,  -1,   5,   1,   1,   5,  -1,  20],
        [  5,  -1,   1,   0,   0,   1,  -1,   5],
        [  5,  -1,   1,   0,   0,   1,  -1,   5],
        [ 20,  -1,   5,   1,   1,   5,  -1,  20],
        [-40, -80,  -1,  -1,  -1,  -1, -80, -40],
        [100, -40,  20,   5,   5,  20, -40, 100]
    ]
    
    def get_opponent(c):
        return 3 - c
    
    def is_valid_move(b, c, col, row):
        if b[row][col] != 0:
            return False
        
        opponent = get_opponent(c)
        directions = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
        
        for dx, dy in directions:
            x, y = col + dx, row + dy
            if 0 <= x < 8 and 0 <= y < 8 and b[y][x] == opponent:
                while 0 <= x < 8 and 0 <= y < 8:
                    if b[y][x] == 0:
                        break
                    if b[y][x] == c:
                        return True
                    x += dx
                    y += dy
        return False
    
    def get_valid_moves(b, c):
        moves = []
        for row in range(8):
            for col in range(8):
                if is_valid_move(b, c, col, row):
                    moves.append((col, row))
        return moves
    
    def apply_move(b, c, col, row):
        new_board = [row[:] for row in b]
        new_board[row][col] = c
        opponent = get_opponent(c)
        directions = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
        
        for dx, dy in directions:
            x, y = col + dx, row + dy
            flips = []
            while 0 <= x < 8 and 0 <= y < 8 and new_board[y][x] == opponent:
                flips.append((x, y))
                x += dx
                y += dy
            if 0 <= x < 8 and 0 <= y < 8 and new_board[y][x] == c and flips:
                for fx, fy in flips:
                    new_board[fy][fx] = c
        return new_board
    
    def evaluate_board(b, c):
        EVAL_TABLE = [
            [100, -40,  20,   5,   5,  20, -40, 100],
            [-40, -80,  -1,  -1,  -1,  -1, -80, -40],
            [ 20,  -1,   5,   1,   1,   5,  -1,  20],
            [  5,  -1,   1,   0,   0,   1,  -1,   5],
            [  5,  -1,   1,   0,   0,   1,  -1,   5],
            [ 20,  -1,   5,   1,   1,   5,  -1,  20],
            [-40, -80,  -1,  -1,  -1,  -1, -80, -40],
            [100, -40,  20,   5,   5,  20, -40, 100]
        ]
        score = 0
        for row in range(8):
            for col in range(8):
                if b[row][col] == c:
                    score += EVAL_TABLE[row][col]
                elif b[row][col] == get_opponent(c):
                    score -= EVAL_TABLE[row][col]
        return score
    
    def minimax(b, c, depth, is_max):
        if depth == 0:
            return evaluate_board(b, color), None
        
        opponent = get_opponent(c)
        moves = get_valid_moves(b, c)
        
        if not moves:
            moves_opp = get_valid_moves(b, opponent)
            if not moves_opp:
                return evaluate_board(b, color), None
            return minimax(b, opponent, depth - 1, not is_max)
        
        best_score = float('-inf') if is_max else float('inf')
        best_move = None
        
        for col, row in moves:
            new_board = apply_move(b, c, col, row)
            score, _ = minimax(new_board, opponent, depth - 1, not is_max)
            
            if is_max and score > best_score:
                best_score = score
                best_move = (col, row)
            elif not is_max and score < best_score:
                best_score = score
                best_move = (col, row)
        
        return best_score, best_move
    
    _, move = minimax(board, color, 3, True)
    
    if move:
        return move
    else:
        valid_moves = get_valid_moves(board, color)
        if valid_moves:
            return valid_moves[0]
        return None

# Generation ID: Hutch_1765945221079_jjbnfyfvl (後半)
