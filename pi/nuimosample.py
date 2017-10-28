from sys import argv
from threading import Thread
from time import sleep

from nuimo import Controller, ControllerManager, ControllerListener, LedMatrix, GestureEvent, Gesture, LedMatrix


class NuimoListener(ControllerListener):
    def __init__(self, controller):
        self.controller = controller

        self.stopping = False
        self.thread = Thread(target=self.show_ready)

    def connect_succeeded(self):
        self.thread.start()

    def received_gesture_event(self, event):
        print("did send gesture event " + str(event))

    def show_ok(self):
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
    controller.listener = listener
    controller.connect()

    try:
        manager.run()
    except KeyboardInterrupt:
        print("Stopping...")
        listener.stop()
        manager.stop()


if __name__ == "__main__":
    if len(argv) > 1:
        main(argv[-1])
    else:
        print("Usage: {} <nuimo_mac_address>".format(argv[0]))