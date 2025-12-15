

## --------------------------------------------------------
## 3. メイン関数
## --------------------------------------------------------

def myai(board, color):
    """
    オセロAI: 3手先を読み、位置の戦略、モビリティ、終盤の石数を考慮して手を決定
    board: 2次元配列(6x6 or 8x8)
    color: 置く色(1=BLACK, 2=WHITE)
    戻り値: (column, row)
    """
    size = len(board)
    ai_agent = OthelloAI(size)
    game_logic = OthelloGame(size)

    # 最初に有効な手をチェック
    valid_moves = game_logic.get_valid_moves(board, color)
    if not valid_moves:
        return None

    # Minimax探索を実行
    # 探索の深さを設定 (元のコードと同じく3手)
    SEARCH_DEPTH = 3
    
    # 序盤・中盤で戦略的評価値に基づいて、ベストムーブを選択
    _, best_move = ai_agent.minimax(board, SEARCH_DEPTH, True, color)
    
    return best_move

# Generation ID: Hutch_1764573767478_wk7yrh8mp (改善後)
