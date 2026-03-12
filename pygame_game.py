import pygame
import sys
from cambio import Cambio
from agent import Agent

pygame.init()
SW, SH = 1920, 1080
screen = pygame.display.set_mode((SW, SH), pygame.SCALED)
pygame.display.set_caption("Cambio")
clock = pygame.time.Clock()

F_SM  = pygame.font.SysFont("monospace", 20)
F_MD  = pygame.font.SysFont("monospace", 26)
F_LG  = pygame.font.SysFont("monospace", 48, bold=True)
F_LOG = pygame.font.SysFont("monospace", 17)

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
BTN_PURP  = (120, 50,  160)
GRAY      = (120, 120, 120)
HIGHLIGHT = (255, 220, 50)
SEL_HL    = (50,  220, 80)
LOG_BG    = (18,  18,  18)
LOG_LINE  = (70,  70,  70)

CW, CH  = 145, 200
LOG_X   = 1650        # log panel starts here (270px wide)
GAME_W  = LOG_X

# card rows: 4 cards centered in GAME_W
ROW_W  = 4 * CW + 3 * 25
ROW_X  = (GAME_W - ROW_W) // 2

# vertical positions
OPP_Y  = 85
MID_Y  = 380
PLR_Y  = 650

# button block (right of middle cards)
BTN_X  = 750
BTN_W  = 290
BTN_H  = 72

# phases
CAMBIO_PHASE = "cambio_phase"
POWER_PHASE  = "power_phase"
SELECT_OWN   = "select_own"
SELECT_OPP   = "select_opp"
DRAW_PHASE   = "draw_phase"
GAME_OVER    = "game_over"

POWER_DESC = {
    "PEEK_SELF":        "Peek at one of your own cards",
    "PEEK_OPPONENT":    "Peek at one of opponent's cards",
    "BLIND_SWAP":       "Swap one of your cards with opponent's",
    "SINGLE_PEEK_SWAP": "Peek opponent's card, then swap",
    "DOUBLE_PEEK_SWAP": "Peek both cards, then swap",
}


# ── helpers ───────────────────────────────────────────────────────────────────

def draw_button(rect, label, color=BTN_G):
    mx, my = pygame.mouse.get_pos()
    c = tuple(min(255, v + 30) for v in color) if rect.collidepoint(mx, my) else color
    pygame.draw.rect(screen, c, rect, border_radius=9)
    pygame.draw.rect(screen, WHITE, rect, 2, border_radius=9)
    t = F_MD.render(label, True, WHITE)
    screen.blit(t, t.get_rect(center=rect.center))


def clicked(rect, event):
    return event.type == pygame.MOUSEBUTTONDOWN and rect.collidepoint(event.pos)


def draw_card(x, y, label, face_up, highlight=False, selectable=False):
    r = pygame.Rect(x, y, CW, CH)
    if selectable:
        pygame.draw.rect(screen, SEL_HL, r.inflate(10, 10), border_radius=10)
    elif highlight:
        pygame.draw.rect(screen, HIGHLIGHT, r.inflate(10, 10), border_radius=10)
    if face_up and label:
        pygame.draw.rect(screen, CREAM, r, border_radius=8)
        pygame.draw.rect(screen, BLACK, r, 2, border_radius=8)
        color = RED_SUIT if label[-1] in ('H', 'D') else BLACK
        t = F_MD.render(label, True, color)
        screen.blit(t, t.get_rect(center=r.center))
    else:
        pygame.draw.rect(screen, CARD_BACK, r, border_radius=8)
        pygame.draw.rect(screen, WHITE,     r, 2, border_radius=8)
        t = F_MD.render("?", True, WHITE)
        screen.blit(t, t.get_rect(center=r.center))


# ── Menu ──────────────────────────────────────────────────────────────────────

