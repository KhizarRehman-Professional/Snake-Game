import pygame
import sys
from snake import Snake, Food, CELL
from ai_agent import AIAgent
from stats import StatsTracker

# ── Colors ───────────────────────────────────────────────────────────────────
BG       = (15, 15, 25)
GRID_CLR = (25, 25, 40)
WHITE    = (240, 240, 240)
YELLOW   = (255, 215, 0)
CYAN     = (0, 200, 220)
RED      = (220, 60, 60)

# ── Screen ───────────────────────────────────────────────────────────────────
WIDTH, HEIGHT = 600, 500
FPS_HUMAN = 10
FPS_AI    = 20


class Game:
    """
    Main game class - combines Pygame, OOP, Graphics, and AI.
    Programming Fundamentals: loops, conditionals, functions.
    """

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake Game + AI Stats")
        self.clock = pygame.time.Clock()
        self.font  = pygame.font.SysFont("Consolas", 18)
        self.big   = pygame.font.SysFont("Consolas", 32, bold=True)

        self.snake   = Snake(WIDTH, HEIGHT)
        self.food    = Food(WIDTH, HEIGHT)
        self.ai      = AIAgent(WIDTH, HEIGHT)
        self.stats   = StatsTracker()

        self.score    = 0
        self.ai_mode  = False
        self.running  = True
        self.game_over = False

    # ── Drawing ───────────────────────────────────────────────────────────
    def _draw_grid(self):
        for x in range(0, WIDTH, CELL):
            pygame.draw.line(self.screen, GRID_CLR, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, CELL):
            pygame.draw.line(self.screen, GRID_CLR, (0, y), (WIDTH, y))

    def _draw_hud(self):
        # Score
        txt = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(txt, (10, 10))
        # Mode
        mode_txt = "Mode: AI  [A=Toggle]" if self.ai_mode else "Mode: Human  [A=Toggle]"
        mode_clr = CYAN if self.ai_mode else YELLOW
        m = self.font.render(mode_txt, True, mode_clr)
        self.screen.blit(m, (WIDTH - m.get_width() - 10, 10))
        # Controls hint
        hint = self.font.render("Arrows=Move  A=AI  R=Restart  S=Stats  Q=Quit", True, (100, 100, 120))
        self.screen.blit(hint, (10, HEIGHT - 26))

    def _draw_game_over(self):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))

        go = self.big.render("GAME OVER", True, RED)
        sc = self.font.render(f"Score: {self.score}   Press R to restart", True, WHITE)
        st = self.font.render("Press S to view Stats Dashboard", True, YELLOW)

        self.screen.blit(go, (WIDTH//2 - go.get_width()//2, HEIGHT//2 - 60))
        self.screen.blit(sc, (WIDTH//2 - sc.get_width()//2, HEIGHT//2))
        self.screen.blit(st, (WIDTH//2 - st.get_width()//2, HEIGHT//2 + 36))

    # ── Events ────────────────────────────────────────────────────────────
    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self._quit()

                if event.key == pygame.K_a:
                    self.ai_mode = not self.ai_mode

                if event.key == pygame.K_r:
                    self._restart()

                if event.key == pygame.K_s:
                    self._show_stats()

                if not self.game_over and not self.ai_mode:
                    if event.key == pygame.K_UP:
                        self.snake.change_direction((0, -CELL))
                    elif event.key == pygame.K_DOWN:
                        self.snake.change_direction((0, CELL))
                    elif event.key == pygame.K_LEFT:
                        self.snake.change_direction((-CELL, 0))
                    elif event.key == pygame.K_RIGHT:
                        self.snake.change_direction((CELL, 0))

    # ── Game Logic ────────────────────────────────────────────────────────
    def _update(self):
        if self.game_over:
            return

        if self.ai_mode:
            direction = self.ai.get_direction(self.snake, self.food)
            self.snake.change_direction(direction)

        self.snake.move()

        # Check collisions
        if self.snake.check_wall_collision() or self.snake.check_self_collision():
            self._end_game()
            return

        # Check eating food
        if self.snake.get_head() == self.food.position:
            self.snake.eat()
            self.food.respawn(self.snake.body)
            self.score += 10

    def _end_game(self):
        self.game_over = True
        mode = "AI" if self.ai_mode else "Human"
        self.stats.save_session(self.score, mode)
        self.stats.print_summary()

    def _restart(self):
        self.snake.reset()
        self.food.respawn(self.snake.body)
        self.score = 0
        self.game_over = False

    def _show_stats(self):
        """Opens matplotlib dashboard (pauses game)"""
        from visualize import show_dashboard, show_numpy_analysis
        df = self.stats.get_scores()
        self.stats.print_summary()
        print("\nTop Sessions:")
        print(self.stats.get_best_sessions().to_string(index=False))
        show_dashboard(df)
        show_numpy_analysis(df)

    def _quit(self):
        pygame.quit()
        sys.exit()

    # ── Main Loop ─────────────────────────────────────────────────────────
    def run(self):
        while self.running:
            self._handle_events()
            self._update()

            # Draw
            self.screen.fill(BG)
            self._draw_grid()
            self.food.draw(self.screen)
            self.snake.draw(self.screen)
            self._draw_hud()
            if self.game_over:
                self._draw_game_over()

            pygame.display.flip()
            fps = FPS_AI if self.ai_mode else FPS_HUMAN
            self.clock.tick(fps)
