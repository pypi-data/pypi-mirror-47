__all__ = [
    "clean_graph", "get_hashob", "validate_request_default",
    "verify_tag_default", "domain_auth"
]

import logging
from urllib.parse import parse_qs, urlencode

from django.conf import settings
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.test import Client
from django.http.request import validate_host

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes

from rdflib import XSD, URIRef, Literal

import requests

from spkcspider.apps.spider.constants import spkcgraph, host_tld_matcher


def validate_request_default(request, form):
    if not form.is_valid():
        return False

    return True


def verify_tag_default(tag):
    tag.save()


def domain_auth(source, hostpart):
    GET = parse_qs(source.get_params)
    if "token" not in GET:
        GET["token"] = "prefer"
    GET["intention"] = "domain"
    GET["referrer"] = "{}{}".format(
        hostpart,
        reverse("spider_verifier:create")
    )
    source.initialize_token()
    source.save(update_fields=["token"])
    GET["payload"] = urlencode(
        {
            "url": source.url,
            "update_secret": source.token
        }
    )

    url = "{}?{}".format(
        source.url, urlencode(GET)
    )
    ret = True
    params, can_inline = get_requests_params(url)

    if can_inline:
        response = Client().get(
            url, follow=True, secure=True, Connection="close"
        )
        if response.status_code >= 400:
            ret = False
    else:
        try:
            with requests.get(
                url, headers={"Connection": "close"},
                **params
            ) as resp:
                resp.close()
                resp.raise_for_status()
        except Exception:
            if settings.DEBUG:
                logging.exception("domain_auth failed")
            ret = False
    # other or own update_secret was successful or url has problems
    source.refresh_from_db()
    return ret


def clean_graph(mtype, graph, start, source, hostpart):
    if not mtype:
        return None
    elif "UserComponent" in mtype:
        return "list"
    elif "SpiderTag" in mtype:
        if (
            URIRef(start),
            spkcgraph["features"],
            Literal("verify", datatype=XSD.string)
        ) in graph:
            return "layout_cb"
        ret = "layout"
        if domain_auth(source, hostpart):
            graph.set(
                (
                    start,
                    spkcgraph["action:view"],
                    Literal(source.get_url(), datatype=XSD.anyURI)
                )
            )
            ret = "layout_cb"
        return ret
    else:
        return "content"


def get_hashob():
    return hashes.Hash(
        getattr(
           settings, "VERIFICATION_HASH_ALGORITHM",
           settings.SPIDER_HASH_ALGORITHM
        ),
        backend=default_backend()
    )


def get_requests_params(url):
    _url = host_tld_matcher.match(url)
    if not _url:
        raise ValidationError(
            _("Invalid URL: \"%(url)s\""),
            code="invalid_url",
            params={"url": url}
        )
    _url = _url.groupdict()
    mapper = getattr(
        settings, "VERIFIER_REQUEST_KWARGS_MAP",
        settings.SPIDER_REQUEST_KWARGS_MAP
    )
    return (
        mapper.get(
            _url["host"],
            mapper.get(
                _url["tld"],  # maybe None but then fall to retrieval 3
                mapper[b"default"]
            )
        ),
        not getattr(settings, "SPIDER_DISABLE_FAKE_CLIENT", None) and
        validate_host(_url["host"], settings.ALLOWED_HOSTS)
    )
