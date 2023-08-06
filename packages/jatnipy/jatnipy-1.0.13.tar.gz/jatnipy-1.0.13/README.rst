JATNIpy
=======

| Justin’s, Andrea’s, and Torbjörn’s network inference package for
Python
| `Nordlinglab <https://www.nordlinglab.org/>`__
| `JATNIpy <https://bitbucket.org/temn/JATNIpy/src/>`__

Why JATNIpy?
------------

We re-implemented
`GeneSPIDER <https://bitbucket.org/sonnhammergrni/genespider/src/>`__
toolbox and chose Python as our programming language. Python is a
popular high-level programming language. It is freely available and
widely used by academic and commercial.

Results:
--------

We incorporate several free available python packages and refer the
package called `scikit-grni <https://pypi.org/project/scikit-grni/>`__
into a new complete package. We finally name the new complete package as
JATNIpy.

Availability and Implementation: Source code freely available for
download at https://bitbucket.org/temn/JATNIpy/, reimplemented
GeneSPIDER toolbox in Python.

How do I get set up?
~~~~~~~~~~~~~~~~~~~~

-  *Alternative 1*: Use `git <https://git-scm.com/>`__ to fetch JATNIpy
   repository run this command

   ::

       git clone https://bitbucket.org/temn/JATNIpy/

-  *Alternative 2*: Download it from
   `JATNIpy <https://bitbucket.org/temn/JATNIpy/>`__
-  *Alternative 3*: Use the pip3 to install JATNIpy from
   `Pypi <https://pypi.org/>`__

   ::

           pip3 install jatnipy -t ~/JATNIpy

   ``~/JATNIpy`` is the folder that you want to download. Then, change
   to the directory where you downloaded from the repository by

   ::

           cd ~/JATNIpy/jatnipy.

   Before we uses JATNIpy, we should make sure pip3 has been installed
   in local computer. If there is not pip in local computer, we use the
   following command to install it.
-  \*For Debian/Ubuntu user:

   ::

           apt-get install python3-pip

-  \*For CentOS 7 user:

   ::

           yum install python34-setuptools
           easy_install pip

After we make sure pip3 is in our local computer, we then install
virtualenvwrapper to create a virtual environment for our local computer
by these commands

::

        pip3 install virtualenvwrapper
        export WORKON_HOME=~/Envs
        mkdir -p $WORKON_HOME
        source /usr/local/bin/virtualenvwrapper.sh
        mkvirtualenv env1
        workon env2

| Create the new virtual environment env1 by
| ``mkvirtualenv env1``
| Choose the virtual environment you want to work on by
| ``workon env1``
| After working on the environment you want, then use pip3 to install
| the open source python3 packages with the command

::

        pip3 install -e

-  Dependencies:

   -  `git <https://git-scm.com/>`__ Version control system for tracking
      the development of programming
   -  `Scipy <https://www.scipy.org/>`__ Python-based software for
      mathematics, science, and engineering
   -  `Numpy <http://www.numpy.org/>`__ Fundamental python package for
      doing numerical or mathematics computation
   -  `pandas <https://pandas.pydata.org/>`__ Using data structures and
      data analysis tools easily in Python
   -  `matplotlib <https://matplotlib.org/>`__ Useful Python 2D plotting
      tool which provides MATLAB-like interface
   -  `scikit-learn <http://scikit-learn.org/stable/>`__ Data mining and
      data analysis which built on Numpy, Scipy and matplotlib
   -  `networkx <https://networkx.github.io/>`__ Python package which is
      made for studying graphs and the complex networks
   -  `glmnet\_py <https://pypi.org/project/glmnet-py/>`__ The popular
      glmnet library for Python version
   -  `py-ubjson <https://pypi.org/project/py-ubjson/>`__ Universal
      Binary JSON encoder/decoder for Python version
   -  `CVXPY <http://www.cvxpy.org/>`__ Handling convex optimization
      problems for Python version
   -  `Requests: HTTP for
      Humans <http://docs.python-requests.org/en/master/>`__ Python
      library for requesting HTTP

-  Datasets are available
   `here <https://bitbucket.org/sonnhammergrni/gs-datasets>`__.
-  Networks are available
   `here <https://bitbucket.org/sonnhammergrni/gs-networks>`__.

Contact: `Justin <mailto:justin.lin@nordlinglab.org>`__, `Andreas
Tjärnberg <mailto:at145@nyu.edu>`__, `Torbjörn
Nordling <t@nordlinglab.org>`__
