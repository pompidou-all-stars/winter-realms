"""Palettes et socles des factions (couleurs reprises de drawFactionTower et draw() dans index.html,
avivées pour la 3D)."""
import math
from outils import cylindre, boite, sphere, pivot, anneau

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

SOCLES = {'alliance': socle_alliance}
