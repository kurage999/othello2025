# Generation ID: Hutch_1763365052161_jzd78n49w (前半)

def myai(board, color):
    """
    オセロAI: 最も多くの石がとれる位置を返す
    board: 2次元配列(6x6 or 8x8)
    color: 置く色(1=BLACK, 2=WHITE)
    戻り値: (column, row)
    """
    
    opponent_color = 3 - color
    board_size = len(board)
    
    def is_valid(r, c):
        return 0 <= r < board_size and 0 <= c < board_size
    
    def count_flips(board, row, col, color):
        """指定位置に置いた場合、ひっくり返される石の数を計算"""
        if board[row][col] != 0:
            return 0
        
        opponent = 3 - color
        flips = 0
        
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), 
                     (0, 1), (1, -1), (1, 0), (1, 1)]
        
        for dr, dc in directions:
            temp_flips = 0
            r, c = row + dr, col + dc
            
            while is_valid(r, c) and board[r][c] == opponent:
                temp_flips += 1
                r += dr
                c += dc
            
            if is_valid(r, c) and board[r][c] == color:
                flips += temp_flips
        
        return flips
    
    def get_valid_moves(board, color):
        """打てる位置のリストを返す"""
        valid = []
        for r in range(board_size):
            for c in range(board_size):
                if board[r][c] == 0 and count_flips(board, r, c, color) > 0:
                    valid.append((r, c))
        return valid
    
    def get_corner_distance(r, c, size):
        """隅までの距離を計算"""
        corners = [(0, 0), (0, size-1), (size-1, 0), (size-1, size-1)]
        return min(abs(r - cr) + abs(c - cc) for cr, cc in corners)
    
    def is_dangerous(r, c, size):
        """危険なマス(C, X)を判定"""
        corners = [(0, 0), (0, size-1), (size-1, 0), (size-1, size-1)]
        for cr, cc in corners:
            dist = abs(r - cr) + abs(c - cc)
            if dist == 1:  # Cマス
                return 2
            if dist == 2:  # Xマス
                return 1
        return 0
    
    def count_empty():
        """空きマス数を数える"""
        return sum(1 for r in range(board_size) for c in range(board_size) if board[r][c] == 0)
    
    def evaluate_position(r, c, board, color):
        """ポジションを評価"""
        flips = count_flips(board, r, c, color)
        danger = is_dangerous(r, c, board_size)
        
        score = flips * 100
        
        if danger == 2:
            score -= 1000
        elif danger == 1:
            score -= 300
        
        # 隅の優先度
        if (r, c) in [(0, 0), (0, board_size-1), (board_size-1, 0), (board_size-1, board_size-1)]:
            score += 500
        
        # 辺の優先度
        if r == 0 or r == board_size - 1 or c == 0 or c == board_size - 1:
            score += 100
        
        # 終盤：相手の選択肢を減らす
        empty = count_empty()
        if empty <= board_size * 2:
            temp_board = [row[:] for row in board]
            temp_board[r][c] = color
            opponent_moves = len(get_valid_moves(temp_board, opponent_color))
            score -= opponent_moves * 50
        
        return score
    
    valid_moves = get_valid_moves(board, color)
    
    if not valid_moves:
        return None
    
    best_move = max(valid_moves, key=lambda pos: evaluate_position(pos[0], pos[1], board, color))
    
    return (best_move[1], best_move[0])

# Generation ID: Hutch_1763365052161_jzd78n49w (後半)
