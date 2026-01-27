# Sorbonne Université 3I024 2024-2025
# TME 2 : Cryptanalyse du chiffre de Vigenere
#
# Etudiant.e 1 : MUBILIGI BETTINA 21101302
# Etudiant.e 2 : ---

import sys, getopt, string, math,string

# Alphabet français
alphabet = string.ascii_uppercase

# Fréquence moyenne des lettres en français
# À modifier
freq_FR = [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

# Chiffrement César
def chiffre_cesar(texte, clef):
    """

    Fonction qui prend une chaîne de caractères et effectue un décalage de chaque
 lettres de n positions dans l’alphabet. Utilisation de la formule du chiffrement de 
 César (alphabet[(indice de la lettre dans l'alphabet + clef) modulo 26]).
 Arguments : texte : chaine de caractères et clef : entier
 Retour : texte chiffré selon César

    """

    texte_chiffr= ""
    for lettre in texte:
        if lettre in alphabet:
            i = alphabet.index(lettre)
            texte_chiffr += alphabet[(i + clef) % 26]
        else:
            texte_chiffr += lettre
    return texte_chiffr


# Déchiffrement César
def dechiffre_cesar(texte, clef):
    """
    Déchifrement selon César (formule inverse du chiffrement).
    Arguments : texte chiffré : chaine de caractères et clef : entier
    Retour : texte déchiffré
    """
    texte_dechiffr= ""
    for lettre in texte:
        if lettre in alphabet:
            i = alphabet.index(lettre)
            texte_dechiffr += alphabet[(i - clef) % 26]
        else:
            texte_dechiffr += lettre
    return texte_dechiffr


# Chiffrement Vigenere
def chiffre_vigenere(txt, key):
    """
    Fonction de chiffrement selon Vigenère (formule de vigenère).
    Arguments : texte à chiffrer : chaine de caractères et key: liste d'entiers avec les décalages 
    de chaque lettres du texte (clé répétée si elle est plus courte que le texte)
    Retour : text.e chiffré
    """
    texte_chiffr = ""
    for i in range(len(txt)):
        j = i % len(key)  #pour contrôler les erreurs en cas de clé trop petites
        texte_chiffr += alphabet[(alphabet.index(txt[i]) + key[j]) % 26]
    return texte_chiffr

#Dechiffrement Vigenere
def dechiffre_vigenere(txt, key):
        """
        Déchifrement selon Vigenére (formule inverse du chiffrement).
    Arguments : texte chiffré : chaine de caractères et clef : liste d'entiers
    Retour : texte déchiffré
        """
        texte_dechiffr = ""
        for i in range(len(txt)):
            j = i % len(key) 
            texte_dechiffr += alphabet[(alphabet.index(txt[i]) - key[j]) % 26]
        return texte_dechiffr



# Analyse de fréquences

def freq(txt):
    """
    Fonction qui prends un texte en argument et renvoie un tableau hist avec la
    liste des fréquences dans le texte pour chaque lettre de l'alphabet.
    Arguments : texte (chaine de caractères)
    Retour : tableau de flottants hist de taille 26 avec la fréquence de chaque lettre de l'alphabet
    """
    i =0
    hist=[0.0]*len(alphabet)
    for i in alphabet :
        hist[alphabet.index(i)] = txt.count(i)

    return hist

# Renvoie l'indice dans l'alphabet
# de la lettre la plus fréquente d'un texte
def lettre_freq_max(txt):
    """
    Fonction étant donné une chaîne de caractères,renvoie la position dans l’alphabet 
    de la lettre qui apparaît le plus grand nombre de fois dans le texte. Si plusieurs lettres
 apparaissent autant de fois, on renverra celle qui apparaît la première dans l’ordre alphabétique.
 Arguments : texte (chaine de caractères)
 Retour : a, entier (position dans l'alphabet de la lettre,la plus fréquente)
    """
    hist=freq(txt)
    freq_max= max(hist)
    a = 25
    for i in range (0,len(hist)):
        if hist[i] == freq_max and i < a :
            a=i
    return a

# indice de coïncidence
def indice_coincidence(hist):
    """
    Fonction qui prend en entrée un tableau qui correspond aux
     occurences des lettres d’un texte (typiquement la sortie de la fonction freq) 
    et renvoie l’indice de coïncidence.
    Argulent : tableau de fréquences des lettres de l'alphabet francais dans le texte (tableau de float)
    Retour : indice de coincidence du texte (float) 
    """
    nb_lettres=sum(hist)
    i_co=0
    if nb_lettres <= 1:
        return 0 
    #on applique la formule de l'indice de coincidence d'un texte grâce au tableau hist des occurences
    for j in range(0,len(hist)):
         if hist[j] != 0 :
             i_co+=( hist[j]*(hist[j] - 1))/(nb_lettres*(nb_lettres-1))
    return i_co

# Recherche la longueur de la clé
def longueur_clef(cipher): 
    """
    Fonction qui prends un texte en entrée et teste toutes les tailles de clef possibles (on suppose que la clef cherchée est
 au plus de longueur 20). On découpe le texte en colonnes et on calcule la moyenne de l’indice de coïncidence de chaque
 colonne. Si la moyenne est > 0.06, c’est qu’on a trouvé la bonne taille de clef que l'on renvoie.
    """
    taille_mot_max = 20
    
    for l in range(1, taille_mot_max + 1):  # on inclut le 20
        colonnes = [''] * l #on crée autant de colonnes que la longueur de la clé
        
        #on répartit les lettres dans chaque colonne à l'aide de enumerate (pour découper chqaue mot du texte en mot de taille maximum l)
        for i, lettre in enumerate(cipher):
            colonnes[i % l] += lettre
        
        # on calcule la moyenne de l'indice de coincidence pour cette clé
        ic_total = 0
        for colonne in colonnes:
            hist = freq(colonne)
            ic_total += indice_coincidence(hist)
        
        ic_moyen = ic_total / l
        
        if ic_moyen > 0.06:
            return l
    
    return 0
    
# Renvoie le tableau des décalages probables étant
# donné la longueur de la clé
# en utilisant la lettre la plus fréquente
# de chaque colonne
def clef_par_decalages(cipher, key_length):
    """
    Fonction qui i prend un texte et la taille de la clé et renvoie la clé sous forme d’une table de
 décalages. La stratégie consiste à raisonner indépendement par colonne.
 Pour chaque colonne on suppose que la lettre qui apparaît le plus correspond au chiffré de la lettre E. On en déduit le
 décalage qu’a subi chaque colonne. Cela correspond bien à la clef utilisée pour chiffrer avec le chiffre de Vigenère.
    """
    decalages=[]*key_length
    colonnes = [''] * key_length
    #même méthode de création de colonne
    for i, lettre in enumerate(cipher):
        colonnes[i % key_length] += lettre  

    #on transforme chaque colonne en texte et on trouve la lettre la plus frequente
    for colonne in colonnes:
        lettre_plus_freq =lettre_freq_max(str(colonne))
         # 4 correspond à 'E' : on retrouve le décalage de la colonne grâce à la lettre E
        decalage = (lettre_plus_freq - 4) % 26 
        decalages.append(decalage)
    return decalages

# Cryptanalyse V1 avec décalages par frequence max
def cryptanalyse_v1(cipher):
    """
    Fonction de cryptanalyse selon Vigenère :  On déduit la longueur de la clef
 avec l’indice de coïncidence, puis on récupère la clef en observant le décalage de chaque colonne. Enfin, 
 on utilise la fonction de déchiffrement de Vigenère sur le texte avec le tableau de décalages comme clé.
    """
    longueur_cle = longueur_clef(cipher)
    decalages = clef_par_decalages(cipher, longueur_cle)
    texte_dechiffre = dechiffre_vigenere(cipher, decalages)
    
    return texte_dechiffre
""" **ANALYSE des résultats** : 18 textes sur 100 sont déchiffrés avec succès. On remarque 
que ce sont les textes avec des clés souvent plus courtes (de taille inférieure à 6). Cela pourrais 
s'expliquer par la méthode utilisée : avec Vigenère, comme chaque colonne est chiffrée avec des clés différentes, 
plus il y a de valeurs dans la clé plus il y a aura de colonnes avec des chiffrements différents, et donc moins la
clé se répètera, ce qui rend le déchiffrement d'autant plus complexe.
"""
################################################################


### Les fonctions suivantes sont utiles uniquement
### pour la cryptanalyse V2.

# Indice de coincidence mutuelle avec décalage
def indice_coincidence_mutuelle(h1,h2,d):
    """
    Fonction qui prend en entrée deux tableaux
 qui correspond aux fréquences des lettres de deux textes (typiquement la sortie de la fonction freq) ainsi qu’un entier d
 et renvoie l’indice de coïncidence du texte 1 et du texte 2 qui aurait été décalé de d positions (comme par un chiffrement
 de César).
    """
    nb_lettres_1=sum(h1)
    nb_lettres_2=sum(h2)

    i_com=0
    if nb_lettres_1 <=1 or nb_lettres_2 <=1 :
        return 0 
    
    #on applique la formule de l'indice de coincidence mutuelle sur les deux textes
    for j in range(0,len(h1)):
            #on applique le décalage d sur chaques indices de h2 comme pour le chiffrement césar(modulo)
            i = (j +d) % len(h2) #contrairement à césar, on ne chiffre-/décale pas avec l'alphabet mais directement avec h1
            if h1[j] != 0 :
                i_com+=( h1[j]*(h2[i]))/(nb_lettres_1*(nb_lettres_2))
    return i_com


# Renvoie le tableau des décalages probables étant
# donné la longueur de la clé
# en comparant l'indice de décalage mutuel par rapport
# à la première colonne
def tableau_decalages_ICM(cipher, key_length):
    """
     Fonction qui prend un texte et une
 longueur de clef supposée, et calcule pour chaque colonne son décalage par rapport à la première colonne. La sortie est
 un tableau d’entiers, dont la première valeur est toujours 0 (puisque la première colonne a un décalage nul par rapport à
 elle-même).
 Stratégie : Pour chaque colonne on calcule l’ICM de la première
 colonne et de cette colonne qu’on aurait décalée de d positions. Le d qui maximise l’ICM correspond au décalage relatif
 par rapport à la première colonne du texte.
    """
    decalages=[]
    colonnes = [''] * key_length
    #même méthode de création de colonne
    for i, lettre in enumerate(cipher):
        colonnes[i % key_length] += lettre  

    #on récupère les fréquences de la première colonne (et la première valeur de decalages est 0)
    h1=freq(str(colonnes[0]))
    decalages.append(0) #pas de décalage entre la 1ere colonne et elle-mêmee
    for j in range (1, len(colonnes)):
        h2=freq(str(colonnes[j])) #on calcule la fréquence de chaque autre colonne pour calculer l'ICM
        dec_max=0 #on définit une variable de décalage max qu'o rajoutera au tableau décalages
        max_icom=0 #maximum d'indice de coincidence mutuelle
        for i in range (0, len(h2)):
            icom=indice_coincidence_mutuelle(h1,h2,i )
            if (icom>max_icom):
                dec_max=i
                max_icom = icom
        decalages.append(dec_max)
    return decalages
# Cryptanalyse V2 avec décalages par ICM
def cryptanalyse_v2(cipher):
    """
    Fonction de cryptanalise avec césar. On déduit la longueur de
 la clef avec l’indice de coïncidence, puis on calcule les décalages relatifs de chaque colonne par rapport à la première
 colonne en utilisant l’ICM. On décale chaque colonne pour l’aligner avec la première colonne. Le texte obtenu est alors
 l’équivalent d’un texte chiffré avec César. On le déchiffre donc comme un texte chiffré avec César, en identifiant la lettre
 la plus fréquente.
 Argument : cipher (chaine de caractères)
 Retour : cipher déchiffré (chaine de caractères)
    """
    #calcul de la longueur de la clé
    clef = longueur_clef(cipher)
    #tableau des décalages relatifs avec la 1ere colonne (avec indice de coincidence mutuelle)
    decalages_ICM = tableau_decalages_ICM(cipher, clef)
    cipher_chiffr=""

    """On calcule le décalage de chaque lettre grace au tableau des décalages de chaque colonne 
    par rapport à la première et on fabrique le texte chiffré lettre par lettre avec les 
      décalages :  il correspond à un texte déchiffré par la méthode César.
        
    """
    for i, lettre in enumerate(cipher):
        dec_lettre=decalages_ICM[i%clef] 
        #note : j'utilise la fonction dechiffre_cesar essentiellement pour 
        #appliquer un décalage négatif sur la lettre (de la forme lettre - decalage % 26)
        #et décaler chaque ligne de chaque colonne pour les aligner à la première colonne
        cipher_chiffr+=dechiffre_cesar(lettre, dec_lettre)

    #on récupère la lettre la plus fréquente du texte partiellement déchiffré en césar
    lettre_freq=lettre_freq_max(cipher_chiffr)
    #comme dans la fonction clef_par_decalages, on retrouve le décalage du texte
    #  grâce à la lettre E et à la lettre la plus fréquente
    decalage_cesar = (lettre_freq - 4) % 26 
    #on déchiffre finalement le texte comme en césar une deuxième fois avec comme clé le décalage par rapport à E
    texte_dechiffre = dechiffre_cesar(cipher_chiffr, decalage_cesar)
    
    return texte_dechiffre
""" **ANALYSE des résultats** : 43/100 textes déchiffrés, soit presque la moitié, ce qui est beaucoup mieux que la premère cryptanalyse.
Cela est en partie grâce méthode de regarder le décalage des colonnes par rapport à la première colonne, avec l'indice de 
coincidence mutuelle. On ne cherche plus seulement à déchiffrer le texte avec les fréquences (indice de coincidence) mais également avec le 
le décalage avec la 1ere colonne. Cela résout en partie notre problème de clé et permet de mieux déchiffrer
les textes plus courts, malgré la taille de la clé. """
################################################################


### Les fonctions suivantes sont utiles uniquement
### pour la cryptanalyse V3.

# Prend deux listes de même taille et
# calcule la correlation lineaire de Pearson
def correlation(L1,L2):
    """
    Arguments : deux listes de même longueur, correspondant à deux
    variables aléatoires ( listes de int )
   et Retour :  renvoie la valeur de la corrélation entre les deux (int)
    """
    correlation=0
    
    sd1=0
    sd2=0
    numerateur=0
    #calcul des espérances de L1 et L2
    n = len(L1)
    esperance_L1 = sum(L1) / n
    esperance_L2 = sum(L2) / n
    #calcul du numérateur de la valeur de corrélation
    for k in range(n):
        numerateur+=( L1[k] - esperance_L1)*( L2[k]- esperance_L2)
    #de même pour le dénominateur avec math.sqrt et les valeurs précédentes
    sd1 = math.sqrt(sum((x - esperance_L1) ** 2 for x in L1))
    sd2 = math.sqrt(sum((x - esperance_L2) ** 2 for x in L2))
    
    #on controle les erreurs de division par 0
    if (sd1 ==0 or sd2 ==0):
        return 0
    correlation = numerateur/(sd1*sd2)
    #on arrondit à 10 décimales sinon le résultat est incorrect (0.999999 au lieu de 1.0 par exemple)
    return round(correlation, 10)

# Renvoie la meilleur clé possible par correlation
# étant donné une longueur de clé fixée
""" REMARQUE: fonction ne marche pas malgré les essais multiples de debuggage
Je pense que l'erreur réside quelque part dans le calcul de décalage mais je n'ai pas réussit
 à trouver la bonne formule """
def clef_correlations(cipher, key_length):
    """
    Etant donné un texte chiffré et une taille de clef, calcule
 pour chaque colonne le décalage qui maximise la corrélation avec un texte français. Vous pourrez utiliser le tableau des
 fréquences d’un texte français freq_FR défini à la question 1 comme référence. La fonction doit renvoyer un tuple
 composé de deux éléments : la moyenne sur les colonnes des corrélations maximales obtenues et un tableau contenant
 pour chaque colonne le décalage qui maximise la corrélation.
    Arguments : cipher (chaine de caractères)
    Retour: clef (entier)
    """
    key = [] * key_length
    score = [] * key_length
    colonnes = [""] * key_length
    
    # même méthode pour la création des colonnes
    for i, lettre in enumerate(cipher):
        colonnes[i % key_length] += lettre  


    for j in range(key_length): 
        #con calcule les fréquence pour chaque colonne 
        hist = freq(colonnes[j])
        co_max = -1
        dec_max = 0
        for d in range(len(hist)): 
            #on trouve la valeur maximale de corrélation  entre hist le tableau des frequences
            #françaises, et on récupère la valeur de décalage maximale du décalage
            #correspondante
            co = correlation([hist[(i - d) % 26] for i in range(len(hist))], freq_FR)
            if co > co_max:
                co_max = co
                dec_max = d
        
        score.append(co_max)
        key.append(dec_max)

    score_moyen = sum(score) / key_length
    #print pour débugger la fonction
    print(score_moyen)
    print(key)
    return (score_moyen, key)

# Cryptanalyse V3 avec correlations
#REMARQUE/ fonction ne peux pas être testée car clef_correlations ne marche pas
def cryptanalyse_v3(cipher):
    """
    Fonction qui effectue  une troisième forme de cryptanalyse. On test pour chaque taille de
 clef (ici on suppose la clef de taille ≤ 20), on calcule les décalages qui maximisent la corrélation de Pearson à l’aide de la
 fonction clef_correlations. On suppose que la bonne taille de clef est celle qui maximise la moyenne de corrélations sur les colonnes. Il reste alors à appliquer le déchiffrement de Vigenère avec la fonction dechiffre_vigenere
 pour récupérer le texte clair. 
 Argument : cipher (chaine de caractère)
 Retour : texte clair (chaine de caractère)
    """

    taille_clef_max= 20
    max_score=0
    key_max_score=[]
    """ On test les score (moyenne de valeur de corrélation) pour chaque taille de clé
    on récupère la moyenne max et le tableau de décalages associé qui nous servira de clé
    pour le déchiffrement de vigenère. """
    for i in range(0, taille_clef_max):
        score, key =clef_correlations(cipher, i)
        if score > max_score:
            max_score = score
            key_max_score=key
    return dechiffre_vigenere(cipher, key_max_score)

""" **ANALYSE des résultats*** Etant donné que la fonction clef_correlation n'a pas marché, 
je n'ai pas de manière exacte de connaître le nombre de textes déchiffrés, mais en faisant l'hypothèse
qu'elle ait fonctionné, je peux conjecturer que la méthode de la valeurd de corrélation appliquée
à chaque colonne du texte avec les fréquences de la langue française devrait donner un résultat plus élevé
que les cryptanalyses précédentes, de l'ordre des 90 à 95 % des textes. En effet, 
l'utilisation de la valeur de corrélation de Pearson est plus efficace que les méthodes précedentes
car elle permet de trouver une clé plus probable,celle qui maximise la corrélation
 entre les colonnes et le modèle (ici, les fréquences en langue française)"""
################################################################
# NE PAS MODIFIER LES FONCTIONS SUIVANTES
# ELLES SONT UTILES POUR LES TEST D'EVALUATION
################################################################


# Lit un fichier et renvoie la chaine de caracteres
def read(fichier):
    f=open(fichier,"r")
    txt=(f.readlines())[0].rstrip('\n')
    f.close()
    return txt

# Execute la fonction cryptanalyse_vN où N est la version
def cryptanalyse(fichier, version):
    cipher = read(fichier)
    if version == 1:
        return cryptanalyse_v1(cipher)
    elif version == 2:
        return cryptanalyse_v2(cipher)
    elif version == 3:
        return cryptanalyse_v3(cipher)

def usage():
    print ("Usage: python3 cryptanalyse_vigenere.py -v <1,2,3> -f <FichierACryptanalyser>", file=sys.stderr)
    sys.exit(1)

def main(argv):
    size = -1
    version = 0
    fichier = ''
    try:
        opts, args = getopt.getopt(argv,"hv:f:")
    except getopt.GetoptError:
        usage()
    for opt, arg in opts:
        if opt == '-h':
            usage()
        elif opt in ("-v"):
            version = int(arg)
        elif opt in ("-f"):
            fichier = arg
    if fichier=='':
        usage()
    if not(version==1 or version==2 or version==3):
        usage()

    print("Cryptanalyse version "+str(version)+" du fichier "+fichier+" :")
    print(cryptanalyse(fichier, version))
    
if __name__ == "__main__":
   main(sys.argv[1:])
