# Generation ID: Hutch_1764573646691_q2eaikexy (前半)

def myai(board, color):
    """
    オセロAI: 3手先を読んで、角を優先的に取る位置を返す
    board: 2次元配列(6x6 or 8x8)
    color: 置く色(1=BLACK, 2=WHITE)
    戻り値: (column, row)
    """

    size = len(board)
    opponent = 3 - color

    def is_valid_move(b, col, row, c):
        if b[row][col] != 0:
            return False
        directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            count = 0
            while 0 <= r < size and 0 <= c < size and b[r][c] == 3 - c:
                count += 1
                r += dr
                c += dc
            if count > 0 and 0 <= r < size and 0 <= c < size and b[r][c] == c:
                return True
        return False

    def flip_stones(b, col, row, c):
        b = [row[:] for row in b]
        b[row][col] = c
        directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
        for dr, dc in directions:
            r, cd = row + dr, col + dc
            flip_list = []
            while 0 <= r < size and 0 <= cd < size and b[r][cd] == 3 - c:
                flip_list.append((r, cd))
                r += dr
                cd += dc
            if flip_list and 0 <= r < size and 0 <= cd < size and b[r][cd] == c:
                for fr, fc in flip_list:
                    b[fr][fc] = c
        return b

    def get_position_value(col, row):
        corners = [(0, 0), (0, size-1), (size-1, 0), (size-1, size-1)]
        if (col, row) in corners:
            return 1000

        edge_distance = min(col, row, size-1-col, size-1-row)
        if edge_distance == 1:
            return -100
        if edge_distance == 0:
            return 500

        center_distance = abs(col - size/2) + abs(row - size/2)
        return 100 - center_distance * 10

    def evaluate_board(b, c):
        count_c = sum(row.count(c) for row in b)
        count_opp = sum(row.count(3-c) for row in b)
        return count_c - count_opp

    def minimax(b, c, depth, is_maximizing):
        if depth == 0:
            return evaluate_board(b, color), None

        valid_moves = [(col, row) for col in range(size) for row in range(size)
                      if is_valid_move(b, col, row, c)]

        if not valid_moves:
            return minimax(b, 3-c, depth-1, not is_maximizing)

        if is_maximizing:
            best_value = float('-inf')
            best_move = valid_moves[0]
            for col, row in valid_moves:
                new_board = flip_stones(b, col, row, c)
                value, _ = minimax(new_board, 3-c, depth-1, False)
                position_bonus = get_position_value(col, row)
                total_value = value + position_bonus
                if total_value > best_value:
                    best_value = total_value
                    best_move = (col, row)
            return best_value, best_move
        else:
            best_value = float('inf')
            best_move = valid_moves[0]
            for col, row in valid_moves:
                new_board = flip_stones(b, col, row, c)
                value, _ = minimax(new_board, 3-c, depth-1, True)
                position_bonus = get_position_value(col, row)
                total_value = value - position_bonus
                if total_value < best_value:
                    best_value = total_value
                    best_move = (col, row)
            return best_value, best_move

    _, best_move = minimax(board, color, 3, True)

    if best_move:
        return best_move

    valid_moves = [(col, row) for col in range(size) for row in range(size)
                  if is_valid_move(board, col, row, color)]
    return max(valid_moves, key=lambda m: get_position_value(m[0], m[1]))

# Generation ID: Hutch_1764573646691_q2eaikexy (後半)
