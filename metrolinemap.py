import sys
import subprocess
import svgwrite
from PIL import ImageFont, ImageDraw, Image


BLACK = '#000000'
WHITE = '#FFFFFF'
BLEU_PARISINE = '#1A3C90'
CUIVRE = '#8D5E2A'


def get_text_width(text, font_path, font_size):
    img = Image.new('RGB', (1, 1), color='white')
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_path, font_size)
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2]-bbox[0], bbox[3]-bbox[1]


class MetroLineMap:

    def __init__(self, name: str, color: str, stations: list, path: str = '') -> None:
        self.name = name
        self.color = color
        self.stations = stations
        self.path = path if path else name+'.svg'
        self.dwg = None
        self.n = len(self.stations)
        self.fonts = {'Parisine-Regular': 'fonts/Parisine Regular.otf',
                      'Parisine-Bold': 'fonts/Parisine Bold.otf',
                      'Parisine-Bold-Italic': 'fonts/Parisine Bold Italic.otf'}

    def draw_line(self, x1, y1, x2, y2, color=BLACK, stroke_width=0.5):
        self.dwg.add(self.dwg.line((x1, y1), (x2, y2), stroke=color, stroke_width=stroke_width))

    def draw_circle(self, x, y, r, color=BLACK, stroke_color=BLACK, stroke_width=0):
        self.dwg.add(self.dwg.circle(center=(x, y), r=r, fill=color, stroke=stroke_color, stroke_width=stroke_width))

    def draw_text(self, text, x, y, color=BLACK, font_family='Arial', font_size=10, angle=0, bgcolor='', lil=False):
        size = f"{font_size}px"
        if bgcolor:
            testfontpath = self.fonts[font_family] if font_family in self.fonts else 'Arial'
            rw, rh = get_text_width(text, testfontpath, font_size)
            if lil:
                rw, rh = 1.2*rw, 0.8*rh
            group = self.dwg.add(svgwrite.container.Group())
            group.add(self.dwg.rect(insert=(x, y-rh), size=(rw+2, rh+3), fill=bgcolor))
            group.add(self.dwg.text(text, insert=(x+2, y), fill=color,
                                    style=f"font-family:{font_family};font-size:{size};"))
            group.rotate(-angle, center=(x, y))
        else:
            self.dwg.add(self.dwg.text(text, insert=(x, y), fill=color,
                                       style=f"font-family:{font_family};font-size:{size};",
                                       transform=f"rotate({-angle},{x},{y})"))

    def draw_rect(self, x, y, width, height, color=BLACK, angle=0):
        rect = self.dwg.rect(insert=(x, y), size=(width, height), fill=color)
        if angle:
            rect.rotate(-angle, center=(x, y))
        self.dwg.add(rect)

    def draw_image(self, image_path, x, y, width=None, height=None):
        if width is not None and height is not None:
            self.dwg.add(self.dwg.image(href=image_path, insert=(x, y), size=(width, height)))
        else:
            self.dwg.add(self.dwg.image(href=image_path, insert=(x, y)))

    def draw_pixel(self, x, y, c=1, color='red'):
        self.dwg.add(self.dwg.rect(insert=(x-c/2, y-c/2), size=(f'{c}px', f'{c}px'), fill=color))

    def _sort_key(self, item):
        try:
            if item.endswith('a') or item.endswith('b'):
                return int(item[:-1])
            return int(item)
        except ValueError:
            return float('inf')

    def generate_map(self, open_image: bool = True) -> None:

        self.dwg = svgwrite.Drawing(self.path, profile='full')

        for font in self.fonts:
            self.dwg.embed_font(font, self.fonts[font])

        spacing = 50
        angle = 30
        linewidth = 4.5
        circlerad = 4
        w0, h0 = 30, 100
        img_width = 9
        font_size = 9
        font_2ndsize = 4

        self.draw_line(w0, h0, w0+(self.n-1)*spacing, h0, color=self.color, stroke_width=linewidth)
        for i, station in enumerate(self.stations):
            x, y = w0 + i*spacing, h0
            terminus = (i == 0) or (i == self.n-1)
            nom_sec, corresp = self.stations[station]

            # cercle station
            if terminus:
                self.draw_circle(x, y, circlerad, color=WHITE, stroke_width=1)
                self.draw_circle(x, y, 3/5*circlerad, color=self.color)
            elif bool(corresp):
                self.draw_circle(x, y, circlerad, color=WHITE, stroke_width=1)
            else:
                self.draw_circle(x, y, circlerad, color=self.color)

            # texte station
            if terminus:
                self.draw_text(station.replace(' - ', '–'), x, y-8, font_family='Parisine-Bold', font_size=font_size,
                               angle=angle, color=WHITE, bgcolor=BLEU_PARISINE)
            else:
                self.draw_text(station.replace(' - ', '–'), x, y-8, font_family='Parisine-Bold', font_size=font_size,
                               angle=angle, color=BLEU_PARISINE)

            # texte secondaire station
            if nom_sec is not None:
                sx, sy = x+15, y-8
                if nom_sec.startswith('m:'):
                    self.draw_text(nom_sec[2:], sx, sy, font_family='Parisine-Bold-Italic', font_size=font_2ndsize,
                                   angle=angle, color=WHITE, bgcolor=CUIVRE, lil=True)
                elif nom_sec == 'Gare Grandes Lignes':
                    self.draw_text(nom_sec, sx, sy, font_family='Parisine-Bold-Italic', font_size=font_2ndsize,
                                   angle=angle, color=WHITE, bgcolor=BLEU_PARISINE, lil=True)
                else:
                    self.draw_text(nom_sec, sx, sy, font_family='Parisine-Bold-Italic', font_size=font_2ndsize,
                                   angle=angle, color=BLEU_PARISINE, lil=True)

            # correspondances
            pfxcorresp = ['M', 'T', 'C', 'B', 'R', 'S', 'p:M', 'p:T', 'p:C', 'p:B', 'p:R', 'p:S']
            dictcorresp = {key: sorted([i[len(key):] for i in corresp if i.startswith(key)], key=self._sort_key) \
                           for key in pfxcorresp}
            c = 0.5
            cx, cy = x, y+circlerad+0.5
            for i in dictcorresp:
                if dictcorresp[i]:
                    xx, yy = x-img_width/2, y+c*(img_width+2)+2
                    if i.startswith('p:'):
                        self.draw_image("img/pieds.png", xx-img_width, yy,
                                        img_width, img_width)
                    self.draw_image(f"img/{i.strip('p:')}.png", xx, yy, img_width, img_width)
                    idx = 0
                    ral = 0
                    for j in dictcorresp[i]:
                        if idx >= 2 and len(dictcorresp[i]) >= 4:
                            ral += 1
                            c += 1
                            idx = 0
                        self.draw_image(f"img/{i.strip('p:')}{j}.png", xx+(idx+1)*(img_width+1), y+c*(img_width+2)+2,
                                        img_width, img_width)
                        idx += 1
                    c += 1
                    self.draw_line(cx, cy+0.3, xx+img_width/2, yy-0.3, color=BLEU_PARISINE)
                    cx, cy = xx+img_width/2, yy+img_width

        self.dwg.save()

        if open_image:
            navig = {'linux': 'xdg-open', 'win32': 'explorer', 'darwin': 'open'}
            subprocess.run([navig[sys.platform], self.path])


