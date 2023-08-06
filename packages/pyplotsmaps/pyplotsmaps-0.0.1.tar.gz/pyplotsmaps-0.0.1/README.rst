PY-PLOTS-MAPS
===============

This is a python library for your iot projects to plot your sensor data and get your location
 Wesbite (https://react-iotmine.firebaseapp.com/)

Functions:
----------
* Plot your sensors data using different types of plots

Installation :
--------------

Python3
-------

::

    pip3 install pyplotsmaps --user

or

Python
------

::

    pip install pyplotsmaps --user


**Map Example :**
~~~~~~~~~~~~~~~~~~

::

    from plots_maps import PLOTSMAPS

    API = 'Your API'

    if __name__ == '__main__':
        ob = PLOTSMAPS(API)
        print(ob.updateMap(mapname='Your Map Name', latitude=48.8584, longitude=2.2945)) #Eiffel Tower


**Plot Example :**
~~~~~~~~~~~~~~~~~~

::

    from plots_maps import PLOTSMAPS

    API = 'Your Api'

    if __name__ == '__main__':
        ob = PLOTSMAPS(API)
        print(ob.updatePlot(plotname='Your Plot Name', ydata=80))
