# Copyright (c) 2018, NVIDIA CORPORATION.  All rights reserved.
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

# pylint: disable=invalid-name, too-few-public-methods, bad-continuation

"""Test cases for the openblas module"""

from __future__ import unicode_literals
from __future__ import print_function

import logging # pylint: disable=unused-import
import unittest

from helpers import centos, docker, ubuntu

from hpccm.building_blocks.openblas import openblas
from hpccm.toolchain import toolchain

class Test_openblas(unittest.TestCase):
    def setUp(self):
        """Disable logging output messages"""
        logging.disable(logging.ERROR)

    @ubuntu
    @docker
    def test_defaults_ubuntu(self):
        """Default openblas building block"""
        tc = toolchain(CC='gcc', FC='gfortran')
        o = openblas(toolchain=tc)
        self.assertEqual(str(o),
r'''# OpenBLAS version 0.3.3
RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        make \
        perl \
        tar \
        wget && \
    rm -rf /var/lib/apt/lists/*
RUN mkdir -p /var/tmp && wget -q -nc --no-check-certificate -P /var/tmp https://github.com/xianyi/OpenBLAS/archive/v0.3.3.tar.gz && \
    mkdir -p /var/tmp && tar -x -f /var/tmp/v0.3.3.tar.gz -C /var/tmp -z && \
    cd /var/tmp/OpenBLAS-0.3.3 && make CC=gcc FC=gfortran USE_OPENMP=1 && \
    make install PREFIX=/usr/local/openblas && \
    rm -rf /var/tmp/v0.3.3.tar.gz /var/tmp/OpenBLAS-0.3.3
ENV LD_LIBRARY_PATH=/usr/local/openblas/lib:$LD_LIBRARY_PATH''')

    @ubuntu
    @docker
    def test_ldconfig(self):
        """ldconfig option"""
        tc = toolchain(CC='gcc', FC='gfortran')
        o = openblas(ldconfig=True, toolchain=tc, version='0.3.3')
        self.assertEqual(str(o),
r'''# OpenBLAS version 0.3.3
RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        make \
        perl \
        tar \
        wget && \
    rm -rf /var/lib/apt/lists/*
RUN mkdir -p /var/tmp && wget -q -nc --no-check-certificate -P /var/tmp https://github.com/xianyi/OpenBLAS/archive/v0.3.3.tar.gz && \
    mkdir -p /var/tmp && tar -x -f /var/tmp/v0.3.3.tar.gz -C /var/tmp -z && \
    cd /var/tmp/OpenBLAS-0.3.3 && make CC=gcc FC=gfortran USE_OPENMP=1 && \
    make install PREFIX=/usr/local/openblas && \
    echo "/usr/local/openblas/lib" >> /etc/ld.so.conf.d/hpccm.conf && ldconfig && \
    rm -rf /var/tmp/v0.3.3.tar.gz /var/tmp/OpenBLAS-0.3.3''')

    @ubuntu
    @docker
    def test_runtime(self):
        """Runtime"""
        o = openblas()
        r = o.runtime()
        self.assertEqual(r,
r'''# OpenBLAS
COPY --from=0 /usr/local/openblas /usr/local/openblas
ENV LD_LIBRARY_PATH=/usr/local/openblas/lib:$LD_LIBRARY_PATH''')
