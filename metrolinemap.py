import sys
import subprocess
import svgwrite
from PIL import ImageFont, ImageDraw, Image
import data


BLACK = '#000000'
WHITE = '#FFFFFF'
BLEU_PARISINE = '#1A3C90'
CUIVRE = '#8D5E2A'


class CouleursIDFM:
    NOIR = '#25303B'
    ROUGE = '#E3051C'
    ORANGE = '#F28E42'
    JAUNE = '#FFCE00'
    OCRE = '#E3B32A'
    MARRON = '#8D5E2A'
    VERT_CLAIR = '#D5C900'
    VERT_KAKI = '#9F9825'
    VERT_FONCE = '#00814F'
    VERT_POMME = '#83C491'
    TURQUOISE = '#00A88F'
    BLEU_CIEL = '#98D4E2'
    BLEU_AZUR = '#5291CE'
    BLEU_FONCE = '#0064B0'
    VIOLET = '#662483'
    FUSHIA = '#C04191'
    MAUVE = '#CEADD2'
    ROSE = '#F3A4BA'
    BORDEAUX = '#F3A4BA'
    GRIS_FONCE = '#706F6F'
    GRIS_CLAIR = '#C6C6C6'


def get_text_width(text, font_path, font_size):
    img = Image.new('RGB', (1, 1), color='white')
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_path, font_size)
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2]-bbox[0], bbox[3]-bbox[1]


class MetroLineMap:

    def __init__(self, name: str, color: str, stations: list, path_logo: str = '', path_out: str = '') -> None:
        self.name = name
        self.color = color
        self.stations = stations
        self.path_logo = path_logo if path_logo else 'img/'+name+'.svg'
        self.path_out = path_out if path_out else name+'.svg'
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
            # if lil:
            #     pass
            group = self.dwg.add(svgwrite.container.Group())
            if lil:
                group.add(self.dwg.rect(insert=(x, y-rh), size=(rw, rh), fill=bgcolor))
            else:
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

    def _sort_int_key(self, item):
        try:
            if item.endswith('a') or item.endswith('b'):
                return int(item[:-1])
            return int(item)
        except ValueError:
            return float('inf')

    def _sort_corresp(self, corresp_list, corresp_pfx):
        if self.pfxcorresp_dict[corresp_pfx.lstrip('p:')] is int:
            return sorted(list(set(corresp_list)), key=self._sort_int_key)
        return sorted(list(set(corresp_list)))

    def _get_layout(self, nbcorr):
        # format d'affichage des correspondances en fonction du nombre de lignes par catégorie modale
        # disposition : 1 [1], 2 [2], 3 [3], 4 [2, 2], 5 [3, 2], 6 [3, 3], 7 [3, 3, 1], 8 [3, 3, 2], etc
        if nbcorr <= 3:
            return [nbcorr]
        elif nbcorr == 4:
            return [2, 2]
        return [3]*(nbcorr//3) + ([nbcorr % 3] if nbcorr % 3 else [])

    def generate_map(self, open_image: bool = True) -> None:

        self.dwg = svgwrite.Drawing(self.path_out, profile='full')

        for font in self.fonts:
            self.dwg.embed_font(font, self.fonts[font])

        spacing = 35
        angle = 30
        linewidth = 4.5
        circlerad = 4
        w0, h0 = 30, 100
        img_width = 9
        font_size = 9
        font_2ndsize = 4
        spacing_2ndname = 12
        subtitle_spacing = 10

        self.pfxcorresp_dict = {'M': int, 'T': int, 'C': int, 'B': int, 'R': str, 'S': str}
        pfxcorresp = list(self.pfxcorresp_dict)
        pfxcorresp.extend([f'p:{i}' for i in pfxcorresp])
        
        self.draw_image(f'img/{self.name[1:]}.png', 100, 100, 200, 200)

        last_station = ''
        max_nbcorr = 0
        nx, y = w0, h0
        for station_idx, station in enumerate(self.stations):
            x = nx
            nx += spacing
            if last_station and self.stations[station][0] is not None:
                nx += subtitle_spacing

            last_station = station
            terminus = (station_idx == 0) or (station_idx == self.n-1)
            nom_sec, corresp = self.stations[station]

            # texte station
            if terminus:
                self.draw_text(station.replace(' - ', '–'), x, y-8, font_family='Parisine-Bold', font_size=font_size,
                               angle=angle, color=WHITE, bgcolor=BLEU_PARISINE)
            else:
                self.draw_text(station.replace(' - ', '–'), x, y-8, font_family='Parisine-Bold', font_size=font_size,
                               angle=angle, color=BLEU_PARISINE)

            # texte secondaire station
            if nom_sec is not None:
                sx, sy = x+spacing_2ndname, y-8
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
            max_nbcorr = 0
            dictcorresp = {key: self._sort_corresp([i[len(key):] for i in corresp if i.startswith(key)], key) \
                           for key in pfxcorresp}
            c = 0.5
            cx, cy = x, y+circlerad+0.5
            for i in dictcorresp:
                if dictcorresp[i]:
                    xx, yy = x-img_width/2, y+c*(img_width+2)+2
                    if i.startswith('p:'):
                        self.draw_image("img/pieds.png", xx-img_width, yy,
                                        img_width, img_width)
                    self.draw_image(f"img/{i.lstrip('p:')}.png", xx, yy, img_width, img_width)

                    layout = self._get_layout(len(dictcorresp[i]))
                    idx = 0
                    line_idx = 0
                    for j in dictcorresp[i]:
                        if idx >= layout[line_idx]:
                            c += 1
                            idx = 0
                            line_idx += 1
                        self.draw_image(f"img/{i.lstrip('p:')}{j}.png", xx+(idx+1)*(img_width+1), y+c*(img_width+2)+2,
                                        img_width, img_width)
                        idx += 1
                        if idx > max_nbcorr:
                            max_nbcorr = idx
                    c += 1
                    self.draw_line(cx, cy+0.3, xx+img_width/2, yy-0.3, color=BLEU_PARISINE)
                    cx, cy = xx+img_width/2, yy+img_width

            # ligne (nx : calcul coordonnée x de la prochaine station)
            if station_idx < self.n-1:
                nx += max_nbcorr*(img_width/2)
                self.draw_line(x, y, nx, y, color=self.color, stroke_width=linewidth)

            # cercle station
            if terminus:
                self.draw_circle(x, y, circlerad, color=WHITE, stroke_width=1)
                self.draw_circle(x, y, 3/5*circlerad, color=self.color)
            elif bool(corresp):
                self.draw_circle(x, y, circlerad, color=WHITE, stroke_width=1)
            else:
                self.draw_circle(x, y, circlerad, color=self.color)

        self.dwg.save()

        if open_image:
            navig = {'linux': 'xdg-open', 'win32': 'explorer', 'darwin': 'open'}
            subprocess.run([navig[sys.platform], self.path_out])


if __name__ == '__main__':
    MetroLineMap('M14', CouleursIDFM.VIOLET, data.M14_data).generate_map()
