from PIL import Image, ImageDraw

def create_chessboard(size=600):
    square_size = size // 8
    board = Image.new("RGB", (size, size), "white")
    draw = ImageDraw.Draw(board)

    for row in range(8):
        for col in range(8):
            if (row + col) % 2 == 1:
                draw.rectangle(
                    [col * square_size, row * square_size, 
                     (col + 1) * square_size, (row + 1) * square_size],
                    fill="gray"
                )

    board.save("board.png")

create_chessboard()
