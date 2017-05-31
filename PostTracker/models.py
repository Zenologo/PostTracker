import logging


class Tracking:
    def __init__(self, pParcelDate, pParcelStatut, pParcelLocation):
        self.parcelDate = pParcelDate
        self.parcelStatut = pParcelStatut
        self.parcelLocation = pParcelLocation
        self.parcelRemark = ""


class ModelTrack:
    def __init__(self, pRefParcel, pDestination=""):
        self.refParcel = pRefParcel
        self.lstTracking = []
        self.destination = pDestination

    def addTracking(self, pTracking):
        self.lstTracking.append(pTracking)

    def printTrack(self):
        if self.lstTracking:
            for index in range(0, len(self.lstTracking)):
                print(self.lstTracking[index].parcelDate + " " + \
                        self.lstTracking[index].parcelStatut + " " + \
                        self.lstTracking[index].parcelLocation)
        else:
            print("lstTrack is empty!")

    def containsTracking(self, pTracking):
        for info in self.lstTracking :
            if info.parcelDate == pTracking.parcelDate and \
                info.parcelStatut == pTracking.parcelStatut and \
                info.parcelLocation == pTracking.parcelLocation :
                return True
        return False