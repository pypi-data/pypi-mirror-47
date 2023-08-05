# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from . import utilities, tables

class NodeBalancerNode(pulumi.CustomResource):
    address: pulumi.Output[str]
    """
    The private IP Address where this backend can be reached. This must be a private IP address.
    """
    config_id: pulumi.Output[float]
    """
    The ID of the NodeBalancerConfig to access.
    """
    label: pulumi.Output[str]
    """
    The label of the Linode NodeBalancer Node. This is for display purposes only.
    """
    mode: pulumi.Output[str]
    """
    The mode this NodeBalancer should use when sending traffic to this backend. If set to `accept` this backend is accepting traffic. If set to `reject` this backend will not receive traffic. If set to `drain` this backend will not receive new traffic, but connections already pinned to it will continue to be routed to it
    """
    nodebalancer_id: pulumi.Output[float]
    """
    The ID of the NodeBalancer to access.
    """
    status: pulumi.Output[str]
    weight: pulumi.Output[float]
    """
    Used when picking a backend to serve a request and is not pinned to a single backend yet. Nodes with a higher weight will receive more traffic. (1-255).
    """
    def __init__(__self__, resource_name, opts=None, address=None, config_id=None, label=None, mode=None, nodebalancer_id=None, weight=None, __name__=None, __opts__=None):
        """
        Provides a Linode NodeBalancer Node resource.  This can be used to create, modify, and delete Linodes NodeBalancer Nodes.
        For more information, see [Getting Started with NodeBalancers](https://www.linode.com/docs/platform/nodebalancer/getting-started-with-nodebalancers/) and the [Linode APIv4 docs](https://developers.linode.com/api/v4#operation/createNodeBalancerNode).
        
        The Linode Guide, [Create a NodeBalancer with Terraform](https://www.linode.com/docs/applications/configuration-management/create-a-nodebalancer-with-terraform/), provides step-by-step guidance and additional examples.
        
        ## Attributes
        
        This resource exports the following attributes:
        
        * `status` - The current status of this node, based on the configured checks of its NodeBalancer Config. (unknown, UP, DOWN).
        
        * `config_id` - The ID of the NodeBalancerConfig this NodeBalancerNode is attached to.
        
        * `nodebalancer_id` - The ID of the NodeBalancer this NodeBalancerNode is attached to.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] address: The private IP Address where this backend can be reached. This must be a private IP address.
        :param pulumi.Input[float] config_id: The ID of the NodeBalancerConfig to access.
        :param pulumi.Input[str] label: The label of the Linode NodeBalancer Node. This is for display purposes only.
        :param pulumi.Input[str] mode: The mode this NodeBalancer should use when sending traffic to this backend. If set to `accept` this backend is accepting traffic. If set to `reject` this backend will not receive traffic. If set to `drain` this backend will not receive new traffic, but connections already pinned to it will continue to be routed to it
        :param pulumi.Input[float] nodebalancer_id: The ID of the NodeBalancer to access.
        :param pulumi.Input[float] weight: Used when picking a backend to serve a request and is not pinned to a single backend yet. Nodes with a higher weight will receive more traffic. (1-255).
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

        if address is None:
            raise TypeError("Missing required property 'address'")
        __props__['address'] = address

        if config_id is None:
            raise TypeError("Missing required property 'config_id'")
        __props__['config_id'] = config_id

        if label is None:
            raise TypeError("Missing required property 'label'")
        __props__['label'] = label

        __props__['mode'] = mode

        if nodebalancer_id is None:
            raise TypeError("Missing required property 'nodebalancer_id'")
        __props__['nodebalancer_id'] = nodebalancer_id

        __props__['weight'] = weight

        __props__['status'] = None

        super(NodeBalancerNode, __self__).__init__(
            'linode:index/nodeBalancerNode:NodeBalancerNode',
            resource_name,
            __props__,
            opts)


    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

