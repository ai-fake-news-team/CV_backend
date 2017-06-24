#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import os

base = '/home/mehdi/work/chainer-caption'

sys.path.append(base+'/code')

from CaptionGenerator import CaptionGenerator

def get_caption(image_path):
    caption_generator=CaptionGenerator(
        rnn_model_place=base+'/data/caption_jp_mt_model40.model',
        cnn_model_place=base+'/data/ResNet50.model',
        dictonary_place=base+'/data/MSCOCO/captions_train2014_jp_translation_processed_dic.json',
        beamsize=3,
        depth_limit=50,
        gpu_id=0,
        first_word= '',
        )

    captions = caption_generator.generate(image_path)

    return captions

if __name__ == '__main__':
    captions = get_caption('../example_images/lion.jpg')

    for caption in captions:
        print (" ".join(caption["sentence"]))
        print (caption["log_likelihood"])
