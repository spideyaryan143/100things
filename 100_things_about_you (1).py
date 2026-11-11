#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
100 THINGS ABOUT YOU
Premium full-screen kinetic typography animation (Pygame, 1200 x 800).

Setup:   pip install pygame
Run:     python 100_things_about_you.py
Quit:    close the window, or press ESC / Q.

One fixed frame, horizontal flowing layers of text, one featured statement at a
time in the centre, thin light trails, a continuous light sweep, soft grain and
sparse atmospheric dust. Everything runs automatically.
"""

import math
import os
import random
import re
import sys
from dataclasses import dataclass

import pygame

# ----------------------------------------------------------------------------
# CONSTANTS
# ----------------------------------------------------------------------------
WIDTH, HEIGHT = 1200, 800
FPS = 60
TITLE = "100 THINGS ABOUT YOU"

# Palette
BG_TOP = (8, 12, 26)            # midnight navy
BG_BOTTOM = (2, 3, 9)           # near black
IVORY = (244, 237, 221)         # main text
CHAMPAGNE = (205, 189, 156)     # secondary text
GOLD = (201, 163, 86)           # antique gold
GOLD_BRIGHT = (236, 203, 128)   # highlighted gold
AMBER = (255, 178, 82)          # accent lighting

# Layout
CENTER_X = WIDTH // 2
TITLE_Y = 56
TITLE_RULE_Y = 98
RULE_TOP_Y = 262
RULE_BOTTOM_Y = 540
NUMBER_Y = 292
FEATURE_CENTER_Y = 410
FEATURE_MAX_W = 880
PROGRESS_Y = 784
MARGIN_X = 60

# Featured statement timing (seconds)
INITIAL_DELAY = 2.6
FADE_IN = 1.2
FADE_OUT = 1.0
SCALE_TIME = 1.6

# Sweep
SWEEP_WIDTH = 460
SWEEP_SPEED = 150.0

# ----------------------------------------------------------------------------
# THE 100 STATEMENTS   (*asterisks* mark highlighted keywords)
# ----------------------------------------------------------------------------
STATEMENTS = [
    # 1 - 10
    "You make *ordinary moments* feel important.",
    "Your *presence* changes the atmosphere.",
    "You notice the *little things*.",
    "You have a way of making people feel *seen*.",
    "Your strength doesn't always need to be *loud*.",
    "Some people are remembered *without trying*.",
    "Rooms feel *warmer* after you walk in.",
    "You listen as though *every word* matters.",
    "Silence feels *comfortable* when you are there.",
    "You carry calm into *noisy places*.",
    # 11 - 20
    "People *exhale* a little around you.",
    "You remember the details everyone assumed *nobody noticed*.",
    "Your laugh *rearranges* a room.",
    "You are *gentle* without ever being fragile.",
    "You say *thank you* like you mean it.",
    "You make *effort* look effortless.",
    "You ask the *second question*, the one that matters.",
    "Your *kindness* has no audience.",
    "You turn *strangers* into familiar faces.",
    "You leave places a little *better* than you found them.",
    # 21 - 30
    "You are *unmistakably* yourself.",
    "Your *honesty* is soft, but never vague.",
    "You hold *space* for people without announcing it.",
    "You *forgive* with a grace most people never learn.",
    "Your *patience* is a quiet kind of generosity.",
    "You know when to *speak*, and when to simply stay.",
    "You make *difficult days* feel survivable.",
    "Your *curiosity* keeps the world interesting.",
    "You find *beauty* in places others walk past.",
    "You *show up*, and that changes everything.",
    # 31 - 40
    "You are *steady* when others are shaking.",
    "Your *courage* rarely announces itself.",
    "You *believe in people* before they have proof.",
    "Your warmth is *never forced*.",
    "You are comfortable with *who you are becoming*.",
    "Your *quiet moments* say more than most speeches.",
    "You make simple plans feel like *occasions*.",
    "You *care* in specific, thoughtful ways.",
    "You notice *how people feel*, not only what they say.",
    "Your *consistency* is a gift to everyone near you.",
    # 41 - 50
    "You *disagree* gracefully.",
    "You *celebrate* other people's wins without keeping score.",
    "You are proof that *gentle people* endure.",
    "You give *credit* freely and take responsibility honestly.",
    "People *trust* you faster than they realize.",
    "Your *voice* sounds like reassurance.",
    "You make *waiting* feel shorter.",
    "Your *style* belongs entirely to you.",
    "You do small favors so naturally that *nobody can repay them*.",
    "You remember *birthdays, names*, and the stories behind them.",
    # 51 - 60
    "You have a *talent for timing*, and know when to lighten the mood.",
    "You turn *awkward* into easy.",
    "You make people feel *at home* almost anywhere.",
    "Your *humor* includes everyone.",
    "You carry *quietly* what would break others.",
    "You are *brave* in ways nobody applauds.",
    "You make good ideas feel *safe to say aloud*.",
    "You *encourage* without ever condescending.",
    "You *stay kind* when it would be easier not to.",
    "Your *standards* are high, and your grace is higher.",
    # 61 - 70
    "You notice who is *standing alone*.",
    "You can *change a mood* with a single sentence.",
    "People *borrow* your courage without ever telling you.",
    "You make *sincerity* look elegant.",
    "Your *influence* is felt long after you leave.",
    "You teach by *example*, never by lecture.",
    "You make *mistakes* feel human, not final.",
    "You *inspire* people to try without pressuring them.",
    "Your *words* stay with people for years.",
    "You are the reason *someone* kept going.",
    # 71 - 80
    "You turn *ordinary places* into memories.",
    "You *listen* between the lines.",
    "You are *gracious* in small moments, which is where it counts.",
    "You treat *everyone* as though they matter, because to you they do.",
    "Your *intuition* arrives quietly, then proves itself.",
    "You are *soft* and unshakable at the same time.",
    "You are *growing* in ways you don't always see.",
    "You have a presence that *cannot be imitated*.",
    "You are only *easy to miss* if no one is paying attention.",
    "You make *time* feel generous.",
    # 81 - 90
    "You *make room* at your table, and in your story.",
    "You show people how to be *gentler* with themselves.",
    "You have *depth* that reveals itself slowly.",
    "Your *loyalty* is quiet, and it never wavers.",
    "You can be *serious* without being distant.",
    "You are *thoughtful* in ways that never ask for thanks.",
    "You treat a *conversation* like something precious.",
    "You make good days *better* and heavy days lighter.",
    "Your *smile* has never felt like an obligation.",
    "You *understand* more than you say.",
    # 91 - 100
    "You leave people feeling *capable*.",
    "You make *belonging* feel simple.",
    "You shape the people around you, *gently and for good*.",
    "You are remembered in *details*: a phrase, a gesture, a tone.",
    "You *matter* in ways that never fit into one sentence.",
    "People *notice* when you are missing, and feel it when you return.",
    "You are the kind of person *people hope to become*.",
    "You *deserve* the same care you give so freely.",
    "The world is *quietly better* because you are in it.",
    "And these are *only a hundred* of the countless reasons.",
]

assert len(STATEMENTS) == 100, "Exactly 100 statements are required."
assert len(set(STATEMENTS)) == 100, "All statements must be unique."
assert all(s.count("*") % 2 == 0 for s in STATEMENTS), "Unbalanced keyword markup."


# ----------------------------------------------------------------------------
# SMALL MATH HELPERS
# ----------------------------------------------------------------------------
def clamp(v, lo=0.0, hi=1.0):
    return lo if v < lo else hi if v > hi else v


def lerp(a, b, t):
    return a + (b - a) * t


def smoothstep(t):
    t = clamp(t)
    return t * t * (3.0 - 2.0 * t)


def ease_out_cubic(t):
    t = clamp(t)
    return 1.0 - (1.0 - t) ** 3


def mix(c1, c2, t):
    return tuple(int(lerp(a, b, t)) for a, b in zip(c1, c2))


def scale_color(c, k):
    return tuple(int(clamp(v * k, 0, 255)) for v in c)


def plain(text):
    return text.replace("*", "")


# ----------------------------------------------------------------------------
# FONTS
# ----------------------------------------------------------------------------
SERIF_NAMES = ("georgia,palatinolinotype,bookantiqua,cambria,garamond,"
               "timesnewroman,dejavuserif,liberationserif,freeserif")
SANS_NAMES = ("segoeui,calibri,gillsansmt,trebuchetms,helvetica,arial,"
              "dejavusans,liberationsans,freesans")


class FontBank:
    """Caches fonts and resolves Windows-friendly families with fallbacks."""
    _cache = {}

    @classmethod
    def get(cls, family, size, bold=False, italic=False):
        key = (family, size, bold, italic)
        font = cls._cache.get(key)
        if font is None:
            names = SERIF_NAMES if family == "serif" else SANS_NAMES
            font = pygame.font.SysFont(names, size, bold=bold, italic=italic)
            cls._cache[key] = font
        return font


# ----------------------------------------------------------------------------
# RICH TEXT (keyword highlighting, wrapping, letter-spaced text)
# ----------------------------------------------------------------------------
def parse_markup(text):
    """Return a list of (word, is_keyword, space_before)."""
    tokens = []
    pending_space = False
    for i, segment in enumerate(text.split("*")):
        is_key = (i % 2 == 1)
        for part in re.findall(r"\s+|\S+", segment):
            if part.isspace():
                pending_space = True
            else:
                tokens.append((part, is_key, pending_space and len(tokens) > 0))
                pending_space = False
    return tokens


def layout_rich(tokens, font, key_font, max_width):
    """Greedy word wrap. Returns (lines, space_width); each line = (groups, width)."""
    groups = []
    for text, is_key, space_before in tokens:
        width = (key_font if is_key else font).size(text)[0]
        if space_before or not groups:
            groups.append([(text, is_key, width)])
        else:
            groups[-1].append((text, is_key, width))  # punctuation glued to the word

    space_w = font.size(" ")[0]
    lines = []
    current, current_w = [], 0
    for group in groups:
        gw = sum(item[2] for item in group)
        add = gw + (space_w if current else 0)
        if current and max_width is not None and current_w + add > max_width:
            lines.append((current, current_w))
            current, current_w = [group], gw
        else:
            current.append(group)
            current_w += add
    if current:
        lines.append((current, current_w))
    return lines, space_w


def render_rich(lines, space_w, font, key_font, color, key_color, line_height,
                align="center", pad=0, bg=None):
    inner_w = max(w for _, w in lines)
    surf = pygame.Surface((inner_w + 2 * pad, line_height * len(lines) + 2 * pad),
                          pygame.SRCALPHA)
    if bg is not None:
        surf.fill(bg)
    y = pad
    for groups, line_w in lines:
        x = pad + ((inner_w - line_w) // 2 if align == "center" else 0)
        for gi, group in enumerate(groups):
            if gi > 0:
                x += space_w
            for text, is_key, width in group:
                img = (key_font if is_key else font).render(
                    text, True, key_color if is_key else color)
                surf.blit(img, (x, y + (line_height - img.get_height()) // 2))
                x += width
        y += line_height
    return surf


def render_spaced(text, font, color, spacing, colors=None, pad=0, bg=None):
    """Letter-spaced single-line text."""
    imgs = [font.render(ch, True, colors[i] if colors else color)
            for i, ch in enumerate(text)]
    total = sum(im.get_width() for im in imgs) + spacing * (len(text) - 1)
    height = max(im.get_height() for im in imgs)
    surf = pygame.Surface((total + 2 * pad, height + 2 * pad), pygame.SRCALPHA)
    if bg is not None:
        surf.fill(bg)
    x = pad
    for im in imgs:
        surf.blit(im, (x, pad))
        x += im.get_width() + spacing
    return surf


def soft_blur(surf, factor=6):
    """Cheap blur: shrink and enlarge with smooth scaling."""
    w, h = surf.get_size()
    small = pygame.transform.smoothscale(
        surf, (max(1, w // factor), max(1, h // factor)))
    return pygame.transform.smoothscale(small, (w, h))


# ----------------------------------------------------------------------------
# PROCEDURAL ASSETS (no external files)
# ----------------------------------------------------------------------------
def build_background():
    """Midnight navy gradient with a soft central lift and a cinematic vignette."""
    sw, sh = 96, 64
    small = pygame.Surface((sw, sh))
    for j in range(sh):
        fy = j / (sh - 1)
        base = mix(BG_TOP, BG_BOTTOM, fy)
        for i in range(sw):
            fx = i / (sw - 1)
            dx, dy = (fx - 0.5) / 0.62, (fy - 0.52) / 0.34
            lift = max(0.0, 1.0 - (dx * dx + dy * dy)) ** 2
            vx, vy = (fx - 0.5) / 0.62, (fy - 0.5) / 0.62
            vignette = 1.0 - 0.55 * smoothstep(vx * vx + vy * vy)
            r = (base[0] + lift * 6) * vignette
            g = (base[1] + lift * 9) * vignette
            b = (base[2] + lift * 20) * vignette
            small.set_at((i, j), (int(clamp(r, 0, 255)),
                                  int(clamp(g, 0, 255)),
                                  int(clamp(b, 0, 255))))
    return pygame.transform.smoothscale(small, (WIDTH, HEIGHT)).convert()


AMBIENT_H = 360


def build_ambient():
    """Wide, soft amber light behind the featured area (alpha gradient)."""
    sw, sh = 96, 32
    small = pygame.Surface((sw, sh), pygame.SRCALPHA)
    for j in range(sh):
        fy = j / (sh - 1)
        for i in range(sw):
            fx = i / (sw - 1)
            dx, dy = (fx - 0.5) / 0.58, (fy - 0.5) / 0.5
            g = max(0.0, 1.0 - (dx * dx + dy * dy))
            small.set_at((i, j), (255, 170, 70, int(34 * g * g)))
    return pygame.transform.smoothscale(small, (WIDTH, AMBIENT_H))


def make_hairline(length, color, peak=1.0, thickness=1):
    """Horizontal gradient line for additive blending."""
    surf = pygame.Surface((length, thickness))
    surf.fill((0, 0, 0))
    for x in range(length):
        p = math.sin(math.pi * x / max(1, length - 1)) ** 2 * peak
        c = scale_color(color, p)
        for y in range(thickness):
            surf.set_at((x, y), c)
    return surf.convert()


def make_trail_surface(length, peak):
    """Thin 3px light streak (additive) that fades at both ends."""
    surf = pygame.Surface((length, 3))
    surf.fill((0, 0, 0))
    vertical = (0.30, 1.0, 0.30)
    for x in range(length):
        s = max(0.0, math.sin(math.pi * x / max(1, length - 1)))
        p = (s ** 1.6) * peak * 0.62
        for y in range(3):
            surf.set_at((x, y), scale_color(AMBER, p * vertical[y]))
    return surf.convert()


def make_sweep_surface(width):
    """Soft vertical band of warm light for the continuous sweep (additive)."""
    surf = pygame.Surface((width, HEIGHT))
    for x in range(width):
        prof = math.sin(math.pi * x / (width - 1)) ** 3
        pygame.draw.line(surf, (int(30 * prof), int(20 * prof), int(7 * prof)),
                         (x, 0), (x, HEIGHT))
    return surf.convert()


def make_dot(radius):
    size = radius * 2 + 1
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    for y in range(size):
        for x in range(size):
            d = math.hypot(x - radius, y - radius) / (radius + 0.5)
            surf.set_at((x, y), (255, 222, 170, int(255 * max(0.0, 1.0 - d) ** 2)))
    return surf


def make_head_glow():
    surf = pygame.Surface((64, 9))
    for y in range(9):
        for x in range(64):
            dx = (x - 32) / 32.0
            dy = (y - 4) / 4.5
            p = max(0.0, 1.0 - (dx * dx + dy * dy)) ** 2
            surf.set_at((x, y), scale_color(AMBER, p * 0.75))
    return surf.convert()


GRAIN_TABLE = bytes(i * 6 // 256 for i in range(256))   # values 0..5


def make_grain_frame():
    n = WIDTH * HEIGHT
    mono = os.urandom(n).translate(GRAIN_TABLE)
    rgb = bytearray(n * 3)
    rgb[0::3] = mono
    rgb[1::3] = mono
    rgb[2::3] = mono
    surf = pygame.image.frombuffer(bytes(rgb), (WIDTH, HEIGHT), "RGB")
    return surf.convert()


def make_edge_profile():
    """1px-high alpha profile used to fade rows out toward the left/right margins."""
    profile = pygame.Surface((WIDTH, 1), pygame.SRCALPHA)
    margin, full = 28, 240
    for x in range(WIDTH):
        d = min(x, WIDTH - 1 - x)
        a = smoothstep((d - margin) / float(full - margin))
        profile.set_at((x, 0), (255, 255, 255, int(255 * a)))
    return profile


# ----------------------------------------------------------------------------
# SCROLLING TEXT LAYERS
# ----------------------------------------------------------------------------
@dataclass
class RowSpec:
    y: int
    family: str
    size: int
    italic: bool
    speed: float          # pixels / second (negative = leftward)
    color: tuple
    key_color: tuple
    alpha: float
    count: int
    big: bool = False


ROW_SPECS = [
    # upper layers
    RowSpec(126, "sans", 14, False, -26, CHAMPAGNE, GOLD, 0.60, 15),
    RowSpec(160, "serif", 22, True, 34, CHAMPAGNE, GOLD_BRIGHT, 0.72, 14),
    RowSpec(206, "serif", 30, False, -20, IVORY, GOLD_BRIGHT, 0.90, 12, True),
    # lower layers
    RowSpec(582, "sans", 16, False, 30, CHAMPAGNE, GOLD, 0.65, 14),
    RowSpec(624, "serif", 24, True, -42, IVORY, GOLD_BRIGHT, 0.72, 14),
    RowSpec(676, "serif", 32, False, 22, IVORY, GOLD_BRIGHT, 0.92, 12, True),
    RowSpec(724, "sans", 15, False, -34, CHAMPAGNE, GOLD, 0.60, 19),
]


class RowItem:
    __slots__ = ("idx", "base", "hot", "w", "h", "base_x", "flash_t")

    def __init__(self, idx, base, hot):
        self.idx = idx
        self.base = base
        self.hot = hot
        self.w, self.h = base.get_size()
        self.base_x = 0.0
        self.flash_t = None


class Row:
    """One horizontally flowing layer of statements, looping seamlessly."""
    GHOST = 0.13   # visibility of statements that have not been revealed yet

    def __init__(self, spec, indices, edge_profile, rng):
        self.spec = spec
        font = FontBank.get(spec.family, spec.size, italic=spec.italic)
        key_font = FontBank.get(spec.family, spec.size, bold=True, italic=spec.italic)
        line_h = font.get_linesize() + 4
        self.band_h = line_h + 8
        self.top = spec.y - self.band_h // 2

        self.items = []
        for idx in indices:
            tokens = parse_markup(STATEMENTS[idx])
            lines, space_w = layout_rich(tokens, font, key_font, None)
            base = render_rich(lines, space_w, font, key_font,
                               spec.color, spec.key_color, line_h)
            hot = render_rich(lines, space_w, font, key_font,
                              GOLD_BRIGHT, GOLD_BRIGHT, line_h)
            self.items.append(RowItem(idx, base, hot))

        self.max_w = max(it.w for it in self.items)
        gap = 64.0 + spec.size * 2.4
        total = sum(it.w + gap for it in self.items)
        minimum = WIDTH + 2 * self.max_w + 120
        if total < minimum:
            gap += (minimum - total) / len(self.items)
        x = 0.0
        for it in self.items:
            it.base_x = x
            x += it.w + gap
        self.length = x
        self.scroll = rng.uniform(0, self.length)

        self.layer = pygame.Surface((WIDTH, self.band_h), pygame.SRCALPHA)
        self.mask = pygame.transform.scale(edge_profile, (WIDTH, self.band_h))

    def update(self, dt):
        self.scroll += self.spec.speed * dt

    def draw(self, screen, now, revealed_at, sweep_x):
        layer = self.layer
        layer.fill((0, 0, 0, 0))
        spec = self.spec
        for it in self.items:
            x = (it.base_x + self.scroll) % self.length - self.max_w
            if x > WIDTH or x + it.w < 0:
                continue

            reveal_t = revealed_at.get(it.idx)
            lit = 0.0 if reveal_t is None else smoothstep((now - reveal_t) / 1.8)
            cx = x + it.w * 0.5

            # first time a revealed statement crosses the bright central zone: flash
            if reveal_t is not None and it.flash_t is None and 260 < cx < 940:
                it.flash_t = now
            flash = 0.0
            if it.flash_t is not None:
                flash = max(0.0, 1.0 - (now - it.flash_t) / 3.2) ** 2

            boost = math.exp(-((cx - sweep_x) / 190.0) ** 2) * lit
            a = spec.alpha * (self.GHOST + (1.0 - self.GHOST) * lit) * (1.0 + 0.35 * boost)
            it.base.set_alpha(int(255 * clamp(a)))
            ty = (self.band_h - it.h) // 2
            layer.blit(it.base, (int(x), ty))

            hot_a = max(boost * 0.70, flash * 0.90) * lit
            if hot_a > 0.02:
                it.hot.set_alpha(int(255 * clamp(hot_a * min(1.0, spec.alpha + 0.2))))
                layer.blit(it.hot, (int(x), ty))

        layer.blit(self.mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        screen.blit(layer, (0, self.top))


def assign_statements(rng):
    """Short statements feed the large rows; the rest are shuffled across the others."""
    order = sorted(range(len(STATEMENTS)), key=lambda i: len(plain(STATEMENTS[i])))
    big_total = sum(s.count for s in ROW_SPECS if s.big)
    big_pool, rest = order[:big_total], order[big_total:]
    rng.shuffle(big_pool)
    rng.shuffle(rest)
    result, bp, rp = [], 0, 0
    for spec in ROW_SPECS:
        if spec.big:
            result.append(big_pool[bp:bp + spec.count])
            bp += spec.count
        else:
            result.append(rest[rp:rp + spec.count])
            rp += spec.count
    return result


# ----------------------------------------------------------------------------
# AMBIENT ELEMENTS
# ----------------------------------------------------------------------------
class Trail:
    """A thin amber light streak travelling horizontally."""

    def __init__(self, y, rng):
        self.y = y
        self.length = rng.randint(180, 420)
        self.speed = rng.choice((-1, 1)) * rng.uniform(110, 330)
        self.x = rng.uniform(-self.length, WIDTH)
        self.surf = make_trail_surface(self.length, rng.uniform(0.40, 0.85))
        self.rng = rng

    def update(self, dt):
        self.x += self.speed * dt
        if self.speed > 0 and self.x > WIDTH + 40:
            self.x = -self.length - self.rng.uniform(0, 700)
        elif self.speed < 0 and self.x < -self.length - 40:
            self.x = WIDTH + self.rng.uniform(0, 700)

    def draw(self, screen):
        screen.blit(self.surf, (int(self.x), self.y - 1), special_flags=pygame.BLEND_RGB_ADD)


class Mote:
    __slots__ = ("x", "y", "vx", "sway", "sway_speed", "phase", "tw_speed", "alpha", "dot")


class Dust:
    """Minimal atmospheric particles: tiny, slow, softly twinkling."""

    def __init__(self, rng, count=44):
        self.dots = [make_dot(1), make_dot(2)]
        self.motes = []
        for _ in range(count):
            m = Mote()
            m.x = rng.uniform(0, WIDTH)
            m.y = rng.uniform(20, HEIGHT - 20)
            m.vx = rng.uniform(4, 16) * rng.choice((1, 1, 1, -1))
            m.sway = rng.uniform(2, 9)
            m.sway_speed = rng.uniform(0.2, 0.7)
            m.phase = rng.uniform(0, math.tau)
            m.tw_speed = rng.uniform(0.4, 1.4)
            m.alpha = rng.uniform(0.10, 0.34)
            m.dot = rng.choice((0, 0, 1))
            self.motes.append(m)

    def update(self, dt):
        for m in self.motes:
            m.x += m.vx * dt
            if m.x > WIDTH + 10:
                m.x = -10
            elif m.x < -10:
                m.x = WIDTH + 10

    def draw(self, screen, now):
        for m in self.motes:
            tw = 0.55 + 0.45 * math.sin(now * m.tw_speed + m.phase)
            dot = self.dots[m.dot]
            dot.set_alpha(int(255 * clamp(m.alpha * tw)))
            y = m.y + math.sin(now * m.sway_speed + m.phase) * m.sway
            screen.blit(dot, (int(m.x), int(y)))


# ----------------------------------------------------------------------------
# THE SCENE
# ----------------------------------------------------------------------------
class Scene:
    def __init__(self, screen):
        self.screen = screen
        rng = random.Random(11)

        # static art
        self.background = build_background()
        self.ambient = build_ambient()
        self.sweep_surf = make_sweep_surface(SWEEP_WIDTH)
        self.rule_top = make_hairline(760, GOLD, 0.55)
        self.rule_title = make_hairline(560, GOLD, 0.75)
        self.head_glow = make_head_glow()
        self.grain = [make_grain_frame() for _ in range(3)]
        self.grain_i = 0
        self.grain_timer = 0.0
        self.intro_cover = pygame.Surface((WIDTH, HEIGHT))
        self.intro_cover.fill((0, 0, 0))

        # text layers
        edge_profile = make_edge_profile()
        assignments = assign_statements(rng)
        self.rows = [Row(spec, idxs, edge_profile, rng)
                     for spec, idxs in zip(ROW_SPECS, assignments)]

        # light trails sit in the gaps between layers
        self.trails = [Trail(y, rng) for y in (139, 181, 244, 555, 600, 647, 705, 745)]
        self.dust = Dust(rng)

        # title
        title_font = FontBank.get("serif", 42)
        colors = [GOLD_BRIGHT if i < 3 else IVORY for i in range(len(TITLE))]
        self.title_img = render_spaced(TITLE, title_font, IVORY, 11, colors)
        glow_src = render_spaced(TITLE, title_font, AMBER, 11, pad=24,
                                 bg=(AMBER[0], AMBER[1], AMBER[2], 0))
        self.title_glow = soft_blur(glow_src, 6)

        # small labels
        self.label_font = FontBank.get("sans", 13, bold=True)
        self.number_font = FontBank.get("sans", 15, bold=True)
        self.label_left = render_spaced("STATEMENTS APPEARED", self.label_font, CHAMPAGNE, 3)
        self.label_cache = {}
        self.number_cache = {}

        # clock + sweep
        self.time = 0.0
        self.sweep_x = -SWEEP_WIDTH

        # featured statement state
        self.revealed_at = {}
        self.k = -1                      # sequence counter (0-based)
        self.phase = -INITIAL_DELAY
        self.duration = 5.0
        self.current = None              # (main, glow, idx)
        self.feature_cache = {}
        self.next_prepared = -1
        self.count = 0
        self.progress_shown = 0.0

    # --- featured statement building -----------------------------------
    def build_featured(self, idx):
        if idx in self.feature_cache:
            return self.feature_cache[idx]
        tokens = parse_markup(STATEMENTS[idx])
        for size in (50, 46, 42, 38, 34):
            font = FontBank.get("serif", size)
            key_font = FontBank.get("serif", size, bold=True, italic=True)
            lines, space_w = layout_rich(tokens, font, key_font, FEATURE_MAX_W)
            if len(lines) <= 3:
                break
        line_h = int(font.get_linesize() * 1.16)
        pad = 36
        main = render_rich(lines, space_w, font, key_font, IVORY, GOLD_BRIGHT,
                           line_h, "center", pad)
        glow_src = render_rich(lines, space_w, font, key_font, AMBER, AMBER,
                               line_h, "center", pad,
                               bg=(AMBER[0], AMBER[1], AMBER[2], 0))
        glow = soft_blur(glow_src, 7)
        self.feature_cache[idx] = (main, glow)
        return main, glow

    def start_feature(self, k):
        self.k = k
        idx = k % len(STATEMENTS)
        if k < len(STATEMENTS):
            self.revealed_at[idx] = self.time
        self.count = min(k + 1, len(STATEMENTS))
        main, glow = self.build_featured(idx)
        self.current = (main, glow, idx)
        n = len(plain(STATEMENTS[idx]))
        self.duration = clamp(3.8 + 0.034 * n, 4.6, 6.4)
        self.next_prepared = -1
        keep = {idx, (idx + 1) % len(STATEMENTS)}
        for key in list(self.feature_cache):
            if key not in keep:
                del self.feature_cache[key]

    # --- update ---------------------------------------------------------
    def update(self, dt):
        self.time += dt

        span = WIDTH + 2 * SWEEP_WIDTH + 500
        self.sweep_x = (self.time * SWEEP_SPEED) % span - SWEEP_WIDTH

        for row in self.rows:
            row.update(dt)
        for trail in self.trails:
            trail.update(dt)
        self.dust.update(dt)

        self.grain_timer += dt
        if self.grain_timer >= 0.085:
            self.grain_timer = 0.0
            self.grain_i = (self.grain_i + 1) % len(self.grain)

        self.phase += dt
        if self.k < 0:
            if self.phase >= 0.0:
                self.start_feature(0)
        elif self.phase >= self.duration:
            self.phase -= self.duration
            self.start_feature(self.k + 1)

        # prepare the next statement while the current one is being read
        if self.k >= 0 and self.phase > 1.0 and self.next_prepared != self.k:
            self.build_featured((self.k + 1) % len(STATEMENTS))
            self.next_prepared = self.k

        target = self.count / float(len(STATEMENTS))
        self.progress_shown += (target - self.progress_shown) * min(1.0, dt * 2.5)

    # --- drawing --------------------------------------------------------
    def draw(self):
        screen = self.screen
        now = self.time

        screen.blit(self.background, (0, 0))

        pulse = 0.78 + 0.22 * math.sin(now * 0.55)
        self.ambient.set_alpha(int(255 * pulse))
        screen.blit(self.ambient, (0, FEATURE_CENTER_Y - AMBIENT_H // 2))

        # fine horizontal rules framing the featured area
        add = pygame.BLEND_RGB_ADD
        screen.blit(self.rule_top, (CENTER_X - 380, RULE_TOP_Y), special_flags=add)
        screen.blit(self.rule_top, (CENTER_X - 380, RULE_BOTTOM_Y), special_flags=add)

        for trail in self.trails:
            trail.draw(screen)

        for row in self.rows:
            row.draw(screen, now, self.revealed_at, self.sweep_x)

        self.draw_featured()

        # continuous light sweep across the whole composition
        screen.blit(self.sweep_surf, (int(self.sweep_x - SWEEP_WIDTH // 2), 0),
                    special_flags=add)

        self.dust.draw(screen, now)
        self.draw_title()
        self.draw_progress()

        screen.blit(self.grain[self.grain_i], (0, 0), special_flags=add)

        intro = clamp(now / 2.4)
        if intro < 1.0:
            self.intro_cover.set_alpha(int(255 * (1.0 - smoothstep(intro))))
            screen.blit(self.intro_cover, (0, 0))

    def draw_title(self):
        screen = self.screen
        glow_alpha = 0.55 + 0.20 * math.sin(self.time * 0.9)
        self.title_glow.set_alpha(int(255 * glow_alpha))
        screen.blit(self.title_glow, self.title_glow.get_rect(center=(CENTER_X, TITLE_Y)))
        screen.blit(self.title_img, self.title_img.get_rect(center=(CENTER_X, TITLE_Y)))
        screen.blit(self.rule_title, (CENTER_X - 280, TITLE_RULE_Y),
                    special_flags=pygame.BLEND_RGB_ADD)

    def draw_featured(self):
        if self.k < 0 or self.current is None:
            return
        screen = self.screen
        t, dur = self.phase, self.duration
        fade_in = ease_out_cubic(t / FADE_IN)
        fade_out = smoothstep((dur - t) / FADE_OUT)
        a = min(fade_in, fade_out)
        if a <= 0.003:
            return

        main, glow, idx = self.current
        w, h = main.get_size()

        # expands slightly as it appears
        s = 0.94 + 0.06 * ease_out_cubic(t / SCALE_TIME) if t < SCALE_TIME else 1.0
        cx = CENTER_X
        cy = FEATURE_CENTER_Y + (1.0 - fade_in) * 10.0 - (1.0 - fade_out) * 8.0

        if s < 0.9995:
            size = (max(1, int(w * s)), max(1, int(h * s)))
            img = pygame.transform.smoothscale(main, size)
            gl = pygame.transform.scale(glow, size)
        else:
            img, gl = main, glow

        breathe = 0.85 + 0.15 * math.sin(self.time * 1.7)
        gl.set_alpha(int(255 * clamp(a * 0.75 * breathe)))
        screen.blit(gl, gl.get_rect(center=(cx, int(cy))))
        img.set_alpha(int(255 * clamp(a)))
        screen.blit(img, img.get_rect(center=(cx, int(cy))))

        # statement number between two short gold rules
        label = self.number_cache.get(idx)
        if label is None:
            label = render_spaced("%03d" % (idx + 1), self.number_font, GOLD_BRIGHT, 7)
            self.number_cache[idx] = label
        label.set_alpha(int(255 * clamp(a)))
        screen.blit(label, label.get_rect(center=(cx, NUMBER_Y)))
        line_color = scale_color(GOLD, 0.7 * a)
        half = label.get_width() // 2 + 16
        pygame.draw.line(screen, line_color, (cx - half - 70, NUMBER_Y), (cx - half, NUMBER_Y))
        pygame.draw.line(screen, line_color, (cx + half, NUMBER_Y), (cx + half + 70, NUMBER_Y))

    def draw_progress(self):
        screen = self.screen
        left, right = MARGIN_X, WIDTH - MARGIN_X
        y = PROGRESS_Y

        pygame.draw.line(screen, (36, 38, 50), (left, y), (right, y))
        for i in range(11):                                   # small tick marks
            tx = left + (right - left) * i // 10
            pygame.draw.line(screen, (46, 48, 62), (tx, y - 3), (tx, y))

        fx = left + (right - left) * self.progress_shown
        if fx > left + 1:
            pygame.draw.line(screen, GOLD, (left, y), (int(fx), y), 2)
            screen.blit(self.head_glow, (int(fx) - 32, y - 4),
                        special_flags=pygame.BLEND_RGB_ADD)

        self.label_left.set_alpha(170)
        screen.blit(self.label_left, (left, y - 26))

        label = self.label_cache.get(self.count)
        if label is None:
            label = render_spaced("%03d / %03d" % (self.count, len(STATEMENTS)),
                                  self.label_font, GOLD_BRIGHT, 3)
            self.label_cache[self.count] = label
        label.set_alpha(220)
        screen.blit(label, (right - label.get_width(), y - 26))


# ----------------------------------------------------------------------------
# MAIN
# ----------------------------------------------------------------------------
def create_screen():
    try:
        return pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED, vsync=1)
    except Exception:
        return pygame.display.set_mode((WIDTH, HEIGHT))


def main():
    pygame.init()
    pygame.display.set_caption(TITLE.title())
    screen = create_screen()

    # show a black frame immediately while assets are generated
    screen.fill((0, 0, 0))
    pygame.display.flip()

    scene = Scene(screen)
    clock = pygame.time.Clock()

    running = True
    while running:
        dt = min(clock.tick(FPS) / 1000.0, 0.05)     # delta time, clamped
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_q):
                running = False
        scene.update(dt)
        scene.draw()
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
