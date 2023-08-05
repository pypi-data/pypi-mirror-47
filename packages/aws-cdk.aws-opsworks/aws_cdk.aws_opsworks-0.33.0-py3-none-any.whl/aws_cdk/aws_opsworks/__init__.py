import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-opsworks", "0.33.0", __name__, "aws-opsworks@0.33.0.jsii.tgz")
class CfnApp(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-opsworks.CfnApp"):
    """A CloudFormation ``AWS::OpsWorks::App``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html
    cloudformationResource:
        AWS::OpsWorks::App
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, name: str, stack_id: str, type: str, app_source: typing.Optional[typing.Union[typing.Optional["SourceProperty"], typing.Optional[aws_cdk.cdk.Token]]]=None, attributes: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional[typing.Mapping[str,str]]]]=None, data_sources: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional[typing.List[typing.Union[aws_cdk.cdk.Token, "DataSourceProperty"]]]]]=None, description: typing.Optional[str]=None, domains: typing.Optional[typing.List[str]]=None, enable_ssl: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.cdk.Token]]]=None, environment: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional[typing.List[typing.Union[aws_cdk.cdk.Token, "EnvironmentVariableProperty"]]]]]=None, shortname: typing.Optional[str]=None, ssl_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional["SslConfigurationProperty"]]]=None) -> None:
        """Create a new ``AWS::OpsWorks::App``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            name: ``AWS::OpsWorks::App.Name``.
            stackId: ``AWS::OpsWorks::App.StackId``.
            type: ``AWS::OpsWorks::App.Type``.
            appSource: ``AWS::OpsWorks::App.AppSource``.
            attributes: ``AWS::OpsWorks::App.Attributes``.
            dataSources: ``AWS::OpsWorks::App.DataSources``.
            description: ``AWS::OpsWorks::App.Description``.
            domains: ``AWS::OpsWorks::App.Domains``.
            enableSsl: ``AWS::OpsWorks::App.EnableSsl``.
            environment: ``AWS::OpsWorks::App.Environment``.
            shortname: ``AWS::OpsWorks::App.Shortname``.
            sslConfiguration: ``AWS::OpsWorks::App.SslConfiguration``.
        """
        props: CfnAppProps = {"name": name, "stackId": stack_id, "type": type}

        if app_source is not None:
            props["appSource"] = app_source

        if attributes is not None:
            props["attributes"] = attributes

        if data_sources is not None:
            props["dataSources"] = data_sources

        if description is not None:
            props["description"] = description

        if domains is not None:
            props["domains"] = domains

        if enable_ssl is not None:
            props["enableSsl"] = enable_ssl

        if environment is not None:
            props["environment"] = environment

        if shortname is not None:
            props["shortname"] = shortname

        if ssl_configuration is not None:
            props["sslConfiguration"] = ssl_configuration

        jsii.create(CfnApp, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        """
        Arguments:
            properties: -
        """
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="appId")
    def app_id(self) -> str:
        return jsii.get(self, "appId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnAppProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnApp.DataSourceProperty", jsii_struct_bases=[])
    class DataSourceProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-app-datasource.html
        """
        arn: str
        """``CfnApp.DataSourceProperty.Arn``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-app-datasource.html#cfn-opsworks-app-datasource-arn
        """

        databaseName: str
        """``CfnApp.DataSourceProperty.DatabaseName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-app-datasource.html#cfn-opsworks-app-datasource-databasename
        """

        type: str
        """``CfnApp.DataSourceProperty.Type``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-app-datasource.html#cfn-opsworks-app-datasource-type
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _EnvironmentVariableProperty(jsii.compat.TypedDict, total=False):
        secure: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnApp.EnvironmentVariableProperty.Secure``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-app-environment.html#cfn-opsworks-app-environment-secure
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnApp.EnvironmentVariableProperty", jsii_struct_bases=[_EnvironmentVariableProperty])
    class EnvironmentVariableProperty(_EnvironmentVariableProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-app-environment.html
        """
        key: str
        """``CfnApp.EnvironmentVariableProperty.Key``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-app-environment.html#cfn-opsworks-app-environment-key
        """

        value: str
        """``CfnApp.EnvironmentVariableProperty.Value``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-app-environment.html#value
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnApp.SourceProperty", jsii_struct_bases=[])
    class SourceProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-source.html
        """
        password: str
        """``CfnApp.SourceProperty.Password``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-source.html#cfn-opsworks-custcookbooksource-pw
        """

        revision: str
        """``CfnApp.SourceProperty.Revision``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-source.html#cfn-opsworks-custcookbooksource-revision
        """

        sshKey: str
        """``CfnApp.SourceProperty.SshKey``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-source.html#cfn-opsworks-custcookbooksource-sshkey
        """

        type: str
        """``CfnApp.SourceProperty.Type``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-source.html#cfn-opsworks-custcookbooksource-type
        """

        url: str
        """``CfnApp.SourceProperty.Url``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-source.html#cfn-opsworks-custcookbooksource-url
        """

        username: str
        """``CfnApp.SourceProperty.Username``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-source.html#cfn-opsworks-custcookbooksource-username
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnApp.SslConfigurationProperty", jsii_struct_bases=[])
    class SslConfigurationProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-app-sslconfiguration.html
        """
        certificate: str
        """``CfnApp.SslConfigurationProperty.Certificate``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-app-sslconfiguration.html#cfn-opsworks-app-sslconfig-certificate
        """

        chain: str
        """``CfnApp.SslConfigurationProperty.Chain``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-app-sslconfiguration.html#cfn-opsworks-app-sslconfig-chain
        """

        privateKey: str
        """``CfnApp.SslConfigurationProperty.PrivateKey``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-app-sslconfiguration.html#cfn-opsworks-app-sslconfig-privatekey
        """


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnAppProps(jsii.compat.TypedDict, total=False):
    appSource: typing.Union["CfnApp.SourceProperty", aws_cdk.cdk.Token]
    """``AWS::OpsWorks::App.AppSource``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-appsource
    """
    attributes: typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]
    """``AWS::OpsWorks::App.Attributes``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-attributes
    """
    dataSources: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnApp.DataSourceProperty"]]]
    """``AWS::OpsWorks::App.DataSources``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-datasources
    """
    description: str
    """``AWS::OpsWorks::App.Description``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-description
    """
    domains: typing.List[str]
    """``AWS::OpsWorks::App.Domains``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-domains
    """
    enableSsl: typing.Union[bool, aws_cdk.cdk.Token]
    """``AWS::OpsWorks::App.EnableSsl``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-enablessl
    """
    environment: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnApp.EnvironmentVariableProperty"]]]
    """``AWS::OpsWorks::App.Environment``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-environment
    """
    shortname: str
    """``AWS::OpsWorks::App.Shortname``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-shortname
    """
    sslConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnApp.SslConfigurationProperty"]
    """``AWS::OpsWorks::App.SslConfiguration``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-sslconfiguration
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnAppProps", jsii_struct_bases=[_CfnAppProps])
class CfnAppProps(_CfnAppProps):
    """Properties for defining a ``AWS::OpsWorks::App``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html
    """
    name: str
    """``AWS::OpsWorks::App.Name``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-name
    """

    stackId: str
    """``AWS::OpsWorks::App.StackId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-stackid
    """

    type: str
    """``AWS::OpsWorks::App.Type``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-type
    """

class CfnElasticLoadBalancerAttachment(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-opsworks.CfnElasticLoadBalancerAttachment"):
    """A CloudFormation ``AWS::OpsWorks::ElasticLoadBalancerAttachment``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-elbattachment.html
    cloudformationResource:
        AWS::OpsWorks::ElasticLoadBalancerAttachment
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, elastic_load_balancer_name: str, layer_id: str) -> None:
        """Create a new ``AWS::OpsWorks::ElasticLoadBalancerAttachment``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            elasticLoadBalancerName: ``AWS::OpsWorks::ElasticLoadBalancerAttachment.ElasticLoadBalancerName``.
            layerId: ``AWS::OpsWorks::ElasticLoadBalancerAttachment.LayerId``.
        """
        props: CfnElasticLoadBalancerAttachmentProps = {"elasticLoadBalancerName": elastic_load_balancer_name, "layerId": layer_id}

        jsii.create(CfnElasticLoadBalancerAttachment, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        """
        Arguments:
            properties: -
        """
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnElasticLoadBalancerAttachmentProps":
        return jsii.get(self, "propertyOverrides")


@jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnElasticLoadBalancerAttachmentProps", jsii_struct_bases=[])
class CfnElasticLoadBalancerAttachmentProps(jsii.compat.TypedDict):
    """Properties for defining a ``AWS::OpsWorks::ElasticLoadBalancerAttachment``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-elbattachment.html
    """
    elasticLoadBalancerName: str
    """``AWS::OpsWorks::ElasticLoadBalancerAttachment.ElasticLoadBalancerName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-elbattachment.html#cfn-opsworks-elbattachment-elbname
    """

    layerId: str
    """``AWS::OpsWorks::ElasticLoadBalancerAttachment.LayerId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-elbattachment.html#cfn-opsworks-elbattachment-layerid
    """

class CfnInstance(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-opsworks.CfnInstance"):
    """A CloudFormation ``AWS::OpsWorks::Instance``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html
    cloudformationResource:
        AWS::OpsWorks::Instance
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, instance_type: str, layer_ids: typing.List[str], stack_id: str, agent_version: typing.Optional[str]=None, ami_id: typing.Optional[str]=None, architecture: typing.Optional[str]=None, auto_scaling_type: typing.Optional[str]=None, availability_zone: typing.Optional[str]=None, block_device_mappings: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional[typing.List[typing.Union[aws_cdk.cdk.Token, "BlockDeviceMappingProperty"]]]]]=None, ebs_optimized: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.cdk.Token]]]=None, elastic_ips: typing.Optional[typing.List[str]]=None, hostname: typing.Optional[str]=None, install_updates_on_boot: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.cdk.Token]]]=None, os: typing.Optional[str]=None, root_device_type: typing.Optional[str]=None, ssh_key_name: typing.Optional[str]=None, subnet_id: typing.Optional[str]=None, tenancy: typing.Optional[str]=None, time_based_auto_scaling: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional["TimeBasedAutoScalingProperty"]]]=None, virtualization_type: typing.Optional[str]=None, volumes: typing.Optional[typing.List[str]]=None) -> None:
        """Create a new ``AWS::OpsWorks::Instance``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            instanceType: ``AWS::OpsWorks::Instance.InstanceType``.
            layerIds: ``AWS::OpsWorks::Instance.LayerIds``.
            stackId: ``AWS::OpsWorks::Instance.StackId``.
            agentVersion: ``AWS::OpsWorks::Instance.AgentVersion``.
            amiId: ``AWS::OpsWorks::Instance.AmiId``.
            architecture: ``AWS::OpsWorks::Instance.Architecture``.
            autoScalingType: ``AWS::OpsWorks::Instance.AutoScalingType``.
            availabilityZone: ``AWS::OpsWorks::Instance.AvailabilityZone``.
            blockDeviceMappings: ``AWS::OpsWorks::Instance.BlockDeviceMappings``.
            ebsOptimized: ``AWS::OpsWorks::Instance.EbsOptimized``.
            elasticIps: ``AWS::OpsWorks::Instance.ElasticIps``.
            hostname: ``AWS::OpsWorks::Instance.Hostname``.
            installUpdatesOnBoot: ``AWS::OpsWorks::Instance.InstallUpdatesOnBoot``.
            os: ``AWS::OpsWorks::Instance.Os``.
            rootDeviceType: ``AWS::OpsWorks::Instance.RootDeviceType``.
            sshKeyName: ``AWS::OpsWorks::Instance.SshKeyName``.
            subnetId: ``AWS::OpsWorks::Instance.SubnetId``.
            tenancy: ``AWS::OpsWorks::Instance.Tenancy``.
            timeBasedAutoScaling: ``AWS::OpsWorks::Instance.TimeBasedAutoScaling``.
            virtualizationType: ``AWS::OpsWorks::Instance.VirtualizationType``.
            volumes: ``AWS::OpsWorks::Instance.Volumes``.
        """
        props: CfnInstanceProps = {"instanceType": instance_type, "layerIds": layer_ids, "stackId": stack_id}

        if agent_version is not None:
            props["agentVersion"] = agent_version

        if ami_id is not None:
            props["amiId"] = ami_id

        if architecture is not None:
            props["architecture"] = architecture

        if auto_scaling_type is not None:
            props["autoScalingType"] = auto_scaling_type

        if availability_zone is not None:
            props["availabilityZone"] = availability_zone

        if block_device_mappings is not None:
            props["blockDeviceMappings"] = block_device_mappings

        if ebs_optimized is not None:
            props["ebsOptimized"] = ebs_optimized

        if elastic_ips is not None:
            props["elasticIps"] = elastic_ips

        if hostname is not None:
            props["hostname"] = hostname

        if install_updates_on_boot is not None:
            props["installUpdatesOnBoot"] = install_updates_on_boot

        if os is not None:
            props["os"] = os

        if root_device_type is not None:
            props["rootDeviceType"] = root_device_type

        if ssh_key_name is not None:
            props["sshKeyName"] = ssh_key_name

        if subnet_id is not None:
            props["subnetId"] = subnet_id

        if tenancy is not None:
            props["tenancy"] = tenancy

        if time_based_auto_scaling is not None:
            props["timeBasedAutoScaling"] = time_based_auto_scaling

        if virtualization_type is not None:
            props["virtualizationType"] = virtualization_type

        if volumes is not None:
            props["volumes"] = volumes

        jsii.create(CfnInstance, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        """
        Arguments:
            properties: -
        """
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="instanceAvailabilityZone")
    def instance_availability_zone(self) -> str:
        """
        cloudformationAttribute:
            AvailabilityZone
        """
        return jsii.get(self, "instanceAvailabilityZone")

    @property
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> str:
        return jsii.get(self, "instanceId")

    @property
    @jsii.member(jsii_name="instancePrivateDnsName")
    def instance_private_dns_name(self) -> str:
        """
        cloudformationAttribute:
            PrivateDnsName
        """
        return jsii.get(self, "instancePrivateDnsName")

    @property
    @jsii.member(jsii_name="instancePrivateIp")
    def instance_private_ip(self) -> str:
        """
        cloudformationAttribute:
            PrivateIp
        """
        return jsii.get(self, "instancePrivateIp")

    @property
    @jsii.member(jsii_name="instancePublicDnsName")
    def instance_public_dns_name(self) -> str:
        """
        cloudformationAttribute:
            PublicDnsName
        """
        return jsii.get(self, "instancePublicDnsName")

    @property
    @jsii.member(jsii_name="instancePublicIp")
    def instance_public_ip(self) -> str:
        """
        cloudformationAttribute:
            PublicIp
        """
        return jsii.get(self, "instancePublicIp")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnInstanceProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnInstance.BlockDeviceMappingProperty", jsii_struct_bases=[])
    class BlockDeviceMappingProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-blockdevicemapping.html
        """
        deviceName: str
        """``CfnInstance.BlockDeviceMappingProperty.DeviceName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-blockdevicemapping.html#cfn-opsworks-instance-blockdevicemapping-devicename
        """

        ebs: typing.Union[aws_cdk.cdk.Token, "CfnInstance.EbsBlockDeviceProperty"]
        """``CfnInstance.BlockDeviceMappingProperty.Ebs``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-blockdevicemapping.html#cfn-opsworks-instance-blockdevicemapping-ebs
        """

        noDevice: str
        """``CfnInstance.BlockDeviceMappingProperty.NoDevice``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-blockdevicemapping.html#cfn-opsworks-instance-blockdevicemapping-nodevice
        """

        virtualName: str
        """``CfnInstance.BlockDeviceMappingProperty.VirtualName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-blockdevicemapping.html#cfn-opsworks-instance-blockdevicemapping-virtualname
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnInstance.EbsBlockDeviceProperty", jsii_struct_bases=[])
    class EbsBlockDeviceProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-ebsblockdevice.html
        """
        deleteOnTermination: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnInstance.EbsBlockDeviceProperty.DeleteOnTermination``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-ebsblockdevice.html#cfn-opsworks-instance-ebsblockdevice-deleteontermination
        """

        iops: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnInstance.EbsBlockDeviceProperty.Iops``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-ebsblockdevice.html#cfn-opsworks-instance-ebsblockdevice-iops
        """

        snapshotId: str
        """``CfnInstance.EbsBlockDeviceProperty.SnapshotId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-ebsblockdevice.html#cfn-opsworks-instance-ebsblockdevice-snapshotid
        """

        volumeSize: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnInstance.EbsBlockDeviceProperty.VolumeSize``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-ebsblockdevice.html#cfn-opsworks-instance-ebsblockdevice-volumesize
        """

        volumeType: str
        """``CfnInstance.EbsBlockDeviceProperty.VolumeType``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-ebsblockdevice.html#cfn-opsworks-instance-ebsblockdevice-volumetype
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnInstance.TimeBasedAutoScalingProperty", jsii_struct_bases=[])
    class TimeBasedAutoScalingProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-timebasedautoscaling.html
        """
        friday: typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]
        """``CfnInstance.TimeBasedAutoScalingProperty.Friday``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-timebasedautoscaling.html#cfn-opsworks-instance-timebasedautoscaling-friday
        """

        monday: typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]
        """``CfnInstance.TimeBasedAutoScalingProperty.Monday``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-timebasedautoscaling.html#cfn-opsworks-instance-timebasedautoscaling-monday
        """

        saturday: typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]
        """``CfnInstance.TimeBasedAutoScalingProperty.Saturday``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-timebasedautoscaling.html#cfn-opsworks-instance-timebasedautoscaling-saturday
        """

        sunday: typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]
        """``CfnInstance.TimeBasedAutoScalingProperty.Sunday``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-timebasedautoscaling.html#cfn-opsworks-instance-timebasedautoscaling-sunday
        """

        thursday: typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]
        """``CfnInstance.TimeBasedAutoScalingProperty.Thursday``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-timebasedautoscaling.html#cfn-opsworks-instance-timebasedautoscaling-thursday
        """

        tuesday: typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]
        """``CfnInstance.TimeBasedAutoScalingProperty.Tuesday``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-timebasedautoscaling.html#cfn-opsworks-instance-timebasedautoscaling-tuesday
        """

        wednesday: typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]
        """``CfnInstance.TimeBasedAutoScalingProperty.Wednesday``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-timebasedautoscaling.html#cfn-opsworks-instance-timebasedautoscaling-wednesday
        """


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnInstanceProps(jsii.compat.TypedDict, total=False):
    agentVersion: str
    """``AWS::OpsWorks::Instance.AgentVersion``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-agentversion
    """
    amiId: str
    """``AWS::OpsWorks::Instance.AmiId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-amiid
    """
    architecture: str
    """``AWS::OpsWorks::Instance.Architecture``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-architecture
    """
    autoScalingType: str
    """``AWS::OpsWorks::Instance.AutoScalingType``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-autoscalingtype
    """
    availabilityZone: str
    """``AWS::OpsWorks::Instance.AvailabilityZone``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-availabilityzone
    """
    blockDeviceMappings: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnInstance.BlockDeviceMappingProperty"]]]
    """``AWS::OpsWorks::Instance.BlockDeviceMappings``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-blockdevicemappings
    """
    ebsOptimized: typing.Union[bool, aws_cdk.cdk.Token]
    """``AWS::OpsWorks::Instance.EbsOptimized``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-ebsoptimized
    """
    elasticIps: typing.List[str]
    """``AWS::OpsWorks::Instance.ElasticIps``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-elasticips
    """
    hostname: str
    """``AWS::OpsWorks::Instance.Hostname``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-hostname
    """
    installUpdatesOnBoot: typing.Union[bool, aws_cdk.cdk.Token]
    """``AWS::OpsWorks::Instance.InstallUpdatesOnBoot``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-installupdatesonboot
    """
    os: str
    """``AWS::OpsWorks::Instance.Os``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-os
    """
    rootDeviceType: str
    """``AWS::OpsWorks::Instance.RootDeviceType``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-rootdevicetype
    """
    sshKeyName: str
    """``AWS::OpsWorks::Instance.SshKeyName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-sshkeyname
    """
    subnetId: str
    """``AWS::OpsWorks::Instance.SubnetId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-subnetid
    """
    tenancy: str
    """``AWS::OpsWorks::Instance.Tenancy``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-tenancy
    """
    timeBasedAutoScaling: typing.Union[aws_cdk.cdk.Token, "CfnInstance.TimeBasedAutoScalingProperty"]
    """``AWS::OpsWorks::Instance.TimeBasedAutoScaling``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-timebasedautoscaling
    """
    virtualizationType: str
    """``AWS::OpsWorks::Instance.VirtualizationType``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-virtualizationtype
    """
    volumes: typing.List[str]
    """``AWS::OpsWorks::Instance.Volumes``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-volumes
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnInstanceProps", jsii_struct_bases=[_CfnInstanceProps])
class CfnInstanceProps(_CfnInstanceProps):
    """Properties for defining a ``AWS::OpsWorks::Instance``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html
    """
    instanceType: str
    """``AWS::OpsWorks::Instance.InstanceType``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-instancetype
    """

    layerIds: typing.List[str]
    """``AWS::OpsWorks::Instance.LayerIds``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-layerids
    """

    stackId: str
    """``AWS::OpsWorks::Instance.StackId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-stackid
    """

class CfnLayer(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-opsworks.CfnLayer"):
    """A CloudFormation ``AWS::OpsWorks::Layer``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html
    cloudformationResource:
        AWS::OpsWorks::Layer
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, auto_assign_elastic_ips: typing.Union[bool, aws_cdk.cdk.Token], auto_assign_public_ips: typing.Union[bool, aws_cdk.cdk.Token], enable_auto_healing: typing.Union[bool, aws_cdk.cdk.Token], name: str, shortname: str, stack_id: str, type: str, attributes: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional[typing.Mapping[str,str]]]]=None, custom_instance_profile_arn: typing.Optional[str]=None, custom_json: typing.Optional[typing.Union[typing.Optional[typing.Mapping[typing.Any, typing.Any]], typing.Optional[aws_cdk.cdk.Token]]]=None, custom_recipes: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional["RecipesProperty"]]]=None, custom_security_group_ids: typing.Optional[typing.List[str]]=None, install_updates_on_boot: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.cdk.Token]]]=None, lifecycle_event_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional["LifecycleEventConfigurationProperty"]]]=None, load_based_auto_scaling: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional["LoadBasedAutoScalingProperty"]]]=None, packages: typing.Optional[typing.List[str]]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None, use_ebs_optimized_instances: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.cdk.Token]]]=None, volume_configurations: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional[typing.List[typing.Union[aws_cdk.cdk.Token, "VolumeConfigurationProperty"]]]]]=None) -> None:
        """Create a new ``AWS::OpsWorks::Layer``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            autoAssignElasticIps: ``AWS::OpsWorks::Layer.AutoAssignElasticIps``.
            autoAssignPublicIps: ``AWS::OpsWorks::Layer.AutoAssignPublicIps``.
            enableAutoHealing: ``AWS::OpsWorks::Layer.EnableAutoHealing``.
            name: ``AWS::OpsWorks::Layer.Name``.
            shortname: ``AWS::OpsWorks::Layer.Shortname``.
            stackId: ``AWS::OpsWorks::Layer.StackId``.
            type: ``AWS::OpsWorks::Layer.Type``.
            attributes: ``AWS::OpsWorks::Layer.Attributes``.
            customInstanceProfileArn: ``AWS::OpsWorks::Layer.CustomInstanceProfileArn``.
            customJson: ``AWS::OpsWorks::Layer.CustomJson``.
            customRecipes: ``AWS::OpsWorks::Layer.CustomRecipes``.
            customSecurityGroupIds: ``AWS::OpsWorks::Layer.CustomSecurityGroupIds``.
            installUpdatesOnBoot: ``AWS::OpsWorks::Layer.InstallUpdatesOnBoot``.
            lifecycleEventConfiguration: ``AWS::OpsWorks::Layer.LifecycleEventConfiguration``.
            loadBasedAutoScaling: ``AWS::OpsWorks::Layer.LoadBasedAutoScaling``.
            packages: ``AWS::OpsWorks::Layer.Packages``.
            tags: ``AWS::OpsWorks::Layer.Tags``.
            useEbsOptimizedInstances: ``AWS::OpsWorks::Layer.UseEbsOptimizedInstances``.
            volumeConfigurations: ``AWS::OpsWorks::Layer.VolumeConfigurations``.
        """
        props: CfnLayerProps = {"autoAssignElasticIps": auto_assign_elastic_ips, "autoAssignPublicIps": auto_assign_public_ips, "enableAutoHealing": enable_auto_healing, "name": name, "shortname": shortname, "stackId": stack_id, "type": type}

        if attributes is not None:
            props["attributes"] = attributes

        if custom_instance_profile_arn is not None:
            props["customInstanceProfileArn"] = custom_instance_profile_arn

        if custom_json is not None:
            props["customJson"] = custom_json

        if custom_recipes is not None:
            props["customRecipes"] = custom_recipes

        if custom_security_group_ids is not None:
            props["customSecurityGroupIds"] = custom_security_group_ids

        if install_updates_on_boot is not None:
            props["installUpdatesOnBoot"] = install_updates_on_boot

        if lifecycle_event_configuration is not None:
            props["lifecycleEventConfiguration"] = lifecycle_event_configuration

        if load_based_auto_scaling is not None:
            props["loadBasedAutoScaling"] = load_based_auto_scaling

        if packages is not None:
            props["packages"] = packages

        if tags is not None:
            props["tags"] = tags

        if use_ebs_optimized_instances is not None:
            props["useEbsOptimizedInstances"] = use_ebs_optimized_instances

        if volume_configurations is not None:
            props["volumeConfigurations"] = volume_configurations

        jsii.create(CfnLayer, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        """
        Arguments:
            properties: -
        """
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="layerId")
    def layer_id(self) -> str:
        return jsii.get(self, "layerId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnLayerProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        """The ``TagManager`` handles setting, removing and formatting tags.

        Tags should be managed either passing them as properties during
        initiation or by calling methods on this object. If both techniques are
        used only the tags from the TagManager will be used. ``Tag`` (aspect)
        will use the manager.
        """
        return jsii.get(self, "tags")

    @jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnLayer.AutoScalingThresholdsProperty", jsii_struct_bases=[])
    class AutoScalingThresholdsProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-loadbasedautoscaling-autoscalingthresholds.html
        """
        cpuThreshold: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnLayer.AutoScalingThresholdsProperty.CpuThreshold``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-loadbasedautoscaling-autoscalingthresholds.html#cfn-opsworks-layer-loadbasedautoscaling-autoscalingthresholds-cputhreshold
        """

        ignoreMetricsTime: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnLayer.AutoScalingThresholdsProperty.IgnoreMetricsTime``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-loadbasedautoscaling-autoscalingthresholds.html#cfn-opsworks-layer-loadbasedautoscaling-autoscalingthresholds-ignoremetricstime
        """

        instanceCount: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnLayer.AutoScalingThresholdsProperty.InstanceCount``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-loadbasedautoscaling-autoscalingthresholds.html#cfn-opsworks-layer-loadbasedautoscaling-autoscalingthresholds-instancecount
        """

        loadThreshold: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnLayer.AutoScalingThresholdsProperty.LoadThreshold``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-loadbasedautoscaling-autoscalingthresholds.html#cfn-opsworks-layer-loadbasedautoscaling-autoscalingthresholds-loadthreshold
        """

        memoryThreshold: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnLayer.AutoScalingThresholdsProperty.MemoryThreshold``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-loadbasedautoscaling-autoscalingthresholds.html#cfn-opsworks-layer-loadbasedautoscaling-autoscalingthresholds-memorythreshold
        """

        thresholdsWaitTime: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnLayer.AutoScalingThresholdsProperty.ThresholdsWaitTime``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-loadbasedautoscaling-autoscalingthresholds.html#cfn-opsworks-layer-loadbasedautoscaling-autoscalingthresholds-thresholdwaittime
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnLayer.LifecycleEventConfigurationProperty", jsii_struct_bases=[])
    class LifecycleEventConfigurationProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-lifecycleeventconfiguration.html
        """
        shutdownEventConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnLayer.ShutdownEventConfigurationProperty"]
        """``CfnLayer.LifecycleEventConfigurationProperty.ShutdownEventConfiguration``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-lifecycleeventconfiguration.html#cfn-opsworks-layer-lifecycleconfiguration-shutdowneventconfiguration
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnLayer.LoadBasedAutoScalingProperty", jsii_struct_bases=[])
    class LoadBasedAutoScalingProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-loadbasedautoscaling.html
        """
        downScaling: typing.Union[aws_cdk.cdk.Token, "CfnLayer.AutoScalingThresholdsProperty"]
        """``CfnLayer.LoadBasedAutoScalingProperty.DownScaling``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-loadbasedautoscaling.html#cfn-opsworks-layer-loadbasedautoscaling-downscaling
        """

        enable: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnLayer.LoadBasedAutoScalingProperty.Enable``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-loadbasedautoscaling.html#cfn-opsworks-layer-loadbasedautoscaling-enable
        """

        upScaling: typing.Union[aws_cdk.cdk.Token, "CfnLayer.AutoScalingThresholdsProperty"]
        """``CfnLayer.LoadBasedAutoScalingProperty.UpScaling``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-loadbasedautoscaling.html#cfn-opsworks-layer-loadbasedautoscaling-upscaling
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnLayer.RecipesProperty", jsii_struct_bases=[])
    class RecipesProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-recipes.html
        """
        configure: typing.List[str]
        """``CfnLayer.RecipesProperty.Configure``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-recipes.html#cfn-opsworks-layer-customrecipes-configure
        """

        deploy: typing.List[str]
        """``CfnLayer.RecipesProperty.Deploy``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-recipes.html#cfn-opsworks-layer-customrecipes-deploy
        """

        setup: typing.List[str]
        """``CfnLayer.RecipesProperty.Setup``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-recipes.html#cfn-opsworks-layer-customrecipes-setup
        """

        shutdown: typing.List[str]
        """``CfnLayer.RecipesProperty.Shutdown``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-recipes.html#cfn-opsworks-layer-customrecipes-shutdown
        """

        undeploy: typing.List[str]
        """``CfnLayer.RecipesProperty.Undeploy``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-recipes.html#cfn-opsworks-layer-customrecipes-undeploy
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnLayer.ShutdownEventConfigurationProperty", jsii_struct_bases=[])
    class ShutdownEventConfigurationProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-lifecycleeventconfiguration-shutdowneventconfiguration.html
        """
        delayUntilElbConnectionsDrained: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnLayer.ShutdownEventConfigurationProperty.DelayUntilElbConnectionsDrained``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-lifecycleeventconfiguration-shutdowneventconfiguration.html#cfn-opsworks-layer-lifecycleconfiguration-shutdowneventconfiguration-delayuntilelbconnectionsdrained
        """

        executionTimeout: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnLayer.ShutdownEventConfigurationProperty.ExecutionTimeout``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-lifecycleeventconfiguration-shutdowneventconfiguration.html#cfn-opsworks-layer-lifecycleconfiguration-shutdowneventconfiguration-executiontimeout
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnLayer.VolumeConfigurationProperty", jsii_struct_bases=[])
    class VolumeConfigurationProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-volumeconfiguration.html
        """
        encrypted: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnLayer.VolumeConfigurationProperty.Encrypted``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-volumeconfiguration.html#cfn-opsworks-layer-volumeconfiguration-encrypted
        """

        iops: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnLayer.VolumeConfigurationProperty.Iops``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-volumeconfiguration.html#cfn-opsworks-layer-volconfig-iops
        """

        mountPoint: str
        """``CfnLayer.VolumeConfigurationProperty.MountPoint``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-volumeconfiguration.html#cfn-opsworks-layer-volconfig-mountpoint
        """

        numberOfDisks: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnLayer.VolumeConfigurationProperty.NumberOfDisks``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-volumeconfiguration.html#cfn-opsworks-layer-volconfig-numberofdisks
        """

        raidLevel: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnLayer.VolumeConfigurationProperty.RaidLevel``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-volumeconfiguration.html#cfn-opsworks-layer-volconfig-raidlevel
        """

        size: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnLayer.VolumeConfigurationProperty.Size``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-volumeconfiguration.html#cfn-opsworks-layer-volconfig-size
        """

        volumeType: str
        """``CfnLayer.VolumeConfigurationProperty.VolumeType``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-volumeconfiguration.html#cfn-opsworks-layer-volconfig-volumetype
        """


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnLayerProps(jsii.compat.TypedDict, total=False):
    attributes: typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]
    """``AWS::OpsWorks::Layer.Attributes``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-attributes
    """
    customInstanceProfileArn: str
    """``AWS::OpsWorks::Layer.CustomInstanceProfileArn``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-custominstanceprofilearn
    """
    customJson: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
    """``AWS::OpsWorks::Layer.CustomJson``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-customjson
    """
    customRecipes: typing.Union[aws_cdk.cdk.Token, "CfnLayer.RecipesProperty"]
    """``AWS::OpsWorks::Layer.CustomRecipes``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-customrecipes
    """
    customSecurityGroupIds: typing.List[str]
    """``AWS::OpsWorks::Layer.CustomSecurityGroupIds``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-customsecuritygroupids
    """
    installUpdatesOnBoot: typing.Union[bool, aws_cdk.cdk.Token]
    """``AWS::OpsWorks::Layer.InstallUpdatesOnBoot``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-installupdatesonboot
    """
    lifecycleEventConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnLayer.LifecycleEventConfigurationProperty"]
    """``AWS::OpsWorks::Layer.LifecycleEventConfiguration``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-lifecycleeventconfiguration
    """
    loadBasedAutoScaling: typing.Union[aws_cdk.cdk.Token, "CfnLayer.LoadBasedAutoScalingProperty"]
    """``AWS::OpsWorks::Layer.LoadBasedAutoScaling``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-loadbasedautoscaling
    """
    packages: typing.List[str]
    """``AWS::OpsWorks::Layer.Packages``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-packages
    """
    tags: typing.List[aws_cdk.cdk.CfnTag]
    """``AWS::OpsWorks::Layer.Tags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-tags
    """
    useEbsOptimizedInstances: typing.Union[bool, aws_cdk.cdk.Token]
    """``AWS::OpsWorks::Layer.UseEbsOptimizedInstances``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-useebsoptimizedinstances
    """
    volumeConfigurations: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnLayer.VolumeConfigurationProperty"]]]
    """``AWS::OpsWorks::Layer.VolumeConfigurations``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-volumeconfigurations
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnLayerProps", jsii_struct_bases=[_CfnLayerProps])
class CfnLayerProps(_CfnLayerProps):
    """Properties for defining a ``AWS::OpsWorks::Layer``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html
    """
    autoAssignElasticIps: typing.Union[bool, aws_cdk.cdk.Token]
    """``AWS::OpsWorks::Layer.AutoAssignElasticIps``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-autoassignelasticips
    """

    autoAssignPublicIps: typing.Union[bool, aws_cdk.cdk.Token]
    """``AWS::OpsWorks::Layer.AutoAssignPublicIps``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-autoassignpublicips
    """

    enableAutoHealing: typing.Union[bool, aws_cdk.cdk.Token]
    """``AWS::OpsWorks::Layer.EnableAutoHealing``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-enableautohealing
    """

    name: str
    """``AWS::OpsWorks::Layer.Name``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-name
    """

    shortname: str
    """``AWS::OpsWorks::Layer.Shortname``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-shortname
    """

    stackId: str
    """``AWS::OpsWorks::Layer.StackId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-stackid
    """

    type: str
    """``AWS::OpsWorks::Layer.Type``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-type
    """

class CfnStack(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-opsworks.CfnStack"):
    """A CloudFormation ``AWS::OpsWorks::Stack``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html
    cloudformationResource:
        AWS::OpsWorks::Stack
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, default_instance_profile_arn: str, name: str, service_role_arn: str, agent_version: typing.Optional[str]=None, attributes: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional[typing.Mapping[str,str]]]]=None, chef_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional["ChefConfigurationProperty"]]]=None, clone_app_ids: typing.Optional[typing.List[str]]=None, clone_permissions: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.cdk.Token]]]=None, configuration_manager: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional["StackConfigurationManagerProperty"]]]=None, custom_cookbooks_source: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional["SourceProperty"]]]=None, custom_json: typing.Optional[typing.Union[typing.Optional[typing.Mapping[typing.Any, typing.Any]], typing.Optional[aws_cdk.cdk.Token]]]=None, default_availability_zone: typing.Optional[str]=None, default_os: typing.Optional[str]=None, default_root_device_type: typing.Optional[str]=None, default_ssh_key_name: typing.Optional[str]=None, default_subnet_id: typing.Optional[str]=None, ecs_cluster_arn: typing.Optional[str]=None, elastic_ips: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional[typing.List[typing.Union[aws_cdk.cdk.Token, "ElasticIpProperty"]]]]]=None, hostname_theme: typing.Optional[str]=None, rds_db_instances: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional[typing.List[typing.Union[aws_cdk.cdk.Token, "RdsDbInstanceProperty"]]]]]=None, source_stack_id: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None, use_custom_cookbooks: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.cdk.Token]]]=None, use_opsworks_security_groups: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.cdk.Token]]]=None, vpc_id: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::OpsWorks::Stack``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            defaultInstanceProfileArn: ``AWS::OpsWorks::Stack.DefaultInstanceProfileArn``.
            name: ``AWS::OpsWorks::Stack.Name``.
            serviceRoleArn: ``AWS::OpsWorks::Stack.ServiceRoleArn``.
            agentVersion: ``AWS::OpsWorks::Stack.AgentVersion``.
            attributes: ``AWS::OpsWorks::Stack.Attributes``.
            chefConfiguration: ``AWS::OpsWorks::Stack.ChefConfiguration``.
            cloneAppIds: ``AWS::OpsWorks::Stack.CloneAppIds``.
            clonePermissions: ``AWS::OpsWorks::Stack.ClonePermissions``.
            configurationManager: ``AWS::OpsWorks::Stack.ConfigurationManager``.
            customCookbooksSource: ``AWS::OpsWorks::Stack.CustomCookbooksSource``.
            customJson: ``AWS::OpsWorks::Stack.CustomJson``.
            defaultAvailabilityZone: ``AWS::OpsWorks::Stack.DefaultAvailabilityZone``.
            defaultOs: ``AWS::OpsWorks::Stack.DefaultOs``.
            defaultRootDeviceType: ``AWS::OpsWorks::Stack.DefaultRootDeviceType``.
            defaultSshKeyName: ``AWS::OpsWorks::Stack.DefaultSshKeyName``.
            defaultSubnetId: ``AWS::OpsWorks::Stack.DefaultSubnetId``.
            ecsClusterArn: ``AWS::OpsWorks::Stack.EcsClusterArn``.
            elasticIps: ``AWS::OpsWorks::Stack.ElasticIps``.
            hostnameTheme: ``AWS::OpsWorks::Stack.HostnameTheme``.
            rdsDbInstances: ``AWS::OpsWorks::Stack.RdsDbInstances``.
            sourceStackId: ``AWS::OpsWorks::Stack.SourceStackId``.
            tags: ``AWS::OpsWorks::Stack.Tags``.
            useCustomCookbooks: ``AWS::OpsWorks::Stack.UseCustomCookbooks``.
            useOpsworksSecurityGroups: ``AWS::OpsWorks::Stack.UseOpsworksSecurityGroups``.
            vpcId: ``AWS::OpsWorks::Stack.VpcId``.
        """
        props: CfnStackProps = {"defaultInstanceProfileArn": default_instance_profile_arn, "name": name, "serviceRoleArn": service_role_arn}

        if agent_version is not None:
            props["agentVersion"] = agent_version

        if attributes is not None:
            props["attributes"] = attributes

        if chef_configuration is not None:
            props["chefConfiguration"] = chef_configuration

        if clone_app_ids is not None:
            props["cloneAppIds"] = clone_app_ids

        if clone_permissions is not None:
            props["clonePermissions"] = clone_permissions

        if configuration_manager is not None:
            props["configurationManager"] = configuration_manager

        if custom_cookbooks_source is not None:
            props["customCookbooksSource"] = custom_cookbooks_source

        if custom_json is not None:
            props["customJson"] = custom_json

        if default_availability_zone is not None:
            props["defaultAvailabilityZone"] = default_availability_zone

        if default_os is not None:
            props["defaultOs"] = default_os

        if default_root_device_type is not None:
            props["defaultRootDeviceType"] = default_root_device_type

        if default_ssh_key_name is not None:
            props["defaultSshKeyName"] = default_ssh_key_name

        if default_subnet_id is not None:
            props["defaultSubnetId"] = default_subnet_id

        if ecs_cluster_arn is not None:
            props["ecsClusterArn"] = ecs_cluster_arn

        if elastic_ips is not None:
            props["elasticIps"] = elastic_ips

        if hostname_theme is not None:
            props["hostnameTheme"] = hostname_theme

        if rds_db_instances is not None:
            props["rdsDbInstances"] = rds_db_instances

        if source_stack_id is not None:
            props["sourceStackId"] = source_stack_id

        if tags is not None:
            props["tags"] = tags

        if use_custom_cookbooks is not None:
            props["useCustomCookbooks"] = use_custom_cookbooks

        if use_opsworks_security_groups is not None:
            props["useOpsworksSecurityGroups"] = use_opsworks_security_groups

        if vpc_id is not None:
            props["vpcId"] = vpc_id

        jsii.create(CfnStack, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        """
        Arguments:
            properties: -
        """
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnStackProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="stackId")
    def stack_id(self) -> str:
        return jsii.get(self, "stackId")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        """The ``TagManager`` handles setting, removing and formatting tags.

        Tags should be managed either passing them as properties during
        initiation or by calling methods on this object. If both techniques are
        used only the tags from the TagManager will be used. ``Tag`` (aspect)
        will use the manager.
        """
        return jsii.get(self, "tags")

    @jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnStack.ChefConfigurationProperty", jsii_struct_bases=[])
    class ChefConfigurationProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-chefconfiguration.html
        """
        berkshelfVersion: str
        """``CfnStack.ChefConfigurationProperty.BerkshelfVersion``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-chefconfiguration.html#cfn-opsworks-chefconfiguration-berkshelfversion
        """

        manageBerkshelf: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnStack.ChefConfigurationProperty.ManageBerkshelf``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-chefconfiguration.html#cfn-opsworks-chefconfiguration-berkshelfversion
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _ElasticIpProperty(jsii.compat.TypedDict, total=False):
        name: str
        """``CfnStack.ElasticIpProperty.Name``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-elasticip.html#cfn-opsworks-stack-elasticip-name
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnStack.ElasticIpProperty", jsii_struct_bases=[_ElasticIpProperty])
    class ElasticIpProperty(_ElasticIpProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-elasticip.html
        """
        ip: str
        """``CfnStack.ElasticIpProperty.Ip``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-elasticip.html#cfn-opsworks-stack-elasticip-ip
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnStack.RdsDbInstanceProperty", jsii_struct_bases=[])
    class RdsDbInstanceProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-rdsdbinstance.html
        """
        dbPassword: str
        """``CfnStack.RdsDbInstanceProperty.DbPassword``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-rdsdbinstance.html#cfn-opsworks-stack-rdsdbinstance-dbpassword
        """

        dbUser: str
        """``CfnStack.RdsDbInstanceProperty.DbUser``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-rdsdbinstance.html#cfn-opsworks-stack-rdsdbinstance-dbuser
        """

        rdsDbInstanceArn: str
        """``CfnStack.RdsDbInstanceProperty.RdsDbInstanceArn``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-rdsdbinstance.html#cfn-opsworks-stack-rdsdbinstance-rdsdbinstancearn
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnStack.SourceProperty", jsii_struct_bases=[])
    class SourceProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-source.html
        """
        password: str
        """``CfnStack.SourceProperty.Password``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-source.html#cfn-opsworks-custcookbooksource-password
        """

        revision: str
        """``CfnStack.SourceProperty.Revision``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-source.html#cfn-opsworks-custcookbooksource-revision
        """

        sshKey: str
        """``CfnStack.SourceProperty.SshKey``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-source.html#cfn-opsworks-custcookbooksource-sshkey
        """

        type: str
        """``CfnStack.SourceProperty.Type``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-source.html#cfn-opsworks-custcookbooksource-type
        """

        url: str
        """``CfnStack.SourceProperty.Url``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-source.html#cfn-opsworks-custcookbooksource-url
        """

        username: str
        """``CfnStack.SourceProperty.Username``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-source.html#cfn-opsworks-custcookbooksource-username
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnStack.StackConfigurationManagerProperty", jsii_struct_bases=[])
    class StackConfigurationManagerProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-stackconfigmanager.html
        """
        name: str
        """``CfnStack.StackConfigurationManagerProperty.Name``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-stackconfigmanager.html#cfn-opsworks-configmanager-name
        """

        version: str
        """``CfnStack.StackConfigurationManagerProperty.Version``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-stackconfigmanager.html#cfn-opsworks-configmanager-version
        """


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnStackProps(jsii.compat.TypedDict, total=False):
    agentVersion: str
    """``AWS::OpsWorks::Stack.AgentVersion``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-agentversion
    """
    attributes: typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]
    """``AWS::OpsWorks::Stack.Attributes``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-attributes
    """
    chefConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnStack.ChefConfigurationProperty"]
    """``AWS::OpsWorks::Stack.ChefConfiguration``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-chefconfiguration
    """
    cloneAppIds: typing.List[str]
    """``AWS::OpsWorks::Stack.CloneAppIds``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-cloneappids
    """
    clonePermissions: typing.Union[bool, aws_cdk.cdk.Token]
    """``AWS::OpsWorks::Stack.ClonePermissions``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-clonepermissions
    """
    configurationManager: typing.Union[aws_cdk.cdk.Token, "CfnStack.StackConfigurationManagerProperty"]
    """``AWS::OpsWorks::Stack.ConfigurationManager``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-configmanager
    """
    customCookbooksSource: typing.Union[aws_cdk.cdk.Token, "CfnStack.SourceProperty"]
    """``AWS::OpsWorks::Stack.CustomCookbooksSource``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-custcookbooksource
    """
    customJson: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
    """``AWS::OpsWorks::Stack.CustomJson``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-custjson
    """
    defaultAvailabilityZone: str
    """``AWS::OpsWorks::Stack.DefaultAvailabilityZone``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-defaultaz
    """
    defaultOs: str
    """``AWS::OpsWorks::Stack.DefaultOs``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-defaultos
    """
    defaultRootDeviceType: str
    """``AWS::OpsWorks::Stack.DefaultRootDeviceType``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-defaultrootdevicetype
    """
    defaultSshKeyName: str
    """``AWS::OpsWorks::Stack.DefaultSshKeyName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-defaultsshkeyname
    """
    defaultSubnetId: str
    """``AWS::OpsWorks::Stack.DefaultSubnetId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#defaultsubnet
    """
    ecsClusterArn: str
    """``AWS::OpsWorks::Stack.EcsClusterArn``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-ecsclusterarn
    """
    elasticIps: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnStack.ElasticIpProperty"]]]
    """``AWS::OpsWorks::Stack.ElasticIps``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-elasticips
    """
    hostnameTheme: str
    """``AWS::OpsWorks::Stack.HostnameTheme``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-hostnametheme
    """
    rdsDbInstances: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnStack.RdsDbInstanceProperty"]]]
    """``AWS::OpsWorks::Stack.RdsDbInstances``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-rdsdbinstances
    """
    sourceStackId: str
    """``AWS::OpsWorks::Stack.SourceStackId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-sourcestackid
    """
    tags: typing.List[aws_cdk.cdk.CfnTag]
    """``AWS::OpsWorks::Stack.Tags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-tags
    """
    useCustomCookbooks: typing.Union[bool, aws_cdk.cdk.Token]
    """``AWS::OpsWorks::Stack.UseCustomCookbooks``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#usecustcookbooks
    """
    useOpsworksSecurityGroups: typing.Union[bool, aws_cdk.cdk.Token]
    """``AWS::OpsWorks::Stack.UseOpsworksSecurityGroups``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-useopsworkssecuritygroups
    """
    vpcId: str
    """``AWS::OpsWorks::Stack.VpcId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-vpcid
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnStackProps", jsii_struct_bases=[_CfnStackProps])
class CfnStackProps(_CfnStackProps):
    """Properties for defining a ``AWS::OpsWorks::Stack``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html
    """
    defaultInstanceProfileArn: str
    """``AWS::OpsWorks::Stack.DefaultInstanceProfileArn``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-defaultinstanceprof
    """

    name: str
    """``AWS::OpsWorks::Stack.Name``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-name
    """

    serviceRoleArn: str
    """``AWS::OpsWorks::Stack.ServiceRoleArn``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-servicerolearn
    """

class CfnUserProfile(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-opsworks.CfnUserProfile"):
    """A CloudFormation ``AWS::OpsWorks::UserProfile``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-userprofile.html
    cloudformationResource:
        AWS::OpsWorks::UserProfile
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, iam_user_arn: str, allow_self_management: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.cdk.Token]]]=None, ssh_public_key: typing.Optional[str]=None, ssh_username: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::OpsWorks::UserProfile``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            iamUserArn: ``AWS::OpsWorks::UserProfile.IamUserArn``.
            allowSelfManagement: ``AWS::OpsWorks::UserProfile.AllowSelfManagement``.
            sshPublicKey: ``AWS::OpsWorks::UserProfile.SshPublicKey``.
            sshUsername: ``AWS::OpsWorks::UserProfile.SshUsername``.
        """
        props: CfnUserProfileProps = {"iamUserArn": iam_user_arn}

        if allow_self_management is not None:
            props["allowSelfManagement"] = allow_self_management

        if ssh_public_key is not None:
            props["sshPublicKey"] = ssh_public_key

        if ssh_username is not None:
            props["sshUsername"] = ssh_username

        jsii.create(CfnUserProfile, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        """
        Arguments:
            properties: -
        """
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnUserProfileProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="userProfileArn")
    def user_profile_arn(self) -> str:
        return jsii.get(self, "userProfileArn")

    @property
    @jsii.member(jsii_name="userProfileSshUsername")
    def user_profile_ssh_username(self) -> str:
        """
        cloudformationAttribute:
            SshUsername
        """
        return jsii.get(self, "userProfileSshUsername")


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnUserProfileProps(jsii.compat.TypedDict, total=False):
    allowSelfManagement: typing.Union[bool, aws_cdk.cdk.Token]
    """``AWS::OpsWorks::UserProfile.AllowSelfManagement``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-userprofile.html#cfn-opsworks-userprofile-allowselfmanagement
    """
    sshPublicKey: str
    """``AWS::OpsWorks::UserProfile.SshPublicKey``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-userprofile.html#cfn-opsworks-userprofile-sshpublickey
    """
    sshUsername: str
    """``AWS::OpsWorks::UserProfile.SshUsername``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-userprofile.html#cfn-opsworks-userprofile-sshusername
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnUserProfileProps", jsii_struct_bases=[_CfnUserProfileProps])
class CfnUserProfileProps(_CfnUserProfileProps):
    """Properties for defining a ``AWS::OpsWorks::UserProfile``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-userprofile.html
    """
    iamUserArn: str
    """``AWS::OpsWorks::UserProfile.IamUserArn``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-userprofile.html#cfn-opsworks-userprofile-iamuserarn
    """

