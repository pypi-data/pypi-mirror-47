# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Copyright 2016-2017 ARM Limited or its affiliates
#
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ----------------------------------------------------------------------------
import logging, sys
LOG = logging.getLogger(__name__)

from manifesttool.v1.create import main as create_v1
from urllib3.exceptions import MaxRetryError
import copy
import time
import tempfile
import os
import os.path
import shutil
import json
from manifesttool import defaults


MAX_NAME_LEN = 128 # The update API has a maximum name length of 128, but this is not queriable.

tempdirname = None
manifest_file = None

def main_wrapped(options):
    try:
        from mbed_cloud.update import UpdateAPI
        import mbed_cloud.exceptions
    except:
        LOG.critical('manifest-tool update commands require installation of the Pelion Device Management SDK:'
                     ' https://github.com/ARMmbed/mbed-cloud-sdk-python')
        return 1
    LOG.debug('Preparing an update on Pelion Device Management')
    # upload a firmware
    api = None
    try:
        # If set use api key set in manifest-tool update.
        if hasattr(options, 'api_key') and options.api_key:
            tempKey = options.api_key
            config = {'api_key': tempKey}
            api = UpdateAPI(config)
        # Otherwise use API key set in manifest-tool init
        else: api = UpdateAPI()

    except ValueError:
        LOG.critical('API key is required to connect to the Update Service. It can be added using manifest-tool init -a'
                     ' <api key> or by manually editing .mbed_cloud_config.json')
        return 1

    manifestInput = {
        'applyImmediately' : True
    }

    try:
        if os.path.exists(defaults.config):
            with open(defaults.config) as f:
                manifestInput.update(json.load(f))
        if not options.input_file.isatty():
            content = options.input_file.read()
            if content and len(content) >= 2: #The minimum size of a JSON file is 2: '{}'
                manifestInput.update(json.loads(content))
    except ValueError as e:
        LOG.critical("JSON Decode Error: {}".format(e))
        return 1

    payload_filePath = manifestInput.get("payloadFile", None)
    if options.payload:
        payload_filePath = options.payload.name

    if not options.payload_name:
        name = os.path.basename(payload_filePath) + time.strftime('-%Y-%m-%dT%H:%M:%S')
        LOG.info('Using {} as payload name.'.format(name))
        options.payload_name = name
    if len(options.payload_name) > MAX_NAME_LEN:
        LOG.critical(
            'Payload name is too long. Maximum length is {size}. ("{base}" <- {size}. overflow -> "{overflow}")'.format(
                size=MAX_NAME_LEN, base=options.payload_name[:MAX_NAME_LEN],
                overflow=options.payload_name[MAX_NAME_LEN:]))
        return 1

    if not options.manifest_name:
        name = os.path.basename(payload_filePath) + time.strftime('-%Y-%m-%dT%H:%M:%S-manifest')
        LOG.info('Using {} as manifest name.'.format(name))
        options.manifest_name = name

    if len(options.manifest_name) > MAX_NAME_LEN:
        LOG.critical(
            'Manifest name is too long. Maximum length is {size}. ("{base}" <- {size}. overflow -> "{overflow}")'.format(
                size=MAX_NAME_LEN, base=options.manifest_name[:MAX_NAME_LEN],
                overflow=options.manifest_name[MAX_NAME_LEN:]))
        return 1

    kwArgs = {}
    if options.payload_description:
        kwArgs['description'] = options.payload_description
    try:
        payload = api.add_firmware_image(
                        name = options.payload_name,
                    datafile = payload_filePath,
                    **kwArgs)
    except mbed_cloud.exceptions.CloudApiException as e:
        # TODO: Produce a better failuer message
        LOG.critical('Upload of payload failed with:\n{}'.format(e).rstrip())
        LOG.critical('Check API server URL "{}"'.format(api.config["host"]))
        return 1
    except MaxRetryError as e:
        LOG.critical('Upload of payload failed with:\n{}'.format(e))
        LOG.critical('Failed to establish connection to API-GW')
        LOG.critical('Check API server URL "{}"'.format(api.config["host"]))
        return 1

    LOG.info("Created new firmware at {}".format(payload.url))
    # create a manifest
    create_opts = copy.copy(options)
    create_opts.uri = payload.url
    create_opts.payload = options.payload
    if not (hasattr(create_opts, "output_file") and create_opts.output_file):
        global manifest_file
        manifest_file = open(os.path.join(tempdirname,'manifest'),'wb')
        create_opts.output_file = manifest_file

    rc = create_v1(create_opts, manifestInput)
    create_opts.output_file.close()
    if rc:
        return rc

    kwArgs = {}
    if options.manifest_description:
        kwArgs['description'] = options.manifest_description

    # upload a manifest
    try:
        manifest = api.add_firmware_manifest(
                        name = options.manifest_name,
                    datafile = create_opts.output_file.name,
                    **kwArgs)
    except mbed_cloud.exceptions.CloudApiException as e:
        # TODO: Produce a better failuer message
        LOG.critical('Upload of manifest failed with:')
        print(e)
        return 1
    LOG.info('Created new manifest at {}'.format(manifest.url))
    LOG.info('Manifest ID: {}'.format(manifest.id))
    return 0

def main(options):
    global tempdirname
    tempdirname = tempfile.mkdtemp()
    RC = main_wrapped(options)
    if manifest_file:
        manifest_file.close()
    shutil.rmtree(tempdirname)
    return RC
