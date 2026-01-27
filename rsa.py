
# TME4 ----  BETTINA MUBILIGI, Crypto G2, 21101302

from math import isqrt
 # --------Utilisations de fonctions implémentées au tme3 : Arithmétique et DLP
def bezout(a, b):
    u0 =1
    v1= 1
    u1= 0
    v0 = 0
    while (b != 0):
        q = a //b
        r = a % b
        a= b
        b= r
        u2 = u0 -q *u1
        v2 = v0-q*v1
        u0=u1
        u1= u2
        v0=v1
        v1= v2
    return (a, u0, v0)


#Q2
def inv_mod(a, n):
    if(n<= 0 or n ==1):
        return None
    a_mod = a % n #cas a négatif

    if(a_mod == 0):
        return None #(car pgcd(a, n) = n != 1)
    pgcd, u, v = bezout(a,n)

    if(pgcd != 1):
        return None
    
    return u % n #pour gérer le cas où u est négatif
#------------------------------------------------------------


def rsa_chiffrement (x,N,e):
    #je ne savais pas à quoi correspondait N, donc j'ai supposé que c'est le module n

    if (x>N): #on vérifie que le module est supérieur à x
        return None

    chiffre= pow(x,e, N ) # on fait x puissance e mod N pour chiffrer x
    return chiffre

def rsa_dechiffrement (y,p,q,d):
    return pow(y, d, p*q) #p*d = N d'après le cours donc on fait y puissance d mod p*q pour déchiffrer y

# Retourne s tel que s % n1 == a1 et s % n2 == a2
def crt2 (a1,a2,n1,n2):
    #on calcule grand N
    N= n1*n2 
    #on trouve les inverses modulaires de n1 et n2 l'un par rapport à l'autre
    inv_n1 = inv_mod(n1,n2)
    inv_n2 = inv_mod(n2,n1)
    #on calcule la solution 
    s = a1 * n2 *inv_n2 + a2 * n1 *inv_n1
    return ((s % N), N)

def rsa_dechiffrement_crt (y,p,q,up,uq,dp,dq,N):
    #Pas de jeux de test ? je ne sais pas si ma foncion fonctionne 
    #on calcul les modulos des puissances de y
    p_mod = y **dp % p
    q_mod = y**dq % q
    #on utilise les modulos pour appliquer le crt : on suppose que N = p*q ici
    s= (q_mod + q *((p_mod - q_mod) * uq % p)) % N
    return s 



#### Wiener
def cfrac(a,b):
    #on utilise l'algortihme d'euclide 
    #on vérifie s'ils sont premiers entre eux
    pgcd, u0, v0 = bezout(a,b)
    if (pgcd != 1):
        return None 
    r0 = a
    r1 = b
    T = []

    while (r1 != 0):
        q = r0//r1
        T.append(q)
        r2 = r0 % r1
        r0 =r1
        r1 = r2
        if(r1 == 0):
            return T
    
##je n'ai pas compris à quoi correspond cette fonction
def reduite(L):
    return


def Wiener(m, c, N, e):
    #problème du cours : N, e, c qui nous servent à trouver d 
    #on calcule la franction continue de e et N
    T = cfrac(e, N)

    if T is None:
        return None
    #on calcule les convergents : algo trouvé sur wikipedia
    p_2 = 0
    p_1 = 1
    q_2 = 1
    q_1 = 0
    conv = []
    for i in T:
        pi = i * p_1 + p_2
        qi = i * q_1 + q_2
        conv.append((pi, qi))
        p_2 = p_1
        p_1 = pi
        q_2 = q_1
        q_1 = qi

    for k, d in conv:
        if d % 2 == 0 or k == 0:
            continue

        if (e * d - 1) % k == 0:
            phi = (e * d - 1) // k
             #résolution de l'équation pour trouver p et q 
            B = N - phi + 1
            delta = B * B - 4 * N
            if delta >= 0:
                delta_sqrt = isqrt(delta)  # pour vérifier si delta est un carré parfait (sinon erreur)
                if delta_sqrt * delta_sqrt == delta:
                    p1 = (B + delta_sqrt) // 2
                    p2 = (B - delta_sqrt) // 2

                    if p1 * p2 == N: #verification si p1 et p2 permettent de factoriser N
                        if pow(c, d, N) == m:
                            return d

    return None 



### Generation de premiers
import random
def is_probable_prime(N, nbases=20):
    """
    True if N is a strong pseudoprime for nbases random bases b < N.
    Uses the Miller--Rabin primality test.
    """

    def miller(a, n):
        """
        Returns True if a proves that n is composite, False if n is probably prime in base n
        """

        def decompose(i, k=0):
            """
            decompose(n) returns (s,d) st. n = 2**s * d, d odd
            """
            if i % 2 == 0:
                return decompose(i // 2, k + 1)
            else:
                return (k, i)

        (s, d) = decompose(n - 1)
        x = pow(a, d, n)
        if (x == 1) or (x == n - 1):
            return False
        while s > 1:
            x = pow(x, 2, n)
            if x == n - 1:
                return False
            s -= 1
        return True

    if N == 2:
        return True
    for i in range(nbases):
        import random
        a = random.randint(2, N - 1)
        if miller(a, N):
            return False
    return True


def random_probable_prime(bits):
    """
    Returns a probable prime number with the given number of bits.
    Remarque : on est sur qu'un premier existe par le postulat de Bertrand
    """
    n = 1 << bits
    import random
    p = random.randint(n, 2 * n - 1)
    while (not (is_probable_prime(p))):
        p = random.randint(n, 2 * n - 1)
    return p
