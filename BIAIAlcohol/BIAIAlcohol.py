#imports


#globals
separator=","

#CLASSES needed to store data

#defaults are for beer 0.5, wine 0.12., vodka 0.30
class AmountOfAlcohol:
    beverage1Amount=0.0 
    beverage1Percentage=0.5
    beverage2Amount=0.0
    beverage2Percentage=0.12
    beverage3Amount=0.0
    beverage3Percentage=0.30

    def __init__(self, beverage1Amount=0.0, beverage1Percentage=0.5, beverage2Amount=0.0, beverage2Percentage=0.12, beverage3Amount=0.0, beverage3Percentage=0.30):
        self.beverage1Amount=beverage1Amount
        self.beverage1Percentage=beverage1Percentage
        self.beverage2Amount=beverage2Amount
        self.beverage2Percentage=beverage2Percentage
        self.beverage3Amount=beverage3Amount
        self.beverage3Percentage=beverage3Percentage
        return None


    def pureAlcohol(self):
        return beverage1Amount*beverage1Percentage+beverage2Amount*beverage2Percentage+beverage3Amount+beverage3Percentage

    def amountOfAlcoholToString(self):
        return str(self.beverage1Amount).ljust(len("Bev1Amount "))+separator+str(self.beverage1Percentage).ljust(len("Bev1% "))+separator+str(self.beverage2Amount).ljust(len("Bev2Amount "))+separator+str(self.beverage2Percentage).ljust(len("Bev2% "))+separator+str(self.beverage3Amount).ljust(len("Bev3Amount "))+separator+str(self.beverage3Percentage).ljust(len("Bev3% "))

    def amountOfAlcoholFromString(self,input):
        self.beverage1Amount=float(input.split(",")[4].replace(" ",""))
        self.beverage1Percentage=float(input.split(",")[5].replace(" ",""))
        self.beverage2Amount=float(input.split(",")[6].replace(" ",""))
        self.beverage2Percentage=float(input.split(",")[7].replace(" ",""))
        self.beverage3Amount=float(input.split(",")[8].replace(" ",""))
        self.beverage3Percentage=float(input.split(",")[9].replace(" ",""))
        return None

class Person:
    age=0.0
    height=0.0
    weight=0.0
    gender=0.0 #0.0 for male 1.0 for female
    

    def __init__(self, age=0.0, height=0.0, weight=0.0,gender=0.0):
        self.age=age
        self.height=height
        self.weight=weight
        self.gender=gender
        return None



    #Watson formula for body liquid calculation 
    #MALE
    #tbw = 2.447 - (0.09156*L) + (0.1074*W) + (0.3362*M)
    #FEMALE
    #tbw = -2.097 + (0.1069*W) + (0.2466*M)
    #where M-mass, W-height, L-age
    def calculateBodyLiquids(self):
        if gender==0.0:
            return 2.447 - (0.09156*age) + (0.1074*height) + (0.3362*weight)
        else:
            return -2.097 + (0.1069*height) +(0.2466*weight)

    def personToString(self):
        return " "+str(self.age).ljust(len("Age   "))+separator+str(self.height).ljust(len("Height "))+separator+str(self.weight).ljust(len("Weight "))+separator+str(self.gender).ljust(len("Gender "))

    def personFromString(self,input):
        self.age=float(input.split(",")[0].replace(" ",""))
        self.height=float(input.split(",")[1].replace(" ",""))
        self.weight=float(input.split(",")[2].replace(" ",""))
        self.gender=float(input.split(",")[3].replace(" ",""))
        return None

class BloodAlcoholContent:
    person:Person#in kg
    amountOfAlcohol:AmountOfAlcohol #in 
    drinkingTime=0
    drinksOften=0.0 #0.0 for rare, 1.0 for sometimes, 2.0 often

    def __init__(self,person=Person(), amountOfAlcohol=AmountOfAlcohol(),drinkingTime=0.0,drinksOften=0.0):
        self.person=person
        self.amountOfAlcohol=amountOfAlcohol
        self.drinkingTime=drinkingTime
        self.drinksOften=drinksOften
        return None

    #Blood Alcohol Content formula
    #P = (A/TBW)*0.79 - (T*e)
    #gdzie:
    #0.79-gęstość alkoholu
    #T - czas spędzony na spożywaniu produktów
    #alkoholowych (w godzinach)
    #e - współczynnik eliminacji alkoholu z organizmu
    #wynoszący:
    #0.1 promila na godzinę dla osób pijących rzadko
    #0.15 promila na godzinę dla osób pijących przeciętnie
    #0.2 promila na godzinę dla osób pijących często
    def CalculateBAC(self):
        alcoholDensity=0.79
        decay=0.1
        if drinksOften==0.0:
            decay=0.1
        elif drinksOften==1.0:
            decay=0.15
        elif drinksOften==2.0:
            decay=0.2
        return (amountOfAlcohol.pureAlcohol()/person.calculateBodyLiquids())*alcoholDensity-(drinkingTime*decay);

    def bloodAlcoholContentToString(self):
        tempPerson=self.person.personToString()
        tempAoA=self.amountOfAlcohol.amountOfAlcoholToString()
        return tempPerson+separator+tempAoA+separator+str(self.drinkingTime).ljust(len("DrinkingTime "))+separator+str(self.drinksOften).ljust(len("DrinksOften "))

    def bloodAlcoholContentFromString(self,input):
        self.person=Person()
        self.person.personFromString(input)
        self.amountOfAlcohol=AmountOfAlcohol()
        self.amountOfAlcohol.amountOfAlcoholFromString(input)
        self.drinkingTime=float(input.split(separator)[10].replace(" ",""))
        self.drinksOften=float(input.split(separator)[11].replace(" ",""))
        return None

BAC=BloodAlcoholContent(Person(20.0,180.0,65.0,0.0),AmountOfAlcohol(1000.0,0.5,500.0,0.12,0.0,0.30),0,1.0)

fileHeader="|Age   |Height |Weight |Gender |Bev1Amount |Bev1% |Bev2Amount |Bev2% |Bev3Amount |Bev3% |DrinkingTime |DrinksOften |"



file= open("WidmarkBACdataset.txt", "r")
s1=file.readline()
s2=file.readline()
print(s1)
BAC=BloodAlcoholContent()
BAC.bloodAlcoholContentFromString(s2)
print(BAC.bloodAlcoholContentToString())
file.write(BAC.bloodAlcoholContentToString())
file.close()


file= open("WidmarkBACdataset.txt", "w")
file.write(fileHeader+"\n")
for i in range(0,6):
    file.write(BAC.bloodAlcoholContentToString()+"\n")
file.close()