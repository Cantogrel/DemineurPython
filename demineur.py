'''Auteur: CANTOGREL Mathieu'''

from tkinter import *
from random import *

#Déclaration des variables
global game, nbBmb, map, fenetre, terrain, carreau, game
game = 1
nbBmb = 10
tailCar = 60
col = 10
lig = 10
map = []

#Fonction création du contenu de la grille
def contenuMap():
    global map
    #Matrice bombe aillant l'emplacement de chaque bombe
    bombe = []
    while (len(bombe)<10):
        i=randint(0,col-1)
        j=randint(0,lig-1)
        test=0
        for a in bombe:
            if ([i,j] == a):
                test=1
        if (test == 0):
            bombe += [[i,j]]
    
    #Matrice aillant les valeur de la grille entiere
    for a in range(10):
        L = []
        for b in range(10):
            testB = 0
            for t in bombe:
                if ([a,b] == t):
                    testB = 1
            if (testB == 1):
                L += ['B']
            else:
                testNbB = 0
                for x in range(3):
                    for y in range(3):
                        for z in bombe:
                            if ([a-1+x,b-1+y] == z):
                                testNbB += 1
                L += [str(testNbB)]
        map+=[L]
    
    #Distinction des zone vide dans la matrice
    zone = 0
    for a in range(10):
        for b in range(10):
            if (map[a][b] == '0'):
                testZ = ' '
                zoneExist=[]
                for x in range(3):
                    for y in range(3):
                        if (-1 < a-1+x < 10 and -1 < b-1+y < 10):
                            testAct = map[a-1+x][b-1+y]
                            if (testAct[0] == 'Z'):
                                testZ = testAct
                                zoneExist += [testAct]
                if (testZ[0] != 'Z'):
                    zone +=1
                    testZ = 'Z' + str(zone)
                map[a][b] = testZ
                if (len(zoneExist) > 1):
                    for x in range(10):
                        for y in range(10):
                            if (map[x][y] in zoneExist):
                                map[x][y] = testZ
    

#Fonction qui s'active lors du clic gauche // Devoile la case
def clic(event):
    global game
    j=event.x//60
    i=event.y//60
    if (terrain.itemcget(carreau[i][j],'fill') == '#DDDDDD' and game == 1):
        if (map[i][j] == 'B'):
            terrain.itemconfigure(carreau[i][j],fill="#000000")
            lbBombes["text"] = 'BOUM !!!'
            game = 0
        elif (map[i][j][0] == 'Z'):
            for a in range(10):
                for b in range(10):
                    if (map[a][b] == map[i][j]):
                        terrain.itemconfigure(carreau[a][b],fill="#FFFFFF")
                    else:
                        testZ = 0
                        for x in range(3):
                            for y in range(3):
                                if (-1 < a-1+x < 10 and -1 < b-1+y < 10):
                                    if (map[a-1+x][b-1+y] == map[i][j]):
                                        testZ += 1
                        if (testZ > 0):
                            terrain.itemconfigure(carreau[a][b],fill="#EEEEEE")
                            terrain.create_text(b*tailCar+30,a*tailCar+30,text=map[a][b])
        else:
            terrain.itemconfigure(carreau[i][j],fill="#EEEEEE")
            terrain.create_text(j*tailCar+30,i*tailCar+30,text=map[i][j])

#Fonction qui s'active lors du clic droit // Pose un drapeau
def clicDroit(event):
    global game, nbBmb
    j=event.x//60
    i=event.y//60
    if (game == 1):
        if (terrain.itemcget(carreau[i][j],'fill') == '#DDDDDD' and nbBmb > 0):
            terrain.itemconfigure(carreau[i][j],fill="#FF0000")
            nbBmb -= 1
        elif (terrain.itemcget(carreau[i][j],'fill') == '#FF0000'):
            terrain.itemconfigure(carreau[i][j],fill="#DDDDDD")
            nbBmb += 1
        lbBombes["text"] = 'Bombes restantes :  ' + str(nbBmb)

#Fonction crétion de la fenetre
def init():
    global fenetre, terrain, carreau, game
    #Creation de la fenetre tkinter
    fenetre = Tk()
    fenetre.title("Démineur")
    
    #Creation du canvas qui va accueillir la grille graphique
    terrain = Canvas(fenetre,height=600,width=600)
    terrain.pack()
    
    #Creation de la grille
    carreau = [[terrain.create_rectangle(i*tailCar,j*tailCar,(i+1)*tailCar,(j+1)*tailCar,fill="#DDDDDD") 
                                                                        for i in range(col)] for j in range(lig)]
    
    #Appel de la fonction qui va remplir la grille
    contenuMap()
    
    for i in range(10):
        for j in range(10):
            print(map[i][j],end=" ")
        print()
    
    #Creation des évenements
    terrain.bind('<ButtonRelease-1>',clic)
    terrain.bind('<ButtonRelease-3>',clicDroit)
    
    #Affichage des widgets
    global lbBombes, btnRestart
    
    lbBombes = Label(fenetre, text='Bombes restantes :  '+str(nbBmb))
    lbBombes.pack(pady='10px')
    
    btnRestart = Button(fenetre, text='Restart', command=restart)
    btnRestart.pack()
    
    #Lancement de la fenetre
    game = 1
    fenetre.mainloop()

#Fonction restart
def restart():
    fenetre.destroy()
    init()

init()