import cv2
import numpy as np


def preprocessing(frame, mean, std):
    # normalize and quantize input
    # with paramaeters obtained during
    # model calibration
    frame = frame.astype(np.float32)
    frame *= (1 / 255)
    expd = np.expand_dims(frame, axis=0)
    quantized = (expd / std + mean)

    return quantized.astype(np.uint8)


def postprocessing(pred_obj, frame, mean, std, in_shape, out_shape):
    # get predicted mask in shape (n_rows*n_cols, )
    # and reshape back to (n_rows, n_cols)
    
    pred = pred_obj.reshape(in_shape)

    # dequantize and cast back to float
    dequantized = (std * (pred - mean))
    dequantized = dequantized.astype(np.float32)

    # resize frame and mask to output shape
    frame = cv2.resize(frame, out_shape)
    mask = cv2.resize(dequantized, (frame.shape[1], frame.shape[0]))

    # perform closing operation on mask to smooth out lane edges
    # overlay frame and segmentation mask
    frame[mask != 0] = (0, 0, 255)
    
    mask = cv2.normalize(mask, None, 255, 0, cv2.NORM_MINMAX, cv2.CV_8U)

    return frame, mask