def run_menu():
    cx = SW // 2
    options = [
        (pygame.Rect(cx - 150, 380, 300, 65), "vs Random",    "random"),
        (pygame.Rect(cx - 150, 465, 300, 65), "vs Heuristic", "heuristic"),
        (pygame.Rect(cx - 150, 550, 300, 65), "vs Neural Net","nn"),
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
        self.ai_mode    = ai_mode
        self.g          = Cambio()
        self.g.starting_peek()
        self.phase      = CAMBIO_PHASE
        self.log        = []
        self.power_ctx  = {}   # tracks multi-step power state

        self.agent = Agent()
        if ai_mode == "random":
            self.agent.epsilon = 1.0
            self._log("Opponent: Random")
        elif ai_mode == "heuristic":
            self._log("Opponent: Heuristic")
        elif ai_mode == "nn":
            self.agent.epsilon = 0.0
            try:
                self.agent.load("model")
                self._log("Opponent: Neural Net (loaded)")
            except FileNotFoundError:
                self.agent.epsilon = 1.0
                self._log("Opponent: Neural Net (no model)")
        self._log("Game started. You peeked 2 cards.")

    def _log(self, msg):
        self.log.append(msg)

    def card_label(self, card):
        return self.g.convert_card(card) if card not in (-1, -2) else None

    def _card_row_x(self, i):
        return ROW_X + i * (CW + 25)

    # ── selectable indices ────────────────────────────────────────────────────

    def _selectable_own(self):
        step = self.power_ctx.get("step", "")
        if "peek_own" in step:
            return [i for i, k in enumerate(self.g.player_one.player_knowledge) if not k]
        return list(range(4))

    def _selectable_opp(self):
        step = self.power_ctx.get("step", "")
        if "peek_opp" in step:
            return [i for i, k in enumerate(self.g.player_one.opponent_knowledge) if not k]
        return list(range(4))

    # ── rendering ─────────────────────────────────────────────────────────────

    def render(self):
        screen.fill(BG)
        self._draw_game()
        self._draw_log_panel()
        pygame.display.flip()

    def _draw_game(self):
        g  = self.g
        p1 = g.player_one

        # ── row y anchors (no overlaps within 1080px) ──
        STATUS_Y  = 8
        OPP_LBL_Y = 72
        OPP_CRD_Y = 100
        SLOT_LBL_OPP = OPP_CRD_Y + CH + 6   # 306
        MID_LBL_Y = SLOT_LBL_OPP + 28        # 334
        MID_CRD_Y = MID_LBL_Y + 28           # 362
        PLR_LBL_Y = MID_CRD_Y + CH + 18      # 580
        PLR_CRD_Y = PLR_LBL_Y + 34           # 614
        SLOT_LBL_PLR = PLR_CRD_Y + CH + 6    # 820
        SCORE_Y   = SLOT_LBL_PLR + 28        # 848

        # status
        if self.phase == GAME_OVER:
            status, col = g.get_winner(), GOLD
        elif self.phase in (SELECT_OWN, SELECT_OPP):
            status, col = self._selection_prompt(), WHITE
        else:
            status, col = "Your Turn  (P1)", WHITE
        t = F_LG.render(status, True, col)
        screen.blit(t, t.get_rect(centerx=GAME_W // 2, y=STATUS_Y))

        # ── cambio alert banner ──
        if g.cambio_called_by == 2:
            banner = pygame.Rect(0, 0, GAME_W, 8)  # thin red strip at top
            pygame.draw.rect(screen, (200, 40, 40), banner)
            alert_txt = F_LG.render("! OPPONENT CALLED CAMBIO — YOUR LAST TURN !", True, WHITE)
            alert_bg  = alert_txt.get_rect(centerx=GAME_W // 2, centery=STATUS_Y + 28)
            pygame.draw.rect(screen, (180, 30, 30), alert_bg.inflate(30, 12), border_radius=8)
            screen.blit(alert_txt, alert_bg)
        elif g.cambio_called_by == 1:
            t2 = F_MD.render("You called Cambio — opponent's last turn", True, GOLD)
            screen.blit(t2, t2.get_rect(centerx=GAME_W // 2, y=STATUS_Y + 52))

        sel_own = self._selectable_own() if self.phase == SELECT_OWN else []
        sel_opp = self._selectable_opp() if self.phase == SELECT_OPP else []

        # opponent hand
        t = F_MD.render("Opponent (P2)", True, WHITE)
        screen.blit(t, t.get_rect(centerx=GAME_W // 2, y=OPP_LBL_Y))
        for i in range(4):
            x = self._card_row_x(i)
            reveal = self.phase == GAME_OVER
            known  = reveal or p1.opponent_knowledge[i]
            lbl    = self.card_label(g.player_two.player_inventory[i]) if reveal else (
                     self.card_label(p1.opponent_inventory[i]) if p1.opponent_knowledge[i] else None)
            draw_card(x, OPP_CRD_Y, lbl, known, selectable=(i in sel_opp))
            t = F_SM.render(f"[{i}]", True, GRAY)
            screen.blit(t, t.get_rect(centerx=x + CW // 2, y=SLOT_LBL_OPP))

        # middle row: deck | discard | drawn card
        deck_x, disc_x, hand_x = 180, 360, 540
        screen.blit(F_SM.render(f"Deck ({len(g.deck)})", True, WHITE), (deck_x, MID_LBL_Y))
        pygame.draw.rect(screen, CARD_BACK, pygame.Rect(deck_x, MID_CRD_Y, CW, CH), border_radius=8)
        pygame.draw.rect(screen, WHITE,     pygame.Rect(deck_x, MID_CRD_Y, CW, CH), 2, border_radius=8)

        screen.blit(F_SM.render("Discard", True, WHITE), (disc_x, MID_LBL_Y))
        if g.discard_pile:
            draw_card(disc_x, MID_CRD_Y, self.card_label(g.discard_pile[-1]), True)
        else:
            pygame.draw.rect(screen, GRAY, pygame.Rect(disc_x, MID_CRD_Y, CW, CH), 2, border_radius=8)

        screen.blit(F_SM.render("Drawn Card", True, WHITE), (hand_x, MID_LBL_Y))
        in_hand = p1.get_in_hand()
        if in_hand != -2:
            draw_card(hand_x, MID_CRD_Y, self.card_label(in_hand), True, highlight=True)
        else:
            pygame.draw.rect(screen, GRAY, pygame.Rect(hand_x, MID_CRD_Y, CW, CH), 2, border_radius=8)

        # your hand
        t = F_MD.render("Your Hand  (P1)", True, WHITE)
        screen.blit(t, t.get_rect(centerx=GAME_W // 2, y=PLR_LBL_Y))
        for i in range(4):
            x = self._card_row_x(i)
            reveal = self.phase == GAME_OVER
            known  = reveal or p1.player_knowledge[i]
            lbl    = self.card_label(p1.player_inventory[i]) if known else None
            draw_card(x, PLR_CRD_Y, lbl, known, selectable=(i in sel_own))
            t = F_SM.render(f"[{i}]", True, GRAY)
            screen.blit(t, t.get_rect(centerx=x + CW // 2, y=SLOT_LBL_PLR))

        # score
        t = F_SM.render(
            f"Known score: {p1.get_player_known_score()}     Risk: {p1.risk_tolerance:.1f}",
            True, WHITE,
        )
        screen.blit(t, t.get_rect(centerx=GAME_W // 2, y=SCORE_Y))

        self._draw_buttons(MID_CRD_Y)

    def _selection_prompt(self):
        step = self.power_ctx.get("step", "")
        prompts = {
            "peek_own":       "Click one of YOUR cards to peek",
            "peek_own_first": "Click one of YOUR cards to peek",
            "peek_opp":       "Click one of OPPONENT'S cards to peek",
            "peek_opp_first": "Click one of OPPONENT'S cards to peek",
            "peek_opp_second":"Click one of OPPONENT'S cards to peek",
            "swap_own":       "Click YOUR card to swap",
            "swap_own_second":"Click YOUR card to swap",
            "swap_opp":       "Click OPPONENT'S card to swap",
        }
        return prompts.get(step, "Choose a card")

    def _draw_buttons(self, by):
        bx = BTN_X

        if self.phase == CAMBIO_PHASE:
            draw_button(pygame.Rect(bx, by,           BTN_W, BTN_H), "Draw Card",   BTN_G)
            if self.g.cambio_called_by is None:
                draw_button(pygame.Rect(bx, by + 90,  BTN_W, BTN_H), "Call Cambio", BTN_R)

        elif self.phase == POWER_PHASE:
            power = self.power_ctx.get("power", "")
            desc  = POWER_DESC.get(power, power)
            t = F_SM.render(f"Power: {desc}", True, GOLD)
            screen.blit(t, (bx, by - 30))
            draw_button(pygame.Rect(bx,              by, BTN_W, BTN_H), "Use Power", BTN_PURP)
            draw_button(pygame.Rect(bx + BTN_W + 20, by, BTN_W, BTN_H), "Skip",      BTN_BLUE)

        elif self.phase == DRAW_PHASE:
            for i in range(4):
                r = pygame.Rect(bx + (i % 2) * (BTN_W + 20),
                                by  + (i // 2) * (BTN_H + 14),
                                BTN_W, BTN_H)
                draw_button(r, f"Swap Slot {i}", BTN_BLUE)
            draw_button(pygame.Rect(bx, by + 2 * (BTN_H + 14) + 12, BTN_W * 2 + 20, BTN_H),
                        "Discard", BTN_R)

        elif self.phase in (SELECT_OWN, SELECT_OPP):
            draw_button(pygame.Rect(bx, by + 220, BTN_W, BTN_H), "Cancel", GRAY)

        elif self.phase == GAME_OVER:
            cx = GAME_W // 2
            draw_button(pygame.Rect(cx - 150, 900, 300, 72), "Play Again", BTN_G)
            draw_button(pygame.Rect(cx - 150, 990, 300, 72), "Menu",       BTN_BLUE)

    def _draw_log_panel(self):
        pygame.draw.rect(screen, LOG_BG, pygame.Rect(LOG_X, 0, SW - LOG_X, SH))
        pygame.draw.line(screen, LOG_LINE, (LOG_X, 0), (LOG_X, SH), 2)
        t = F_MD.render("Log", True, GOLD)
        screen.blit(t, (LOG_X + 12, 14))
        pygame.draw.line(screen, LOG_LINE, (LOG_X, 48), (SW, 48), 1)
        line_h   = 26
        max_vis  = (SH - 65) // line_h
        for i, msg in enumerate(self.log[-max_vis:]):
            t = F_LOG.render(msg, True, WHITE)
            screen.blit(t, (LOG_X + 10, 56 + i * line_h))

    # ── input handling ────────────────────────────────────────────────────────

    def handle(self, event):
        g   = self.g
        bx  = BTN_X
        by  = 100 + CH + 28 + 28   # matches MID_CRD_Y = OPP_CRD_Y + CH + lbl + lbl = 362
        plr_y = by + CH + 18 + 34  # matches PLR_CRD_Y = 614
        opp_y = 100                 # matches OPP_CRD_Y

        if self.phase == CAMBIO_PHASE:
            if clicked(pygame.Rect(bx, by, BTN_W, BTN_H), event):
                if not g.deck:
                    g.game_over = True; self.phase = GAME_OVER
                    self._log("Deck empty — game over."); return
                g.player_get_card_from_pile(1)
                in_hand = g.player_one.get_in_hand()
                self._log(f"You drew: {self.card_label(in_hand)}")
                power = g.player_one.get_power(in_hand)
                if power:
                    self.power_ctx = {"power": power}
                    self.phase = POWER_PHASE
                else:
                    self.phase = DRAW_PHASE
            elif clicked(pygame.Rect(bx, by + 90, BTN_W, BTN_H), event) and g.cambio_called_by is None:
                g.cambio_called_by = 1
                self._log("You called Cambio!")
                self._ai_turn()

        elif self.phase == POWER_PHASE:
            if clicked(pygame.Rect(bx, by, BTN_W, BTN_H), event):
                self._use_power_start()
            elif clicked(pygame.Rect(bx + BTN_W + 20, by, BTN_W, BTN_H), event):
                self._log(f"You skipped the {self.power_ctx['power']} power")
                self.phase = DRAW_PHASE

        elif self.phase == DRAW_PHASE:
            for i in range(4):
                r = pygame.Rect(bx + (i % 2) * (BTN_W + 20),
                                by  + (i // 2) * (BTN_H + 14),
                                BTN_W, BTN_H)
                if clicked(r, event):
                    old = self.card_label(g.player_one.player_inventory[i])
                    g.player_put_card_in_hand_into_deck(i, 1)
                    self._log(f"You swapped into slot {i} (was {old})")
                    self._after_human_turn(); return
            disc_r = pygame.Rect(bx, by + 2 * (BTN_H + 14) + 12, BTN_W * 2 + 20, BTN_H)
            if clicked(disc_r, event):
                lbl = self.card_label(g.player_one.get_in_hand())
                g.discard_card_from_hand(1)
                self._log(f"You discarded: {lbl}")
                self._after_human_turn()

        elif self.phase == SELECT_OWN:
            for i in self._selectable_own():
                if clicked(pygame.Rect(self._card_row_x(i), plr_y, CW, CH), event):
                    self._on_select_own(i); return
            if clicked(pygame.Rect(bx, by + 220, BTN_W, BTN_H), event):
                self.phase = POWER_PHASE

        elif self.phase == SELECT_OPP:
            for i in self._selectable_opp():
                if clicked(pygame.Rect(self._card_row_x(i), opp_y, CW, CH), event):
                    self._on_select_opp(i); return
            if clicked(pygame.Rect(bx, by + 220, BTN_W, BTN_H), event):
                self.phase = POWER_PHASE

        elif self.phase == GAME_OVER:
            cx = GAME_W // 2
            if clicked(pygame.Rect(cx - 150, 900, 300, 72), event):
                self.__init__(self.ai_mode)
            elif clicked(pygame.Rect(cx - 150, 990, 300, 72), event):
                return "menu"

    # ── power card flows ──────────────────────────────────────────────────────

    def _use_power_start(self):
        power = self.power_ctx["power"]
        steps = {
            "PEEK_SELF":        ("peek_own",       SELECT_OWN),
            "PEEK_OPPONENT":    ("peek_opp",       SELECT_OPP),
            "BLIND_SWAP":       ("swap_own",       SELECT_OWN),
            "SINGLE_PEEK_SWAP": ("peek_opp_first", SELECT_OPP),
            "DOUBLE_PEEK_SWAP": ("peek_own_first", SELECT_OWN),
        }
        step, phase = steps[power]
        self.power_ctx["step"] = step
        self.phase = phase

    def _on_select_own(self, i):
        g    = self.g
        step = self.power_ctx["step"]
        if "peek_own" in step:
            g.player_one.peek_self(i)
            lbl = self.card_label(g.player_one.player_inventory[i])
            self._log(f"You peeked your slot {i}: {lbl}")
            if step == "peek_own":
                self._finish_power()
            else:  # peek_own_first → DOUBLE_PEEK_SWAP
                self.power_ctx["step"] = "peek_opp_second"
                self.phase = SELECT_OPP
        elif "swap_own" in step:
            self.power_ctx["own_idx"] = i
            self.power_ctx["step"]    = "swap_opp"
            self.phase = SELECT_OPP

    def _on_select_opp(self, i):
        g    = self.g
        step = self.power_ctx["step"]
        if "peek_opp" in step:
            g.player_one.peek_opponent(g.player_two.get_inventory(), i)
            lbl = self.card_label(g.player_one.opponent_inventory[i])
            self._log(f"You peeked opponent slot {i}: {lbl}")
            if step == "peek_opp":
                self._finish_power()
            elif step == "peek_opp_first":   # SINGLE_PEEK_SWAP → now swap
                self.power_ctx["step"] = "swap_own_second"
                self.phase = SELECT_OWN
            elif step == "peek_opp_second":  # DOUBLE_PEEK_SWAP → now swap
                self.power_ctx["step"] = "swap_own_second"
                self.phase = SELECT_OWN
        elif step == "swap_opp":
            own_idx = self.power_ctx["own_idx"]
            g.swap_player_cards(own_idx, i)
            self._log(f"You swapped your slot {own_idx} with opponent slot {i}")
            self._finish_power()

    def _finish_power(self):
        self.g.discard(1)
        self._after_human_turn()

    # ── turn flow ─────────────────────────────────────────────────────────────

    def _after_human_turn(self):
        if self.g.cambio_called_by == 2:
            self.g.game_over = True
            self.phase = GAME_OVER
            self._log(self.g.get_winner())
            return
        self._ai_turn()

    def _ai_turn(self):
        g        = self.g
        is_final = g.cambio_called_by == 1

        if self.ai_mode == "heuristic":
            g.current_player_turn = 2
            g.step()
            if g.cambio_called_by == 2 and not is_final:
                self._log("Opponent called Cambio! Your last turn.")
            elif g.last_power:
                self._log(f"Opponent used power: {g.last_power}")
            else:
                top = self.card_label(g.discard_pile[-1]) if g.discard_pile else "?"
                self._log(f"Opponent discarded: {top}")

        else:
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
                self._log(f"Opponent used power: {power}")
            else:
                action = self.agent.act(g.get_state_vector(2))
                action = min(action, 4)
                if action in (0, 1, 2, 3):
                    g.player_put_card_in_hand_into_deck(action, 2)
                    self._log(f"Opponent swapped into slot {action}")
                else:
                    g.discard_card_from_hand(2)
                    self._log(f"Opponent discarded")

        if is_final or g.game_over:
            g.game_over = True
            self.phase  = GAME_OVER
            self._log(g.get_winner())
        else:
            self.phase = CAMBIO_PHASE


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    while True:
        mode    = run_menu()
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
