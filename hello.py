import glob
import os

from flask import Flask, render_template, url_for
app = Flask(__name__)

conf = {}
conf['station']     = 'W2NAF'
conf['QTH']         = 'Spring Brook Township, Pennsylvania'
conf['grid']        = 'FN21ei'
conf['data_path']   = 'static'

@app.route('/')
def index():
    ds  = {}

    fpaths  = glob.glob(os.path.join(conf['data_path'],'*'))
    fpaths.sort()
    days    = []

    for fpath in fpaths:
        day = os.path.basename(fpath)
        url = url_for('display_day',day=day)

        dct = {}
        dct['fpath'] = fpath
        dct['day']   = day
        dct['url']   = url
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
        dct['png'] = png
        lfms.append(dct)

    ds['day']       = day
    ds['lfms']      = lfms
    ds['n_iono']    = len(lfms)

    return render_template('day.html',ds=ds,conf=conf)

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)
