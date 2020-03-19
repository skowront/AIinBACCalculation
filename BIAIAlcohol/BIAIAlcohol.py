#Application generates data for AI and teaches it to approximate Blood Alcohol Content based on amount of beverages drunk and person parameters.

#currently working with http://www.kenderdinemathstutoring.com.au/downloads/3011085/BAC+formula+questioned+amended.pdf
#https://mojafirma.infor.pl/moto/kalkulatory/30,kalkulator-alkomat.html

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
    doAddUncertainity=0
    genderDiversity="both"
    datasetLocation="WidmarkBACdataset.txt"
    doTrainModel=1
    doUseModel=0
    modelLocation="model.h5"
    selfTest=0
    generateTestSet=1
    testSetSize=10
    testSetLocation="testSet.txt"
    useTestSet=1
    def __init__(self):
        file=open(configurationFile, "r")
        self.generateData=int(file.readline().split(configurationFileSeparator)[1].replace('\n',''))
        self.roundPlaces=int(file.readline().split(configurationFileSeparator)[1].replace('\n',''))
        self.datasetSize=int(file.readline().split(configurationFileSeparator)[1].replace('\n',''))
        self.randomDrinkingTimeMaxHours=float(file.readline().split(configurationFileSeparator)[1].replace('\n',''))
        self.Beverage1MaxAmountML=float(file.readline().split(configurationFileSeparator)[1].replace('\n',''))
        self.Beverage1MinAmountML=float(file.readline().split(configurationFileSeparator)[1].replace('\n',''))
        self.Beverage2MaxAmountML=float(file.readline().split(configurationFileSeparator)[1].replace('\n',''))
        self.Beverage2MinAmountML=float(file.readline().split(configurationFileSeparator)[1].replace('\n',''))
        self.Beverage3MaxAmountML=float(file.readline().split(configurationFileSeparator)[1].replace('\n',''))
        self.Beverage3MinAmountML=float(file.readline().split(configurationFileSeparator)[1].replace('\n',''))
        self.Beverage1PercentageMin=float(file.readline().split(configurationFileSeparator)[1].replace('\n',''))
        self.Beverage1PercentageMax=float(file.readline().split(configurationFileSeparator)[1].replace('\n',''))
        self.Beverage2PercentageMin=float(file.readline().split(configurationFileSeparator)[1].replace('\n',''))
        self.Beverage2PercentageMax=float(file.readline().split(configurationFileSeparator)[1].replace('\n',''))
        self.Beverage3PercentageMin=float(file.readline().split(configurationFileSeparator)[1].replace('\n',''))
        self.Beverage3PercentageMax=float(file.readline().split(configurationFileSeparator)[1].replace('\n',''))
        self.AgeMin=float(file.readline().split(configurationFileSeparator)[1].replace('\n',''))
        self.AgeMax=float(file.readline().split(configurationFileSeparator)[1].replace('\n',''))
        self.HeightMin=float(file.readline().split(configurationFileSeparator)[1].replace('\n',''))
        self.HeightMax=float(file.readline().split(configurationFileSeparator)[1].replace('\n',''))
        self.WeightMin=float(file.readline().split(configurationFileSeparator)[1].replace('\n',''))
        self.WeightMax=float(file.readline().split(configurationFileSeparator)[1].replace('\n',''))
        self.doAddUncertainity=int(file.readline().split(configurationFileSeparator)[1].replace('\n',''))
        self.GenderDiversity=(file.readline().split(configurationFileSeparator)[1].replace('\n',''))
        self.datasetLocation=(file.readline().split(configurationFileSeparator)[1].replace('\n',''))
        self.doTrainModel=int(file.readline().split(configurationFileSeparator)[1].replace('\n',''))
        self.doUseModel=int(file.readline().split(configurationFileSeparator)[1].replace('\n',''))
        self.modelLocation=(file.readline().split(configurationFileSeparator)[1].replace('\n',''))
        self.selfTest=int(file.readline().split(configurationFileSeparator)[1].replace('\n',''))
        self.generateTestSet=int(file.readline().split(configurationFileSeparator)[1].replace('\n',''))
        self.testSetSize=int(file.readline().split(configurationFileSeparator)[1].replace('\n',''))
        self.testSetLocation=(file.readline().split(configurationFileSeparator)[1].replace('\n',''))
        self.useTestSet=int(file.readline().split(configurationFileSeparator)[1].replace('\n',''))
        file.close()
        return None

