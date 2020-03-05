#Application generates data for AI and teaches it to approximate Blood Alcohol Content based on amount of beverages drunk and person parameters.


#globals
separator=","
configurationFileSeparator=":"
configurationFile="config.ini"

#configuration
class Configuration:
    generateData=0
    datasetSize=10000
    roundPlaces=2
    randomDrinkingTimeMaxHours=24
    Beverage1MaxAmountML=5000.0
    Beverage1MinAmountML=0.0
    Beverage2MaxAmountML=5000.0
    Beverage2MinAmountML=0.0
    Beverage3MaxAmountML=5000.0
    Beverage3MinAmountML=0.0
    Beverage1PercentageMin=0.0
    Beverage1PercentageMax=1.0
    Beverage2PercentageMin=0.0
    Beverage2PercentageMax=1.0
    Beverage3PercentageMin=0.0
    Beverage3PercentageMax=1.0
    AgeMin=18.0
    AgeMax=110.0
    HeightMin=100.0
    HeightMax=230.0
    WeightMin=40.0
    WeightMax=300.0
    genderDiversity="both"
    datasetLocation="WidmarkBACdataset.txt"
    def __init__(self):
        file=open(configurationFile, "r")
        self.generateData=int(file.readline().split(configurationFileSeparator)[1])
        self.roundPlaces=int(file.readline().split(configurationFileSeparator)[1])
        self.datasetSize=int(file.readline().split(configurationFileSeparator)[1])
        self.randomDrinkingTimeMaxHours=float(file.readline().split(configurationFileSeparator)[1])
        self.Beverage1MaxAmountML=float(file.readline().split(configurationFileSeparator)[1])
        self.Beverage1MinAmountML=float(file.readline().split(configurationFileSeparator)[1])
        self.Beverage2MaxAmountML=float(file.readline().split(configurationFileSeparator)[1])
        self.Beverage2MinAmountML=float(file.readline().split(configurationFileSeparator)[1])
        self.Beverage3MaxAmountML=float(file.readline().split(configurationFileSeparator)[1])
        self.Beverage3MinAmountML=float(file.readline().split(configurationFileSeparator)[1])
        self.Beverage1PercentageMin=float(file.readline().split(configurationFileSeparator)[1])
        self.Beverage1PercentageMax=float(file.readline().split(configurationFileSeparator)[1])
        self.Beverage2PercentageMin=float(file.readline().split(configurationFileSeparator)[1])
        self.Beverage2PercentageMax=float(file.readline().split(configurationFileSeparator)[1])
        self.Beverage3PercentageMin=float(file.readline().split(configurationFileSeparator)[1])
        self.Beverage3PercentageMax=float(file.readline().split(configurationFileSeparator)[1])
        self.AgeMin=float(file.readline().split(configurationFileSeparator)[1])
        self.AgeMax=float(file.readline().split(configurationFileSeparator)[1])
        self.HeightMin=float(file.readline().split(configurationFileSeparator)[1])
        self.HeightMax=float(file.readline().split(configurationFileSeparator)[1])
        self.WeightMin=float(file.readline().split(configurationFileSeparator)[1])
        self.WeightMax=float(file.readline().split(configurationFileSeparator)[1])
        self.GenderDiversity=(file.readline().split(configurationFileSeparator)[1])
        self.datasetLocation=(file.readline().split(configurationFileSeparator)[1])
        file.close()
        return None

#globalConfiguration
applicationConfiguration=Configuration()

#imports
import random
import math

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

    def randomize(self):
        self.beverage1Amount=round(random.uniform(applicationConfiguration.Beverage1MinAmountML,applicationConfiguration.Beverage1MaxAmountML),applicationConfiguration.roundPlaces)
        self.beverage2Amount=round(random.uniform(applicationConfiguration.Beverage2MinAmountML,applicationConfiguration.Beverage2MaxAmountML),applicationConfiguration.roundPlaces)
        self.beverage3Amount=round(random.uniform(applicationConfiguration.Beverage3MinAmountML,applicationConfiguration.Beverage3MaxAmountML),applicationConfiguration.roundPlaces)
        self.beverage1Percentage=round(random.uniform(applicationConfiguration.Beverage1PercentageMin,applicationConfiguration.Beverage1PercentageMax),applicationConfiguration.roundPlaces)
        self.beverage2Percentage=round(random.uniform(applicationConfiguration.Beverage2PercentageMin,applicationConfiguration.Beverage2PercentageMax),applicationConfiguration.roundPlaces)
        self.beverage3Percentage=round(random.uniform(applicationConfiguration.Beverage3PercentageMin,applicationConfiguration.Beverage3PercentageMax),applicationConfiguration.roundPlaces)
        return self

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

    def randomize(self):
        self.age=round(random.uniform(applicationConfiguration.AgeMin,applicationConfiguration.AgeMax),applicationConfiguration.roundPlaces)
        self.height=round(random.uniform(applicationConfiguration.HeightMin,applicationConfiguration.HeightMax),applicationConfiguration.roundPlaces)
        self.weight=round(random.uniform(applicationConfiguration.WeightMin,applicationConfiguration.WeightMax),applicationConfiguration.roundPlaces)
        if applicationConfiguration.genderDiversity=="both":
            self.gender=float(random.randint(0,1))
        if applicationConfiguration.genderDiversity=="male":
            self.gender=0.0
        if applicationConfiguration.genderDiversity=="female":
            self.gender=1.0
        return self

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

    def randomize(self):
        self.person=Person().randomize()
        self.amountOfAlcohol=AmountOfAlcohol().randomize()
        self.drinkingTime=round(random.uniform(0.0,applicationConfiguration.randomDrinkingTimeMaxHours),applicationConfiguration.roundPlaces)
        self.drinksOften=random.randint(0,2)
        return self

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

#APPLICATION START

#check if user wants to generate dataset
if applicationConfiguration.generateData==1:
    #generate random data and send it to file
    fileHeader="|Age   |Height |Weight |Gender |Bev1Amount |Bev1% |Bev2Amount |Bev2% |Bev3Amount |Bev3% |DrinkingTime |DrinksOften |"
    file=open(applicationConfiguration.datasetLocation, "w")
    _=file.write(fileHeader+"\n")
    for i in range(0,applicationConfiguration.datasetSize):
        _=file.write(BloodAlcoholContent().randomize().bloodAlcoholContentToString()+"\n")
    file.close()





