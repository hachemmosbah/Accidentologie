#!/usr/bin/env python
# coding: utf-8
#import library
from app import create_app

app = create_app()
# run app from local host
app.run( debug=True, host='127.0.0.1', port=5000 )

