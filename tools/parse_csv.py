import csv
import requests
import argparse
import os
import logging
from logging import handlers

parser = argparse.ArgumentParser()
parser.add_argument("--csv", type=str, default="4533959")
parser.add_argument("--hit", type=str, default="")
parser.add_argument("--save_videos", action='store_const', const='save', default=False)
parser.add_argument("--vis_label", action='store_const', const='save', default=False)
args=parser.parse_args()

class Logger(object):
    level_relations = {
        'debug':logging.DEBUG,
        'info':logging.INFO,
        'warning':logging.WARNING,
        'error':logging.ERROR,
        'crit':logging.CRITICAL
    }

    def __init__(self,filename,level='info',when='D',backCount=3,fmt='',screen=False):
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)
        self.logger.setLevel(self.level_relations.get(level))
        if screen:
            sh = logging.StreamHandler()
            sh.setFormatter(format_str)
            self.logger.addHandler(sh)
        th = handlers.TimedRotatingFileHandler(filename=filename,when=when,backupCount=backCount,encoding='utf-8')
        th.setFormatter(format_str)
        self.logger.addHandler(th)

def srt_format(start, end=""):
    s_min = int(start.split('.')[0]) // 60
    s_sec = int(start.split('.')[0]) % 60
    s_ms = int(start.split('.')[1]) * 100
    if end:
        e_min = int(end.split('.')[0]) // 60
        e_sec = int(end.split('.')[0]) % 60
        e_ms = int(end.split('.')[1]) * 100
    else:
        e_min = int(start.split('.')[0]) // 60
        e_sec = int(start.split('.')[0]) % 60
        e_ms = int(start.split('.')[1]) * 100 + 800 # contact notification lasts 800 ms
        if e_ms >= 1000:
            e_sec +=1 
        e_ms = e_ms % 1000
    return "00:{:0>2d}:{:0>2d},{:0>3d} --> 00:{:0>2d}:{:0>2d},{:0>3d}".format(s_min, s_sec, s_ms, e_min, e_sec, e_ms)

with open('Batch_{}_batch_results.csv'.format(args.csv), newline='') as csvfile:
    log = Logger('all.log', level='info',screen=True)
    reader = csv.DictReader(csvfile)
    for row in reader:
        if (args.hit and row['HITId'] != args.hit):
            continue
        if (row['AssignmentStatus'] == 'Rejected'):
            continue
        url = row['Input.url']
        name = url[-12:-4]
        log.logger.info("========================")
        log.logger.info("Video: {}.mp4".format(name))
        log.logger.info("HIT ID: {}".format(row["HITId"]))
        srt = Logger('videos/{}.srt'.format(name), level='info')

        log.logger.info("Low-quality: {}".format(row["Answer.invalid"] if row["Answer.invalid"] else 'False'))
        log.logger.info("Rotated: {}".format(row["Answer.rotated"] if row["Answer.invalid"] else 'False'))

        srt_line = 1
        for i in range(1,6):
            action_exists = len(row["Answer.verb{}".format(i)]) > 2 or len(row["Answer.object{}".format(i)]) > 2 \
                or len(row["Answer.start{}".format(i)]) > 2 or len(row["Answer.end{}".format(i)]) > 2 \
                or len(row["Answer.contact{}".format(i)]) > 2
            if (not action_exists):
                continue
            verb = row["Answer.verb"+str(i)]
            object = row["Answer.object"+str(i)]
            log.logger.info("|--Activity: {}".format(i))
            log.logger.info("  |--Verb: {}".format(verb))
            log.logger.info("  |--Object: {}".format(object))
            for j in range (1, 5):
                index = ["zero", "one", "two", "three"]
                if j == 1:
                    start = row["Answer.start{}".format(i)]
                    end = row["Answer.end{}".format(i)]
                    contact = row["Answer.contact{}".format(i)]
                    succ = row["Answer.succ{}".format(i)]
                else:
                    if row["Answer.morethan{}{}".format(index[j-1], i)] != "on":
                        continue
                    start = row["Answer.start{}_{}".format(i,j)]
                    end = row["Answer.end{}_{}".format(i,j)]
                    contact = row["Answer.contact{}_{}".format(i,j)]
                    succ = row["Answer.succ{}{}".format(i,j)]
                succ = succ if succ else 'False'
                log.logger.info("  |--Trial: {}".format(j))
                log.logger.info("    |--Start time: {}".format(start))
                log.logger.info("    |--End time: {}".format(end))
                log.logger.info("    |--Contact time: {}".format(contact))
                log.logger.info("    |--Successful: {}".format(succ))
                if(args.vis_label):
                    srt.logger.info(srt_line)
                    srt.logger.info(srt_format(start, end))
                    srt.logger.info("{} {}".format(verb, object))
                    srt.logger.info("No. {} trial, {}\n".format(j, succ))
                    srt_line += 1
                    srt.logger.info(srt_line)
                    srt.logger.info(srt_format(contact))
                    srt.logger.info("first contacts with the object\n")
                    srt_line += 1
                    
        if (args.save_videos):
            f = open('videos/{}.mp4'.format(name), 'wb')
            data = requests.get(url)
            f.write(data.content)
            if(args.vis_label):
                os.system("ffmpeg -i videos/{}.mp4 -vf subtitles=videos/{}.srt videos/{}_sub.mp4".format(name,name,name))