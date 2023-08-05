'''

Copyright (C) 2017-2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

from sregistry.logger import bot
import sys
import os

def main(args,parser,subparser):

    from sregistry.main import get_client

    # Does the user have a valid image?
    image = args.image[0]
    if not os.path.exists(image):  
        subparser.print_help()
        bot.exit("Please supply one or more paths to existing images.")

    # Authenticate
    cli = get_client(args.name, quiet=args.quiet)
    cli.announce(args.command)

    # If the client doesn't have the command, exit
    if not hasattr(cli, 'push'):
        msg = "push is not implemented for %s. Why don't you add it?"
        bot.exit(msg % cli.client_name)

    response = cli.push(path=image,
                        name=args.name,
                        tag=args.tag)
