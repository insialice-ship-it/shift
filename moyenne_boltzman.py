#Paramètres
R = 8.314e-3 # Constante en kJ/mol/K
T = 298.15    # Température en Kelvin

#Energie des conformères en kJ/mol
try:
    E1_raw = float(input(f"Énergie du conformère 1 (E1) [{UNITE_ENERGIE}] : "))
    E2_raw = float(input(f"Énergie du conformère 2 (E2) [{UNITE_ENERGIE}] : "))
except ValueError:
    print("Erreur : veuillez entrer des valeurs numériques.")
    sys.exit(1)

#lire les tableaux
def lire_fichier_donnees(nom_fichier):
    donnees_nettoyees = []
    
    try:
        with open(nom_fichier, 'r', encoding='utf-8') as fichier:
            for ligne in fichier:
                # 1. On retire les espaces inutiles au début et à la fin (strip)
                ligne = ligne.strip()
                
                # 2. On ignore les lignes vides ou celles qui commencent par '#'
                if not ligne or ligne.startswith('#'):
                    continue
                
                # 3. .split() sans argument gère "un ou plusieurs" espaces
                valeurs = [float(i) for i in ligne.split()]
                donnees_nettoyees.append(valeurs)

        return donnees_nettoyees

    except FileNotFoundError:
        print(f"Erreur : Le fichier '{nom_fichier}' est introuvable.")
        return []
        
t1 = lire_fichier_donnees(nom_fichier1)
t2 = lire_fichier_donnees(nom_fichier2)

#calcul des poids de Boltzmann
E-min = min(E1,E2)
w1_brut = np.exp(-(E1 - E_min) / (kb * T))
w2_brut = np.exp(-(E2 - E_min) / (kb * T))

#Normalisation
w1 = w1_brut / (w1_brut+w2_brut)
w2 = w2_brut / (w1_brut+w2_brut)

print(f"  Conformère 1 : w1 = {w1:.4f}")
print(f"  Conformère 2 : w2 = {w2:.4f}")

#poids
t1_weighted = tableau1.copy()
t1_weighted[:, 1] = tableau1[:, 1] * w1

t2_weighted = tableau2.copy()
t2_weighted[:, 1] = tableau2[:, 1] * w2

# Combiner les deux tableaux (toutes les barres)
tableau_combined = np.vstack([t1_weighted, t2_weighted])

# Trier par longueur d'onde croissante
tableau_combined = tableau_combined[tableau_combined[:, 0].argsort()]

#Sauvegarde fichier texte
output_file = "ecd_boltzmann_combined.txt"
with open(output_file, "w") as f:
    for row in tableau_combined:
        wl = row[0]
        intensity = row[1]
        f.write(f"{wl:.4f}  {intensity:.8f}\n")

print(f"\n✓ Tableau sauvegardé dans : {output_file}")







