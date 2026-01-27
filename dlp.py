# TME3 -- BETTINA MUBILIGI, G2, 21101302

from prime import is_probable_prime
from prime import random_probable_prime

from math import sqrt
import random


#Exercice 1
#Q1
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


def invertibles(N):
    inv = set()
    if(N<1): #si N est négatif alors pas d'inverse modulaire de l'anneau Z/NZ
        return set()
    
    for i in range (1, N):
        pgcd, u,v = bezout(i, N)
        if(pgcd == 1): 
            inv.add(i)
    return inv


#Q3
def phi(N): #les nombres premiers entre eux ont leurs pgcd égal à 1
    s=invertibles(N) #on utilise la liste des inverses modulaires calculée précédemment
    return len(s)


#Exercice 2
#Q1
def exp(a, n, p):
        r =1
        a = a %p
        binaire = bin(n)[2:] #conversion en binaire de n (sans le 0b)

        for bit in binaire :
            r = r**2 % p
            if bit == '1':
                r = r*a % p
        print(r)
        return r 


#Q2
def factor(n):
    facteurs = []
    d = 2  
    cpt=0
    #on vérifie si 2 ets un facteur de n
    while ( n % d) == 0:  
        cpt += 1
        n //= d
    if cpt > 0:  
        facteurs.append((d, cpt))
    
    d = 3  # on passe aux nombres impairs
    while (d * d <= n):  # vérification jusqu'à √n
        cpt = 0
        while (n % d == 0):
            cpt += 1
            n //= d
        if cpt > 0:
            facteurs.append((d, cpt))
        d += 2  # on passe au nombre impair suivant
  # Si après la boucle n > 1, c'est que n est un facteur premier
    if n > 1:
        facteurs.append((n, 1))
   

    print(facteurs)
    return facteurs


#Q3
def order(g, p, factors_p_minus1):
    ord = p - 1 #on part de l'ordre max
    for i,j in factors_p_minus1:
        while ord % i== 0:
            if pow(g, ord // i, p) == 1: #on utulise la définition de l'odre
                ord //= i #on réduit l'odre d'un facteur i
            else:
                break #si la condition échoue, sortie du while
    return ord #on retourne l'odre minimal



#Q4
def find_generator(p, factors_p_minus1):
     #on teste tous les entiers de 2 à p-1
     for g in range(2, p): 
        #on vérifie si c'est l'odre maximal
        if order(g, p, factors_p_minus1) == p - 1:  
            return g
        return None 

#Q5
def generate_safe_prime(k):
    while True:
        """ on génère un entier premier probable avec random et on calcule p """
        q = random_probable_prime(k - 1)
        p = 2 * q + 1
        
        # on vérifie si p est aussi un probable premier
        if is_probable_prime(p):
            return p

#Q6
def bsgs(n, g, p):
    return
"""Remarque : je n'ai pas compris comment implémenter la méthode 
Baby Steps Giant Steps vu en TD et en cours"""