#https://github.com/AdamKomosinski/SymulatorOgame
import random

class DaneStatkow():
    '''Klasa zawierająca dane statków.'''
    def __init__(self):
        self.klasystatkow = self.pobierz_klasy()[1:]
    
    def pobierz_klasy(self):
        klasy = []
        with open('dane_statkow.txt') as plik:
            for linia in plik:
                klasa = linia.strip().split()
                for i in range(0, len(klasa)):
                    if klasa[i].isdigit():
                        klasa[i] = int(klasa[i])
                klasy.append(klasa)
        return klasy
    
    def zwroc_dane_klasy(self, skrot):
        '''Zwraca dane klasy potrzebne do klasy Statek'''
        for i in self.klasystatkow:
            if (skrot == i[0]):
                return i[0], i[2], i[3], i[4]
    
class Statek():
    '''Klasa posiadająca wszysktie parametry
    danego statku.'''
    def __init__(self, skrot, ps, oslona, atak):
        '''skrot - skrótowa nazwa statku,
        ps - punkty strukturalne
        oslona - punkty oslony
        atak - punkty ataku
        ops, ooslona - obecnie posiadane ps i oslona
        sdziala - szybkie dziala
        zniszczony - znacznik czy statek zostal juz zniszczony'''
        self.skrot = skrot
        self.ps = ps
        self.ops = ps
        self.oslona = oslona
        self.ooslona = oslona
        self.atak = atak
        self.sdziala = self.pobierz_dziala()
        self.zniszczony = False
        
    def __str__(self):
        return str(self.skrot)
    def strzal(self, wflota):
        '''Losowo wybiera niezniszczony cel z
        wrogiej floty(lista statków)
        i wywołuje u niego obrazenia. Zwraca True jeżeli 
        może wystrzelić jeszcze raz w przeciwnym
        wypadku zwraca False.
        '''
        wrog = random.choice(wflota)
        wrog.obrazenia(self.atak)
        return self.szansa_na_strzal(wrog)
        
    def obrazenia(self, obr):
        '''Obliczanie otrzymanych obrażeń i 
        szansy na wybuch.'''
        if (obr > (self.ooslona * 0.01) and self.ops > 0):
            if (self.ooslona > 0):
                tmp = obr
                obr = obr - self.ooslona
                self.ooslona -= tmp
                if(obr > 0):
                    self.ops -= obr
            else:
                self.ops -= obr
            if (float(self.ops/self.ps) < 0.7):
                x = random.random()
                bum = 1.0 - (self.ops/self.ps)
                if x < bum:
                    self.ops = 0
                

    def pobierz_dziala(self):
        '''Wczytywanie szybkich dzial'''
        tmp = []
        plik = open('szybkie_dziala.txt', 'r')
        tmp.append(list(plik.readline().strip().split()))
        a = plik.readlines()
        plik.close()
        for linia in a:
            line = linia.split()
            if (line[0] == self.skrot):
                tmp.append(line)
                break
        for i in range(len(tmp[1])):
            if (tmp[1][i].isdigit()):
                tmp[1][i] = int(tmp[1][i])
                
        return tmp    

    def szansa_na_strzal(self, wrog):
        '''Obliczanie szans na kolejny strzał'''
        pom = 0
        for i in range (len(self.sdziala[0])):
            if (self.sdziala[0][i] == wrog.skrot):
                pom = i
                break
        x = random.random()
        szansa = 1 - (1 / self.sdziala[1][pom])
        if x < szansa:
            return True
        else:
            return False
        
    def czy_zniszczony(self):
        '''Oznacza statek jako zniszczony jeżeli jego punkty strukturalne
        się wyczerpały'''
        if(self.ops <= 0):
            self.zniszczony = True
            
    def odnow_oslony(self):
        '''Odnawia oslony statku.'''
        self.ooslona = self.oslona

class Symulator(DaneStatkow):
    '''Klasa symulatora, w której odbywa sie symulacja'''
    def __init__(self):
        DaneStatkow.__init__(self)
        
        self.flota1 = []
        plik = open('flota_1.txt', 'r')
        plik.readline()
        a = [a.split() for a in plik]
        plik.close()
        for i in a:
            for j in range(0, int(i[1])):
                self.flota1.append(Statek(*DaneStatkow.zwroc_dane_klasy(self,i[0])))

        self.flota2 = []
        plik = open('flota_2.txt', 'r')
        plik.readline()
        a = [a.split() for a in plik]
        plik.close()
        for i in a:
            for j in range(int(i[1])):
                self.flota2.append(Statek(*DaneStatkow.zwroc_dane_klasy(self, i[0])))

    def bitwa(self):
        '''Symulacja bitwy, skladajacej sie z 6 rund'''
        flota1 = self.flota1[:]
        flota2 = self.flota2[:]
        for i in range(6):
            for j in flota1:
                strzal = True
                while (strzal):
                    
                    strzal = j.strzal(flota2)

            for j in flota2:
                strzal = True
                while (strzal):
                    strzal = j.strzal(flota1)
                    
            for j in flota1:
                j.czy_zniszczony()
            for j in flota2:
                j.czy_zniszczony()
            
            tmp = []
            for j in flota1:
                if (not j.zniszczony):
                    
                    tmp.append(j)
            flota1 = tmp[:]
                    
            tmp2 = []
            for j in flota2:
                if(not j.zniszczony):
                    tmp.append(j)
            flota2 = tmp2[:]
            
            if (flota1 == [] and not flota2 == []):
                return 0 #zwraca 0 jeżeli remis
            if (flota1 == []):
                return 1 #zwraca 1 jeżeli wygrała flota 1
            if (flota2 == []):
                return 2 #zwraca 2 jeżeli wygrała flota 2
            
            for j in flota1:
                j.odnow_oslony()
            for j in flota2:
                j.odnow_oslony()
        return 0 
    
    def start(self):
        '''Po podaniu przez uzytkownika ilosc bitw do stoczenia nastepuje
        symulacja x bitew po 6 rund'''
        ile_bitew = int(input("Podaj ilość bitew do symulacji: "))
        wyniki = []
        for i in range(ile_bitew):
            wyniki.append(self.bitwa())
        w1 = 0
        w2 = 0
        r = 0
        for i in wyniki:
            if (i == 0):
                r += 1
            elif (i == 1):
                w1 += 1
            else:
                w2 += 1
        if (w1 > w2 and w1 > r):
            print ("Flota 1 wygrała najwięcej bitew na ",ile_bitew)

        if (w2 > w1 and w2 > r):
            print ("Flota 2 wygrała najwięcej bitew na ",ile_bitew)

        if (r > w1 and r > w2):
            print ("Najwięcej było remisów (skrajnie nieprawdopodobne)")
        
        print("Flota 1 wygrała", w1, " bitew.")
        print("Flota 2 wygrała", w2, " bitew.")
        print(r, " bitew skończyło się remisem.")
        
S = Symulator()
S.start()