M14_data = {
        'Saint-Denis - Pleyel': ['m:Stade de France', ['M15', 'M16', 'M17', 'p:RD', 'p:SH', 'p:M13']],
        'Mairie de Saint-Ouen': ['Region Île-de-France', ['M13']],
        'Gare de Saint-Ouen': [None, ['RC']],
        'Porte de Clichy': ['Tribunal de Paris', ['M13', 'T3b', 'RC']],
        'Pont Cardinet': [None, ['p:SL']],
        'Saint-Lazare': ['Gare Grandes Lignes', ['M3', 'M9', 'M12', 'M13', 'RA', 'RE', 'SJ', 'SL']],
        'Madeleine': [None, ['M8', 'M12']],
        'Pyramides': [None, ['M7']],
        'Châtelet': [None, ['M1', 'M4', 'M7', 'M11', 'RA', 'RB', 'RD']],
        'Gare de Lyon': ['Gare Grandes Lignes', ['M1', 'RA', 'RD', 'SR']],
        'Bercy': ['Gare Grandes Lignes', ['M6']],
        'Cour Saint-Émilion': [None, []],
        'Bibliothèque François Mitterrand': [None, ['RC']],
        'Olympiades': [None, []],
        'Maison Blanche': [None, ['M7', 'p:T3a']],
        'Hôpital Bicêtre': [None, []],
        'Villejuif - Gustave Roussy': [None, ['M15']],
        'L\'Haÿ-les-Roses': [None, []],
        'Chevilly-Larue': ['Marché International', ['T7']],
        'Thiais - Orly': ['Pont de Rungis', ['RC']],
        'Aéroport d\'Orly': ['Terminaux 1, 2 et 3', ['M18', 'p:T7']]
    }

