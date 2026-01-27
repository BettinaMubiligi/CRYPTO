# Sorbonne Université LU3IN024 2024-2025
# TME 5 : Cryptographie à base de courbes elliptiques
#
# Etudiant.e 1 : MUBILIGI BETTINA, 21101302

from math import sqrt
import matplotlib.pyplot as plt
from random import randint
from random import choice

# Fonctions utiles

def exp(a, N, p):
    """Renvoie a**N % p par exponentiation rapide."""
    def binaire(N):
        L = list()
        while (N > 0):
            L.append(N % 2)
            N = N // 2
        L.reverse()
        return L
    res = 1
    for Ni in binaire(N):
        res = (res * res) % p
        if (Ni == 1):
            res = (res * a) % p
    return res


def factor(n):
    """ Return the list of couples (p, a_p) where p is a prime divisor of n and
    a_p is the p-adic valuation of n. """
    def factor_gen(n):
        j = 2
        while n > 1:
            for i in range(j, int(sqrt(n)) + 1):
                if n % i == 0:
                    n //= i
                    j = i
                    yield i
                    break
            else:
                if n > 1:
                    yield n
                    break

    factors_with_multiplicity = list(factor_gen(n))
    factors_set = set(factors_with_multiplicity)

    return [(p, factors_with_multiplicity.count(p)) for p in factors_set]


def inv_mod(x, p):
    """Renvoie l'inverse de x modulo p."""
    return exp(x, p-2, p)


