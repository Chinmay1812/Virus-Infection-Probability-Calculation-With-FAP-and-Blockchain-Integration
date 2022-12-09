from cProfile import label
import csv
from distutils.command.clean import clean
from posixpath import split
import tkinter as tktr
from tkinter import *
import math
import random
from tkinter import font
from tkinter.tix import DECREASING
from turtle import color, position
import matplotlib.pyplot as plt
from Crypto.Cipher import AES
import binascii, os, json
from colour import Color
from pyrsistent import l

                 
                 
symp_fac = {"fever": 0.89, "dry_cough": 0.68, "tiredness": 0.48, "fatigue": 0.33, "productive_cough": 0.29, "breath_problem": 0.17, "pain": 0.14,
                    "sore_throat": 0.11, "headache": 0.10, "diarrhea": 0.04, "nausea": 0.04, "rhinorrhea": 0.03, "chest_pain": 0.001}
dis_fac = {"hypertension": 0.5, "lipid_metabolism": 0.49, "lung_dis": 0.35, "kidney_disease": 0.24, "diabetes": 0.32, "obesity": 0.33,
                    "Neurocognitive": 0.14, "heart_disease": 0.25}
age_fac = {"0-4": 0.07, "5-9": 0.13, "10-14": 0.22, "15-19": 0.38, "20-24": 0.57, "25-29": 0.73, "30-34": 0.84, "35-39": 0.93, "40-44": 0.97, "45-49": 0.98,
                    "50-54": 0.99, "55-59": 0.99, "60-64": 1.00, "65-69": 1.00, "70-74": 1.00, "75-79": 1.00, "80-84": 1.00, "85-89": 1.00, "90-94": 1.00, "95-99": 1.00}
vac_fac = {"vaccinated": 0.24, "single_dose": 0.4, "not-vaccinated": 1}   
        
          
                 

data = {}
stand_c_prob = []
stand_tot_prob = []

