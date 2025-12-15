import math
import copy

# --- グローバル定数 ---
BLACK = 1
WHITE = 2
EMPTY = 0
# ポジションの重み (8x8ボード用) - 隅(120)を重視し、Cマス(-20)/Xマス(-40)を嫌う
WEIGHTS_8X8 = [
    [ 120, -20,  20,   5,   5,  20, -20,  120],
    [-20, -40,  -5,  -5,  -5,  -5, -40,  -20],
    [ 20,  -5,  15,   3,   3,  15,  -5,   20],
    [  5,  -5,   3,   3,   3,   3,  -5,    5],
    [  5,  -5,   3,   3,   3,   3,  -5,    5],
    [ 20,  -5,  15,   3,   3,  15,  -5,   20],
    [-20, -40,  -5,  -5,  -5,  -5, -40,  -20],
    [ 120, -20,  20,   5,   5,  20, -20,  120]
]

# --- ヘルパー関数 ---

def is_valid(r, c, board_size):
    """座標がボード内か判定"""
    return 0 <= r < board_size and 0 <= c < board_size

def get_flips_and_path(board, row, col, color, board_size):
    """指定位置に置いた場合、ひっくり返される石の数とパスを計算"""
    if board[row][col] != EMPTY:
        return 0, []

    opponent = 3 - color
    total_flips = 0
    flips_path = []

    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                  (0, 1), (1, -1), (1, 0), (1, 1)]

    for dr, dc in directions:
        temp_path = []
        r, c = row + dr, col + dc

        while is_valid(r, c, board_size) and board[r][c] == opponent:
            temp_path.append((r, c))
            r += dr
            c += dc

        if is_valid(r, c, board_size) and board[r][c] == color:
            total_flips += len(temp_path)
            flips_path.extend(temp_path)

    return total_flips, flips_path

def get_valid_moves(board, color):
    """打てる位置のリストを返す [(r, c), ...]"""
    board_size = len(board)
    valid = []
    for r in range(board_size):
        for c in range(board_size):
            if board[r][c] == EMPTY:
                flips, _ = get_flips_and_path(board, r, c, color, board_size)
                if flips > 0:
                    valid.append((r, c))
    return valid

def make_move(board, r, c, color, board_size):
    """手を打ち、盤面を更新する (新しい盤面を返す)"""
    new_board = [row[:] for row in board]
    _, flips_path = get_flips_and_path(new_board, r, c, color, board_size)

    if flips_path:
        new_board[r][c] = color
        for fr, fc in flips_path:
            new_board[fr][fc] = color
    return new_board

# --- 評価関数 ---

def evaluate_board(board, player_color, opponent_color):
    """現在の盤面を評価する"""
    board_size = len(board)
    score = 0

    # 1. 位置の評価 (Position) - 終盤まで重要
    if board_size == 8:
        weights = WEIGHTS_8X8
        for r in range(board_size):
            for c in range(board_size):
                if board[r][c] == player_color:
                    score += weights[r][c]
                elif board[r][c] == opponent_color:
                    score -= weights[r][c]

    # 2. 着手可能数 (Mobility) - 中盤で特に重要
    my_moves = len(get_valid_moves(board, player_color))
    opponent_moves = len(get_valid_moves(board, opponent_color))

    # 自分の着手可能数を最大化し、相手の着手可能数を最小化
    mobility_score = (my_moves - opponent_moves) * 20
    score += mobility_score

    # 3. 確定石 (Stability) - 終盤で最も重要
    # 隅の石は確定石とみなし、高いボーナスを与える
    corners = [(0, 0), (0, board_size-1), (board_size-1, 0), (board_size-1, board_size-1)]
    for r, c in corners:
        if board[r][c] == player_color:
            score += 400
        elif board[r][c] == opponent_color:
            score -= 400

    # 4. 石の数 (Disc Count) - 終盤でのみ重要
    empty_cells = sum(1 for r in range(board_size) for c in range(board_size) if board[r][c] == EMPTY)
    if empty_cells < 12: # 残り12マス以下を終盤と定義
        my_discs = sum(1 for r in range(board_size) for c in range(board_size) if board[r][c] == player_color)
        opponent_discs = sum(1 for r in range(board_size) for c in range(board_size) if board[r][c] == opponent_color)
        # 終盤は石の数を重視
        score += (my_discs - opponent_discs) * 10

    return score

# --- Minimax関数 (Alpha-Beta枝刈り付き) ---

def minimax(board, current_depth, is_maximizing_player, alpha, beta, original_color):
    """Minimax探索関数 (Alpha-Beta枝刈り付き)"""
    board_size = len(board)
    current_player = original_color if is_maximizing_player else 3 - original_color
    opponent_player = 3 - current_player

    # 終端条件: 探索深さに達した or ゲーム終了
    # ゲーム終了判定: どちらも打てる手がない場合
    if current_depth == 0 or (not get_valid_moves(board, BLACK) and not get_valid_moves(board, WHITE)):
        return evaluate_board(board, original_color, 3 - original_color)

    valid_moves = get_valid_moves(board, current_player)

    if not valid_moves:
        # パス: 相手のターンとして探索を続行 (深さは1減らす)
        return minimax(board, current_depth - 1, not is_maximizing_player, alpha, beta, original_color)

    if is_maximizing_player:
        # 自分のターン (評価値を最大化)
        max_eval = -math.inf
        for r, c in valid_moves:
            new_board = make_move(board, r, c, current_player, board_size)
            eval = minimax(new_board, current_depth - 1, False, alpha, beta, original_color)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break # β枝刈り
        return max_eval

    else:
        # 相手のターン (評価値を最小化)
        min_eval = math.inf
        for r, c in valid_moves:
            new_board = make_move(board, r, c, current_player, board_size)
            eval = minimax(new_board, current_depth - 1, True, alpha, beta, original_color)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break # α枝刈り
        return min_eval

# --- メインAI関数 ---

def myai(board, color):
    """
    オセロAI: Minimax探索により最善手を返す
    board: 2次元配列(6x6 or 8x8)
    color: 置く色(1=BLACK, 2=WHITE)
    戻り値: (column, row) または None (パス)
    """
    # 探索深さ: 速度と強さのバランスを見て3を設定。PC性能に応じて4も可能。
    SEARCH_DEPTH = 3

    board_size = len(board)

    valid_moves = get_valid_moves(board, color)

    if not valid_moves:
        # 打てる手がない場合はNoneを返し、パスを宣言
        return None

    best_move = valid_moves[0] # 初期の最善手として、最初の有効な手を設定
    max_eval = -math.inf
    alpha = -math.inf
    beta = math.inf

    # すべての可能な手に対してMinimaxを呼び出し、評価する
    for r, c in valid_moves:
        # 実際に打った後の盤面を作成
        new_board = make_move(board, r, c, color, board_size)

        # Minimaxの呼び出し (次は相手の番 is_maximizing_player=False)
        # 探索深さは depth-1
        eval = minimax(new_board, SEARCH_DEPTH - 1, False, alpha, beta, color)

        if eval > max_eval:
            max_eval = eval
            best_move = (r, c)

        alpha = max(alpha, eval) # トップレベルでのαの更新

    # 戻り値の形式を (column, row) に合わせる
    return (best_move[1], best_move[0])

# --- 実行方法 ---
# from sakura import othello
# othello.play(myai)


