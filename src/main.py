#!/usr/bin/env python3

import logging

import openstack
import requests

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')


def travis_job_status(name):
    try:
        job = name.split("-")[1]
    except:
        job = name.split("molecule")[1]

    result = requests.get("https://api.travis-ci.org/v3/job/%s" % job)
    result = result.json()

    if "error_type" in result:
        return 2
    elif result["finished_at"] != None:
        return 0
    else:
        return 1


def cleanup_servers(conn):
    logging.info("clean up servers")
    for server in conn.compute.servers():
        server_dict = server.to_dict()
        server_name = server_dict["name"]

        if not server_name.startswith("molecule"):
            continue

        if travis_job_status(server_name) == 0:
            logging.info(server_name)
            conn.compute.delete_server(server_dict["id"], force=True)


def cleanup_keypairs(conn):
    logging.info("clean up keypairs")
    for keypair in conn.compute.keypairs():
        keypair_dict = keypair.to_dict()
        keypair_name = keypair_dict["name"]

        if not keypair_name.startswith("molecule"):
            continue

        if travis_job_status(keypair_name) == 0:
            logging.info(keypair_name)
            conn.compute.delete_keypair(keypair)


def cleanup_security_groups(conn):
    logging.info("clean up security groups")
    for security_group in conn.network.security_groups():
        security_group_dict = security_group.to_dict()
        security_group_name = security_group_dict["name"]

        if not security_group_name.startswith("molecule"):
            continue

        if travis_job_status(security_group_name) == 0:
            logging.info(security_group_name)
            conn.network.delete_security_group(security_group)


def cleanup_floating_ips(conn):
    logging.info("clean up floating ips")
    for floating_ip in conn.search_floating_ips():
        floating_ip_dict = dict(floating_ip)
        floating_ip_name = floating_ip["floating_ip_address"]

        if not floating_ip_dict["attached"]:
            logging.info(floating_ip_name)
            conn.delete_floating_ip(floating_ip_dict["id"])


def main():
    conn = openstack.connect(cloud='molecule')
    cleanup_servers(conn)
    cleanup_keypairs(conn)
    cleanup_security_groups(conn)
    cleanup_floating_ips(conn)


if __name__ == '__main__':
    main()
