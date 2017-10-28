from sys import argv
from threading import Thread
from time import sleep
from picamera import PiCamera
from time import sleep
from google.cloud import storage
import datetime



from nuimo import Controller, ControllerManager, ControllerListener, LedMatrix, GestureEvent, Gesture, LedMatrix


class NuimoListener(ControllerListener):
    def __init__(self, controller):
        self.controller = controller
        print("init");

		# Enable Storage
        self.client = storage.Client()
        # Reference an existing bucket.
        self.bucket = self.client.get_bucket('smartfood-184220.appspot.com')
        # Cam
        self.camera = PiCamera()

        self.stopping = False
        print("init show ready");
        self.thread = Thread(target=self.show_ready)

    def connect_succeeded(self):
        self.thread.start()

    def take_picture(self, inOut):
        mydatetime = datetime.datetime.now()
        mypicname = 'camerapic_' + inOut + '_{:%Y-%m-%d:%H:%M:%S}.jpg'.format(mydatetime)
        print("take picture:" + mypicname)
        #camera.start_preview()
        self.camera.capture('/home/pi/Desktop/' + mypicname)

        # Upload a local file to a new file to be created in your bucket.
        print("upload picture")
        imageBlob = self.bucket.blob(mypicname)
        imageBlob.upload_from_filename(filename='/home/pi/Desktop/' + mypicname)
        #camera.stop_preview()
        self.thread = Thread(target=self.show_ok)

    def received_gesture_event(self, event):
        print("did receive gesture event " + str(event))
        print("SWIPE_LEFT: " + str(Gesture.SWIPE_LEFT))
        print("SWIPE_RIGHT: " + str(Gesture.SWIPE_RIGHT))
        if str(event) == str(Gesture.SWIPE_LEFT):
            print ("left --> take picture")
            inOut = "in"
            self.take_picture(inOut)
        if str(event) == str(Gesture.SWIPE_RIGHT):
            print ("right --> take picture")
            inOut = "out"
            self.take_picture(inOut)

    def show_ok(self):
        print("Show ok...")
        matrix = LedMatrix(
                "         "
                "        *"
                "       * "
                "      *  "
                "     *   "
                "*   *    "
                " * *     "
                "  *      "
                "         "

        )
        self.controller.display_matrix(matrix , interval=3.0, brightness=1.0, fading=True)

    def show_ready(self):
        print("Show ready...")
        matrix = LedMatrix(
                "         "
                "   ***   "
                "  *   *  "
                " *       "
                " *       "
                " *       "
                "  *   *  "
                "   ***   "
                "         "

        )
        self.controller.display_matrix(matrix , interval=3.0, brightness=1.0, fading=True)


    def stop(self):
        self.controller.disconnect()
        self.stopping = True


def main(mac_address):
    manager = ControllerManager(adapter_name="hci0")
    controller = Controller(mac_address=mac_address, manager=manager)
    listener = NuimoListener(controller)
    print("main")
    controller.listener = listener
    print("main listener")
    controller.connect()
    print("main connect")

    try:
        manager.run()
    except KeyboardInterrupt:
        print("Stopping...")
        listener.stop()
        manager.stop()


if __name__ == "__main__":
    main('C5:AC:9A:2E:1C:DF')
