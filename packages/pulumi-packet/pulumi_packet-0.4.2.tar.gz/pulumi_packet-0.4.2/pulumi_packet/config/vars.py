# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from .. import utilities, tables

__config__ = pulumi.Config('packet')

auth_token = __config__.get('authToken') or utilities.get_env('PACKET_AUTH_TOKEN')
"""
The API auth key for API operations.
"""