class covid_spread_analyser():
    
    def __init__(self):
        self.window = tktr.Tk()
        self.window.title('Covid-19 Spread Detector')
        self.canvas = tktr.Canvas(self.window, width=1200, height=600)
        # self.window.bind('<B1-Motion>', self.paint)
        self.canvas.pack()
        self.main_fun()

    def mainloop(self):
        self.window.mainloop()

    # def paint(self, event):
    #     x, y = event.x, event.y
    #     self.canvas.create_oval(x-3, y+3, x+3, y-3, fill='blue')

    def main_fun(self):
        key_done = False
        keys = []
        user_id = -2
        
                                    ####################### Data Collection ######################
        
        with open('needed_data.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                if not key_done:
                    key_done = True
                    for i in range(30):
                        keys.append(row[i])
                user_id += 1
                data[user_id] = {}
                for i in range(30):
                    data[user_id][keys[i]] = row[i]
            data.pop(-1)
        
        cleaned_data = {}
        
        print("total users : ", len(data))
        
        for i in range(len(data)):
            
            temp = {}
            
            #age
            try:
                temp["age"] = int(data[i]["age"])
            except:
                t = list(map(int, data[i]["age"].split("-")))
                temp["age"] = int(sum(t)/len(t))
            
            
            #vaccination
            temp["vaccinated"] = False
            
            #symptoms
            symptoms = []
            if data[i]["respiratory"] == "1":
                symptoms.append("breath_problem")
            if data[i]["fever"] == "1":
                symptoms.append("fever")
            if data[i]["weakness/pain"] == "1":
                symptoms.append("tiredness")
                symptoms.append("pain")
            if data[i]["nausea"] == "1":
                symptoms.append("nausea")
            if data[i]["cardiac"] == "1":
                symptoms.append("chest_pain")
            temp["symptoms"] = symptoms
            
            #diseases
            diseases = []
            if data[i]["hypertension"] == "1":
                diseases.append("hypertension")
            if data[i]["respiratory_CD"] == "1":
                diseases.append("lung_dis")
            if data[i]["gastrointestinal"] == "1":
                diseases.append("lipid_metabolism")
            if data[i]["kidney"] == "1":
                diseases.append("kidney_disease")
            if data[i]["diabetes"] == "1":
                diseases.append("diabetes")
            if data[i]["weakness/pain"] == "1":
                diseases.append("obesity")
            if data[i]["neuro"] == "1":
                diseases.append("Neurocognitive")
            if data[i]["cardiacs_cd"] == "1":
                diseases.append("heart_disease")
            temp["diseases"] = diseases
            
            cleaned_data[i] = temp
        
                    
                
                                    ####################### Encryption ######################
                                    
        secretKey = os.urandom(32)  # 256-bit random encryption key
        msg = bytes(str(cleaned_data), 'utf-8')
        
        aesCipher = AES.new(secretKey, AES.MODE_GCM)
        ciphertext, authTag = aesCipher.encrypt_and_digest(msg)
        
        encryptedMsg = (ciphertext, aesCipher.nonce, authTag)



                                    ####################### Data upload ######################

        
        
                                    ####################### Decryption ######################

        
        (ciphertext, nonce, authTag) = encryptedMsg
        aesCipher = AES.new(secretKey, AES.MODE_GCM, nonce)

        decryptedMsg = str(aesCipher.decrypt_and_verify(ciphertext, authTag))
        
                                            ####################### Probability Evaluation ######################
                                            

        tr = decryptedMsg[3:len(decryptedMsg)-2]
                
        d = {}
        f = False
        temp_s = ""
        temp_f = []
        for i in range(len(tr)):
            if tr[i] == "{":
                f = True
            if tr[i] == "}":
                f = False
                temp_s += "}"
                temp_f.append(temp_s)
                temp_s = ""
            if f:
                temp_s += tr[i]
        
        print()
        
        data_for_c = {}
        ind = 0
        
        
        for i in temp_f:
            new_d = {}
            h = str(i)
            age = h[h.index("age")+6:h.index("vaccinated")-3]
            new_d["age"] = int(age)
            
            vaccinated = h[h.index("vaccinated")+13:h.index("symptoms")-3]
            if vaccinated == "False":
                new_d["vaccinated"] = "not-vaccinated"
            
            symptoms = []
            fs = h[h.index("symptoms")+12:h.index("diseases")-4]
            if len(fs) > 0:
                symptoms = fs[1:len(fs)-1].split("', '")
            
            new_d["symptoms"] = symptoms
            # print(fs, symptoms)
            
            diseases = []
            fs = h[h.index("diseases")+12:h.index("}")-1]
            if len(fs) > 0:
                diseases = fs[1:len(fs)-1].split("', '")
            
            new_d["diseases"] = diseases
            
            # print(diseases)
            
            data_for_c[ind] = new_d
            ind += 1
    
        h_prob = []
        
        fever_h_prob = []
        fever_c_prob = []
        
        stand_fever_prob = []
        stand_hyper_prob = []
        stand_cough_prob = []
        stand_tired_prob = []
        stand_lipid_prob = []
        
        cough_c_prob = []
        cough_h_prob = []
        
        tiredness_c_prob = []
        tiredness_h_prob = []
        
        age_info = []
        
        hypertension_h_prob = []
        lipid_metabolism_h_prob = []
        age_infection_info = [0 for i in range(21)]
        
        age_info_bar = []
        
        a2 = []
        
        for val in data_for_c.values():
            symptom_factor = 0
            disease_factor = 0
            age_factor = 0
            vaccination_factor = 0
            
            a2.append(val["age"])
                        
            for i in val["symptoms"]:
                symptom_factor += (1-symptom_factor)*symp_fac[i]
            
            for i in val["diseases"]:
                disease_factor += (1-disease_factor)*dis_fac[i]
            
            got_age = val["age"]
            age_info_bar.append(val["age"])
            age_factor = age_fac[str( int(got_age/5)*5 ) + "-" + str(int((got_age+5)/5)*5 - 1)]
            
            age_info.append(int(val["age"]))
            
            vaccination_factor = vac_fac[val["vaccinated"]]
            
            h_prob.append(symptom_factor * age_factor * vaccination_factor + ( 1 - symptom_factor * age_factor * vaccination_factor) * ( disease_factor*math.ceil(symptom_factor)*age_factor*vaccination_factor ))
            
            if "fever" in val["symptoms"]:
                fever_h_prob.append((symptom_factor + ( 1 - symptom_factor) * disease_factor * math.ceil(symptom_factor) ) *age_factor * vaccination_factor )
            else:
                fever_h_prob.append(0)
                
            if "dry_cough" in val["symptoms"]:
                cough_h_prob.append((symptom_factor + ( 1 - symptom_factor) * disease_factor * math.ceil(symptom_factor) ) *age_factor * vaccination_factor )
            else:
                cough_h_prob.append(0)
            
            if "tiredness" in val["symptoms"]:
                tiredness_h_prob.append((symptom_factor + ( 1 - symptom_factor) * disease_factor * math.ceil(symptom_factor) ) *age_factor * vaccination_factor )
            else:
                tiredness_h_prob.append(0)
            
            if "hypertension" in val["diseases"]:
                hypertension_h_prob.append((symptom_factor + ( 1 - symptom_factor) * disease_factor * math.ceil(symptom_factor) ) *age_factor * vaccination_factor )
            else:
                hypertension_h_prob.append(0)
                        
            if "lipid_metabolism" in val["diseases"]:
                lipid_metabolism_h_prob.append((symptom_factor + ( 1 - symptom_factor) * disease_factor * math.ceil(symptom_factor) ) *age_factor * vaccination_factor )
            else:
                lipid_metabolism_h_prob.append(0)
                
            
        stand_age_inf = [0 for i in range(21)]
        prop_age_ct_inf = [0 for i in range(21)]
        prop_age_tot_inf = [0 for i in range(21)]
        
        g1 = []
        g2 = []
        g3 = []
        g4 = []
          
                
        c_prob = []
                
        for i in range(len(h_prob)):
            num_of_contacts = random.randint(0, 10)
                
            contact_prob = 0
            stand_contact_prob = 0
            
            for contacts in range(num_of_contacts):
                signal_strength = random.randint(-120, -24)

                time_of_contact = random.randint(0, 100)
                
                opponent_probability = random.random()
                
                M = 2
                signal_strength_factor = 1 - math.exp(-math.log(16/3)*(10**((-69-signal_strength)/(10*M))))
                time_of_contact_factor = 1 - math.exp(-math.log(100/12)*(time_of_contact*60/1200))
                
                contact_prob += (1 - contact_prob)*(signal_strength_factor * time_of_contact_factor * opponent_probability)
                
                if time_of_contact >= 15 and pow(10, (-69-signal_strength)/(10*M)) <= 1.8:
                    stand_contact_prob = max(stand_contact_prob, opponent_probability)
                
            c_prob.append(contact_prob)
            
            age_infection_info[int(data_for_c[i]["age"]/5)] += 1
            
            if stand_contact_prob > 0.6:
                stand_age_inf[int(data_for_c[i]["age"]/5)] += 1
            
            if contact_prob > 0.6:
                prop_age_ct_inf[int(data_for_c[i]["age"]/5)] += 1
            
            if contact_prob + (1 - contact_prob)*h_prob[i] > 0.6:
                prop_age_tot_inf[int(data_for_c[i]["age"]/5)] += 1
            
            if "fever" in data_for_c[i]["symptoms"]:
                stand_fever_prob.append(stand_contact_prob)
                # g4.append(stand_contact_prob)
                # g2.append(h_prob[i] + (1-h_prob[i])*stand_contact_prob)
                # g3.append(contact_prob)
                # g1.append(contact_prob + (1-contact_prob)*h_prob[i])
                
            if "hypertension" in data_for_c[i]["diseases"]:
                stand_hyper_prob.append(stand_contact_prob)
                # g4.append(stand_contact_prob)
                # g2.append(h_prob[i] + (1-h_prob[i])*stand_contact_prob)
                # g3.append(contact_prob)
                # g1.append(contact_prob + (1-contact_prob)*h_prob[i])
            
            if "dry_cough" in data_for_c[i]["symptoms"]:
                stand_cough_prob.append(stand_contact_prob)
                # g4.append(stand_contact_prob)
                # g2.append(h_prob[i] + (1-h_prob[i])*stand_contact_prob)
                # g3.append(contact_prob)
                # g1.append(contact_prob + (1-contact_prob)*h_prob[i])
            
            if "tiredness" in data_for_c[i]["symptoms"]:
                stand_tired_prob.append(stand_contact_prob)
                # g4.append(stand_contact_prob)
                # g2.append(h_prob[i] + (1-h_prob[i])*stand_contact_prob)
                # g3.append(contact_prob)
                # g1.append(contact_prob + (1-contact_prob)*h_prob[i])
                
            if "lipid_metabolism" in data_for_c[i]["diseases"]:
                stand_lipid_prob.append(stand_contact_prob)
                # g4.append(stand_contact_prob)
                # g2.append(h_prob[i] + (1-h_prob[i])*stand_contact_prob)
                # g3.append(contact_prob)
                # g1.append(contact_prob + (1-contact_prob)*h_prob[i])
            
            stand_c_prob.append(stand_contact_prob)
            stand_tot_prob.append(stand_contact_prob + (1 - stand_contact_prob)*h_prob[i])
            
            fever_c_prob.append(contact_prob)
                
            cough_c_prob.append(contact_prob)
            
            tiredness_c_prob.append(contact_prob)
                
        # print(asymp)
            
        x_axis = [i+1 for i in range(len(h_prob))]
        
        both_prob = [[h_prob[i], c_prob[i]] for i in range(len(h_prob))]
        tot_prob = [h_prob[i] + (1 - h_prob[i])*c_prob[i] for i in range(len(h_prob))]
        
        a1 = [i for i in tot_prob]
        f1 = [i for i in stand_c_prob]
        
        #             *****************************    AGE SPECIFIC BARS   *****************************
        
        # plt.bar([(i+1)*5-1-2.5 for i in range(len(stand_age_inf))], stand_age_inf, width=1, color="skyblue")
        # plt.bar([(i+1)*5-2.5 for i in range(len(prop_age_ct_inf))], prop_age_tot_inf, width=1, color="blue")
        # plt.bar([(i+1)*5+1-2.5 for i in range(len(age_infection_info))], age_infection_info, width=1, color="yellowgreen")
        # plt.legend(labels=["Standard Model", "Proposed Mdoel", "Truly infected"])
        # plt.show()
        
        # plt.plot(x_axis, h_prob)
        # plt.plot(x_axis, c_prob)
        # plt.plot(x_axis, tot_prob)
        # plt.plot(x_axis, [both_prob[i][0]+(1-both_prob[i][0])*both_prob[i][1] for i in range(len(tot_prob))])
        
        # for i in range(len(fever_h_prob)):
        #     if fever_h_prob[i] != 0:
        #         fever_tot_prob.append(fever_h_prob[i] + (1 - fever_h_prob[i])*fever_c_prob[i])
        
        # fever_tot_prob.sort()
        # plt.plot([i+1 for i in range(len(fever_tot_prob))], fever_tot_prob)
        
        # h_prob.sort()
        # plt.plot([i+1 for i in range(len(h_prob))], h_prob)
        
        # c_prob.sort()
        # plt.plot([i+1 for i in range(len(c_prob))], c_prob)
        
                
        print("&&&&&&&&&&&&&&&&&&&&&&&&&&&")
        print(len(fever_c_prob), len(fever_h_prob))
                
        num_safe = 0
        num_low_risk = 0
        num_moderate_risk = 0
        num_high_risk = 0
        num_very_high_risk = 0
        num_infected = 0
        
        for i in tot_prob:
            if i > 0 and i < 0.2:
                num_safe += 1
            elif i >= 0.2 and i < 0.4:
                num_low_risk += 1
            elif i >= 0.4 and i < 0.6:
                num_moderate_risk += 1
            elif i >= 0.6 and i < 0.8:
                num_high_risk += 1
            elif i >= 0.8 and i < 1:
                num_very_high_risk += 1
            else:
                num_infected += 1
        
        
        print("safe :", num_safe)
        print("low :", num_low_risk)
        print("moderate :", num_moderate_risk)
        print("high :", num_high_risk)
        print("very_high : ", num_very_high_risk)
        print("infected :", num_infected)
                
        print("Proposed Solution Accuracy 1 :", (num_high_risk + num_very_high_risk + num_infected) / (num_infected + num_high_risk + num_low_risk + num_moderate_risk + num_safe + num_very_high_risk) * 100, "%")
        print("Proposed Solution Accuracy 2 :", (num_very_high_risk + num_infected) / (num_infected + num_high_risk + num_low_risk + num_moderate_risk + num_safe + num_very_high_risk) * 100, "%")
                
        
        
        
                                                    ####################### Save in database and report to user ######################

                                                    ####################### Authority Access ######################
                                                    
        # for medical staff : They can directly add&update data after lab test results
        
        # for police authority :
        
        # yellow_color = Color("yellow")
        # colors = list(yellow_color.range_to(Color("red"), 250))
        
        
        # for i in range(1000):
        #     random_x = random.randint(100, 1100)
        #     random_y = random.randint(100, 500)
        #     self.canvas.create_oval(random_x-3, random_y-3, random_x+3, random_y+3, fill="yellow", outline="green")
        
        # # defining random locations for lorge number of people gatherings
        
        # for i in tot_prob[0:200]:
        #     c = colors[int(i*len(colors))]
        #     random_x = random.randint(100, 1100)
        #     random_y = random.randint(100, 500)
        #     self.canvas.create_oval(random_x-3, random_y-3, random_x+3, random_y+3, fill=c, outline=c)
            
        # for i in tot_prob[200:250]:
        #     c = colors[int(i*len(colors))]
        #     random_x = random.randint(400, 550)
        #     random_y = random.randint(250, 350)
        #     self.canvas.create_oval(random_x-3, random_y-3, random_x+3, random_y+3, fill=c, outline=c)

        # defining random location for normal interactions

        # for i in tot_prob[0:250]:
        #     c = colors[int(i*len(colors))]
        #     random_x = random.randint(100, 1100)
        #     random_y = random.randint(100, 500)
        #     self.canvas.create_oval(random_x-3, random_y-3, random_x+3, random_y+3, fill=c, outline=c)
        
        
        
        # Standard solution
        # Standart min time of contact for infection = 15 minutes = 900 seconds
        # Standard distance for infection = 6 feet = 1.8 meter

    
                
        stand_inf = 0
        for i in stand_tot_prob:
            if i >= 0.6:
                stand_inf += 1
        stand_accuracy = stand_inf/len(stand_tot_prob)
        
        print("Standard method Accuracy :", (stand_accuracy*100), "%")
            
        tot_prob.sort()
        stand_tot_prob.sort()
        c_prob.sort()
        stand_c_prob.sort()
        
        ##########################          Infection probability compatision proposed model vs Dist-time model         ##########################
        
        # plt.plot([i+1 for i in range(len(tot_prob))], tot_prob)
        # plt.plot([i+1 for i in range(len(stand_tot_prob))], stand_tot_prob)
        # plt.plot([i+1 for i in range(len(c_prob))], c_prob, "--")
        # plt.plot([i+1 for i in range(len(stand_c_prob))], stand_c_prob, "--")
        # plt.legend(labels=['proposed model total prob', 'dist-time model total prob', 'proposed model contact prob', 'dist-time model contact prob'])
        
        proposed_model_accuracy = [0 for i in range(101)]
        cur_set_threshold = 0
        cur_set_users = 0
        accuracy_index = 0
        i_ind = 0
        i = tot_prob[i_ind]
        number = 0
        while i_ind < 1448:
            number += 1
            if i < cur_set_threshold:
                cur_set_users += 1
                i_ind += 1
                if i_ind == 1448:
                    proposed_model_accuracy[accuracy_index] = 1-cur_set_users/1448
                    break
                i = tot_prob[i_ind]
            else:
                cur_set_threshold += 0.01
                proposed_model_accuracy[accuracy_index] = 1 - cur_set_users/1448
                accuracy_index += 1
        
        # proposed_model_accuracy.reverse()
        proposed_model_accuracy = proposed_model_accuracy[1:]
        
        dist_time_model_accuracy = [0 for i in range(101)]
        cur_set_threshold = 0
        cur_set_users = 0
        accuracy_index = 0
        i_ind = 0
        i = stand_tot_prob[i_ind]
        number = 0
        while i_ind < 1448:
            number += 1
            if i < cur_set_threshold:
                cur_set_users += 1
                i_ind += 1
                if i_ind == 1448:
                    dist_time_model_accuracy[accuracy_index] = 1-cur_set_users/1448
                    break
                i = stand_tot_prob[i_ind]
            else:
                cur_set_threshold += 0.01
                dist_time_model_accuracy[accuracy_index] = 1 - cur_set_users/1448
                accuracy_index += 1
        
        # dist_time_model_accuracy.reverse()
        dist_time_model_accuracy = dist_time_model_accuracy[1:]
        
        
        #####################        Accuract comparision proposed model vs dist-time comparision variation with threshold     ######################
        
        
        # plt.plot([(i+1)/100 for i in range(100)], dist_time_model_accuracy)
        # plt.plot([(i+1)/100 for i in range(100)], proposed_model_accuracy)
        # plt.legend(labels=['Proposed model accuracy', 'Dist-time model accuracy'])
        
        fever_h_prob.sort()
        stand_fever_prob.sort()
        # cough_h_prob.sort()
        tiredness_h_prob.sort()
        stand_tired_prob.sort()

        
        # print(fever_h_prob[0:20])
        # print(stand_fever_prob[0:20])
        # print(tiredness_h_prob[0:20])
        
        # plt.plot([i+1 for i in range(len(fever_h_prob))], fever_h_prob)
        # plt.plot([i+1 for i in range(len(tiredness_h_prob))], tiredness_h_prob)
        # plt.plot([i+1 for i in range(len(stand_tired_prob))], stand_tired_prob)
        # plt.plot([i+1 for i in range(len(stand_fever_prob))], stand_fever_prob)
            
            
        
        
        


        #             *****************************    FEVER SPECIFIC PLOT   *****************************
                        
        # to_plot_for_fever = [fever_h_prob[i] for i in range(len(fever_h_prob))]
        
        # to_plot_for_fever.sort()
                
        # with_ct_for_fever = [0]
        # not_with_h_for_fever = [0]
        
        # for i in range(len(c_prob)):
        #     if "fever" in data_for_c[i]["symptoms"]:
        #         with_ct_for_fever.append(c_prob[i] + (1 - c_prob[i])*h_prob[i] )
        #         not_with_h_for_fever.append(c_prob[i])
        
        # with_ct_for_fever.sort()
        # not_with_h_for_fever.sort();
        
        # mm = with_ct_for_fever;
        # if len(mm) < len(stand_fever_prob):
        #     mm = stand_fever_prob
            
        # stand_fever_prob.sort()
        
        
        # plt.plot([i+1 for i in range(len(mm))], [0 for i in range(len(mm))], "--")
        # plt.plot([i+1 for i in range(len(mm))], [0.2 for i in range(len(mm))], "--")
        # plt.plot([i+1 for i in range(len(mm))], [0.4 for i in range(len(mm))], "--")
        # plt.plot([i+1 for i in range(len(mm))], [0.6 for i in range(len(mm))], "--")
        # plt.plot([i+1 for i in range(len(mm))], [0.8 for i in range(len(mm))], "--")
        # plt.plot([i+1 for i in range(len(mm))], [1 for i in range(len(mm))], "--")
        
        
        # plt.plot([i+1 for i in range(len(stand_fever_prob))], stand_fever_prob)
        # plt.plot([i+1 for i in range(len(not_with_h_for_fever))], not_with_h_for_fever)
        # plt.plot([i+1 for i in range(len(with_ct_for_fever))], with_ct_for_fever)
        
        # prop_inf = 0
        # stand_inf = 0
        
        # for i in with_ct_for_fever:
        #     if i > 0.6:
        #         prop_inf += 1
                
        # for i in stand_fever_prob:
        #     if i > 0.6:
        #         stand_inf += 1
            
        # print("Accuracy with Standatd Model: ", stand_inf/len(stand_fever_prob)*100, "%")
        # print("Axxuracy with Proposed Model: ", prop_inf/len(with_ct_for_fever)*100, "%")
        
        
        # plt.legend(labels=['Not infected', 'Safe limit', 'Moderate limit', 'Threshold limit', 'High risk limit', 'Very high risk limit' , 'SM Total Infection Prob.', 'PM CT Infection Prob.', "PM Total Indection Prob."], loc="lower right")
        # plt.show()
        
        
        
        #             *****************************    TIREDNESS SPECIFIC PLOT   *****************************
                        
        # to_plot_for_tired = [tiredness_h_prob[i] for i in range(len(tiredness_h_prob))]
        
        # to_plot_for_tired.sort()
                
        # total_for_tired = [0]
        # ct_for_tired = [0]
        
        # for i in range(len(c_prob)):
        #     if "tiredness" in data_for_c[i]["symptoms"]:
        #         total_for_tired.append(c_prob[i] + (1 - c_prob[i])*h_prob[i])
        #         ct_for_tired.append(c_prob[i])
        
        # total_for_tired.sort()
        # ct_for_tired.sort()
        
        # mm = total_for_tired;
        # if len(mm) < len(stand_tired_prob):
        #     mm = stand_tired_prob
            
        # plt.plot([i+1 for i in range(len(mm))], [0.6 for i in range(len(mm))], "--")
        
        # stand_tired_prob.sort()
        
        # plt.plot([i+1 for i in range(len(stand_tired_prob))], stand_tired_prob)
        
        # plt.plot([i for i in range(len(ct_for_tired))], ct_for_tired)
        
        # plt.plot([i+1 for i in range(len(total_for_tired))], total_for_tired)
        
        
        
        
        # prop_inf = 0
        # stand_inf = 0
        
        # for i in total_for_tired:
        #     if i > 0.6:
        #         prop_inf += 1
                
        # for i in stand_tired_prob:
        #     if i > 0.6:
        #         stand_inf += 1
            
        # print("Accuracy with Standatd Model: ", stand_inf/len(stand_tired_prob)*100, "%")
        # print("Axxuracy with Proposed Model: ", prop_inf/len(total_for_tired)*100, "%")
        
        # plt.legend(labels=['Threshold limit', 'SM Total Infection Prob.', 'PM CT Infection Prob.', "PM Total Indection Prob."])
        
        # plt.show()
        
        
        
        
        #             *****************************    HYPERTENSION SPECIFIC PLOT   *****************************
        
        # to_plot_for_hypertension = [hypertension_h_prob[i] for i in range(len(hypertension_h_prob))]
        
        # to_plot_for_hypertension.sort()
                
        # total_for_hyper = [0]
        # ct_for_hyper = [0]
        
        # for i in range(len(c_prob)):
        #     if "hypertension" in data_for_c[i]["diseases"]:
        #         total_for_hyper.append(c_prob[i] + (1 - c_prob[i])*h_prob[i])
        #         ct_for_hyper.append(c_prob[i])
                
        
        # total_for_hyper.sort()
        # ct_for_hyper.sort()
        
        # mm = total_for_hyper;
        # if len(mm) < len(stand_hyper_prob):
        #     mm = stand_hyper_prob
        
        # plt.plot([i+1 for i in range(len(mm))], [0.6 for i in range(len(mm))], "--")
        
        # stand_hyper_prob.sort()
        
        # plt.plot([i+1 for i in range(len(stand_hyper_prob))], stand_hyper_prob)
        
        # plt.plot([i for i in range(len(ct_for_hyper))], ct_for_hyper)
        
        # plt.plot([i for i in range(len(total_for_hyper))], total_for_hyper)
        
        # prop_inf = 0
        # stand_inf = 0
        
        # for i in total_for_hyper:
        #     if i > 0.6:
        #         prop_inf += 1
                
        # for i in stand_hyper_prob:
        #     if i > 0.6:
        #         stand_inf += 1
            
        # print("Accuracy with Standatd Model: ", stand_inf/len(stand_hyper_prob)*100, "%")
        # print("Axxuracy with Proposed Model: ", prop_inf/len(total_for_hyper)*100, "%")
            
        # plt.legend(labels=['Threshold limit', 'SM Total Infection Prob.', 'PM CT Infection Prob.', "PM Total Indection Prob."])
        
        # plt.show()
        
        
        # Lipid specail
        
        # to_plot_for_lipid = [lipid_metabolism_h_prob[i] for i in range(len(lipid_metabolism_h_prob))]
        
        # to_plot_for_lipid.sort()
                
        # total_for_lipid = [0]
        # ct_for_lipid = [0]
        
        # for i in range(len(c_prob)):
        #     if "lipid_metabolism" in data_for_c[i]["diseases"]:
        #         total_for_lipid.append(c_prob[i] + (1 - c_prob[i])*h_prob[i])
        #         ct_for_lipid.append(c_prob[i])
                
        
        # total_for_lipid.sort()
        # ct_for_lipid.sort()
        
        # mm = total_for_lipid;
        # if len(mm) < len(stand_lipid_prob):
        #     mm = stand_lipid_prob
            
        
        # plt.plot([i+1 for i in range(len(mm))], [0.6 for i in range(len(mm))], "--")
            
        # stand_lipid_prob.sort()
        
        # plt.plot([i+1 for i in range(len(stand_lipid_prob))], stand_lipid_prob)
                
        # plt.plot([i for i in range(len(ct_for_lipid))], ct_for_lipid)
        
        # plt.plot([i for i in range(len(total_for_lipid))], total_for_lipid)
        
        
        
        
        # prop_inf = 0
        # stand_inf = 0
        
        # for i in total_for_lipid:
        #     if i > 0.6:
        #         prop_inf += 1
                
        # for i in stand_lipid_prob:
        #     if i > 0.6:
        #         stand_inf += 1
            
        # print("Accuracy with Standatd Model: ", stand_inf/len(stand_lipid_prob)*100, "%")
        # print("Axxuracy with Proposed Model: ", prop_inf/len(total_for_lipid)*100, "%")
            
        
        
        # plt.legend(labels=['Threshold limit', 'SM Total Infection Prob.', 'PM CT Infection Prob.', "PM Total Indection Prob."])
        # plt.show()
        

        #1
        
        # plt.figure(figsize=(7, 4.5))
        # plt.plot([i+1 for i in range(len(tot_prob))], tot_prob)
        # plt.plot([i+1 for i in range(len(stand_tot_prob))], stand_tot_prob)
        
        # c_prob.sort()
        # plt.plot([i+1 for i in range(len(c_prob))], c_prob, "--")
        # plt.plot([i+1 for i in range(len(stand_c_prob))], stand_c_prob, "--")
        
        
        # plt.legend(labels=['PM Total IP', 'D-TM CT + PM HIP', 'PM CT IP', 'D-TM CT IP'], loc="lower right")
        
        # plt.xlabel("User", fontsize=15)
        # plt.ylabel("Infection Probability", fontsize=15)
        
        # plt.savefig("abcd.pdf", bbox_inches='tight')
        
        # plt.show()
        
        
        
        # g1.sort()
        # g2.sort()
        # g3.sort()
        # g4.sort()
        
        # plt.figure(figsize=(7, 4.5))
        # plt.plot([i+1 for i in range(len(g1))], g1)
        # plt.plot([i+1 for i in range(len(g2))], g2)
        
        # c_prob.sort()
        # plt.plot([i+1 for i in range(len(g3))], g3, "--")
        # plt.plot([i+1 for i in range(len(g4))], g4, "--")
        
        # plt.legend(labels=['PM Total IP', 'D-TM CT + PM HIP', 'PM CT IP', 'D-TM CT IP'], loc="lower right")
        
        # plt.xlabel("User", fontsize=15)
        # plt.ylabel("Infection Probability", fontsize=15)
        
        # plt.savefig("abcd.pdf", bbox_inches='tight')
        
        # plt.show()
        
        
        
        
        ##########################################
        
        
        dict_bar = {}
        
        db = {}
        
        for i in range(11):
            dict_bar[i] = []
            db[i] = []
        total_in_age = [0 for i in range(10)]
        
        b1 = [int((int(i)+10)/10) for i in a2]

        for i in b1:
            total_in_age[i-1] += 1
            
        for i in range(len(a1)):
            dict_bar[b1[i]].append(a1[i])
        
        for i in range(len(f1)):
            db[b1[i]].append(f1[i])
        
        
        for i in dict_bar.keys():
            dict_bar[i] = list(sorted(dict_bar[i]))
        
        for i in db.keys():
            db[i] = list(sorted(db[i]))
        
        
        arr1 = []
        arr2 = []
        
        
        for i in dict_bar.keys():
            te = 0
            for k in dict_bar[i]:
                if k >= 0.9:
                    te += 1
            arr1.append(te)
        
        for i in db.keys():
            te = 0
            for k in db[i]:
                if k >= 0.9:
                    te += 1
            arr2.append(te)
        
        plt.figure(figsize=(9.5, 5))
        
        plt.bar([(i-0.7+1)*10 for i in range(len(total_in_age))], total_in_age, 2)
        plt.bar([(i-0.5+1)*10 for i in range(len(arr1)-1)], arr1[1:], 2)
        plt.bar([(i-0.3+1)*10 for i in range(len(arr2)-1)], arr2[1:], 2)
        
        print(total_in_age)
        print(arr1)
        print(arr2)
        
        plt.xlabel("Age", fontsize=15)
        plt.ylabel("Number of infected users", fontsize=15)
        
        plt.legend(labels=["Truly infected users", "Infected users with PM", "Infected users with D-TM"], loc="upper right", fontsize=11)
        
        plt.savefig("abcd.pdf", bbox_inches='tight')
        
        plt.show()
        
        
        
        
        

task = covid_spread_analyser()