def racine_carree(a, p):
    """Renvoie une racine carrée de a mod p si p = 3 mod 4."""
    assert p % 4 == 3, "erreur: p != 3 mod 4"

    return exp(a, (p + 1) // 4, p)


# Fonctions demandées dans le TME

def est_elliptique(E):
    """
    Renvoie True si la courbe E est elliptique et False sinon.

    E : un triplet (p, a, b) représentant la courbe d'équation
    y^2 = x^3 + ax + b sur F_p, p > 3
    """

    p, a, b = E

    y2= 4*a**3+27*b**2
    y2_mod = y2 % p

    return y2_mod != 0


def point_sur_courbe(P, E):
    """Renvoie True si le point P appartient à la courbe E et False sinon."""
    p, a, b = E 
    
    if P == ():
        return True 
    else: 
        x, y = P
        #gestion des y négatifs sinon erreur, avce la réduction modulo p
        x = x % p
        y = y % p
        if x >= p or y >= p: #on veérifie l'intervalle pour x et y
            return False
        
        # Calcul de y² et x³ + ax + b modulo p
        y2 = (y**2) % p
        eq = (x**3 + a*x + b) % p 

        return eq == y2


def symbole_legendre(a, p):
    """Renvoie le symbole de Legendre de a mod p."""
    """ D'après la définition du symbole de Legendre (Wikipedia)
    Si p est un nombre premier et a un entier, 
     le symbole de Legendre ( a / p )  vaut :
        0 si a est divisible par p ;
        1 si a est un résidu quadratique modulo p (ce qui signifie qu'il existe un entier k tel que a ≡ k**2 mod p) mais n'est pas divisible par p ;
        −1 ou p -1 si a n'est pas un résidu quadratique modulo p.
        """
    #cas où a est divisible par p
    if (a % p ==0):
        return 0
    a =a % p
    r = exp(a, (p-1)//2, p)
    if (r == 1): 
        return 1
    if (r == p-1):
        return p-1 #ou -1, selons les tests effectués
    
    return None 


def cardinal(E):
        """Renvoie le cardinal du groupe de points de la courbe E."""
        """ Méthode vue en TD : calcul du discriminant (pour savoir 
        la courbe est bien élliptique), puis calcul des points en trouvant les 
        coordonnées x y à l'aide des collisions entre l'équation de la courbe E modulo p et 
        y2 mod p  """
    
        p, a, b = E
        if not est_elliptique(E):
            raise ValueError("La courbe n'est pas elliptique")
        count = 1  # on compte  le point à l'infini
        #on utilise le symbole de legendre pour connaitre le nb de solutions
        for x in range(p):
            z = (x**3 + a * x + b) % p
            s = symbole_legendre(z, p)
            if s == 1:
                count += 2  # si deux solutions y
            elif s == 0:
                count += 1  # une solution y = 0
        return count
    



def liste_points(E):
    """Renvoie la liste des points de la courbe elliptique E."""
    p, a, b = E

    assert p % 4 == 3, "erreur: p n'est pas congru à 3 mod 4."
     
    points = [()] #Liste non vide car on a mit le point à l'infini
    for x in range(p):
        z = (x**3 + a*x + b) % p #on calcule le polynome de la courbe E mod p
        s = symbole_legendre(z, p)
        
        if s == 1:  # 2 solutions y
            y = racine_carree(z, p)  # d'après l'énoncé, car y = z^((p+1)//4) mod p
            points.append((x, y))
            points.append((x, (-y) % p))
        elif s == 0:  # une seule solution y = 0
            points.append((x, 0))

    return points
    


def cardinaux_courbes(p):
    """
    Renvoie la distribution des cardinaux des courbes elliptiques définies sur F_p.

    Renvoie un dictionnaire D où D[i] contient le nombre de courbes elliptiques
    de cardinal i sur F_p.
    """
    """rappel du théorème de Hasse : Pour une courbe elliptique EE définie sur un corps fini FpFp, le nombre de points N sur E vérifie :
                | N -(p+1)| ≤ 2 * sqrt(p), donc N appartient à l'intervalle : p+1-2 *sqrt(p) <= N <= p+1+2 +sqrt(p).
                Ce théorème garantit que le nombre de points est proche de p+1, avec une erreur bornée par 2*sqrt(p)
                """
  

    #on calcule les bornes du théorème de Hasse pour initialiser le dictionnaire D avec les bornes
    borne_inf = int(p + 1 - 2 * sqrt(p))
    borne_sup = int(p + 1 + 2 *  sqrt(p))
    D = {i: 0 for i in range(borne_inf, borne_sup + 1)}
    
    for a in range(p):
        for b in range(p):
            E = (p, a, b)
            if est_elliptique(E): 
                N = cardinal(E)    # on calcule le cardinal avec la fonction existante
                D[N] += 1  # on incémente le compteur
                
    return D

def dessine_graphe(p):
    """Dessine le graphe de répartition des cardinaux des courbes elliptiques définies sur F_p."""
    bound = int(2 * sqrt(p))
    C = [c for c in range(p + 1 - bound, p + 1 + bound + 1)]
    D = cardinaux_courbes(p)

    plt.bar(C, [D[c] for c in C], color='b')
    plt.show()


def moins(P, p):
    """Retourne l'opposé du point P mod p."""
    #cas si le point est le point à l'infini car son opposé est lui même
    if P == () :
        return ()
    x, y = P
    #Je suppose ici que l'opposé de x, ydans F est x, -y
    return  (x % p, (-y) % p) 


def est_egal(P1, P2, p):
    """Teste l'égalité de deux points mod p."""
    #test égalité pour le point à l'infini
    if P1 == () or P2 == ():
        return P1 == P2
    
    #On utilise la réduction des coordonnéess pour traiter le cas des coordoonées négatives
    #Puis on les compare 
    x1, y1 = P1
    x2, y2 = P2
    x1_mod = x1 % p
    y1_mod = y1 % p
    x2_mod = x2 % p
    y2_mod = y2 % p
    if ((x1_mod == x2_mod) and (y1_mod == y2_mod)):
        return True
    return False

def est_zero(P):
    """Teste si un point est égal au point à l'infini."""
    return P == ()


def addition(P1, P2, E):
    """Renvoie P1 + P2 sur la courbe E."""
    #si l'un est le point infini, l'addition de P1 et P2 est égale à celui qui ne l'est pas
    if est_zero(P1): 
        return P2  
    if est_zero(P2):
        return P1
    
    p, a, b = E
    x1, y1 =P1
    x2, y2 = P2
    
    if est_egal(P1, moins(P2, p), p): 
        #si P1 et P2 son opposés, leur addition est le point infini
        return ()
    
    s= 0
    # on calcule la pente s
    # si P1 = P2 
    if est_egal(P1, P2, p): 
        if y1 == 0: 
            return ()
        s = (3 * x1**2 + a) * inv_mod(2 * y1, p) 
    else:  # si  P1 et P2 différents
        s = (y2 - y1) * inv_mod(x2 - x1, p)
    
    # Calcul de (x3, y3)
    x3 = (s**2 - x1 - x2) % p
    y3 = (s * (x1 - x3) - y1) % p
    return (x3, y3)


def multiplication_scalaire(k, P, E):
    """Renvoie la multiplication scalaire k*P sur la courbe E."""
    p, a, b = E

    if est_zero(P) or k == 0 :
        return ()
    
    #pour éviter les erreurs, cas où k négaif pour la multiplication --> appel de -k à la place ?
    if k < 0 :
        return multiplication_scalaire(-k, moins(P, p), E)
    
    A = () #variable de stockage du point, qui commence à l'infini
    P_courant= P
    #o utlise un décalage (division par 2) sur les k pour ne pas effecter k -1 additions de P
    while k > 0 : 
        if k % 2 == 1 :
            A = addition(A, P_courant, E)
        P_courant = addition(P_courant, P_courant, E)
        k = k //2
    return A


def ordre(N, factors_N, P, E):
    """Renvoie l'ordre du point P dans les points de la courbe E mod p. 
    N est le nombre de points de E sur Fp.
    factors_N est la factorisation de N en produit de facteurs premiers."""
    #D'après le cours, : L'ordre de PP est le plus petit diviseur d de N tel que -
    #le produit scalaire de d et P est égal au point infini
    ordre = N #on suppose que son ordre max est N
    for i, j in factors_N:
        while (j > 0) and (ordre % i ==0) :
            ordre_tmp = ordre //i
            #comme indiqué dans le cours, on vérifie si l'odre * P est égal au point infini
            if est_zero(multiplication_scalaire(ordre_tmp, P, E)):
                ordre = ordre_tmp
                j = j - 1
            else :
                break
    return ordre


def point_aleatoire_naif(E):
    """Renvoie un point aléatoire (différent du point à l'infini) sur la courbe E."""
    p, a, b = E
    while True : #boucle infinie 
        x= randint(0, p-1)
        y=randint(0,p-1)
        #onutilise la fonction point sur courbe précédente pour vérifier
        P = (x, y)
        if (point_sur_courbe((x,y), E) and not est_zero(P)):
            return (x, y)
     
"""Note : Quand on teste la fonction  point_aleatoire_naif avec la courbe
 E =(360040014289779780338359,117235701958358085919867,18575864837248358617992) 
 le temps d'éxécution est trop long, et  la compléxité de l'algo est en O(p)."""


def point_aleatoire(E):
    """Renvoie un point aléatoire (différent du point à l'infini) sur la courbe E."""
    """Au lieu de générer x et y alétoirement, on génère uniquement x, et
    on calcule le polynome de la courbe modulo p (cf.cours , x**3+a*x+b mod p), 
    et on utilise le symbole de legendre pour connaître le nombre de points 
     sur la courbe et la valeur de y  """
    p, a, b = E
    while True:
        x = randint(0, p - 1)
        z = (x**3 + a * x + b) % p
        s = symbole_legendre(z, p)
        if s == 1:
            y = racine_carree(z, p)
            return (x, y) if choice([True, False]) else (x, (-y) % p)
        elif s == 0:
            return (x, 0)


def point_ordre(E, N, factors_N, n):
    """Renvoie un point aléatoire d'ordre N sur la courbe E.
    Ne vérifie pas que n divise N."""
    p,a, b = E

    #on génère un point aléatoire sur E et un ordre avec les fonctions
    while True:
        P = point_aleatoire(E) 
        ordre_P = ordre(N, factors_N, P, E) 
        #on vérifie si l'odre est divisible par n
        if ordre_P % n == 0:
                Point_n = multiplication_scalaire(ordre_P // n, P, E)
                return Point_n
    


def keygen_DH(P, E, n):
    """Génère une clé publique et une clé privée pour un échange Diffie-Hellman.
    P est un point d'ordre n sur la courbe E.
    """
    #créer la clé secrète
    sec =  randint(1, n)
    #on créer aussi la clé publique avec la multiplication scalaire avec la clé secrète
    #méthode selon Diffie-Helman 
    pub =  multiplication_scalaire(sec, P, E)
    return (sec, pub)
    
    return (sec, pub)

def echange_DH(sec_A, pub_B, E):
    """Renvoie la clé commune à l'issue d'un échange Diffie-Hellman.
    sec_A est l'entier secret d'Alice et pub_b est l'entier public de Bob."""
    cle = multiplication_scalaire(sec_A, pub_B, E) 
    return cle

"""Q.15*****
D'après le théorème, pour trouver un bon point P il faut qu'il est un ordre élévé pour que les clés
soient plus difficiles à trouver, donc plus sécurisées.
L'odre va etre un grand nombre premier q, et on va utiliser la fonction 
 point_ordre(E, N, factors_N, q) pour trouver un pint P d'odre q. Comme dans le test 9,
on va vérifier que le point P n'est pas le point à l'infini, et que q*P (multiplication scalaire)
est lui le point à l'infini, avec assert not est_zero(P)
assert est_zero(multiplication_scalaire(q, P, E))
assert ordre(P, E, N, factor_N) ==  q

"""