"""Test Module for training.

Test project

Usage:
    run.py create
    run.py fetch <url>

Options
    url     URL to fetch
"""
import docopt

import app.main as app

if __name__ ==  "__main__":
    args = docopt.docopt(__doc__)

    if args['create']:
        app.create()
    elif args['fetch']:
        app.fetch(args['<url>'])
