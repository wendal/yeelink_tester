'''
Created on 2014-8-11

@author: wendal
'''

from distutils.core import setup

import py2exe

setup(console=['main.py'],
      options={

# And now, configure py2exe by passing more options;

          'py2exe': {

# This is magic: if you don't add these, your .exe may
# or may not work on older/newer versions of windows.

              "dll_excludes": [
                  "MSVCP90.dll",
                  "MSWSOCK.dll",
                  "mswsock.dll",
                  "powrprof.dll",
                  ],

# Py2exe will not figure out that you need these on its own.
# You may need one, the other, or both.

              'includes': [
                  'sip',
                  'PyQt4.QtNetwork',
                  ],

# Optional: make one big exe with everything in it, or
# a folder with many things in it. Your choice
#             'bundle_files': 1,
          }
      },

# Qt's dynamically loaded plugins and py2exe really don't
# get along.

data_files = [
            ('phonon_backend', [
                'C:\Python27\Lib\site-packages\PyQt4\plugins\phonon_backend\phonon_ds94.dll'
                ]),
            ('imageplugins', [
            'c:\Python27\lib\site-packages\PyQt4\plugins\imageformats\qgif4.dll',
            'c:\Python27\lib\site-packages\PyQt4\plugins\imageformats\qjpeg4.dll',
            'c:\Python27\lib\site-packages\PyQt4\plugins\imageformats\qsvg4.dll',
            ]),
],

# If you choose the bundle above, you may want to use this, too.
#     zipfile=None,
)