import streamlit as st
import random
import copy

st.title("Multi-Game Arcade")

# Dropdown to select the game
game = st.selectbox("Choose a Game", ["Zero Kata", "Sudoku", "Guess the Higher Number"])

# Initialize session state for each game
if 'game_state' not in st.session_state:
    st.session_state.game_state = {
        'zero_kata': {'pile': 21, 'turn': 'player', 'winner': None},
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

# Zero Kata Game Logic
def zero_kata():
    st.subheader("Zero Kata")
    st.write("Remove 1, 2, or 3 items from the pile. Force your opponent to take the last item to win!")
    
    def computer_move():
        pile = st.session_state.game_state['zero_kata']['pile']
        if pile % 4 == 0:
            move = random.randint(1, min(3, pile))
        else:
            move = pile % 4
        st.session_state.game_state['zero_kata']['pile'] -= move
        st.session_state.game_state['zero_kata']['turn'] = 'player'
        if st.session_state.game_state['zero_kata']['pile'] <= 0:
            st.session_state.game_state['zero_kata']['winner'] = 'Computer'
    
    st.write(f"Pile: {st.session_state.game_state['zero_kata']['pile']} items left")
    if st.session_state.game_state['zero_kata']['winner']:
        st.write(f"Game Over! {st.session_state.game_state['zero_kata']['winner']} wins!")
    else:
        if st.session_state.game_state['zero_kata']['turn'] == 'player':
            col1, col2, col3 = st.columns(3)
            if col1.button("Take 1", disabled=st.session_state.game_state['zero_kata']['pile'] < 1, key="zk_take1"):
                st.session_state.game_state['zero_kata']['pile'] -= 1
                st.session_state.game_state['zero_kata']['turn'] = 'computer'
                if st.session_state.game_state['zero_kata']['pile'] <= 0:
                    st.session_state.game_state['zero_kata']['winner'] = 'Player'
            if col2.button("Take 2", disabled=st.session_state.game_state['zero_kata']['pile'] < 2, key="zk_take2"):
                st.session_state.game_state['zero_kata']['pile'] -= 2
                st.session_state.game_state['zero_kata']['turn'] = 'computer'
                if st.session_state.game_state['zero_kata']['pile'] <= 0:
                    st.session_state.game_state['zero_kata']['winner'] = 'Player'
            if col3.button("Take 3", disabled=st.session_state.game_state['zero_kata']['pile'] < 3, key="zk_take3"):
                st.session_state.game_state['zero_kata']['pile'] -= 3
                st.session_state.game_state['zero_kata']['turn'] = 'computer'
                if st.session_state.game_state['zero_kata']['pile'] <= 0:
                    st.session_state.game_state['zero_kata']['winner'] = 'Player'
        else:
            computer_move()
            st.experimental_rerun()
    if st.button("Reset Zero Kata", key="zk_reset"):
        st.session_state.game_state['zero_kata'] = {'pile': 21, 'turn': 'player', 'winner': None}
        st.experimental_rerun()

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
        st.experimental_rerun()

# Guess the Higher Number Game Logic
def guess_number():
    st.subheader("Guess the Higher Number")
    st.write("Pick a number between 1 and 10. The higher number wins!")
    
    st.session_state.game_state['guess_number']['player_num'] = st.slider("Your number", 1, 10, st.session_state.game_state['guess_number']['player_num'], key="gn_slider")
    if st.button("Play", key="gn_play"):
        st.session_state.game_state['guess_number']['computer_num'] = random.randint(1, 10)
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
        st.experimental_rerun()

# Run the selected game
if game == "Zero Kata":
    zero_kata()
elif game == "Sudoku":
    sudoku()
elif game == "Guess the Higher Number":
    guess_number()