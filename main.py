#!/usr/bin/env python3

import crowd
import argparse
import json

class Arguments:
    pass

def delete_group(server, name):
    resp = server.delete_group(name)
    if resp == 204:
        print("%s : Deleted" % name)
    else:
         print("%s : Not deleted, could not be found" % name)

def add_group(server, name, description):
    resp = server.add_group(name, description)

    if "link" in resp: 
        print("%s : Created" % name)
    else:
        print("%s : Failed to create: %s" % (name, resp['message']))

def main():
    args = Arguments()
    parser = argparse.ArgumentParser(description="Dumps groups from an Atlassian Crowd directory")
    parser.add_argument('--username', dest='username', help='Username of the Crowd application to authenticate as', required=True)
    parser.add_argument('--host', dest='host', help='Crowd host URL', required=True)
    parser.add_argument('--password', dest='password')
    
    parser.parse_args(namespace=args)


    
    app_url = "https://%s/crowd/" % (args.host)

    src_server = crowd.CrowdServer(app_url, args.username, args.password)
    dest_server = crowd.CrowdServer(app_url, "dump_groups_new", args.password)


    for group in src_server.get_all_groups()['groups']:
        g = src_server.search('group', 'name', group['name'])
        gr = g['groups'][0]
        description =  gr['description'] if 'description' in gr else ''

        add_group(dest_server, gr['name'], description )

        # delete_group(dest_server, gr['name'])


if __name__ == "__main__":
    main()