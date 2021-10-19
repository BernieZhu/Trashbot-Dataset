import csv
import json

BATCH_ID='4574137'

with open('wrong_hit.txt'.format(BATCH_ID)) as f:
    wrong_hit = f.read().splitlines()
    # print(len(wrong_hit))

save_data = []
csv_columns = []
all = 0
wrong = 0
with open('csv/Batch_{}_batch_results.csv'.format(BATCH_ID), newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row['AssignmentStatus'] != 'Submitted':
            continue
        all += 1
        time_missing = False
        label_missing = False
        for i in range(1, 6):
            label_exist = len(row["Answer.verb{}".format(i)]) > 2 and len(row["Answer.object{}".format(i)]) > 2
            time_exist = len(row["Answer.start{}".format(i)]) > 2 and len(row["Answer.end{}".format(i)]) > 2
            # print(row["Answer.verb{}".format(i)], row["Answer.object{}".format(i)], row["Answer.start{}".format(i)], row["Answer.end{}".format(i)])
            # print(label_exist, time_exist)
            if (label_exist == False and time_exist == False):
                continue
            if (label_exist != time_exist):
                label_missing = True
                break
            for j in range (1, 5):
                index = ["zero", "one", "two", "three"]
                if j == 1:
                    start = row["Answer.start{}".format(i)]
                    end = row["Answer.end{}".format(i)]
                else:
                    if row["Answer.morethan{}{}".format(index[j-1], i)] != "on":
                        continue
                    start = row["Answer.start{}_{}".format(i,j)]
                    end = row["Answer.end{}_{}".format(i,j)]
                if (len(start) > 2) != (len(end) > 2):
                    time_missing = True
                    break

        if time_missing or label_missing:
            row['Reject']='Incomplete annotations'
            wrong += 1
        elif row['HITId'] in wrong_hit:
            row['Reject']='Wrong annotations'
            wrong += 1 
        else:
            row['Approve']='x'
        save_data.append(row)
        csv_columns = row.keys()
    print('Wrong annos {}/{}={:.2%}'.format(wrong, all, wrong/all))

with open('csv/rev_'+BATCH_ID+'.csv', 'w') as save_csv:
    writer = csv.DictWriter(save_csv, fieldnames=csv_columns)
    writer.writeheader()
    for row in save_data:
        writer.writerow(row)