import pygame, sys
from board import *
from sudoku_generator import *
import copy
pygame.init()
screen = pygame.display.set_mode((780, 880))
pygame.display.set_caption("Sudoku")

# Global variables to track difficulty selection
difficulty_selected = False
game_started = False
selected = False



def background(difficulty):
    screen.fill(White)
    board = Board(750, 750, screen, difficulty)
    board.draw()

    # Reset button
    resetfont = pygame.font.Font(None, 36)
    reset = resetfont.render("Reset", True, White, None)
    resetrect = reset.get_rect(topleft=(230, 800))
    pygame.draw.rect(screen, (255, 102, 0), resetrect)
    screen.blit(reset, resetrect)

    # Restart button
    restartfont = pygame.font.Font(None, 36)
    restart = restartfont.render("Restart", True, White, None)
    restartrect = restart.get_rect(topleft=(355, 800))
    pygame.draw.rect(screen, (255, 102, 0), restartrect)
    screen.blit(restart, restartrect)

    # Exit button
    exitfont = pygame.font.Font(None, 36)
    exit_ = exitfont.render("Exit", True, White, None)
    exitrect = exit_.get_rect(topleft=(505, 800))
    pygame.draw.rect(screen, (255, 102, 0), exitrect)
    screen.blit(exit_, exitrect)

    pygame.display.flip()



def start_screen():
    # background image
    bg = pygame.image.load("sudoimage.jpg")
    bg = pygame.transform.scale(bg, (780, 880))
    screen.blit(bg, (0, 0))

    # Welcome message
    welcomefont = pygame.font.Font(None, 50)
    welcome = welcomefont.render("Welcome to Sudoku", True, Black, None)
    screen.blit(welcome, (235, 100))

    # Select game mode message
    sgmfont = pygame.font.Font(None, 50)
    sgm = sgmfont.render("Select Game Mode:", True, Black, White)
    screen.blit(sgm, (235, 400))

    # Game mode buttons(Easy)
    easyfont = pygame.font.Font(None, 36)
    easy = easyfont.render("Easy", True, White, None)
    easyrect = easy.get_rect(topleft=(230, 490))
    pygame.draw.rect(screen, (255, 102, 0), easyrect)
    screen.blit(easy, easyrect)

    # Game mode button(Medium)
    medfont = pygame.font.Font(None, 36)
    med = medfont.render("Medium", True, White, None)
    medrect = med.get_rect(topleft=(350, 490))
    pygame.draw.rect(screen, (255, 102, 0), medrect)
    screen.blit(med, medrect)

    # Game mode button(Hard)
    hardfont = pygame.font.Font(None, 36)
    hard = hardfont.render("Hard", True, White, None)
    hardrect = hard.get_rect(topleft=(500, 490))
    pygame.draw.rect(screen, (255, 102, 0), hardrect)
    screen.blit(hard, hardrect)

    # Only show additional buttons if a difficulty has been selected

    return [easyrect, medrect, hardrect]