#globalConfiguration
applicationConfiguration=Configuration()


#imports
import random
import math
import tensorflow as tf
import keras
from keras.models import load_model
import numpy as np

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
        #       na gramy*gęstość alkoholu w litrze*(procentowe zawartości)
        return 0.001*0.79*((1000*self.beverage1Amount*self.beverage1Percentage)+(1000*self.beverage2Amount*self.beverage2Percentage)+(1000*self.beverage3Amount*self.beverage3Percentage))

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

    #!important comments
    def toArray(self):
        result = []
        result.append(self.beverage1Amount)
        result.append(self.beverage1Percentage)
        result.append(self.beverage2Amount)
        result.append(self.beverage2Percentage)
        result.append(self.beverage3Amount)
        result.append(self.beverage3Percentage)
        return result

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
        if self.gender==0.0:
            return 2.447 - (0.09156*self.age) + (0.1074*self.height) + (0.3362*self.weight)
        else:
            return -2.097 + (0.1069*self.height) +(0.2466*self.weight)

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

    def toArray(self):
        result=[]
        #result.append(self.age)
        #result.append(self.height)
        result.append(self.weight)
        result.append(self.gender)
        return result

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
    #returns resul*100
    def CalculateBAC(self):
        alcoholDensity=0.79
        decay=0.1
        if self.drinksOften==0.0:
            decay=0.01
        elif self.drinksOften==1.0:
            decay=0.015
        elif self.drinksOften==2.0:
            decay=0.02
        #backup of extended equation
        #result=(self.amountOfAlcohol.pureAlcohol()/self.person.calculateBodyLiquids())*alcoholDensity-(self.drinkingTime*decay)
        result=0.0
        #http://www.kenderdinemathstutoring.com.au/downloads/3011085/BAC+formula+questioned+amended.pdf
        if self.person.gender==0.0:
            result=(self.amountOfAlcohol.pureAlcohol()*100/(0.7*self.person.weight))-(decay*self.drinkingTime)
        else:
            result=(self.amountOfAlcohol.pureAlcohol()*100/(0.6*self.person.weight))-(decay*self.drinkingTime)
        #end of simplified equation changes
        if applicationConfiguration.doAddUncertainity==1:
            result=result+result*(0.21)
        if result<0:
            result=0
        return result*10;#percent do promile, dlatego *10

    #max 0.0010% alcohol content
    def randomize(self):
        self.person=Person().randomize()
        self.amountOfAlcohol=AmountOfAlcohol().randomize()
        self.drinkingTime=round(random.uniform(0.0,applicationConfiguration.randomDrinkingTimeMaxHours),applicationConfiguration.roundPlaces)
        self.drinksOften=random.randint(0,2)
        while self.CalculateBAC()>100:
            self.person=Person().randomize()
            self.amountOfAlcohol=AmountOfAlcohol().randomize()
            self.drinkingTime=round(random.uniform(0.0,applicationConfiguration.randomDrinkingTimeMaxHours),applicationConfiguration.roundPlaces)
            self.drinksOften=random.randint(0,2)
        return self

    #returns result
    def bloodAlcoholContentToString(self):
        tempPerson=self.person.personToString()
        tempAoA=self.amountOfAlcohol.amountOfAlcoholToString()
        result= tempPerson+separator+tempAoA+separator+str(self.drinkingTime).ljust(len("DrinkingTime "))+separator+str(self.drinksOften).ljust(len("DrinksOften "))
        return result

    def bloodAlcoholContentFromString(self,input):
        self.person=Person()
        self.person.personFromString(input)
        self.amountOfAlcohol=AmountOfAlcohol()
        self.amountOfAlcohol.amountOfAlcoholFromString(input)
        self.drinkingTime=float(input.split(separator)[10].replace(" ",""))
        self.drinksOften=float(input.split(separator)[11].replace(" ",""))
        return None

    def toArray(self):
        result=[]
        tPerson=self.person.toArray()
        for obj in tPerson:
            result.append(float(obj))
        tAoA=self.amountOfAlcohol.toArray()
        for obj in tAoA:
            result.append(float(obj))
        result.append(float(self.drinkingTime))
        result.append(float(self.drinksOften))
        return result

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


