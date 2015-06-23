/**
 * config/require.js
 * Configuration for Require.js
 *
 * Copyright (C) 2014 University of Maryland
 * For license information, see LICENSE.txt
 *
 * Author:  Benjamin Bengfort <bengfort@cs.umd.edu>
 * Created: Wed Jan 22 23:52:24 2014 -0500
 *
 * ID: require.js [] bengfort@cs.umd.edu $
 */

requirejs.config({
  baseUrl: '/static/js',
  urlArgs: '?v=' + new Date().getTime(),
  paths: {
    'underscore': 'libs/underscore',
    'jquery': 'libs/jquery',
    'bootstrap': 'libs/bootstrap',
    'backbone': 'libs/backbone',
    'text': 'libs/require-text',
    'moment': 'libs/moment'
  },
  shim: {
    'underscore': {
      exports: '_'
    },
    'jquery': {
      exports: '$'
    },
    'backbone': {
      deps: ['jquery', 'underscore'],
      exports: 'Backbone'
    },
    'bootstrap': {
      deps: ['jquery']
    }
  }
});
