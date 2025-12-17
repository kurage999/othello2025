
def myai(board, color):
    """
    【最終解決版】
    配列参照を専用関数 get_cell で保護し、IndexError を物理的に封じ込めました。
    """
    
    # 評価テーブル
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

    def get_cell(b, col, row):
        """盤面の値を安全に取得する（範囲外なら -1 を返す）"""
        if 0 <= row < len(b) and 0 <= col < len(b[0]):
            return b[row][col]
        return -1

    def is_valid_move(b, c, col, row):
        # 空きマスでないならFalse
        if get_cell(b, col, row) != 0:
            return False
        
        opp = get_opponent(c)
        directions = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
        
        for dc, dr in directions:
            nc, nr = col + dc, row + dr
            # 隣が相手の石か
            if get_cell(b, nc, nr) == opp:
                # その方向に自分の石があるか探索
                tc, tr = nc + dc, nr + dr
                while True:
                    cell = get_cell(b, tc, tr)
                    if cell == c:
                        return True
                    if cell <= 0: # 空きマスか盤外
                        break
                    tc += dc
                    tr += dr
        return False

    def get_valid_moves(b, c):
        valid_list = []
        for r in range(8):
            for l in range(8):
                if is_valid_move(b, c, l, r):
                    valid_list.append((l, r))
        return valid_list

    def apply_move(b, c, col, row):
        new_b = [line[:] for line in b]
        new_b[row][col] = c
        opp = get_opponent(c)
        directions = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
        
        for dc, dr in directions:
            nc, nr = col + dc, row + dr
            flips = []
            while get_cell(new_b, nc, nr) == opp:
                flips.append((nc, nr))
                nc += dc
                nr += dr
            if get_cell(new_b, nc, nr) == c:
                for fc, fr in flips:
                    new_b[fr][fc] = c
        return new_b

    def evaluate_board(b, target):
        score = 0
        opp = get_opponent(target)
        for r in range(8):
            for c in range(8):
                val = get_cell(b, c, r)
                if val == target:
                    score += EVAL_TABLE[r][c]
                elif val == opp:
                    score -= EVAL_TABLE[r][c]
        return score

    def minimax(b, curr_c, depth, is_max):
        if depth == 0:
            return evaluate_board(b, color), None
        
        moves = get_valid_moves(b, curr_c)
        opp = get_opponent(curr_c)
        
        if not moves:
            if not get_valid_moves(b, opp):
                return evaluate_board(b, color), None
            val, _ = minimax(b, opp, depth - 1, not is_max)
            return val, None
        
        best_val = float('-inf') if is_max else float('inf')
        best_move = None
        
        for m_col, m_row in moves:
            next_b = apply_move(b, curr_c, m_col, m_row)
            val, _ = minimax(next_b, opp, depth - 1, not is_max)
            
            if is_max:
                if val > best_val:
                    best_val, best_move = val, (m_col, m_row)
            else:
                if val < best_val:
                    best_val, best_move = val, (m_col, m_row)
        return best_val, best_move

    # 実行
    _, move_found = minimax(board, color, 3, True)
    
    if move_found:
        return move_found
    else:
        v_moves = get_valid_moves(board, color)
        return v_moves[0] if v_moves else None
