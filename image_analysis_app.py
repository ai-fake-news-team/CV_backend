#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

os.environ['PATH'] += ':/usr/local/cuda-8.0/bin'
os.environ['LD_LIBRARY_PATH'] += ':/usr/local/cuda-8.0/lib64'

base = '/home/mehdi/work/CV_backend/'
sys.path.append(base)

from flask import Flask, jsonify, abort, request, make_response, url_for
#from flask.ext.httpauth import HTTPBasicAuth
from flask_httpauth import HTTPBasicAuth
import cv2
import requests
from subprocess import call
import codecs


from caption_generation import get_caption
from ELA import cv2_ELA

app = Flask(__name__, static_url_path = "")
auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'fey_kun_rails_server':
        return 'achecki_3027'
    if username == 'mehdi':
        return 'test'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify( { 'error': 'Unauthorized access' } ), 403)
    # return 403 instead of 401 to prevent browsers from displaying the default auth dialog

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

@app.route('/request_analysis/api', methods = ['POST'])
@auth.login_required
def launch_analysis():
    if not request.json or not 'image_id' in request.json or not 'image_url' in request.json:
        abort(400)

    # Get ID and make directory
    image_id = request.json['image_id']
    dir_path = base+'analysis_results/'+image_id
    if not os.path.isdir(dir_path):
        os.makedirs(base+'analysis_results/'+image_id)

    # Download image
    image_url = request.json['image_url']
    r = requests.get(image_url, timeout=0.5)

    if r.status_code == 200:
        with open(dir_path+'/{}_original.jpg'.format(image_id), 'wb') as f:
            f.write(r.content)

    # Captioning
    captions = get_caption(dir_path+'/{}_original.jpg'.format(image_id))
    sentence = u"".join(captions[0]["sentence"])
    with open(dir_path+'/{}_caption.txt'.format(image_id), 'w') as f:
        f.write(sentence.encode('utf8'))

    # ELA analysis
    ratio, output_image = cv2_ELA(dir_path+'/{}_original.jpg'.format(image_id))
    cv2.imwrite(dir_path+'/{}_ela.png'.format(image_id), output_image)

    # Object detection
    call(['./darknet',
            'detect',
            '/home/mehdi/work/darknet/cfg/yolo.cfg',
            '/home/mehdi/work/darknet/yolo.weights',
            dir_path+'/{}_original.jpg'.format(image_id)],
            cwd='/home/mehdi/work/darknet/')

    os.rename('/home/mehdi/work/darknet/predictions.png', dir_path+'/{}_yolo.png'.format(image_id))

    # Send results
    result_url = 'http://taptappun.net/fey_kun/analized'
    # files = {'object_img': open(dir_path+'/{}_yolo.png'.format(image_id), 'rb'),
    #          'error_img': open(dir_path+'/{}_ela.png'.format(image_id), 'rb'),
    #          'error_ratio': ratio,
    #          'caption': sentence}

    multiple_files = [
        ('object_img', ('{}_yolo.png'.format(image_id), open(dir_path+'/{}_yolo.png'.format(image_id), 'rb'), 'image/png')),
        ('error_img', ('{}_ela.png'.format(image_id), open(dir_path+'/{}_ela.png'.format(image_id), 'rb'), 'image/png'))]

    payload = {'image_id': image_id,
                'result': {'error_ratio': str(ratio),
                            'caption': sentence}
                }

    r = requests.post(result_url, files=multiple_files, json=payload)
    print "Post request status:", r.status_code

    return jsonify({'image_id': image_id, 'status': 'done'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
