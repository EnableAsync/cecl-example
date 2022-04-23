# -!- coding: utf-8 -!-
import argparse
import itertools
import sys
import threading
import time
import numpy as np
import cv2
import paho.mqtt.client as mqtt


def parse_arguments(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--camera', type=int,
                        help='camera/ip camera',
                        default=0)
    parser.add_argument('--show', action='store_true',
                        help='display or not ',
                        default=False)
    parser.add_argument('--host', type=str,
                        help='mqtt broker host',
                        default='127.0.0.1')
    parser.add_argument('--port', type=int,
                        help='mqtt broker port',
                        default=1883)
    parser.add_argument('--topic', type=str,
                        help='mqtt topic',
                        default='camera'
                        )
    return parser.parse_args(argv)


def main(args):
    num = 0
    global flag
    global over
    global image
    over = True
    flag = False

    client = mqtt.Client()
    client.connect(args.host, args.port)

    camera = cv2.VideoCapture(args.camera)

    lastFrame1 = None
    lastFrame2 = None
    count = 0
    frame_start_time = 0
    fps = 0
    while camera.isOpened():
        (ret, frame) = camera.read()
        image = frame
        frame = cv2.resize(frame, (640, 480), interpolation=cv2.INTER_CUBIC)
        if lastFrame2 is None:
            if lastFrame1 is None:
                lastFrame1 = frame
            else:
                lastFrame2 = frame
                global frameDelta1
                frameDelta1 = cv2.absdiff(lastFrame1, lastFrame2)
            continue
        frameDelta2 = cv2.absdiff(lastFrame2, frame)
        thresh = cv2.bitwise_and(frameDelta1, frameDelta2)
        thresh2 = thresh.copy()
        lastFrame1 = lastFrame2
        lastFrame2 = frame.copy()
        frameDelta1 = frameDelta2
        thresh = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(thresh, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=3)
        thresh = cv2.erode(thresh, None, iterations=1)
        List = list(itertools.chain.from_iterable(thresh.tolist()))
        if (List.count(255) > 1000):
            if (count == 3):
                print("Moving object detected")
                flag = True
                publish_status(client, args.topic, "Moving")
                # if (over):
                #     print("Start the video")
                #     num += 1
                #     threading.Thread(target=storeVideo, args=(num,)).start()
            else:
                count = count + 1
        else:
            print("Still picture")
            flag = False
            count = 0
            publish_status(client, args.topic, "Still")
        cv2.putText(frame, "FPS:   " + str(fps.__round__(2)), (20, 100), cv2.FONT_ITALIC, 0.8, (0, 255, 0), 1,
                    cv2.LINE_AA)
        isShow = args.show
        if (isShow):
            cv2.imshow("frame", frame)
            cv2.imshow("thresh", thresh)
            cv2.imshow("threst2", thresh2)
        # if cv2.waitKey(200) & 0xFF == ord('q'):
        #     break
        now = time.time()
        frame_time = now - frame_start_time
        fps = 1.0 / frame_time
        frame_start_time = now
    camera.release()
    # cv2.destroyAllWindows()


def publish_status(client: mqtt.Client, topic: str, state: str):
    client.publish(topic, state)

def storeVideo(num):
    global image
    global over
    over = False
    global flag
    out_fps = 3
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out1 = cv2.VideoWriter('./data/video/' + str(num) +
                           ".avi", fourcc, out_fps, (640, 480))
    start = time.time()
    count = 5
    image0 = np.zeros(image.shape)
    while (True):
        if(image != image0).all():
            out1.write(image)
            image = image0
        else:
            continue
        end = time.time()
        if(flag == False):
            if (end - start >= 10):
                if (flag):
                    continue
                    start = end
                    count = 0
                else:
                    if (count == 5):
                        over = True
                        print("End of the video")
                        break
                    else:
                        count += 1
                        continue
        else:
            start = end
    out1.release()


if __name__ == '__main__':
    main(parse_arguments(sys.argv[1:]))
