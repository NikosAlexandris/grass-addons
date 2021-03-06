#!/usr/bin/env python

#
############################################################################
#
# MODULE:	    ann.maskrcnn config
# PURPOSE:	    Configuration class used in ann.maskrcnn.* modules
# WRITTEN:  	2017    Ondrej Pesek
#                       Based on config.py by Waleed Abdulla (Matterport, Inc.)
#                           https://github.com/matterport/Mask_RCNN
#                           Written __init__ to allow attributes to be
#                               modified during the class call
# Licensed under the MIT License (see LICENSE for details)
#
#############################################################################


import math
import numpy as np


class ModelConfig(object):
    """
    Base configuration class.
    Written by Waleed Abdulla (Matterport, Inc.)
    """

    # NOT RECOMMENDED TO MODIFY:

    # The strides of each layer of the FPN Pyramid. These values
    # are based on a Resnet101 backbone.
    BACKBONE_STRIDES = [4, 8, 16, 32, 64]

    # Size of the fully-connected layers in the classification graph
    FPN_CLASSIF_FC_LAYERS_SIZE = 1024

    # Size of the top-down layers used to build the feature pyramid
    TOP_DOWN_PYRAMID_SIZE = 256

    ## RPN ##
    # Length of square anchor side in pixels
    RPN_ANCHOR_SCALES = (32, 64, 128, 256, 512)

    # Ratios of anchors at each cell (width/height)
    # A value of 1 represents a square anchor, and 0.5 is a wide anchor
    RPN_ANCHOR_RATIOS = [0.5, 1, 2]

    # Anchor stride
    # If 1 then anchors are created for each cell in the backbone feature map.
    # If 2, then anchors are created for every other cell, and so on.
    RPN_ANCHOR_STRIDE = 1  # 2 before change

    # Non-max suppression threshold to filter RPN proposals.
    # You can increase this during training to generate more proposals.
    RPN_NMS_THRESHOLD = 0.7

    # How many anchors per image to use for RPN training
    RPN_TRAIN_ANCHORS_PER_IMAGE = 256

    # ROIs kept after tf.nn.top_k and before non-maximum suppression
    PRE_NMS_LIMIT = 6000

    # ROIs kept after non-maximum suppression (training and inference)
    POST_NMS_ROIS_TRAINING = 2000
    POST_NMS_ROIS_INFERENCE = 1000

    # Minimum scaling ratio. Checked after MIN_IMAGE_DIM and can force further
    # up scaling. For example, if set to 2 then images are scaled up to double
    # the width and height, or more, even if MIN_IMAGE_DIM doesn't require it.
    # However, in 'square' mode, it can be overruled by IMAGE_MAX_DIM.
    IMAGE_MIN_SCALE = 0

    # Image mean (RGB)
    MEAN_PIXEL = np.array([123.7, 116.8, 103.9])

    # Percent of positive ROIs used to train classifier/mask heads
    ROI_POSITIVE_RATIO = 0.33

    # Pooled ROIs
    POOL_SIZE = 7
    MASK_POOL_SIZE = 14

    # Shape of output mask
    # To change this you also need to change the neural network mask branch
    MASK_SHAPE = [28, 28]

    # Maximum number of ground truth instances to use in one image
    MAX_GT_INSTANCES = 100

    # Bounding box refinement standard deviation for RPN and final detections.
    RPN_BBOX_STD_DEV = np.array([0.1, 0.1, 0.2, 0.2])
    BBOX_STD_DEV = np.array([0.1, 0.1, 0.2, 0.2])

    # Max number of final detections
    DETECTION_MAX_INSTANCES = 100

    # Minimum probability value to accept a detected instance
    # ROIs below this threshold are skipped
    DETECTION_MIN_CONFIDENCE = 0.7

    # Non-maximum suppression threshold for detection
    DETECTION_NMS_THRESHOLD = 0.3

    # Learning rate and momentum
    # The Mask RCNN paper uses lr=0.02, but on TensorFlow it causes
    # weights to explode. Likely due to differences in optimizer
    # implementation.
    LEARNING_RATE = 0.001  # 0.002 before change
    LEARNING_MOMENTUM = 0.9

    # Weight decay regularization
    WEIGHT_DECAY = 0.0001

    # Loss weights for more precise optimization.
    # Can be used for R-CNN training setup.
    LOSS_WEIGHTS = {
        "rpn_class_loss": 1.,
        "rpn_bbox_loss": 1.,
        "mrcnn_class_loss": 1.,
        "mrcnn_bbox_loss": 1.,
        "mrcnn_mask_loss": 1.
    }

    # Use RPN ROIs or externally generated ROIs for training
    # Keep this True for most situations. Set to False if you want to train
    # the head branches on ROI generated by code rather than the ROIs from
    # the RPN. For example, to debug the classifier head without having to
    # train the RPN.
    USE_RPN_ROIS = True

    # Gradient norm clipping
    GRADIENT_CLIP_NORM = 5.0

    def __init__(self, name='model', imagesPerGPU=1, GPUcount=1, numClasses=1,
                 trainROIsPerImage=64, stepsPerEpoch=1500,
                 miniMaskShape=None, validationSteps=100,
                 imageMaxDim=768, imageMinDim=768, backbone='resnet101',
                 trainBatchNorm=False, resizeMode='square',
                 image_channel_count=3):
        """Set values of attributes.
        Written by Ondrej Pesek, but using attributes from Waleed Abdulla"""

        # Give the configuration a recognizable name
        self.NAME = name

        # Number of images to train on each GPU
        self.IMAGES_PER_GPU = imagesPerGPU

        # NUMBER OF GPUs to use.
        # When using only a CPU, this needs to be set to 1.
        self.GPU_COUNT = GPUcount

        # Number of classes (including background)
        self.NUM_CLASSES = numClasses

        # Number of ROIs per image to feed to classifier/mask heads
        # Try to keep keep a positive:negative
        # ratio of 1:3. You can increase the number of proposals by adjusting
        # the RPN NMS threshold.
        self.TRAIN_ROIS_PER_IMAGE = trainROIsPerImage

        # Number of training steps per epoch. A model is saved after each epoch
        self.STEPS_PER_EPOCH = stepsPerEpoch // self.IMAGES_PER_GPU

        # Number of steps to run at the end of every training epoch
        self.VALIDATION_STEPS = validationSteps

        # Input image resizing
        # Generally, use the "square" resizing mode for training and predicting
        # and it should work well in most cases. In this mode, images are scaled
        # up such that the small side is = IMAGE_MIN_DIM, but ensuring that the
        # scaling doesn't make the long side > IMAGE_MAX_DIM. Then the image is
        # padded with zeros to make it a square so multiple images can be put
        # in one batch.
        # Available resizing modes:
        # none:   No resizing or padding. Return the image unchanged.
        # square: Resize and pad with zeros to get a square image
        #         of size [max_dim, max_dim].
        self.IMAGE_RESIZE_MODE = resizeMode
        self.IMAGE_MAX_DIM = imageMaxDim
        self.IMAGE_MIN_DIM = imageMinDim

        # mini_mask to save memory
        # If True, resizes masks to a smaller size to reduce memory load
        if miniMaskShape:
            self.USE_MINI_MASK = True
            self.MINI_MASK_SHAPE = tuple(
                int(a) for a in miniMaskShape.split(','))  # (height, width)
        else:
            self.USE_MINI_MASK = False
            self.MINI_MASK_SHAPE = None

        # Effective batch size
        self.BATCH_SIZE = self.IMAGES_PER_GPU * self.GPU_COUNT

        # Set the backbone architecture
        # Use a pedefined one or provide a callable that should have the
        # signature of model.resnet_graph. If you do so, you need to supply
        # a callable to COMPUTE_BACKBONE_SHAPE as well
        self.BACKBONE = backbone

        # Only useful if you supply a callable to BACKBONE. Should compute
        # the shape of each layer of the FPN Pyramid.
        # See model.compute_backbone_shapes
        self.COMPUTE_BACKBONE_SHAPE = None

        # Number of color channels per image. RGB = 3, grayscale = 1, RGB-D = 4
        # Changing this requires other changes in the code. See the WIKI for more
        # details: https://github.com/matterport/Mask_RCNN/wiki
        self.IMAGE_CHANNEL_COUNT = image_channel_count

        # Input image size
        self.IMAGE_SHAPE = np.array([self.IMAGE_MAX_DIM, self.IMAGE_MAX_DIM,
             self.IMAGE_CHANNEL_COUNT])

        # Compute backbone size from input image size
        # TODO Ondrej Pesek: Maybe delete it and see Matterport's (avoid math
        #  import)
        self.BACKBONE_SHAPES = np.array(
            [[int(math.ceil(self.IMAGE_SHAPE[0] / stride)),
              int(math.ceil(self.IMAGE_SHAPE[1] / stride))]
             for stride in self.BACKBONE_STRIDES])

        # Train or freeze batch normalization layers
        #  None: Train BN layers in a normal mode
        #  False: Freeze BN layers (recommended for small batch size)
        #  True: Set layer in training mode even when predicting
        self.TRAIN_BN = trainBatchNorm

        # Image meta data length
        # See compose_image_meta() for details
        self.IMAGE_META_SIZE = 1 + 3 + 3 + 4 + 1 + self.NUM_CLASSES

    def display(self):
        """Display Configuration values."""
        print("\nConfigurations:")
        for a in dir(self):
            if not a.startswith("__") and not callable(getattr(self, a)):
                print("{:30} {}".format(a, getattr(self, a)))
        print("\n")
