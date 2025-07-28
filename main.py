import pygame
import asyncio
import platform
from typing import Optional

from config import (
    SCREEN_WIDTH, 
    SCREEN_HEIGHT, 
    WINDOW_TITLE, 
    TARGET_FPS,
    Colors,
    FontConfig
)
from components.matrix_effect import MatrixRainEffect
from components.terminal import Terminal
from components.title_screen import TitleScreen
from utils.file_cleanup import clean_pycache

class BasiliskProtocol:
    """
    Main application class for The Basilisk Protocol game.
    
    Manages the game loop, coordinates between different screens,
    and handles top-level game state.
    """
    
    def __init__(self) -> None:
        """Initialize the game application."""
        pygame.init()
        self._setup_display()
        self._setup_fonts()
        self._setup_components()
        
        # Game state
        self.running = True
        self.show_title_screen = True
        self.clock = pygame.time.Clock()
    
    def _setup_display(self) -> None:
        """Configure the game display."""
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
    
    def _setup_fonts(self) -> None:
        """Initialize all game fonts."""
        self.fonts = {
            'stream': pygame.font.SysFont(
                FontConfig.STREAM_FONT_NAME, 
                FontConfig.STREAM_FONT_SIZE
            ),
            'terminal': pygame.font.SysFont(
                FontConfig.TERMINAL_FONT_NAME, 
                FontConfig.TERMINAL_FONT_SIZE
            ),
            'title': pygame.font.SysFont(
                FontConfig.TITLE_FONT_NAME,
                FontConfig.TITLE_FONT_SIZE
            ),
            'subtitle': pygame.font.SysFont(
                FontConfig.TERMINAL_FONT_NAME,
                FontConfig.SUBTITLE_FONT_SIZE
            ),
            'mini_terminal': pygame.font.SysFont(
                FontConfig.TERMINAL_FONT_NAME,
                FontConfig.MINI_TERMINAL_FONT_SIZE
            )
        }
    
    def _setup_components(self) -> None:
        """Initialize game components."""
        self.matrix_effect = MatrixRainEffect(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.terminal = Terminal()
        self.title_screen = TitleScreen(self.screen, self.fonts)
    
    def handle_events(self) -> None:
        """Process all pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event)
    
    def _handle_keydown(self, event: pygame.event.Event) -> None:
        """
        Route keyboard events to appropriate handler.
        
        Args:
            event: The pygame keyboard event
        """
        if event.key == pygame.K_ESCAPE:
            self.running = False
            return
        
        if self.show_title_screen:
            self._handle_title_screen_input(event)
        else:
            self._handle_game_input(event)
    
    def _handle_title_screen_input(self, event: pygame.event.Event) -> None:
        """Handle input on the title screen."""
        if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            if self.title_screen.handle_enter():
                self.show_title_screen = False
        elif event.key == pygame.K_BACKSPACE:
            self.title_screen.handle_backspace()
        elif event.unicode and event.unicode.isprintable():
            self.title_screen.handle_input(event.unicode)
    
    def _handle_game_input(self, event: pygame.event.Event) -> None:
        """Handle input during main game."""
        # Special key combinations
        if event.key == pygame.K_SPACE and pygame.key.get_mods() & pygame.KMOD_CTRL:
            self.matrix_effect.clear_all_streams()
            return
        
        # Terminal input
        if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            self.terminal.execute_command()
        elif event.key == pygame.K_BACKSPACE:
            self.terminal.handle_backspace()
        elif event.unicode and event.unicode.isprintable():
            self.terminal.handle_input(event.unicode)
    
    def update(self) -> None:
        """Update all game components."""
        self.matrix_effect.update()
        
        if self.show_title_screen:
            if self.title_screen.update():
                # Transition from boot sequence to main game
                self.show_title_screen = False
        else:
            self.terminal.update()
    
    def draw(self) -> None:
        """Render all game components."""
        self.screen.fill(Colors.BLACK)
        
        if self.show_title_screen:
            self._draw_title_screen()
        else:
            self._draw_game_screen()
        
        pygame.display.flip()
    
    def _draw_title_screen(self) -> None:
        """Draw the title screen with dimmed matrix effect."""
        # Draw dimmed matrix background
        dim_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        dim_surface.fill(Colors.BLACK)
        self.matrix_effect.draw(dim_surface, self.fonts['stream'])
        dim_surface.set_alpha(30)
        self.screen.blit(dim_surface, (0, 0))
        
        # Draw title screen on top
        self.title_screen.draw(self.screen)
    
    def _draw_game_screen(self) -> None:
        """Draw the main game screen."""
        # Draw matrix effect (dimmed if terminal is expanded)
        if self.terminal.is_expanded:
            self._draw_dimmed_matrix()
        else:
            self.matrix_effect.draw(self.screen, self.fonts['stream'])
        
        # Draw terminal
        self.terminal.draw(self.screen, self.fonts['terminal'])
    
    def _draw_dimmed_matrix(self) -> None:
        """Draw matrix effect with reduced opacity."""
        dim_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        dim_surface.fill(Colors.BLACK)
        self.matrix_effect.draw(dim_surface, self.fonts['stream'])
        dim_surface.set_alpha(50)
        self.screen.blit(dim_surface, (0, 0))
    
    async def run(self) -> None:
        """
        Main game loop with platform-specific timing.
        
        Supports both native and Emscripten (web) platforms.
        """
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            
            # Platform-specific frame timing
            if platform.system() == "Emscripten":
                await asyncio.sleep(1.0 / TARGET_FPS)
            else:
                self.clock.tick(TARGET_FPS)
    
    def cleanup(self) -> None:
        """Clean up pygame resources."""
        pygame.quit()


def main() -> None:
    """Entry point for The Basilisk Protocol."""
    app = BasiliskProtocol()
    
    try:
        # Run with appropriate event loop for platform
        if platform.system() == "Emscripten":
            asyncio.ensure_future(app.run())
        else:
            asyncio.run(app.run())
    finally:
        app.cleanup()
        clean_pycache()


if __name__ == "__main__":
    main()# SPYHVER-01: THE
