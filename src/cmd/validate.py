#!/usr/bin/env python

import cli.log


@cli.log.LoggingApp
def validate(app):
    print_pseudo("starting validation with input: {}".format(app.params))




validate.add_param("-i", "--in", help="input file", default="out.v", type=str)

if __name__ == "__main__":
    validate.run()
