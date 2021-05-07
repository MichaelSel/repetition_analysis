import json
import csv
import scipy.stats
import numpy as np
import reformat_data
import statistics as stat

#define directories
processed_dir = './processed'
analyzed_dir = './analyzed'
all_data_path = processed_dir + "/repetition_all_subjects.json"


responses_excluded=0
def get_json(path):
        json_file = open(path)
        json_file = json_file.read()
        return json.loads(json_file)

def mean(ls):
        if len(ls)>0:
                return stat.mean(ls)
        return float('NaN')

def make_csv(subs, keys_to_store,filename='/repetition_results_new.csv'):
        subs = [sub for sub in subs if 'analyzed' in sub] #only analyze subjects that have data
        with open(analyzed_dir + filename, 'w', newline='') as file:

                writer = csv.writer(file)
                writer.writerow(['Subject_ID','excluded'] + keys_to_store)
                for s in subs:
                        values = [s['id'],s['excluded']]
                        for key in keys_to_store:
                                if(key not in s['analyzed']): values.append("ERROR")
                                values.append(s['analyzed'][key])
                        writer.writerow(values)
        print("Aggregate analysis file saved.")
        return False

def make_json(subs):
        json_export = json.dumps(subs)
        f = open(analyzed_dir + "/repetition_results_new.json", "w")
        f.write(json_export)
        f.close()
        print("saved data.")

reformat_data.run()

all_subjects = get_json(all_data_path)
for s in all_subjects: #every subject in the cohort
        s['excluded']=False
        s['analyzed']={
                'block':[]
        }
        block_ids_to_run = [block['block'] for block in s['blocks']]

        #you can run specific blocks by uncommenting below
        # block_ids_to_run = [1]

        #This task doesn't have a practice block
        # #don't run the practice block:
        # block_ids_to_run.remove(0) #practice block is index 0

        for block in s['blocks']: #every block for the subject
                if(block['block'] not in block_ids_to_run): continue #if it's not in the blocks we want, skip it
                data = {
                        'trials_total': 0,
                        'chose_diatonic': 0,
                        'chose_chromatic': 0,
                        'rts':[],
                        'rt_diatonic':[],
                        'rt_chromatic': [],
                        'pressed_button1':0,
                        'pressed_button2': 0,
                }
                for Q in block['repetition']: #Q is every question/trial in the block
                        Q['excluded'] = False
                        # Trial level Time-based exclusion should be written here

                        if(Q['name']!='choice'): continue #if not a choice question, continue to next Q

                        if(Q['response']=='1st'):
                                response_pos = 0
                                data['pressed_button1']+=1
                        elif (Q['response'] == '2nd'):
                                response_pos = 1
                                data['pressed_button2'] += 1
                        else:
                                print("there was an error.")


                        # increment trial tally
                        data['trials_total'] +=1
                        data['rts'].append(Q['rt'])
                        if(Q['order'][response_pos]=='diatonic'):
                                data['chose_diatonic'] += 1
                                data['rt_diatonic'].append(Q['rt'])
                        elif (Q['order'][response_pos] == 'chromatic'):
                                data['chose_chromatic'] += 1
                                data['rt_chromatic'].append(Q['rt'])


                s['analyzed']['block'].append(data)

                #once all the per block data was collected(above), append it to subject totales:
                #if the key doesn't exist in the subject level, create it, otherwise, add to it
                for key in data:
                        try:
                                s['analyzed'][key] += data[key]
                        except:
                                s['analyzed'][key] = data[key]



        if(s['analyzed']['trials_total']!=0):
                s['analyzed']['%_diatonic'] = s['analyzed']['chose_diatonic'] / s['analyzed']['trials_total']
                s['analyzed']['%_chromatic'] = s['analyzed']['chose_chromatic'] / s['analyzed']['trials_total']
                s['analyzed']['rt_diatonic'] = mean(s['analyzed']['rt_diatonic'])
                s['analyzed']['rt_chromatic'] = mean(s['analyzed']['rt_chromatic'])
                s['analyzed']['rt'] = mean(s['analyzed']['rts'])
                s['analyzed']['rt_diatonic:average'] = s['analyzed']['rt_diatonic'] / s['analyzed']['rt']
                s['analyzed']['rt_chromatic:average'] = s['analyzed']['rt_chromatic'] / s['analyzed']['rt']

for i in range(len(all_subjects)-1,0,-1):
        subject = all_subjects[i]
        true_trials = subject['analyzed']['trials_total']

        # # exclude participants who have a bias toward a certain button (press one button more than 2 times the other button)
        # if (max(s['analyzed']['pressed_button1'], s['analyzed']['pressed_button2']) / min(
        #         s['analyzed']['pressed_button1'], s['analyzed']['pressed_button2']) > 2):
        #         s['excluded']=True
        #         print("Excluded. Button bias")
        #         # all_subjects.pop(i)
        #         continue
        # #exclude subjects with fewer than 10 responses in either condition (not including neithers)
        # if(s['analyzed']['trials_chromatic'] - s['analyzed']['chromatic_neither']<10):
        #         s['excluded'] = True
        #         print("Excluded. Less than 10 responses")
        #         # all_subjects.pop(i)
        #         continue
        # if (s['analyzed']['trials_diatonic'] - s['analyzed']['diatonic_neither'] < 10):
        #         s['excluded'] = True
        #         print("Excluded. Less than 10 responses")
        #         # all_subjects.pop(i)
        #         continue


keys_to_store = ['trials_total', 'chose_diatonic', 'chose_chromatic','%_diatonic', '%_chromatic', 'rt_diatonic', 'rt_chromatic', 'rt','rt_diatonic:average','rt_chromatic:average', 'pressed_button1', 'pressed_button2']

make_csv(all_subjects, keys_to_store)

make_json(all_subjects)



