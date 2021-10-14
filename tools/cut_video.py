import os
from tqdm import tqdm

def run_ffmpeg(start, end, video, num):
    if end != '':
        cmd = "ffmpeg -hide_banner -loglevel warning -ss 00:{} -to 00:{} -i long_videos/{}.MP4 -vcodec copy -acodec copy test/{}-{}.mp4".format(start, end, video, video, str(num))
    else:
        cmd = "ffmpeg -hide_banner -loglevel warning -ss 00:{} -i long_videos/{}.MP4 -vcodec copy -acodec copy test/{}-{}.mp4".format(start, video, video, str(num))
    os.system(cmd)

count = 0
for root, dirs, files in os.walk('./long_videos'):
    for file in tqdm(files):
        if file.endswith(".txt"):
            # print(file)
            with open('{}/{}'.format('long_videos', file)) as f:
                lines = f.readlines()
                count += len(lines)
                video = lines[0].rstrip()
                # print(lines)
                for i in range(1, len(lines)):
                    if i == 1:
                        start = '00:00'
                    else:
                        start = lines[i-1].rstrip()
                    end = lines[i].rstrip()
                    num = i
                    run_ffmpeg(start, end, video, num)
                start = lines[-1].rstrip()
                num = len(lines)
                run_ffmpeg(start, '', video, num)
print(count)