#!/usr/bin/python3

# Usage: python3 frequence.py fichier_texte
import sys


def frequence ():
		m=sys.argv[1]
		f = open(m, 'r', encoding='ASCII')
		Occurrences = {}
		i = f.read()
		length = 0
		for k in i :
			if (k != '\n'):
				length+=1
		for j in i :
			if (j != '\n'):
				nb_lettre = i.count(j)
				Occurrences[j]= i.count(j)/length
		f.close()


		#On affiche les occurences 
		for cle, valeur in Occurrences.items():
			print (cle, valeur)
			print ("\n")
		return Occurrences

frequence()




