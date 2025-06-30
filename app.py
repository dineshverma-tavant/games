import streamlit as st
import random
import copy

st.title("Multi-Game Arcade")

# Dropdown to select the game
game = st.selectbox("Choose a Game", ["Tic-Tac-Toe", "Sudoku", "Guess the Higher Number"])

# Initialize session state for each game
if 'game_state' not in st.session_state:
    st.session_state.game_state = {
        'tic_tac_toe': {
            'board': [['' for _ in range(3)] for _ in range(3)],
            'current_player': 'X',
            'winner': None
        },
        'sudoku': {
            'board': [
                [5,3,0,0,7,0,0,0,0],
                [6,0,0,1,9,5,0,0,0],
                [0,9,8,0,0,0,0,6,0],
                [8,0,0,0,6,0,0,0,3],
                [4,0,0,8,0,3,0,0,1],
                [7,0,0,0,2,0,0,0,6],
                [0,6,0,0,0,0,2,8,0],
                [0,0,0,4,1,9,0,0,5],
                [0,0,0,0,8,0,0,7,9]
            ],
            'editable': [[False for _ in range(9)] for _ in range(9)]
        },
        'guess_number': {'player_num': 5, 'computer_num': None, 'result': None}
    }

# Initialize editable cells for Sudoku
if not any(st.session_state.game_state['sudoku']['editable']):
    initial_board = st.session_state.game_state['sudoku']['board']
    st.session_state.game_state['sudoku']['editable'] = [[initial_board[i][j] == 0 for j in range(9)] for i in range(9)]

# Tic-Tac-Toe Game Logic
def tic_tac_toe():
    st.subheader("Tic-Tac-Toe")
    st.write("You are X. Click a cell to place your mark. The computer plays as O. Win by getting 3 in a row!")

    def check_winner(board):
        # Check rows, columns, and diagonals
        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] != '':
                return board[i][0]
            if board[0][i] == board[1][i] == board[2][i] != '':
                return board[0][i]
        if board[0][0] == board[1][1] == board[2][2] != '':
            return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] != '':
            return board[0][2]
        return None

    def computer_move(board):
        # Simple AI: Check for winning move or block player
        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    board[i][j] = 'O'
                    if check_winner(board):
                        return
                    board[i][j] = ''
        # If no win/block, pick a random empty cell
        empty_cells = [(i, j) for i in range(3) for j in range(3) if board[i][j] == '']
        if empty_cells:
            i, j = random.choice(empty_cells)
            board[i][j] = 'O'

    # Display board
    board = st.session_state.game_state['tic_tac_toe']['board']
    cols = st.columns(3)
    for i in range(3):
        with st.container():
            row_cols = st.columns(3)
            for j in range(3):
                with row_cols[j]:
                    if st.button(board[i][j] if board[i][j] else f"{i},{j}", key=f"btn_{i}{j}"):
                        if board[i][j] == '' and st.session_state.game_state['tic_tac_toe']['current_player'] == 'X':
                            board[i][j] = 'X'
                            st.session_state.game_state['tic_tac_toe']['current_player'] = 'O'
                            winner = check_winner(board)
                            if winner:
                                st.session_state.game_state['tic_tac_toe']['winner'] = winner
                            elif all(board[i][j] != '' for i in range(3) for j in range(3)):
                                st.session_state.game_state['tic_tac_toe']['winner'] = 'Tie'
                            else:
                                computer_move(board)
                                st.session_state.game_state['tic_tac_toe']['current_player'] = 'X'
                                winner = check_winner(board)
                                if winner:
                                    st.session_state.game_state['tic_tac_toe']['winner'] = winner
                                elif all(board[i][j] != '' for i in range(3) for j in range(3)):
                                    st.session_state.game_state['tic_tac_toe']['winner'] = 'Tie'
                            st.rerun()

    # Display winner
    if st.session_state.game_state['tic_tac_toe']['winner']:
        st.write(f"Game Over! {st.session_state.game_state['tic_tac_toe']['winner']} wins!" if st.session_state.game_state['tic_tac_toe']['winner'] != 'Tie' else "Game Over! It's a tie!")
    if st.button("Reset Tic-Tac-Toe", key="ttt_reset"):
        st.session_state.game_state['tic_tac_toe'] = {
            'board': [['' for _ in range(3)] for _ in range(3)],
            'current_player': 'X',
            'winner': None
        }
        st.rerun()

