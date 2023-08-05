""" Argus module to create facts from argus events """

import re
from collections import defaultdict
from ipaddress import AddressValueError, IPv4Address
from logging import debug, error, warning
from typing import Dict, Text, cast, List

import act.api
import act.api.helpers

HASH_MD5_RE = re.compile(r'^[0-9a-fA-F]{32}$')
HASH_SHA1_RE = re.compile(r'^[0-9a-fA-F]{40}$')
HASH_SHA256_RE = re.compile(r'^[0-9a-fA-F]{64}$')
HASH_SHA5112_RE = re.compile(r'^[0-9a-fA-F]{128}$')

def is_public_ip(ip_str: Text) -> bool:
    """ Return True if IP (str) is a valid, public IP """
    try:
        return IPv4Address(ip_str).is_global
    except AddressValueError:
        return False


def handle_fact(fact: act.api.fact.Fact, output_format: Text) -> None:
    """ wrap act.helpers.handle_fact and log all errors (and continue) """
    try:
        act.api.helpers.handle_fact(fact, output_format)
    except act.api.base.ResponseError:
        error("Error adding fact (ResponseError): {}".format(fact, exc_info=True))
    except act.api.schema.MissingField:
        error("Error adding fact (missing field): {}".format(fact, exc_info=True))


def handle_uri(actapi: act.api.Act, uri: Text, output_format: Text) -> None:
    """ wrap act.helpers.handle_uri and log all errors (and continue) """
    try:
        act.api.helpers.handle_uri(actapi, uri, output_format)
    except act.api.base.ResponseError:
        error("Error adding uri (ResponseError): {}".format(uri, exc_info=True))
    except act.api.schema.MissingField:
        error("Error adding uri (missing field): {}".format(uri, exc_info=True))


def handle_argus_event_hash(
        actapi: act.api.Act,
        properties: defaultdict,
        event_id: Text,
        content_props: List[Text],
        hash_props: List[Text],
        output_format: Text) -> None:
    """ Handle file/process hash properties in events """

    # For all hash values that represents a content object (typically sha256)
    for prop in content_props:
        if properties[prop]:
            # Properties can be aggregated (separated by newlines)
            for value in properties[prop].split("\n"):
                if not HASH_SHA256_RE.search(value):
                    warning('Illegal sha256: "{}" in property "{}"'.format(value, prop))
                    continue

                handle_fact(
                    actapi.fact("observedIn", "event")
                    .source("content", value)
                    .destination("event", event_id),
                    output_format=output_format
                )

    # For all hash values that needs a placeholder (unknown content/sha256)
    for prop in hash_props:
        if properties[prop]:
            for value in properties[prop].split("\n"):
                if not (HASH_MD5_RE.search(value) or HASH_SHA1_RE.search(value) or HASH_SHA5112_RE.search(value)):
                    warning("Unknown hash: {} in property {}".format(value, prop))
                    continue

                if value:
                    chain = act.api.fact.fact_chain(
                        actapi.fact("represents")
                        .source("hash", value)
                        .destination("content", "*"),
                        actapi.fact("observedIn", "event")
                        .source("content", "*")
                        .destination("event", event_id),
                    )

                    for fact in chain:
                        handle_fact(fact, output_format=output_format)


def get_scheme(event: defaultdict) -> Text:
    "Get scheme based on protocol, default to 'network'"

    protocols = ("tcp", "udp", "icmp")

    # If we have a known protocol, use this as scheme when constructing URI
    if event["protocol"] in protocols:
        return cast(Text, event["protocol"])
    return "network"


def handle_argus_event_ip(
        actapi: act.api.Act,
        event: defaultdict,
        event_id: Text,
        output_format: Text) -> None:
    "Create facts from source/destination IP address"

    scheme = get_scheme(event)

    for direction in ["source", "destination"]:
        # ensure we have IP information for this direction
        if not event[direction] and event[direction]["networkAddress"]:
            continue

        address = event[direction]["networkAddress"]["address"]

        if not is_public_ip(address):
            continue

        # Check if the flag <direction>_IS_CUSTOMERNET is set
        if "{}_IS_CUSTOMERNET".format(direction.upper()) in event["flags"]:
            debug("Address is customernet: {}, event={}".format(address, event))
            continue

        uri = "{}://{}".format(scheme, address)

        # Facts: uri components
        handle_uri(actapi, uri, output_format=output_format)

        # Fact: uri -> event
        handle_fact(
            actapi.fact("observedIn", "event").source("uri", uri).destination("event", event_id),
            output_format=output_format)


def handle_argus_event_fqdn(
        actapi: act.api.Act,
        event: defaultdict,
        event_id: Text,
        output_format: Text) -> None:
    "Create fact from fqdn"

    scheme = get_scheme(event)

    # Fact: fqdn -> event
    if event["domain"] and event["domain"]["fqdn"]:
        uri = "{}://{}".format(scheme, event["domain"]["fqdn"])

        # Facts, uri components
        handle_uri(actapi, uri, output_format=output_format)

        # Fact: uri -> event
        handle_fact(
            actapi.fact("observedIn", "event").source("uri", uri).destination("event", event_id),
            output_format=output_format)


def handle_argus_event(
        actapi: act.api.Act,
        event: Dict,
        content_props: List[Text],
        hash_props: List[Text],
        output_format: Text) -> None:
    "handle all facts from an argus event"

    # Use defaultdicts that defaults to None
    properties = defaultdict(lambda: None, event["properties"])
    event = defaultdict(lambda: None, event)

    signature = event["attackInfo"]["signature"]

    # Use argus ID (AGGRid) as event_id
    event_id = "ARGUS-{}".format(event["id"])

    # Fact: event -> incident
    if event["associatedCase"]:
        case_id = "ARGUS-{}".format(event["associatedCase"]["id"])
        handle_fact(
            actapi.fact("attributedTo", "incident").source("event", event_id).destination("incident", case_id),
            output_format=output_format)
        handle_fact(
            actapi.fact("name", event["associatedCase"]["description"]).source("incident", case_id),
            output_format=output_format)

    # Facts: hash/content -> event
    handle_argus_event_hash(actapi, properties, event_id, content_props, hash_props, output_format)

    # Facts: sourceIP -> event, destinationIP -> event
    handle_argus_event_ip(actapi, event, event_id, output_format)

    # Fact: signature -> event
    handle_fact(
        actapi.fact("detects", "event").source("signature", signature).destination("event", event_id),
        output_format=output_format)

    # Fact: uri -> event
    if event["uri"]:
        handle_uri(actapi, event["uri"], output_format=output_format)
        handle_fact(
            actapi.fact("observedIn", "event").source("uri", event["uri"]).destination("event", event_id),
            output_format=output_format)
    else:
        # Only construct URI from fqdn if we do not have an uri on the event. The URI
        # Is normally more correct (e.g. scheme and path will be more correctly specified)
        # Facts: uri fqdn -> uri ->  event
        handle_argus_event_fqdn(actapi, event, event_id, output_format)
