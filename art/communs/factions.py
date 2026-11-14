"""Palettes et socles des factions (couleurs reprises de drawFactionTower et draw() dans index.html,
avivées pour la 3D)."""
import math
from .outils import cylindre, boite, sphere, pivot, anneau

# stone, mid, dark, glow, accent
PAL = {
    'alliance': dict(pierre='#ece4cf', moyen='#a9b4c2', sombre='#5e6f86', or_='#e3b44a', accent='#2f5fa8', toit='#2b56a0'),
    'horde': dict(pierre='#bd7042', moyen='#6b3e2b', sombre='#33251f', or_='#d34d36', accent='#e5b24e'),
    'sylvestres': dict(pierre='#8dcf8b', moyen='#397c57', sombre='#244b3c', or_='#d8e99b', accent='#8c70bd'),
    'nains': dict(pierre='#c6b5a0', moyen='#766b60', sombre='#3d4148', or_='#e0a34d', accent='#5f91a8'),
    'ombres': dict(pierre='#b8a0d9', moyen='#5c477d', sombre='#282039', or_='#a879c9', accent='#7ff3ff'),
}
SOL = {'alliance': ('#5a9a45', '#66a64f'), 'horde': ('#52683b', '#647b43'), 'sylvestres': ('#356d4b', '#407d58'),
       'nains': ('#68604d', '#77705b'), 'ombres': ('#493858', '#594568')}
BIOME = {'alliance': dict(bord='#6b6253', terre='#5a4632', haut='#a8c878', bas='#31563a', detail='#c8e08a', fleur='#f4e27a'),
         'horde': dict(bord='#303b25', terre='#4b3a2a', haut='#b5b879', bas='#4b6133', detail='#c9a36a', fleur='#e07a3a'),
         'sylvestres': dict(bord='#244a39', terre='#3a3326', haut='#9bd39a', bas='#2e6248', detail='#d6e8a2', fleur='#c79bff'),
         'nains': dict(bord='#4b4538', terre='#4a4036', haut='#c5b18b', bas='#5a5143', detail='#d9c9a5', fleur='#e0a34d'),
         'ombres': dict(bord='#382d4a', terre='#2a2236', haut='#b9a0d7', bas='#49395e', detail='#a78cdb', fleur='#7ff3ff')}

HAUT_SOCLE = 0.12

def socle_alliance(racine):
    """Dalle octogonale de pierre taillée, pierres d'angle, liseré d'or et écussons bleus."""
    p = PAL['alliance']
    cylindre('SocleBas', p['moyen'], .43, .41, .07, 8, (0, 0, 0), racine, biseau=.015, rot=(0, 0, math.pi / 8))
    cylindre('SocleHaut', p['pierre'], .36, .35, .05, 8, (0, 0, .07), racine, biseau=.012, rot=(0, 0, math.pi / 8))
    anneau('LisereOr', p['or_'], .365, .012, 16, 3, (0, 0, .07), racine, metal=.7, rough=.3)
    for q in range(4):
        a = q * math.pi / 2 + math.pi / 4
        boite(f'PierreAngle{q}', p['sombre'], .1, .1, .1, (math.cos(a) * .37, math.sin(a) * .37, .05), 0, racine, (0, 0, a))
        sphere(f'Clou{q}', p['or_'], .022, (math.cos(a) * .37, math.sin(a) * .37, .105), (1, 1, .6), 6, 4, racine, metal=.7, rough=.3)
    return HAUT_SOCLE

def socle_horde(racine):
    """Plateforme de rondins cerclée de fer, défenses d'os plantées autour."""
    p = PAL['horde']
    cylindre('Plateforme', '#6b4423', .42, .4, .08, 12, (0, 0, 0), racine, biseau=.015)
    anneau('Cercle', '#3a3330', .41, .016, 16, 3, (0, 0, .055), racine, metal=.5)
    cylindre('Dessus', '#8a5a33', .36, .35, .04, 12, (0, 0, .08), racine, biseau=.01)
    for q in range(5):
        a = q * 2 * math.pi / 5 + .3
        from .outils import cone
        cone(f'Defense{q}', '#f0e6cc', .03, .16, 6, (math.cos(a) * .4, math.sin(a) * .4, .06), racine,
             (math.cos(a + math.pi / 2) * .5, math.sin(a + math.pi / 2) * .5, 0))
    return HAUT_SOCLE

def socle_sylvestres(racine):
    """Souche moussue et racines noueuses, champignons luisants."""
    from .outils import cone
    cylindre('Souche', '#6b4a2f', .38, .32, .08, 10, (0, 0, 0), racine, biseau=.02)
    cylindre('Mousse', '#4f9a4a', .33, .31, .04, 10, (0, 0, .08), racine, biseau=.01)
    for q in range(5):
        a = q * 2 * math.pi / 5
        cone(f'Racine{q}', '#5a3d26', .06, .26, 6, (math.cos(a) * .28, math.sin(a) * .28, .03), racine,
             (0, 1.75, a))
    for q in range(3):
        a = q * 2.1 + .5
        sphere(f'Champignon{q}', '#c79bff', .035, (math.cos(a) * .34, math.sin(a) * .34, .1), (1, 1, .55), 8, 4, racine, emis=1.5)
    return HAUT_SOCLE

def socle_nains(racine):
    """Base hexagonale de pierre et d'acier riveté, bandeau de cuivre."""
    p = PAL['nains']
    cylindre('Hexa', '#4a4d55', .43, .41, .07, 6, (0, 0, 0), racine, biseau=.015)
    cylindre('Dalle', p['pierre'], .36, .35, .05, 6, (0, 0, .07), racine, biseau=.012)
    anneau('Cuivre', '#c8803e', .36, .013, 12, 3, (0, 0, .07), racine, metal=.7, rough=.3)
    for q in range(6):
        a = q * math.pi / 3
        sphere(f'Rivet{q}', '#d9b37a', .025, (math.cos(a) * .4, math.sin(a) * .4, .07), (1, 1, .6), 6, 4, racine, metal=.7)
    return HAUT_SOCLE

def socle_ombres(racine):
    """Dalle d'obsidienne et anneaux runiques flottants (lueur cyan)."""
    cylindre('Obsidienne', '#2c2340', .4, .36, .08, 7, (0, 0, 0), racine, biseau=.015)
    cylindre('Dalle', '#4a3a66', .32, .31, .04, 7, (0, 0, .08), racine, biseau=.01)
    a = pivot('AnneauFlottant', (0, 0, .16), racine)
    anneau('Rune', '#7ff3ff', .41, .012, 20, 3, (0, 0, 0), a, emis=2)
    for q in range(3):
        b = q * 2.094
        sphere(f'Eclat{q}', '#b8a0d9', .03, (math.cos(b) * .41, math.sin(b) * .41, 0), (1, 1, 1.5), 6, 4, a, emis=1)
    return HAUT_SOCLE

SOCLES = {'alliance': socle_alliance, 'horde': socle_horde, 'sylvestres': socle_sylvestres, 'nains': socle_nains, 'ombres': socle_ombres}
