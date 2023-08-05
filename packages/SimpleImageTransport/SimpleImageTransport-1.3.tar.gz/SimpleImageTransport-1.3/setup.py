import setuptools

setuptools.setup(
    name='SimpleImageTransport',
    version='1.3',
    author="Raymond Tunstill",
    author_email="ray.tunstill@live.co.uk",
    description="Simple python 2/3 library for transporting images to a remote machine, applying transformations and "
                "returning a response.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/RaymondKirk/SimpleImageTransport",
    packages=["SimpleImageTransport"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    install_requires=['opencv-python', 'Flask', 'numpy', 'requests', 'jsonpickle'],
)
