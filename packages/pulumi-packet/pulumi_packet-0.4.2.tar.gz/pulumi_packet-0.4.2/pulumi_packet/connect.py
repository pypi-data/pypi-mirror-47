# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from . import utilities, tables

class Connect(pulumi.CustomResource):
    facility: pulumi.Output[str]
    """
    Facility where to create the VLAN
    """
    name: pulumi.Output[str]
    """
    Name for the Connect resource
    """
    port_speed: pulumi.Output[float]
    """
    Port speed in Mbps
    """
    project_id: pulumi.Output[str]
    """
    ID of parent project
    """
    provider_id: pulumi.Output[str]
    """
    ID of Connect Provider. Provider IDs are
    * Azure ExpressRoute - "ed5de8e0-77a9-4d3b-9de0-65281d3aa831"
    """
    provider_payload: pulumi.Output[str]
    """
    Authorization key for the Connect provider
    """
    status: pulumi.Output[str]
    """
    Status of the Connect resource, one of PROVISIONING, PROVISIONED, DEPROVISIONING, DEPROVISIONED
    """
    vxlan: pulumi.Output[float]
    """
    VXLAN Network identifier of the linked Packet VLAN
    """
    def __init__(__self__, resource_name, opts=None, facility=None, name=None, port_speed=None, project_id=None, provider_id=None, provider_payload=None, vxlan=None, __name__=None, __opts__=None):
        """
        Provides a resource for [Packet Connect](https://www.packet.com/cloud/all-features/packet-connect/), a link between Packet VLANs and VLANs in other cloud providers.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] facility: Facility where to create the VLAN
        :param pulumi.Input[str] name: Name for the Connect resource
        :param pulumi.Input[float] port_speed: Port speed in Mbps
        :param pulumi.Input[str] project_id: ID of parent project
        :param pulumi.Input[str] provider_id: ID of Connect Provider. Provider IDs are
               * Azure ExpressRoute - "ed5de8e0-77a9-4d3b-9de0-65281d3aa831"
        :param pulumi.Input[str] provider_payload: Authorization key for the Connect provider
        :param pulumi.Input[float] vxlan: VXLAN Network identifier of the linked Packet VLAN
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

        if facility is None:
            raise TypeError("Missing required property 'facility'")
        __props__['facility'] = facility

        if name is None:
            raise TypeError("Missing required property 'name'")
        __props__['name'] = name

        if port_speed is None:
            raise TypeError("Missing required property 'port_speed'")
        __props__['port_speed'] = port_speed

        if project_id is None:
            raise TypeError("Missing required property 'project_id'")
        __props__['project_id'] = project_id

        if provider_id is None:
            raise TypeError("Missing required property 'provider_id'")
        __props__['provider_id'] = provider_id

        if provider_payload is None:
            raise TypeError("Missing required property 'provider_payload'")
        __props__['provider_payload'] = provider_payload

        if vxlan is None:
            raise TypeError("Missing required property 'vxlan'")
        __props__['vxlan'] = vxlan

        __props__['status'] = None

        super(Connect, __self__).__init__(
            'packet:index/connect:Connect',
            resource_name,
            __props__,
            opts)


    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

