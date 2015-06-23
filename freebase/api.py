"""
Very simple API access to Freebase - requires error handling!
"""

import requests

from urllib import urlencode
from django.conf import settings
from freebase.exceptions import FreebaseException

ENDPOINTS = {
    "search": "https://www.googleapis.com/freebase/v1/search",
    "topic":  "https://www.googleapis.com/freebase/v1/topic",
    "images": "https://usercontent.googleapis.com/freebase/v1/image",
    "fbref":  "http://www.freebase.com"
}

def search(query, **kwargs):
    kwargs['query'] = query
    kwargs['key']   = settings.FREEBASE_API_KEY
    endpoint = ENDPOINTS['search'] + '?' + urlencode(kwargs)
    response = requests.get(endpoint)

    if response.status_code != 200:
        raise FreebaseException(**response.json())

    return response.json()

def topic(mid, **kwargs):
    kwargs['key']    = settings.FREEBASE_API_KEY
    kwargs['filter'] = 'suggest'
    endpoint = ENDPOINTS["topic"] + mid + '?' + urlencode(kwargs)
    response = requests.get(endpoint)

    if response.status_code != 200:
        raise FreebaseException(**response.json())

    return response.json()

def image(mid, **kwargs):
    if mid is None: return None

    kwargs['maxwidth']  = 225
    kwargs['maxheight'] = 225
    return ENDPOINTS['images'] + mid + '?' + urlencode(kwargs)

def reference(mid, **kwargs):
    url = ENDPOINTS['fbref'] + mid
    if kwargs:
        url += '?' + urlencode(kwargs)
    return url

def summarize(data, **kwargs):
    """
    Provides a simple, accessible summary of a Freebase result
    """

    # return data

    def first(doc, key, ns="text"):
        if doc is None: return None

        props = doc.get('property', doc)
        obj   = props.get(key, {})

        if 'values' in obj and len(obj['values']) > 0:
            first = obj['values'][0]
            if ns:
                return first.get(ns, None)
            return first
        return None

    keys    = ('mid', 'name', 'notability', 'image', 'description', 'attrs')
    summary = dict(map(lambda key: (key, None), keys))

    # Add the 'MID' field
    summary['mid'] = data.get('id')

    # Add the 'Name' field
    summary['name'] = first(data, '/type/object/name')

    # Add the 'Notabiliity' field
    summary['notability'] = first(data, '/common/topic/notable_for')

    # Add the 'Image' field
    img_id = first(data, '/common/topic/image', ns='id')
    summary['image'] = image(img_id)

    # Add the 'Description' field
    article = first(data, '/common/topic/article', ns=None)
    summary['description'] = first(article, '/common/document/text', ns='value')

    # Add the 'Attrs' field
    attrs = data.get('property', {}).get('/common/topic/notable_properties', {}).get('values', [])
    summary['attrs'] = []
    for val in attrs:
        summary['attrs'].append({
            'key': val['text'],
            'value': first(data, val['id'])
        })

    # Add a bonus 'Links' field for meta urls
    summary['links'] = {
        'html': reference(data.get('id')),
        'json': ENDPOINTS["topic"] + data.get('id', '') + '?' + urlencode({'filter':'suggest'}),
    }

    # Add the article if it exists
    wiki = first(article, '/common/document/source_uri', ns="value")
    if wiki:
        summary['links']['wiki'] = wiki

    return summary
