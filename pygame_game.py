import pygame
import sys
from cambio import Cambio
from agent import Agent

pygame.init()
SW, SH = 1920, 1080
screen = pygame.display.set_mode((SW, SH))
pygame.display.set_caption("Cambio")
clock = pygame.time.Clock()

F_SM  = pygame.font.SysFont("monospace", 16)
F_MD  = pygame.font.SysFont("monospace", 22)
F_LG  = pygame.font.SysFont("monospace", 36, bold=True)
F_LOG = pygame.font.SysFont("monospace", 15)

BG        = (34,  100, 50)
WHITE     = (255, 255, 255)
BLACK     = (0,   0,   0)
CREAM     = (255, 248, 220)
CARD_BACK = (70,  70,  180)
RED_SUIT  = (200, 30,  30)
GOLD      = (218, 165, 32)
BTN_G     = (60,  160, 80)
BTN_R     = (160, 50,  50)
BTN_BLUE  = (60,  80,  180)
GRAY      = (120, 120, 120)
HIGHLIGHT = (255, 220, 50)
LOG_BG    = (20,  20,  20)
LOG_BORDER= (80,  80,  80)

CW, CH = 110, 155

# layout constants — game area left, log panel right
LOG_X     = 1380          # log panel starts here
LOG_W     = SW - LOG_X    # 540px wide
GAME_W    = LOG_X         # game area width

# game phases
CAMBIO_PHASE = "cambio_phase"
DRAW_PHASE   = "draw_phase"
GAME_OVER    = "game_over"


# ── helpers ───────────────────────────────────────────────────────────────────

def draw_button(rect, label, color=BTN_G):
    mx, my = pygame.mouse.get_pos()
    c = tuple(min(255, v + 30) for v in color) if rect.collidepoint(mx, my) else color
    pygame.draw.rect(screen, c, rect, border_radius=10)
    pygame.draw.rect(screen, WHITE, rect, 2, border_radius=10)
    t = F_MD.render(label, True, WHITE)
    screen.blit(t, t.get_rect(center=rect.center))


def clicked(rect, event):
    return event.type == pygame.MOUSEBUTTONDOWN and rect.collidepoint(event.pos)


def draw_card(x, y, label, face_up, highlight=False):
    r = pygame.Rect(x, y, CW, CH)
    if highlight:
        pygame.draw.rect(screen, HIGHLIGHT, r.inflate(10, 10), border_radius=10)
    if face_up and label:
        pygame.draw.rect(screen, CREAM, r, border_radius=8)
        pygame.draw.rect(screen, BLACK, r, 2, border_radius=8)
        color = RED_SUIT if label[-1] in ('H', 'D') else BLACK
        t = F_MD.render(label, True, color)
        screen.blit(t, t.get_rect(center=r.center))
    else:
        pygame.draw.rect(screen, CARD_BACK, r, border_radius=8)
        pygame.draw.rect(screen, WHITE, r, 2, border_radius=8)
        t = F_MD.render("?", True, WHITE)
        screen.blit(t, t.get_rect(center=r.center))


# ── Menu ──────────────────────────────────────────────────────────────────────

def run_menu():
    cx = SW // 2
    options = [
        (pygame.Rect(cx - 160, 380, 320, 70), "vs Random",    "random"),
        (pygame.Rect(cx - 160, 470, 320, 70), "vs Heuristic", "heuristic"),
        (pygame.Rect(cx - 160, 560, 320, 70), "vs Neural Net","nn"),
    ]
    while True:
        screen.fill(BG)
        t = F_LG.render("CAMBIO", True, GOLD)
        screen.blit(t, t.get_rect(centerx=cx, y=220))
        sub = F_MD.render("Choose your opponent", True, WHITE)
        screen.blit(sub, sub.get_rect(centerx=cx, y=300))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            for rect, _, mode in options:
                if clicked(rect, event):
                    return mode

        for rect, label, _ in options:
            draw_button(rect, label)

        pygame.display.flip()
        clock.tick(60)


# ── Game session ──────────────────────────────────────────────────────────────

