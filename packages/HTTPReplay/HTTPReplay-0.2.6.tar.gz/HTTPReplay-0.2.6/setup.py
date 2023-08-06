# Copyright (C) 2015-2018 Jurriaan Bremer <jbr@cuckoo.sh>
# Copyright (C) 2019 Hatching B.V.
# This file is part of HTTPReplay - http://jbremer.org/httpreplay/
# See the file 'LICENSE' for copying permission.

from setuptools import setup

setup(
    name="HTTPReplay",
    version="0.2.6",
    author="Hatching B.V.",
    author_email="info@hatching.io",
    packages=[
        "httpreplay",
    ],
    license="GPLv3",
    description="Properly interpret, decrypt, and replay pcap files",
    install_requires=[
        "dpkt==1.8.7",
        "tlslite-ng==0.6.0",
        "click>=6.6, <7",
    ],
    extras_require={
        "mitmproxy": [
            "mitmproxy==0.18.2",
        ],
        "dev": [
            "pytest>=2.9.1"
        ]
    },
    entry_points={
        "console_scripts": [
            "httpreplay = httpreplay.main:httpreplay",
            "pcap2mitm = httpreplay.main:do_pcap2mitm",
        ]
    },
)
