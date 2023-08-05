# Copyright (C) 2015-2016 Regents of the University of California
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import absolute_import
from builtins import str
from builtins import object
import datetime
import logging
import os

from bd2k.util import parse_iso_utc, less_strict_bool


logger = logging.getLogger(__name__)


def awsRemainingBillingInterval(instance):
    """
    Takes a node object and determines how far into it's billing cycle it is.

    :param instance:
    :return:
    """
    def partialBillingInterval(instance):
        """
        Returns a floating point value between 0 and 1.0 representing how far we are into the
        current billing cycle for the given instance. If the return value is .25, we are one
        quarter into the billing cycle, with three quarters remaining before we will be charged
        again for that instance.
        """
        launch_time = parse_iso_utc(instance.launchTime)
        now = datetime.datetime.utcnow()
        delta = now - launch_time
        return delta.total_seconds() / 3600.0 % 1.0

    return 1.0 - partialBillingInterval(instance)


def awsFilterImpairedNodes(nodes, ec2):
    # if TOIL_AWS_NODE_DEBUG is set don't terminate nodes with
    # failing status checks so they can be debugged
    nodeDebug = less_strict_bool(os.environ.get('TOIL_AWS_NODE_DEBUG'))
    if not nodeDebug:
        return nodes
    nodeIDs = [node.id for node in nodes]
    statuses = ec2.get_all_instance_status(instance_ids=nodeIDs)
    statusMap = {status.id: status.instance_status for status in statuses}
    healthyNodes = [node for node in nodes if statusMap.get(node.id, None) != 'impaired']
    impairedNodes = [node.id for node in nodes if statusMap.get(node.id, None) == 'impaired']
    logger.warn('TOIL_AWS_NODE_DEBUG is set and nodes %s have failed EC2 status checks so '
                'will not be terminated.', ' '.join(impairedNodes))
    return healthyNodes


class Cluster(object):
    def __init__(self, clusterName, provisioner, zone=None):
        self.clusterName = clusterName
        self.zone = zone
        self.provisionerType = provisioner
        if provisioner == 'aws':
            from toil.provisioners.aws.awsProvisioner import AWSProvisioner
            self.provisioner = AWSProvisioner
        elif provisioner == 'azure':
            from toil.provisioners.azure.azureProvisioner import AzureProvisioner
            self.provisioner = AzureProvisioner
        elif provisioner == 'gce':
            from toil.provisioners.gceProvisioner import GCEProvisioner
            self.provisioner = GCEProvisioner()
        else:
            assert False, "Invalid provisioner '%s'" % provisioner

    def sshCluster(self, args, **kwargs):
        self.provisioner.sshLeader(self.clusterName, args, self.zone, **kwargs)

    def rsyncCluster(self, args, **kwargs):
        self.provisioner.rsyncLeader(self.clusterName, args, self.zone, **kwargs)

        # Why was this added? It is undocumented and calling private methods.
        #ctx = self.provisioner._buildContext(self.clusterName, zone=self.zone)
        #instances = self.provisioner._getNodesInCluster(ctx, self.clusterName, both=True)
        #leader = self.provisioner._getLeader(self.clusterName, zone=self.zone)
        #workers = [i for i in instances if i.public_dns_name != leader.public_dns_name]
        #for instance in workers:
        #    self.provisioner._waitForNode(instance, 'toil_worker')
        #    self.provisioner._coreRsync(instance.public_dns_name, args, applianceName='toil_worker', **kwargs)

    def destroyCluster(self):
        self.provisioner.destroyCluster(self.clusterName, self.zone)


class Node(object):
    def __init__(self, publicIP, privateIP, name, launchTime, nodeType, preemptable):
        self.publicIP = publicIP
        self.privateIP = privateIP
        self.name = name
        self.launchTime = launchTime
        self.nodeType = nodeType
        self.preemptable = preemptable

    def __str__(self):
        return "%s at %s" % (self.name, self.publicIP)

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(self.publicIP)


class NoSuchClusterException(Exception):
    """Indicates that the specified cluster does not exist."""
    def __init__(self, clusterName):
        super(NoSuchClusterException, self).__init__("The cluster '%s' could not be found" % clusterName)
