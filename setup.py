from distutils.core import setup

setup(
    name='spnav',
    version='0.9',
    description='ctypes wrapper around libspnav, a client for reading events from a Space Navigator 3D mouse',
    author='Stanley Seibert',
    author_email='stan@mtrr.org',
    packages=['spnav',],
    license='BSD license',
    long_description=open('README.txt').read(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: X11 Applications',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: Human Machine Interfaces'
        ],
)
