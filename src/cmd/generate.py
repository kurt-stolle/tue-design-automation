#!/usr/bin/env python

import cli.log


@cli.log.LoggingApp
def generate(app):
    print("starting generation with input: {}".format(app.params))


generate.add_param("-f", "--fpga-model", help="the fpga model", default="default", type=str, )
generate.add_param("-c", "--cnn-model", help="the convolution layer model", default="default", type=str)
generate.add_param("-o", "--output-file", help="the output file", default="out.v", type=str)

if __name__ == "__main__":
    generate.run()
