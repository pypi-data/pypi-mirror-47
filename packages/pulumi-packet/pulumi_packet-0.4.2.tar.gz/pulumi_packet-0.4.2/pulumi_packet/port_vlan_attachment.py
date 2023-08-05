# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from . import utilities, tables

class PortVlanAttachment(pulumi.CustomResource):
    device_id: pulumi.Output[str]
    """
    ID of device to be assigned to the VLAN
    """
    force_bond: pulumi.Output[bool]
    """
    Add port back to the bond when this resource is removed. Default is false.
    """
    native: pulumi.Output[bool]
    """
    Mark this VLAN a native VLAN on the port. This can be used only if this assignment assigns second or further VLAN to the port. To ensure that this attachment is not first on a port, you can use `depends_on` pointing to another packet_port_vlan_attachment, just like in the layer2-individual example above. 
    """
    port_id: pulumi.Output[str]
    port_name: pulumi.Output[str]
    """
    Name of network port to be assigned to the VLAN
    """
    vlan_id: pulumi.Output[str]
    vlan_vnid: pulumi.Output[float]
    """
    VXLAN Network Identifier, integer
    """
    def __init__(__self__, resource_name, opts=None, device_id=None, force_bond=None, native=None, port_name=None, vlan_vnid=None, __name__=None, __opts__=None):
        """
        Provides a resource to attach device ports to VLANs.
        
        Device and VLAN must be in the same facility.
        
        If you need this resource to add the port back to bond on removal, set `force_bond = true`.
        
        To learn more about Layer 2 networking in Packet, refer to
        * https://support.packet.com/kb/articles/layer-2-configurations
        * https://support.packet.com/kb/articles/layer-2-overview
        
        ## Attribute Referece
        
        * `id` - UUID of device port used in the assignment
        * `vlan_id` - UUID of VLAN API resource
        * `port_id` - UUID of device port
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] device_id: ID of device to be assigned to the VLAN
        :param pulumi.Input[bool] force_bond: Add port back to the bond when this resource is removed. Default is false.
        :param pulumi.Input[bool] native: Mark this VLAN a native VLAN on the port. This can be used only if this assignment assigns second or further VLAN to the port. To ensure that this attachment is not first on a port, you can use `depends_on` pointing to another packet_port_vlan_attachment, just like in the layer2-individual example above. 
        :param pulumi.Input[str] port_name: Name of network port to be assigned to the VLAN
        :param pulumi.Input[float] vlan_vnid: VXLAN Network Identifier, integer
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

        if device_id is None:
            raise TypeError("Missing required property 'device_id'")
        __props__['device_id'] = device_id

        __props__['force_bond'] = force_bond

        __props__['native'] = native

        if port_name is None:
            raise TypeError("Missing required property 'port_name'")
        __props__['port_name'] = port_name

        if vlan_vnid is None:
            raise TypeError("Missing required property 'vlan_vnid'")
        __props__['vlan_vnid'] = vlan_vnid

        __props__['port_id'] = None
        __props__['vlan_id'] = None

        super(PortVlanAttachment, __self__).__init__(
            'packet:index/portVlanAttachment:PortVlanAttachment',
            resource_name,
            __props__,
            opts)


    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

