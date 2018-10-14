import os
import platform
import struct
import sys
import glob
from datetime import datetime
from threading import Thread

import numpy as np
import pyaudio
import soundfile

sys.path.append('/home/khedd/Dev/Fun/Porcupine/binding/python/')
from porcupine import Porcupine

library_path = "/home/khedd/Dev/Fun/Porcupine/lib/linux/x86_64/libpv_porcupine.so"
model_file_path = "/home/khedd/Dev/Fun/Porcupine/lib/common/porcupine_params.pv"
keyword_file_paths = ""

class Listener:
    def __init__(self,
            library_path,
            model_file_path,
            keyword_file_paths,
            sensitivities):
        self._library_path = library_path
        self._model_file_path = model_file_path
        self._keyword_file_paths = keyword_file_paths
        self._sensitivities = sensitivities
        self._input_device_index = None
        

        num_keywords = len(self._keyword_file_paths)

        self.keyword_names =\
            [os.path.basename(x).replace('.ppn', '').replace('_tiny', '').split('_')[0] for x in self._keyword_file_paths]

        print('listening for:')
        for keyword_name, sensitivity in zip(self.keyword_names, sensitivities):
            print('- %s (sensitivity: %f)' % (keyword_name, sensitivity))

        self.porcupine = None
        self.pa = None
        self.audio_stream = None

        # print(self._library_path, self._model_file_path, self._keyword_file_paths, self._sensitivities)
        self.porcupine = Porcupine(
            library_path=self._library_path,
            model_file_path=self._model_file_path,
            keyword_file_paths=self._keyword_file_paths,
            sensitivities=self._sensitivities)

        pa = pyaudio.PyAudio()
        self.audio_stream = pa.open(
            rate=self.porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=self.porcupine.frame_length,
            input_device_index=self._input_device_index)
    
    def listen(self):
        pcm = self.audio_stream.read(self.porcupine.frame_length)
        pcm = struct.unpack_from("h" * self.porcupine.frame_length, pcm)

        result = self.porcupine.process(pcm)
        if result >= 0:
            return self.keyword_names[result]
        else:
            return None

    @staticmethod
    def create():
        keyword_file_paths = glob.glob( "/home/khedd/Dev/python/asst/khedd/keywords/*.ppn")
        sensitivities = [0.5] * len(keyword_file_paths)
        print(sensitivities)
        print(keyword_file_paths)
        l = Listener(library_path, model_file_path, keyword_file_paths, sensitivities)
        return l
