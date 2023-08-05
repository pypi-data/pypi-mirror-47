# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from . import utilities, tables

class GetSshKeyResult:
    """
    A collection of values returned by getSshKey.
    """
    def __init__(__self__, fingerprint=None, name=None, public_key=None, id=None):
        if fingerprint and not isinstance(fingerprint, str):
            raise TypeError("Expected argument 'fingerprint' to be a str")
        __self__.fingerprint = fingerprint
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        __self__.name = name
        if public_key and not isinstance(public_key, str):
            raise TypeError("Expected argument 'public_key' to be a str")
        __self__.public_key = public_key
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        __self__.id = id
        """
        id is the provider-assigned unique ID for this managed resource.
        """

async def get_ssh_key(name=None,opts=None):
    """
    Get information on a ssh key. This data source provides the name, public key,
    and fingerprint as configured on your DigitalOcean account. This is useful if
    the ssh key in question is not managed by Terraform or you need to utilize any
    of the keys data.
    
    An error is triggered if the provided ssh key name does not exist.
    """
    __args__ = dict()

    __args__['name'] = name
    if opts is None:
        opts = pulumi.ResourceOptions()
    if opts.version is None:
        opts.version = utilities.get_version()
    __ret__ = await pulumi.runtime.invoke('digitalocean:index/getSshKey:getSshKey', __args__, opts=opts)

    return GetSshKeyResult(
        fingerprint=__ret__.get('fingerprint'),
        name=__ret__.get('name'),
        public_key=__ret__.get('publicKey'),
        id=__ret__.get('id'))
