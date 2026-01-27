#!/usr/bin/python3

# Usage: python3 cesar.py clef c/d phrase
# Returns the result without additional text
import string
#prends un texte en majuscule et une clef en argument et renvoie le chiffrement césar du texte ( x + clef mod 26 pour la nouvelle lettre)
def chiffrement_cesar (texte, clef):
    alphabet = string.ascii_uppercase
    texte_chiffr= ""
    for lettre in texte:
        if lettre in alphabet:
            i = alphabet.index(lettre)
            texte_chiffr += alphabet[(i + clef) % 26]
        else:
            texte_chiffr += lettre
    return texte_chiffr

#pour déchiffrer, on applique la méthode inverse :  x - clef mod 26
def dechiffrement_cesar(texte, clef):
    alphabet = string.ascii_uppercase
    texte_dechiffr= ""
    for lettre in texte:
        if lettre in alphabet:
            i = alphabet.index(lettre)
            texte_dechiffr += alphabet[(i - clef) % 26]
        else:
            texte_dechiffr += lettre
    return texte_dechiffr

        
print( chiffrement_cesar("AA", 2))
print( dechiffrement_cesar(chiffrement_cesar("AA", 2), 2))

 
