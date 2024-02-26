import cv2
import numpy as np
from pycoral.adapters import classify
from pycoral.adapters import common
from pycoral.utils.edgetpu import make_interpreter
from lanefinder.image.processing import preprocessing, postprocessing

class Lanefinder:

    def __init__(self, model, input_shape, output_shape, quant, dequant, video_path):
        self._window = None
        self._interpreter = make_interpreter(model)
        self._interpreter.allocate_tensors()
        self._cap = cv2.VideoCapture(video_path)
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
            
            pred, edges = self._postprocess(pred, frmcpy)
            yield pred, edges

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
