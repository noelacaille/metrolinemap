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

if __name__ == '__main__':
    import metrolinemap
    dir(metrolinemap)
