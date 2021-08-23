from os import stat_result
import cv2
import numpy as np
import csv
import requests
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--save_videos", action='store_const', const='save', default=False)
parser.add_argument("--HITId", type=str, default="")
args=parser.parse_args()

with open('Batch_4533959_batch_results.csv', newline='') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		if ( args.HITId and row['HITId'] != args.HITId):
			continue
		if (row['AssignmentStatus'] == 'Rejected'):
			continue
		url = row['Input.url']
		name = url[-12:-4]
		print("========================")
		print("Video: {}.mp4".format(name))
		print("HIT ID: {}".format(row["HITId"]))
		if (args.save_videos):
			f = open('videos/{}.mp4'.format(name), 'wb')
			data = requests.get(url)
			f.write(data.content)

		print("Low-quality: {}".format(row["Answer.invalid"] if row["Answer.invalid"] else 'False'))
		print("Rotated: {}".format(row["Answer.rotated"] if row["Answer.invalid"] else 'False'))

		for i in range(1,6):
			act = row['Input.url']
			action_exists = len(row["Answer.verb"+str(i)]) > 2 or len(row["Answer.object"+str(i)]) > 2 \
				or len(row["Answer.start{}".format(i)]) > 2 or len(row["Answer.end{}".format(i)]) > 2 \
				or len(row["Answer.contact{}".format(i)]) > 2
			if (not action_exists):
				continue
			print("|--Activity: {}".format(i))
			print("  |--Verb: {}".format(row["Answer.verb"+str(i)]))
			print("  |--Object: {}".format(row["Answer.object"+str(i)]))
			for j in range (1, 5):
				index = ["zero", "one", "two", "three"]
				if j == 1:
					print("  |--Trial {}".format(j))
					print("    |--Start time: {}".format(row["Answer.start{}".format(i)]))
					print("    |--End time: {}".format(row["Answer.end{}".format(i)]))
					print("    |--Contact time: {}".format(row["Answer.contact{}".format(i)]))
					succ = row["Answer.succ{}".format(i)]
					print("    |--Successful: {}".format(succ if succ else 'False'))
				else:
					if row["Answer.morethan{}{}".format(index[j-1], i)] != "on":
						continue
					print("  |--Trial: {}".format(j))
					print("    |--Start time: {}".format(row["Answer.start{}_{}".format(i,j)]))
					print("    |--End time: {}".format(row["Answer.end{}_{}".format(i,j)]))
					print("    |--Contact time: {}".format(row["Answer.contact{}_{}".format(i,j)]))
					succ = row["Answer.succ{}{}".format(i,j)]
					print("    |--Successful: {}".format(succ if succ else 'False'))