class GameSession:
    def __init__(self, ai_mode):
        self.ai_mode = ai_mode
        self.g = Cambio()
        self.g.starting_peek()
        self.phase = CAMBIO_PHASE
        self.log = []          # list of strings shown in the log panel

        self.agent = Agent()
        if ai_mode == "random":
            self.agent.epsilon = 1.0
            self._log("Opponent: Random agent")
        elif ai_mode == "heuristic":
            self._log("Opponent: Heuristic agent")
        elif ai_mode == "nn":
            self.agent.epsilon = 0.0
            try:
                self.agent.load("model")
                self._log("Opponent: Neural Net (model loaded)")
            except FileNotFoundError:
                self.agent.epsilon = 1.0
                self._log("Opponent: Neural Net (no model — using random)")

        self._log("Game started. You peeked at 2 cards.")

    def _log(self, msg):
        self.log.append(msg)

    def card_label(self, card):
        return self.g.convert_card(card) if card not in (-1, -2) else None

    # ── layout helpers ────────────────────────────────────────────────────────
    # card row x positions (4 cards centered in game area)
    def _card_row_x(self, i):
        total = 4 * CW + 3 * 20
        start = (GAME_W - total) // 2
        return start + i * (CW + 20)

    # ── rendering ─────────────────────────────────────────────────────────────

    def render(self):
        screen.fill(BG)
        self._draw_game()
        self._draw_log_panel()
        pygame.display.flip()

    def _draw_game(self):
        g = self.g
        p1 = g.player_one

        # title
        if self.phase == GAME_OVER:
            status = g.get_winner()
            color = GOLD
        else:
            status = "Your Turn  (P1)"
            color = WHITE
        t = F_LG.render(status, True, color)
        screen.blit(t, t.get_rect(centerx=GAME_W // 2, y=18))

        # ── opponent hand (top) ──
        lbl = F_MD.render("Opponent (P2)", True, WHITE)
        screen.blit(lbl, lbl.get_rect(centerx=GAME_W // 2, y=80))
        for i in range(4):
            x = self._card_row_x(i)
            known = p1.opponent_knowledge[i]
            card_lbl = self.card_label(p1.opponent_inventory[i]) if known else None
            draw_card(x, 110, card_lbl, known)
            # slot index below card
            s = F_SM.render(f"[{i}]", True, GRAY)
            screen.blit(s, s.get_rect(centerx=x + CW // 2, y=275))

        # ── middle row: deck | discard | drawn card ──
        mid_y  = 330
        lbl_y  = mid_y - 28
        deck_x = GAME_W // 2 - 280

        screen.blit(F_SM.render(f"Deck  ({len(g.deck)})", True, WHITE), (deck_x, lbl_y))
        pygame.draw.rect(screen, CARD_BACK, pygame.Rect(deck_x, mid_y, CW, CH), border_radius=8)
        pygame.draw.rect(screen, WHITE,     pygame.Rect(deck_x, mid_y, CW, CH), 2, border_radius=8)

        disc_x = GAME_W // 2 - 55
        screen.blit(F_SM.render("Discard", True, WHITE), (disc_x, lbl_y))
        if g.discard_pile:
            draw_card(disc_x, mid_y, self.card_label(g.discard_pile[-1]), True)
        else:
            pygame.draw.rect(screen, GRAY, pygame.Rect(disc_x, mid_y, CW, CH), 2, border_radius=8)

        hand_x = GAME_W // 2 + 170
        screen.blit(F_SM.render("Drawn Card", True, WHITE), (hand_x, lbl_y))
        in_hand = p1.get_in_hand()
        if in_hand != -2:
            draw_card(hand_x, mid_y, self.card_label(in_hand), True, highlight=True)
        else:
            pygame.draw.rect(screen, GRAY, pygame.Rect(hand_x, mid_y, CW, CH), 2, border_radius=8)

        # ── your hand (bottom) ──
        lbl = F_MD.render("Your Hand  (P1)", True, WHITE)
        screen.blit(lbl, lbl.get_rect(centerx=GAME_W // 2, y=560))
        for i in range(4):
            x = self._card_row_x(i)
            known = p1.player_knowledge[i]
            card_lbl = self.card_label(p1.player_inventory[i]) if known else None
            draw_card(x, 590, card_lbl, known)
            s = F_SM.render(f"[{i}]", True, GRAY)
            screen.blit(s, s.get_rect(centerx=x + CW // 2, y=755))

        # score line
        score_txt = F_SM.render(
            f"Known score: {p1.get_player_known_score()}     Risk tolerance: {p1.risk_tolerance:.1f}",
            True, WHITE,
        )
        screen.blit(score_txt, score_txt.get_rect(centerx=GAME_W // 2, y=790))

        self._draw_buttons()

    def _draw_buttons(self):
        bx = GAME_W // 2 + 420   # buttons on right side of game area

        if self.phase == CAMBIO_PHASE:
            draw_button(pygame.Rect(bx, 330, 220, 60), "Draw Card", BTN_G)
            if self.g.cambio_called_by is None:
                draw_button(pygame.Rect(bx, 410, 220, 60), "Call Cambio", BTN_R)

        elif self.phase == DRAW_PHASE:
            for i in range(4):
                r = pygame.Rect(bx + (i % 2) * 230, 310 + (i // 2) * 75, 215, 60)
                draw_button(r, f"Swap Slot {i}", BTN_BLUE)
            draw_button(pygame.Rect(bx, 475, 215, 60), "Discard", BTN_R)

        elif self.phase == GAME_OVER:
            cx = GAME_W // 2
            draw_button(pygame.Rect(cx - 120, 860, 240, 65), "Play Again", BTN_G)
            draw_button(pygame.Rect(cx - 120, 945, 240, 65), "Menu",       BTN_BLUE)

    def _draw_log_panel(self):
        # panel background
        panel = pygame.Rect(LOG_X, 0, LOG_W, SH)
        pygame.draw.rect(screen, LOG_BG, panel)
        pygame.draw.line(screen, LOG_BORDER, (LOG_X, 0), (LOG_X, SH), 2)

        # title
        t = F_MD.render("Game Log", True, GOLD)
        screen.blit(t, (LOG_X + 20, 18))
        pygame.draw.line(screen, LOG_BORDER, (LOG_X, 52), (SW, 52), 1)

        # log lines (newest at bottom, scroll to fit)
        line_h = 22
        max_lines = (SH - 70) // line_h
        visible = self.log[-max_lines:]
        for i, msg in enumerate(visible):
            t = F_LOG.render(msg, True, WHITE)
            screen.blit(t, (LOG_X + 12, 62 + i * line_h))

    # ── input handling ────────────────────────────────────────────────────────

    def handle(self, event):
        g = self.g
        bx = GAME_W // 2 + 420

        if self.phase == CAMBIO_PHASE:
            if clicked(pygame.Rect(bx, 330, 220, 60), event):
                if not g.deck:
                    g.game_over = True
                    self.phase = GAME_OVER
                    self._log("Deck empty — game over.")
                    return
                g.player_get_card_from_pile(1)
                drawn = self.card_label(g.player_one.get_in_hand())
                self._log(f"You drew: {drawn}")
                power = g.player_one.get_power(g.player_one.get_in_hand())
                if power:
                    g.use_power(g.player_one.get_in_hand(), 1)
                    g.discard(1)
                    self._log(f"Power used: {power}")
                    self._after_human_turn()
                else:
                    self.phase = DRAW_PHASE

            elif clicked(pygame.Rect(bx, 410, 220, 60), event) and g.cambio_called_by is None:
                g.cambio_called_by = 1
                self._log("You called Cambio!")
                self._ai_turn()

        elif self.phase == DRAW_PHASE:
            for i in range(4):
                r = pygame.Rect(bx + (i % 2) * 230, 310 + (i // 2) * 75, 215, 60)
                if clicked(r, event):
                    old = self.card_label(g.player_one.player_inventory[i])
                    g.player_put_card_in_hand_into_deck(i, 1)
                    self._log(f"You swapped drawn card into slot {i} (was {old})")
                    self._after_human_turn()
                    return
            if clicked(pygame.Rect(bx, 475, 215, 60), event):
                discarded = self.card_label(g.player_one.get_in_hand())
                g.discard_card_from_hand(1)
                self._log(f"You discarded: {discarded}")
                self._after_human_turn()

        elif self.phase == GAME_OVER:
            cx = GAME_W // 2
            if clicked(pygame.Rect(cx - 120, 860, 240, 65), event):
                self.__init__(self.ai_mode)
            elif clicked(pygame.Rect(cx - 120, 945, 240, 65), event):
                return "menu"

    def _after_human_turn(self):
        if self.g.cambio_called_by == 2:
            self.g.game_over = True
            self.phase = GAME_OVER
            self._log(g_winner := self.g.get_winner())
            return
        self._ai_turn()

    def _ai_turn(self):
        g = self.g
        is_final = g.cambio_called_by == 1

        if self.ai_mode == "heuristic":
            g.current_player_turn = 2
            g.step()
            if g.cambio_called_by == 2 and not is_final:
                self._log("Opponent called Cambio! Your last turn.")
            elif g.last_power:
                drawn_lbl = self.card_label(g.last_drawn) if g.last_drawn is not None else "?"
                self._log(f"Opponent drew {drawn_lbl} and used power: {g.last_power}")
            else:
                top = self.card_label(g.discard_pile[-1]) if g.discard_pile else "?"
                self._log(f"Opponent took their turn. Discard: {top}")

        else:
            # random or nn — decide cambio before drawing
            if g.cambio_called_by is None:
                action = self.agent.act(g.get_state_vector(2))
                if action == 5:
                    g.cambio_called_by = 2
                    self._log("Opponent called Cambio! Your last turn.")
                    self.phase = CAMBIO_PHASE
                    return

            if not g.deck:
                g.game_over = True
                self.phase = GAME_OVER
                self._log("Deck empty — game over.")
                return

            g.player_get_card_from_pile(2)
            drawn_lbl = self.card_label(g.player_two.get_in_hand())
            power = g.player_two.get_power(g.player_two.get_in_hand())
            if power:
                g.use_power(g.player_two.get_in_hand(), 2)
                g.discard(2)
                self._log(f"Opponent drew {drawn_lbl} and used power: {power}")
            else:
                action = self.agent.act(g.get_state_vector(2))
                action = min(action, 4)
                if action in (0, 1, 2, 3):
                    g.player_put_card_in_hand_into_deck(action, 2)
                    self._log(f"Opponent drew {drawn_lbl} and swapped into slot {action}")
                else:
                    g.discard_card_from_hand(2)
                    self._log(f"Opponent drew {drawn_lbl} and discarded it")

        if is_final or g.game_over:
            g.game_over = True
            self.phase = GAME_OVER
            self._log(self.g.get_winner())
        else:
            self.phase = CAMBIO_PHASE


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    while True:
        mode = run_menu()
        session = GameSession(mode)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if session.handle(event) == "menu":
                    break
            else:
                session.render()
                clock.tick(60)
                continue
            break


if __name__ == "__main__":
    main()
