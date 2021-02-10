import pandas as pd
import time
import random
#import spreadsheet as ss
# Event APOGEE occurred at t=8.8872 seconds

def noisy_sim(sim):
    noisy_sim = sim
    for index, row in noisy_sim.iterrows():
        if index <10:
            row["Altitude (m)"] = row["Altitude (m)"] + random.uniform(0,1)
        else:
            row["Altitude (m)"] = row["Altitude (m)"] + random.uniform(-1,1)
    return noisy_sim



class Flight_Computer():
    def __init__(self, path_to_csv_of_simulation, apogee_t, apogee_m):
        self.sim = pd.DataFrame(pd.read_csv(path_to_csv_of_simulation))
        self.correct_apogee_t = apogee_t#seconds; change this as needed between different openrocket simulations
        self.correct_apogee_m =apogee_m 


    @staticmethod
    def instant_velocity(time_now, time_previous, altitude_now, altitude_previous):
        return (altitude_now-altitude_previous)/(time_now-time_previous)
    

    def check_liftoff(self, velocities):
        count = 0
        for v in velocities:
            if v>0:
                count +=1
            else:
                pass
        if count >=7:
            return True
        else:
            return False

    #apogee detector needs to be changed to a counter system because the true-false approach doesn't work with noise
    def closetozero(self, velocity):
        if -1 <= velocity <= 1:
            return True
        else:
            return False

    def apogeeDetector(self,velocities):
        good = False
        for i in range(1,5):
            #this is where we stopped in the club
            if self.closetozero(velocities[-i]) == True:
                good = True
                continue
            else:
                good = False
                break
        return good

    def calculate_accuracy(self,prediction, correct):
        accuracy = abs(prediction-correct) / correct
        return round(1 - accuracy, 5)
    #hello
    def Fly(self, simulation_frame):
        velocities = []
        apogee = False
        liftoff = False
        for index, row in simulation_frame.iterrows():
            #print(index, row["Time (s)"], row["Altitude (m)"])

            if index == 0:
                continue
            else:
                #v is in m/s
                v = self.instant_velocity(simulation_frame["Time (s)"][index],simulation_frame["Time (s)"][index-1], simulation_frame["Altitude (m)"][index],simulation_frame["Altitude (m)"][index-1])
                velocities.append(v)
                if index > 5:
                    if liftoff == False:
                        liftoff = self.check_liftoff(velocities)

            if liftoff== True:
                if index > 20:
                    apogee = self.apogeeDetector(velocities)
                    if apogee == True:
                        #print("APOGEE!!! ")
                        return [row["Time (s)"],row["Altitude (m)"]]
                        break

apogee_m = 408.54
apogee_t = 8.8872
path_to_sim = "//Users//jeremi//Documents//Flight_computer//simulation1.csv"
Eddie = Flight_Computer(path_to_sim, apogee_m,apogee_t)
#print(noise_1[:10])
#print(Eddie.sim[0:10])

print(Eddie.Fly(Eddie.sim))