def main():
    global difficulty_selected, game_started, selected_difficulty
    running = True
    win = False
    lose = False
    screen.fill(White)
    start_screen()
    difficulty_rects = start_screen()
    easyrect = start_screen()[0]
    medrect = start_screen()[1]
    hardrect = start_screen()[2]

    resetfont = pygame.font.Font(None, 36)
    reset = resetfont.render("Reset", True, White, None)
    resetrect = reset.get_rect(topleft=(230, 800))

    restartfont = pygame.font.Font(None, 36)
    restart = restartfont.render("Restart", True, White, None)
    restartrect = restart.get_rect(topleft=(355, 800))

    exitfont = pygame.font.Font(None, 36)
    exit_ = exitfont.render("Exit", True, White, None)
    exitrect = exit_.get_rect(topleft=(505, 800))

    winscreenfont = pygame.font.Font(None, 50)
    win_text = winscreenfont.render("Game Won :)", True, Black)
    win_rect = win_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

    losescreenfont = pygame.font.Font(None, 50)
    lose_text = losescreenfont.render("Game Lost :(", True, Black)
    lose_rect = lose_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

    while running:
        # Main Loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            for i, rect in enumerate(difficulty_rects):
                difficulty_selected = True
                difficulty_levels = ["easy", "medium", "hard"]
                selected_difficulty = difficulty_levels[i]

            # Create the board instance outside the event loop
            board = Board(780, 780, screen, selected_difficulty)

            # Inside the event loop
            if game_started:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    index = board.click(position[0], position[1])

                    # Check if the index is valid before proceeding
                    if index is not None:
                        # Removes previously selected cell
                        board = Board(750, 750, screen, selected_difficulty)
                        board.draw()
                        board.select(index[0], index[1])

                        # Adjust the position of the cell based on the index
                        cell = board.cells[index[0]][index[1]]
                        if index[1] in [3, 4, 5]:
                            cell.x += 6
                        elif index[1] in [6, 7, 8]:
                            cell.x += 12

                        if index[0] in [3, 4, 5]:
                            cell.y += 6
                        elif index[0] in [6, 7, 8]:
                            cell.y += 12

                        # Set the selected flag and draw the cell
                        cell.draw()
                        cell.selected = True

                    return_key_pressed = False

                # This line should be unindented to be at the same level as the if statement above
                if event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_1 or event.key == pygame.K_2 or event.key == pygame.K_3 or
                            event.key == pygame.K_4 or event.key == pygame.K_5 or event.key == pygame.K_6 or
                            event.key == pygame.K_7 or event.key == pygame.K_8 or event.key == pygame.K_9):

                        # Determine the value pressed (from 1 to 9)
                        value = event.key - pygame.K_1 + 1

                        # You can only type in a selected box

                        # Check if the clicked cell is valid
                        if index:
                            # Check if the cell is empty
                            if copy_of_sudoku[index[0]][index[1]] == 0:
                                # Update the board with the pressed number
                                guess_board[index[0]][index[1]] = value
                                sketch_board[index[0]][index[1]] = guess_board[index[0]][index[1]]

                                for i in range(row_length):
                                    for j in range(row_length):
                                        if sketch_board[i][j] in (1, 2, 3, 4, 5, 6, 7, 8, 9):
                                            text = font.render(str(sketch_board[i][j]), True, (150,150,150), White)
                                            text_rect = text.get_rect(
                                            center=(j * Cell_size + Cell_size // 2, i * Cell_size + Cell_size // 2))
                                            screen.blit(text, text_rect)

                                            pygame.display.flip()

                    # Check if return key is pressed, only add numbers to Sudoku Array if it has
                    elif event.key == pygame.K_RETURN:
                        if guess_board[index[0]][index[1]] in (1, 2, 3, 4, 5, 6, 7, 8, 9):
                            print("ITS WORKING")
                            sudoku_board[index[0]][index[1]] = guess_board[index[0]][index[1]]
                            enter_board[index[0]][index[1]] = sketch_board[index[0]][index[1]]
                            return_key_pressed = True
                            if sudoku_board == completed_board:
                                win = True
                            elif all(all(cell != 0 for cell in row) for row in sudoku_board):
                                lose = True
                        else:
                            print("Not Changing Board")

                        # Print board states
                    print("Only entered Values")
                    for items in enter_board:
                        print(items)

                    print("Only Sketched Values")
                    for items in sketch_board:
                        print(items)

                        print("Copy of Sudoku")
                        for items in copy_of_sudoku:
                            print(items)

                        print("Guess Board")
                        for items in guess_board:
                            print(items)

                        print("Sudoku Board")
                        for items in sudoku_board:
                            print(items)

                        print("Completed Board")
                        for items in completed_board:
                            print(items)

                        print("Guess Board Values In Cells:", guess_board[index[0]][index[1]])



                    if return_key_pressed:
                        for i in range(row_length):
                            for j in range(row_length):
                                if enter_board[i][j] in (1, 2, 3, 4, 5, 6, 7, 8, 9):
                                    text = font.render(str(enter_board[i][j]), True, Black, White)
                                    text_rect = text.get_rect(
                                    center=(j * Cell_size + Cell_size // 2, i * Cell_size + Cell_size // 2))
                                    screen.blit(text, text_rect)
                                    sketch_board[index[0]][index[1]] = 0
                                    enter_board[index[0]][index[1]] = 0



                        pygame.display.flip()

            # Mouse Button event for Easy Medium and Hard Modes
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not game_started:
                    if easyrect.collidepoint(event.pos):
                        for i, rect in enumerate(difficulty_rects):
                            difficulty_selected = True
                            difficulty_levels = ["easy", "medium", "hard"]
                            selected_difficulty = difficulty_levels[i]
                        game_started = True

                        sudoku_generator = SudokuGenerator(9, 30)
                        sudoku_generator.Removed_cells = 30
                        enter_board = copy.deepcopy(sudoku_generator.get_board())
                        sketch_board = copy.deepcopy(sudoku_generator.get_board())
                        sudoku_generator.fill_values()
                        completed_board = copy.deepcopy(sudoku_generator.get_board())
                        sudoku_generator.remove_cells()
                        sudoku_board = sudoku_generator.get_board()
                        copy_of_sudoku = copy.deepcopy(sudoku_board)
                        guess_board = copy.deepcopy(sudoku_board)
                        

                        background(selected_difficulty)

                        font = pygame.font.Font(None, 36)
                        for i in range(row_length):
                            for j in range(row_length):
                                if sudoku_board[i][j] != 0:
                                    text = font.render(str(sudoku_board[i][j]), True, Black)
                                    text_rect = text.get_rect(
                                        center=(j * Cell_size + Cell_size // 2, i * Cell_size + Cell_size // 2))
                                    screen.blit(text, text_rect)

                        pygame.display.flip()
                        pygame.time.Clock().tick(60)
                        

                if not game_started:
                    if medrect.collidepoint(event.pos):
                        for i, rect in enumerate(difficulty_rects):
                            difficulty_selected = True
                            difficulty_levels = ["easy", "medium", "hard"]
                            selected_difficulty = difficulty_levels[i]
                        game_started = True

                        sudoku_generator = SudokuGenerator(9, 40)
                        sudoku_generator.Removed_cells = 40
                        enter_board = copy.deepcopy(sudoku_generator.get_board())
                        sketch_board = copy.deepcopy(sudoku_generator.get_board())
                        sudoku_generator.fill_values()
                        completed_board = copy.deepcopy(sudoku_generator.get_board())
                        sudoku_generator.remove_cells()
                        sudoku_board = sudoku_generator.get_board()
                        copy_of_sudoku = copy.deepcopy(sudoku_board)
                        guess_board = copy.deepcopy(sudoku_board)

                        background(selected_difficulty)

                        font = pygame.font.Font(None, 36)
                        for i in range(row_length):
                            for j in range(row_length):
                                if sudoku_board[i][j] != 0:
                                    text = font.render(str(sudoku_board[i][j]), True, Black)
                                    text_rect = text.get_rect(
                                        center=(j * Cell_size + Cell_size // 2, i * Cell_size + Cell_size // 2))
                                    screen.blit(text, text_rect)

                        pygame.display.flip()
                        pygame.time.Clock().tick(60)


                if not game_started:
                    if hardrect.collidepoint(event.pos):
                        for i, rect in enumerate(difficulty_rects):
                            difficulty_selected = True
                            difficulty_levels = ["easy", "medium", "hard"]
                            selected_difficulty = difficulty_levels[i]
                        game_started = True

                        sudoku_generator = SudokuGenerator(9, 50)
                        sudoku_generator.Removed_cells = 50
                        enter_board = copy.deepcopy(sudoku_generator.get_board())
                        sketch_board = copy.deepcopy(sudoku_generator.get_board())
                        sudoku_generator.fill_values()
                        completed_board = copy.deepcopy(sudoku_generator.get_board())
                        sudoku_generator.remove_cells()
                        sudoku_board = sudoku_generator.get_board()
                        copy_of_sudoku = copy.deepcopy(sudoku_board)
                        guess_board = copy.deepcopy(sudoku_board)

                        background(selected_difficulty)

                        font = pygame.font.Font(None, 36)
                        for i in range(row_length):
                            for j in range(row_length):
                                if sudoku_board[i][j] != 0:
                                    text = font.render(str(sudoku_board[i][j]), True, Black)
                                    text_rect = text.get_rect(
                                        center=(j * Cell_size + Cell_size // 2, i * Cell_size + Cell_size // 2))
                                    screen.blit(text, text_rect)

                        pygame.display.flip()
                        pygame.time.Clock().tick(60)
                        
                
                            


                #Implementation of Reset, Return, Exit functionality

                if game_started or not game_started:
                    if resetrect.collidepoint(event.pos):
                        screen.fill(White)
                        background(selected_difficulty)

                        font = pygame.font.Font(None, 36)
                        for i in range(row_length):
                            for j in range(row_length):
                                if copy_of_sudoku[i][j] != 0:
                                    text = font.render(str(copy_of_sudoku[i][j]), True, Black)
                                    text_rect = text.get_rect(
                                        center=(j * Cell_size + Cell_size // 2, i * Cell_size + Cell_size // 2))
                                    screen.blit(text, text_rect)
                        for i in range(0, 9):
                            for j in range(0, 9):
                                guess_board[i][j] = copy_of_sudoku[i][j]
                                sudoku_board[i][j] = copy_of_sudoku[i][j]
                                sketch_board[i][j] = 0
                                enter_board[i][j] = 0

                        pygame.display.flip()
                        pygame.time.Clock().tick(60)
                           
                        # Reset button clicked
                    elif restartrect.collidepoint(event.pos):
                        # Restart button clicked
                        # Reset game_started flag and any other necessary variables
                        game_started = False
                        # Return to the home screen
                        screen.fill(White)
                        start_screen()

                    elif exitrect.collidepoint(event.pos):
                        # Exit button clicked
                        pygame.quit()
                        sys.exit()

                if win:
                    screen.fill(White)
                    bg = pygame.image.load("sudoimage.jpg")
                    bg = pygame.transform.scale(bg, (780, 880))
                    screen.blit(bg, (0, 0))
                    screen.blit(win_text, win_rect)
                    pygame.draw.rect(screen, (255, 102, 0), exitrect)
                    screen.blit(exit_, exitrect)
                    pygame.display.flip()

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if exitrect.collidepoint(event.pos):
                                pygame.quit()
                                sys.exit()
                elif lose:
                    screen.fill(White)
                    bg = pygame.image.load("sudoimage.jpg")
                    bg = pygame.transform.scale(bg, (780, 880))
                    screen.blit(bg, (0, 0))
                    screen.blit(lose_text, lose_rect)
                    pygame.draw.rect(screen, (255, 102, 0), exitrect)
                    screen.blit(exit_, exitrect)
                    pygame.display.flip()

                    for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                running = False
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                if exitrect.collidepoint(event.pos):
                                    pygame.quit()
                                    sys.exit()

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()