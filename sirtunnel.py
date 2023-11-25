#!/usr/bin/env python3

import sys
import json
import time
import logging
from urllib import request

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)

APP_NAME = "tunnelboi"
CADDY_HOST = "127.0.0.1"
CADDY_API_PORT = "2019"


def add_route(tunnel_id: str, host: str, port: str):
    caddy_add_route_request = {
        "@id": tunnel_id,
        "match": [
            {
                "host": [host],
            }
        ],
        "handle": [{"handler": "reverse_proxy", "upstreams": [{"dial": ":" + port}]}],
    }
    body = json.dumps(caddy_add_route_request).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    create_url = (
        f"http://{CADDY_HOST}:{CADDY_API_PORT}/config/apps/http/servers/{APP_NAME}/routes"
    )
    # POST to caddy routes endpoint to add new route
    req = request.Request(method="POST", url=create_url, headers=headers)
    resp = request.urlopen(req, body)
    logger.info("Tunnel created successfully")
    return resp


def cleanup_route(tunnel_id: str):
    logger.info("Cleaning up tunnel")
    delete_url = f"http://{CADDY_HOST}:{CADDY_API_PORT}/id/{tunnel_id}"
    # DELETE route by id
    req = request.Request(method="DELETE", url=delete_url)
    resp = request.urlopen(req)
    return resp


def main(args):
    host = args[0]
    port = args[1]
    tunnel_id = host + "-" + port

    # call Caddy's api to create a reverse proxy forwarding traffic toward
    # host will be sent to :port on server
    resp = add_route(tunnel_id, host, port)
    logger.info(f"resp: {resp}")

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            cleanup_route(tunnel_id)
            return


if __name__ == "__main__":
    main(sys.argv[1:])
