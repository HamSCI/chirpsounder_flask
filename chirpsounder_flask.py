import glob
import os

from flask import Flask, render_template, url_for
app = Flask(__name__)

conf = {}
conf['station']     = 'W2NAF'
conf['QTH']         = 'Spring Brook Township, Pennsylvania'
conf['grid']        = 'FN21ei'
conf['data_path']   = '/var/www/chirpsounder_flask/static'

@app.route('/')
def index():
    ds  = {}

    fpaths  = glob.glob(os.path.join(conf['data_path'],'*'))
    fpaths.sort()
    days    = []

    for fpath in fpaths:
        day     = os.path.basename(fpath)
        url     = url_for('display_day',day=day)
        n_chirp = len(glob.glob(os.path.join(fpath,'*chirp*.h5')))
        n_lfm   = len(glob.glob(os.path.join(fpath,'*lfm*.h5')))
        n_png   = len(glob.glob(os.path.join(fpath,'*.png')))

        dct = {}
        dct['fpath']    = fpath
        dct['day']      = day
        dct['url']      = url
        dct['n_chirp']  = n_chirp
        dct['n_lfm']    = n_lfm
        dct['n_png']    = n_png
        days.append(dct)

    ds['days']  = days

    return render_template('index.html',ds=ds,conf=conf)

@app.route('/<day>')
def display_day(day):
    ds = {}

    fpath   = os.path.join(conf['data_path'],day)
    pngs    = glob.glob(os.path.join(fpath,'*.png'))
    pngs.sort()

    lfms    = []
    for png in pngs:
        dct = {}
        basename    = os.path.basename(png)
        png_path    = os.path.join(day,basename)
        dct['png'] = url_for('static',filename=png_path)
        lfms.append(dct)

    ds['day']       = day
    ds['lfms']      = lfms
    ds['n_iono']    = len(lfms)

    return render_template('day.html',ds=ds,conf=conf)

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)
