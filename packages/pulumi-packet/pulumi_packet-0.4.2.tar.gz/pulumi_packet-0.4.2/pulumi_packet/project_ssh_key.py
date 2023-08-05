# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from . import utilities, tables

class ProjectSshKey(pulumi.CustomResource):
    created: pulumi.Output[str]
    """
    The timestamp for when the SSH key was created
    """
    fingerprint: pulumi.Output[str]
    """
    The fingerprint of the SSH key
    """
    name: pulumi.Output[str]
    """
    The name of the SSH key for identification
    """
    project_id: pulumi.Output[str]
    """
    The ID of parent project
    """
    public_key: pulumi.Output[str]
    """
    The public key. If this is a file, it can be read using the file interpolation function
    """
    updated: pulumi.Output[str]
    """
    The timestamp for the last time the SSH key was updated
    """
    def __init__(__self__, resource_name, opts=None, name=None, project_id=None, public_key=None, __name__=None, __opts__=None):
        """
        Provides a Packet project SSH key resource to manage project-specific SSH keys. On contrary to user SSH keys, project SSH keys are used to exclusively populate `authorized_keys` in new devices.
        
        If you supply a list of project SSH keys when creating a new device, only the listed keys are used; user SSH keys are ignored.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] name: The name of the SSH key for identification
        :param pulumi.Input[str] project_id: The ID of parent project
        :param pulumi.Input[str] public_key: The public key. If this is a file, it can be read using the file interpolation function
        """
        if __name__ is not None:
            warnings.warn("explicit use of __name__ is deprecated", DeprecationWarning)
            resource_name = __name__
        if __opts__ is not None:
            warnings.warn("explicit use of __opts__ is deprecated, use 'opts' instead", DeprecationWarning)
            opts = __opts__
        if not resource_name:
            raise TypeError('Missing resource name argument (for URN creation)')
        if not isinstance(resource_name, str):
            raise TypeError('Expected resource name to be a string')
        if opts and not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')

        __props__ = dict()

        if name is None:
            raise TypeError("Missing required property 'name'")
        __props__['name'] = name

        if project_id is None:
            raise TypeError("Missing required property 'project_id'")
        __props__['project_id'] = project_id

        if public_key is None:
            raise TypeError("Missing required property 'public_key'")
        __props__['public_key'] = public_key

        __props__['created'] = None
        __props__['fingerprint'] = None
        __props__['updated'] = None

        super(ProjectSshKey, __self__).__init__(
            'packet:index/projectSshKey:ProjectSshKey',
            resource_name,
            __props__,
            opts)


    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