#load dataset from file 
dataset = []
file=open((applicationConfiguration.datasetLocation),"r")
_=file.readline()
for i in range(0,applicationConfiguration.datasetSize):
    BAC=BloodAlcoholContent()
    BAC.bloodAlcoholContentFromString(file.readline())
    dataset.append(BAC)
file.close()

#BELOW UNCERTAIN, TODO then

#convert BACs to array X and Y
datasetX=[]
datasetY=[]
#for i in range(0,applicationConfiguration.datasetSize):
for i in range(0,applicationConfiguration.datasetSize):
    datasetX.append(dataset[i].toArray())
    #bac=[]
    #bac.append(dataset[i].CalculateBAC())
    datasetY.append(dataset[i].CalculateBAC())
    
model=0
#create model and train it with dataset
if applicationConfiguration.doTrainModel==1:
    print("Creating model")
    model = keras.models.Sequential()
    model.add(keras.layers.Dense(100,activation='sigmoid'))
    model.add(keras.layers.Dense(100,activation='sigmoid'))
    model.add(keras.layers.Dense(100,activation='relu'))
    model.add(keras.layers.Dense(1,activation='relu'))
    model.compile('nadam','mean_squared_error',['cosine_proximity'])
    model.fit(x=np.array(datasetX),y=np.asarray(datasetY),epochs=10,verbose=2)
    model.save(applicationConfiguration.modelLocation)
    #TODO
    

#use model
if applicationConfiguration.doUseModel==1:
    model=keras.models.load_model(applicationConfiguration.modelLocation)
    print("Model loaded from: "+applicationConfiguration.modelLocation)

val_loss,val_acc=model.evaluate([datasetX],datasetY)
print(val_loss,val_acc)


#predict sth that ML learned
if applicationConfiguration.selfTest==1:
    for i in range(0,100):
        id=random.randint(0,applicationConfiguration.datasetSize-1)
        data=[]
        for obj in datasetX[id]:
            data.append(obj)
        prediction=model.predict([[data]])
        print("ML predicted: ") 
        print(float(np.argmax(prediction[0]))/10.0)
        print("Result is: ")
        print(dataset[id].CalculateBAC()/10.0)
        print("-----------------------")

#check if user wants to generate testSet
if applicationConfiguration.generateTestSet==1:
    #generate random data and send it to file
    fileHeader="|Age   |Height |Weight |Gender |Bev1Amount |Bev1% |Bev2Amount |Bev2% |Bev3Amount |Bev3% |DrinkingTime |DrinksOften |"
    file=open(applicationConfiguration.testSetLocation, "w")
    _=file.write(fileHeader+"\n")
    for i in range(0,applicationConfiguration.testSetSize):
        _=file.write(BloodAlcoholContent().randomize().bloodAlcoholContentToString()+"\n")
    file.close()

#test if user wants to use testset
if applicationConfiguration.useTestSet==1:
    #load dataset from file 
    testSet = []
    file=open((applicationConfiguration.testSetLocation),"r")
    _=file.readline()
    for i in range(0,applicationConfiguration.testSetSize):
        BAC=BloodAlcoholContent()
        BAC.bloodAlcoholContentFromString(file.readline())
        testSet.append(BAC)
    file.close()
    #convert BACs to array X and Y
    testsetX=[]
    testsetY=[]
    #for i in range(0,applicationConfiguration.datasetSize):
    for i in range(0,applicationConfiguration.testSetSize):
        testsetX.append(testSet[i].toArray())
        testsetY.append(testSet[i].CalculateBAC())
    for i in range(0,applicationConfiguration.testSetSize):
        testdata=[]
        for obj in testsetX[i]:
            testdata.append(obj)
        prediction=model.predict([[testdata]])
        print("ML predicted: ") 
        print(prediction[0][0])
        print("Result is: ")
        print(testSet[i].CalculateBAC())
        print("-----------------------")


#TODO console interface