M20_data = {
        'Javel - André Citroën': [None, ['M10', 'RC']],
        'Saint-Charles': [None, []],
        'Boucicaut': [None, ['M8']],
        'Convention': [None, ['M12']],
        'Brancion - Vouillé': [None, []],
        'Plaisance': [None, ['M13']],
        'Hippolyte Maindron': [None, []],
        'Alésia': [None, ['M4']],
        'Hôpital Sainte-Anne': [None, []],
        'Butte aux Cailles': [None, []],
        'Choisy - Tolbiac': [None, ['M7', 'T9']],
        'Olympiades': [None, ['M14']],
        'Avenue de France': [None, ['T3a', 'M10']],
        'Charenton - Liberté': [None, ['M8', 'RD']]
    }

T13_data = {
        'Pont de Levallois - Bécon': [None, ['M3']],
        'André Malraux': [None, []],
        'Île de la Grande Jatte': [None, []],
        'Square Nokovitch': [None, []],
        'Place Hérold': [None, []],
        'Place Charras': [None, []],
        'Coulée Gambetta': [None, []],
        'La Défense - 4 Temps': [None, ['T2', 'M1', 'M15', 'M18', 'RA', 'RE', 'SL']],
        'Les Graviers': [None, []],
        'Rond-Point des Bergères': [None, []],
        'Les Fontenelles': [None, []],
        'Clémenceau - Sadi Carnot': [None, []],
        'Nanterre - La Boule': [None, ['T1', 'M15']],
        'Place Foch': [None, []],
        'Saint-Saëns': [None, []],
        'Gare de Rueil-Malmaison': [None, ['C4', 'RA']],
        'Pont de Chatou': [None, []]
    }

C2_data = {
        'Pont de Sèvres': [None, ['M9', 'M15', 'p:T2']],
        'Île Seguin': ['La Seine Musicale', []],
        'Meudon-sur-Seine': [None, ['T2']],
        'Gare de Meudon': [None, ['RE']],
        'Meudon - Val Fleury': [None, ['RC']],
        'Meudon - Bois de Clamart': ['Lycée Rabelais', []],
        'Etang de Chalais': [None, []],
        'Carrefour des Arbres Verts': [None, []],
        'Meudon-la-Forêt': [None, ['p:T6']],
        'Vélizy 2': ['Centre Commercial', ['T6']],
        'Vélizy - Europe Sud': [None, []],
        'Vélizy 3': ['Centre Commercial', []],
        'Malabry': ['Vallée aux Loups', ['T10']]
    }

# format 'Nom station': ['Nom secondaire', [correspondances]]
# prefixes nom secondaires : m: (monument), 'Gare Grandes Lignes' ou rien (autres)
# prefixes correspondances : M (Metro), T (Tram), C (Cable), B (BHNS), R (RER), S (Transilien) ou p: (a pied)

M14 = MetroLineMap('M14', '#662483', M14_data)
M14.generate_map(False)

M20 = MetroLineMap('M20', '#00AA90', M20_data)
M20.generate_map(False)

T13 = MetroLineMap('T13', '#558B2F', T13_data)
T13.generate_map(False)

C2 = MetroLineMap('C2', '#E40116', C2_data)
C2.generate_map(True)
