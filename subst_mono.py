#!/usr/bin/python3

# Usage: python3 subst_mono.py clef c/d phrase
# Returns the result without additional text
#Chiffrement mono-alpahétique qui utilise une clé qui définit le nombre de décalages max
import string
def subst_mono(texte, clef):
    alphabet = string.ascii_uppercase
    texte_chiffr = ""
    for j in range(len(texte)):
        lettre = texte[j]
        if lettre in alphabet:
            i = alphabet.index(lettre)
            decalage = int(clef[j % len(clef)]) 
            texte_chiffr += alphabet[(i + decalage) % 26]
        else:
            texte_chiffr += lettre 

    return texte_chiffr
def dechiff_mono(texte, clef):
    alphabet = string.ascii_uppercase
    texte_chiffr = ""
    for j in range(len(texte)):
        lettre = texte[j]
        if lettre in alphabet:
            i = alphabet.index(lettre)
            decalage = int(clef[j % len(clef)]) #pour boucler sur la clef (revient au début de la clef)
            texte_chiffr += alphabet[(i - decalage) % 26]
        else:
            texte_chiffr += lettre 

    return texte_chiffr


print( subst_mono("BBB", '123'))
print(dechiff_mono(subst_mono("BBB", '123'), '123'))