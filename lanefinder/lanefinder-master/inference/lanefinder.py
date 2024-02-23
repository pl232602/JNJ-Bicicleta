import cv2
import numpy as np
from pycoral.adapters import classify
from pycoral.adapters import common
from pycoral.utils.edgetpu import make_interpreter
from image.processing import preprocessing, postprocessing

class Lanefinder:

    def __init__(self, model, input_shape, output_shape, quant, dequant):
        self._window = None
        self._interpreter = make_interpreter(model)
        self._interpreter.allocate_tensors()
        self._cap = cv2.VideoCapture("/home/nilesosa/Documents/JNJ-Bicicleta/30 minute Fat Burning Indoor Cycling Workout Alps South Tyrol Lake Tour Garmin 4K Video.mp4")
        self._size = input_shape
        self._output_shape = output_shape
        self._quant = quant
        self._dequant = dequant
        self._input_shape = input_shape

    @property
    def window(self):
        return self._window

    @window.setter
    def window(self, name):
        self._window = name

    def _preprocess(self, frame):
        # normalize and quantize input
        # with parameters obtained during
        # model calibration
        return preprocessing(frame, self._quant['mean'], self._quant['std'])

    def _postprocess(self, pred_obj, frame):
        # get predicted mask from pred object
        # reshape to output size
        # perform closing operation to smooth out lane edges
        # and overlay with original frame
        return postprocessing(
            pred_obj=pred_obj,
            frame=frame,
            mean=self._quant['mean'],
            std=self._quant['std'],
            in_shape=self._size,
            out_shape=self._output_shape
        )

    def stream(self):
        """
        Starts real time video stream with
        pycoral supported traffic lane segmentation

        :return:    void
        """
        while True:
            # get next video frame
            ret, frame = self._cap.read()

            if not ret:
                # frame has not been
                # retrieved
                break

            frame = np.array(frame)

            frame = cv2.resize(frame, self._input_shape)
            frmcpy = frame.copy()

            frame = self._preprocess(frame)

            # Run inference
            common.set_input(self._interpreter, frame)
            self._interpreter.invoke()

            # Get the output tensor
            pred = common.output_tensor(self._interpreter, 0)

            pred = self._postprocess(pred, frmcpy)

            if self._window is not None:
                # show in window with fullscreen setup
                cv2.imshow(self._window, pred)

            else:
                # user did not specify window name
                # for fullscreen use so use default opencv size
                cv2.imshow('default', pred)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                # exit on key press
                break

    def destroy(self):
        """
        Runs cleanup after main loop exit

        :return:    void
        """
        cv2.destroyAllWindows()
        self._cap.release()


class LanefinderFromVideo(Lanefinder):

    def __init__(self, src, model, input_shape, output_shape, quant, dequant):
        Lanefinder.__init__(self, model, input_shape, output_shape, quant, dequant)
        self._cap = cv2.VideoCapture(src)