# Sudoku Game Logic
def sudoku():
    st.subheader("Sudoku")
    
    def is_valid(board, row, col, num):
        for x in range(9):
            if board[row][x] == num or board[x][col] == num:
                return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if board[i + start_row][j + start_col] == num:
                    return False
        return True
    
    for i in range(9):
        cols = st.columns(9)
        for j in range(9):
            with cols[j]:
                if st.session_state.game_state['sudoku']['editable'][i][j]:
                    value = st.number_input("", min_value=0, max_value=9, value=st.session_state.game_state['sudoku']['board'][i][j], key=f"sudoku_{i}{j}")
                    if value != st.session_state.game_state['sudoku']['board'][i][j]:
                        if value == 0 or is_valid(st.session_state.game_state['sudoku']['board'], i, j, value):
                            st.session_state.game_state['sudoku']['board'][i][j] = value
                        else:
                            st.error(f"Invalid move at ({i+1},{j+1})")
                else:
                    st.write(st.session_state.game_state['sudoku']['board'][i][j])
    
    if st.button("Reset Sudoku", key="sudoku_reset"):
        initial_board = [
            [5,3,0,0,7,0,0,0,0],
            [6,0,0,1,9,5,0,0,0],
            [0,9,8,0,0,0,0,6,0],
            [8,0,0,0,6,0,0,0,3],
            [4,0,0,8,0,3,0,0,1],
            [7,0,0,0,2,0,0,0,6],
            [0,6,0,0,0,0,2,8,0],
            [0,0,0,4,1,9,0,0,5],
            [0,0,0,0,8,0,0,7,9]
        ]
        st.session_state.game_state['sudoku']['board'] = copy.deepcopy(initial_board)
        st.session_state.game_state['sudoku']['editable'] = [[initial_board[i][j] == 0 for j in range(9)] for i in range(9)]
        st.rerun()

# Guess the Higher Number Game Logic
def guess_number():
    st.subheader("Guess the Higher Number")
    st.write("Pick a number between 1 and 1000. The higher number wins!")
    
    st.session_state.game_state['guess_number']['player_num'] = st.slider("Your number", 1, 1000, st.session_state.game_state['guess_number']['player_num'], key="gn_slider")
    if st.button("Play", key="gn_play"):
        st.session_state.game_state['guess_number']['computer_num'] = random.randint(1, 1000)
        player_num = st.session_state.game_state['guess_number']['player_num']
        computer_num = st.session_state.game_state['guess_number']['computer_num']
        st.write(f"Your number: {player_num}")
        st.write(f"Computer's number: {computer_num}")
        if player_num > computer_num:
            st.success("You win!")
            st.session_state.game_state['guess_number']['result'] = "You win!"
        elif player_num < computer_num:
            st.error("Computer wins!")
            st.session_state.game_state['guess_number']['result'] = "Computer wins!"
        else:
            st.warning("It's a tie!")
            st.session_state.game_state['guess_number']['result'] = "It's a tie!"
    if st.session_state.game_state['guess_number']['result']:
        st.write(f"Result: {st.session_state.game_state['guess_number']['result']}")
    if st.button("Reset Guess Number", key="gn_reset"):
        st.session_state.game_state['guess_number'] = {'player_num': 5, 'computer_num': None, 'result': None}
        st.rerun()

# Run the selected game
if game == "Tic-Tac-Toe":
    tic_tac_toe()
elif game == "Sudoku":
    sudoku()
elif game == "Guess the Higher Number":
    guess_number()
