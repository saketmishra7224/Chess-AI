import pygame
import chess
import chess.engine
from flask import Flask, render_template

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 512, 512
square_size = WIDTH // 8
WHITE = (240, 217, 181)
BLACK = (181, 136, 99)
HIGHLIGHT = (186, 202, 68)
CHECK_COLOR = (255, 0, 0)
TEXT_COLOR = (0, 0, 0)
LAST_MOVE_COLOR = (255, 255, 0)  # Yellow for last move highlight

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Game")

# Load chess engine
engine_path = r"C:\Users\gours\Downloads\chessss\stockfish\stockfish-windows-x86-64-avx2.exe"

engine = chess.engine.SimpleEngine.popen_uci(engine_path)

# Initialize chess board
board = chess.Board()
selected_square = None  # Track first-clicked square
legal_moves = []  # Store legal moves for selected piece
last_move = None  # Store the last move

# Load chess piece images
piece_images = {}
piece_map = {
    'P': 'wp', 'R': 'wr', 'N': 'wn', 'B': 'wb', 'Q': 'wq', 'K': 'wk',
    'p': 'bp', 'r': 'br', 'n': 'bn', 'b': 'bb', 'q': 'bq', 'k': 'bk'
}
for piece, filename in piece_map.items():
    piece_images[piece] = pygame.image.load(f"pieces/{filename}.png")
    piece_images[piece] = pygame.transform.scale(piece_images[piece], (square_size, square_size))

# Function to draw board
def draw_board():
    for row in range(8):
        for col in range(8):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(screen, color, (col * square_size, row * square_size, square_size, square_size))

# Function to draw pieces
def draw_pieces():
    for row in range(8):
        for col in range(8):
            square = chess.square(col, 7 - row)
            piece = board.piece_at(square)
            if piece:
                screen.blit(piece_images[piece.symbol()], (col * square_size, row * square_size))

# Function to highlight legal moves
def highlight_moves():
    for move in legal_moves:
        move_col, move_row = chess.square_file(move.to_square), 7 - chess.square_rank(move.to_square)
        pygame.draw.rect(screen, HIGHLIGHT, (move_col * square_size, move_row * square_size, square_size, square_size), 5)

# Function to highlight the last move
def highlight_last_move():
    if last_move:
        from_square, to_square = last_move.from_square, last_move.to_square
        from_col, from_row = chess.square_file(from_square), 7 - chess.square_rank(from_square)
        pygame.draw.rect(screen, LAST_MOVE_COLOR, (from_col * square_size, from_row * square_size, square_size, square_size), 5)

# Function to display messages
def display_message(text):
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, TEXT_COLOR)
    screen.blit(text_surface, (WIDTH // 4, HEIGHT - 40))

# Flask app setup
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# Main loop
running = True
while running:
    draw_board()
    highlight_moves()
    highlight_last_move()
    draw_pieces()
    
    if board.is_check():
        display_message("Check!")
    if board.is_checkmate():
        display_message("Better luck next time")
    
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            square = chess.square(x // square_size, 7 - (y // square_size))

            if selected_square is None:
                # First click: Select a piece
                if board.piece_at(square) is not None:
                    selected_square = square
                    legal_moves = [move for move in board.legal_moves if move.from_square == selected_square]
            else:
                # Second click: Move piece
                move = chess.Move(selected_square, square)
                if move in board.legal_moves:
                    board.push(move)  # Apply move
                    last_move = move  # Store last move
                    
                    # AI move
                    if not board.is_checkmate():
                        result = engine.play(board, chess.engine.Limit(time=0.1))
                        board.push(result.move)
                        last_move = result.move
                selected_square = None  # Reset selection
                legal_moves = []  # Clear highlighted moves

# Quit engine and pygame
engine.quit()
pygame.quit()