class CfnVolume(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-opsworks.CfnVolume"):
    """A CloudFormation ``AWS::OpsWorks::Volume``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-volume.html
    cloudformationResource:
        AWS::OpsWorks::Volume
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, ec2_volume_id: str, stack_id: str, mount_point: typing.Optional[str]=None, name: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::OpsWorks::Volume``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            ec2VolumeId: ``AWS::OpsWorks::Volume.Ec2VolumeId``.
            stackId: ``AWS::OpsWorks::Volume.StackId``.
            mountPoint: ``AWS::OpsWorks::Volume.MountPoint``.
            name: ``AWS::OpsWorks::Volume.Name``.
        """
        props: CfnVolumeProps = {"ec2VolumeId": ec2_volume_id, "stackId": stack_id}

        if mount_point is not None:
            props["mountPoint"] = mount_point

        if name is not None:
            props["name"] = name

        jsii.create(CfnVolume, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        """
        Arguments:
            properties: -
        """
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnVolumeProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="volumeId")
    def volume_id(self) -> str:
        return jsii.get(self, "volumeId")


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnVolumeProps(jsii.compat.TypedDict, total=False):
    mountPoint: str
    """``AWS::OpsWorks::Volume.MountPoint``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-volume.html#cfn-opsworks-volume-mountpoint
    """
    name: str
    """``AWS::OpsWorks::Volume.Name``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-volume.html#cfn-opsworks-volume-name
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnVolumeProps", jsii_struct_bases=[_CfnVolumeProps])
class CfnVolumeProps(_CfnVolumeProps):
    """Properties for defining a ``AWS::OpsWorks::Volume``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-volume.html
    """
    ec2VolumeId: str
    """``AWS::OpsWorks::Volume.Ec2VolumeId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-volume.html#cfn-opsworks-volume-ec2volumeid
    """

    stackId: str
    """``AWS::OpsWorks::Volume.StackId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-volume.html#cfn-opsworks-volume-stackid
    """

__all__ = ["CfnApp", "CfnAppProps", "CfnElasticLoadBalancerAttachment", "CfnElasticLoadBalancerAttachmentProps", "CfnInstance", "CfnInstanceProps", "CfnLayer", "CfnLayerProps", "CfnStack", "CfnStackProps", "CfnUserProfile", "CfnUserProfileProps", "CfnVolume", "CfnVolumeProps", "__jsii_assembly__"]

publication.publish()
