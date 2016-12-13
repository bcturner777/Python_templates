"""
config generator with custom filter
-----------------------------------
This script will generate an interface configuration for a Cisco IOS and Juniper JUNOS device based on a common set of
parameters to demonstrate the use of custom filters with the Jinja2 template engine.
"""
import jinja2
import json
import os
from ipaddress import IPv4Network

parameter_file = "test-parameters.json"
template_file = "testrouter.jinja2"
output_directory = "test_output"


def dotted_decimal(prefix_length):
    """
    converts the given prefix to a IPv4 dotted decimal representation
    :param prefix_length:
    :return:
    """
    try:
        ip = IPv4Network(u"0.0.0.0/" + str(prefix_length))
        return ip.netmask
    except Exception:
        return "[INVALID VALUE(" + str(prefix_length) + ")]"


print("Read JSON parameter file...")
config_parameters = json.load(open(parameter_file))

# next we need to create the central Jinja2 environment and we will load
# the Jinja2 template file (the two parameters ensure a clean output in the
# configuration file)

print "Create the Jinja2 environment..."
env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath="."),
                         trim_blocks=True,
                         lstrip_blocks=True)

    # register custom filters on the jinja2 environment
env.filters["dotted_decimal"] = dotted_decimal
# load template file
template = env.get_template(template_file)

# just make sure that the output directory exists
if not os.path.exists(output_directory):
    os.mkdir(output_directory)

# create the templates for all vendors
print("Create templates...")
#for parameter in config_parameters:
#    print parameter
print "config_parameters dictionary below"
print config_parameters
print template
# http://jinja.pocoo.org/docs/dev/api/
# Python 2.7 render function requires two iterators
result = template.render(config_parameters=config_parameters)
f = open(os.path.join(output_directory, "test-router.cfg"), "w")
f.write(result)
f.close()
#    print("Configuration '%s' created for %s" % ("wanex.config"))

print("DONE")

