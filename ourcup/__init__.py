import logging
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

VERSION = '0.2'

# setup logging
logging.basicConfig(level=logging.DEBUG,
                    format="[%(asctime)s][%(levelname)s] %(name)s %(filename)s:%(funcName)s:%(lineno)d | %(message)s")
logger = logging.getLogger(__name__)
logger.info("---------------------------------------------------------------------------")

# setup cache dir correctly
basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
logging.info("Loaded from basedir {}".format(basedir))
import ourcup.util.filecache
ourcup.util.filecache.set_dir(os.path.join(basedir, "cache"))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'wc-2018.db')
logger.info("Connecting to DB at {}".format(app.config['SQLALCHEMY_DATABASE_URI']))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
alchemy_db = SQLAlchemy(app)

# connect to database
import ourcup.acs.manager
db = ourcup.acs.manager.CensusDataManager(alchemy_db)
logger.info("Connected to db")

import ourcup.fixtures.match_picker
picker = ourcup.fixtures.match_picker.MatchPicker()

import ourcup.views