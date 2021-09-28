import random
class Suggested_pass:

    def __init__(self,nombre,lettres,char):
        self.password=None
        self.nb_nombres=nombre
        self.nb_lettres=lettres
        self.nb_char=char

    def generate(self):
        liste_lettre=[]
        liste_char=[]
        liste_nombres=[]
        lettres="abcdefghijklmnopqrstuvwxyz"
        number="1234567890"
        char='{([$%!:;.,=+)]}_-*'
        for loop in range(self.nb_lettres+1):
            random_numb=random.randint(0,len(lettres)-1)
            liste_lettre.append(lettres[random_numb])

        for loop in range(self.nb_nombres+1):
            random_numb=random.randint(0,len(number)-1)
            liste_nombres.append(number[random_numb])

        for loop in range(self.nb_char+1):
            random_numb=random.randint(0,len(char)-1)
            liste_char.append(char[random_numb])

        chaine=''
        final=None
        for elem in liste_lettre:
            if elem!=" ":
                chaine+=elem
        for elem in liste_nombres:
            if elem!=" ":
                chaine+=elem
        for elem in liste_char:
            if elem!=" ":
                chaine+=elem

        final=chaine
        return final
if __name__=='__main__':
    pass1=Suggested_pass(5,5,5)
    password=pass1.generate()
    print('Loading')
    print(f'Your Suggested password :{password}')
