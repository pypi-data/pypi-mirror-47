import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-pinpointemail", "0.33.0", __name__, "aws-pinpointemail@0.33.0.jsii.tgz")
class CfnConfigurationSet(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-pinpointemail.CfnConfigurationSet"):
    """A CloudFormation ``AWS::PinpointEmail::ConfigurationSet``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpointemail-configurationset.html
    cloudformationResource:
        AWS::PinpointEmail::ConfigurationSet
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, name: str, delivery_options: typing.Optional[typing.Union[typing.Optional["DeliveryOptionsProperty"], typing.Optional[aws_cdk.cdk.Token]]]=None, reputation_options: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional["ReputationOptionsProperty"]]]=None, sending_options: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional["SendingOptionsProperty"]]]=None, tags: typing.Optional[typing.List["TagsProperty"]]=None, tracking_options: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional["TrackingOptionsProperty"]]]=None) -> None:
        """Create a new ``AWS::PinpointEmail::ConfigurationSet``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            name: ``AWS::PinpointEmail::ConfigurationSet.Name``.
            deliveryOptions: ``AWS::PinpointEmail::ConfigurationSet.DeliveryOptions``.
            reputationOptions: ``AWS::PinpointEmail::ConfigurationSet.ReputationOptions``.
            sendingOptions: ``AWS::PinpointEmail::ConfigurationSet.SendingOptions``.
            tags: ``AWS::PinpointEmail::ConfigurationSet.Tags``.
            trackingOptions: ``AWS::PinpointEmail::ConfigurationSet.TrackingOptions``.
        """
        props: CfnConfigurationSetProps = {"name": name}

        if delivery_options is not None:
            props["deliveryOptions"] = delivery_options

        if reputation_options is not None:
            props["reputationOptions"] = reputation_options

        if sending_options is not None:
            props["sendingOptions"] = sending_options

        if tags is not None:
            props["tags"] = tags

        if tracking_options is not None:
            props["trackingOptions"] = tracking_options

        jsii.create(CfnConfigurationSet, self, [scope, id, props])

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
    @jsii.member(jsii_name="configurationSetName")
    def configuration_set_name(self) -> str:
        return jsii.get(self, "configurationSetName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnConfigurationSetProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-pinpointemail.CfnConfigurationSet.DeliveryOptionsProperty", jsii_struct_bases=[])
    class DeliveryOptionsProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpointemail-configurationset-deliveryoptions.html
        """
        sendingPoolName: str
        """``CfnConfigurationSet.DeliveryOptionsProperty.SendingPoolName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpointemail-configurationset-deliveryoptions.html#cfn-pinpointemail-configurationset-deliveryoptions-sendingpoolname
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-pinpointemail.CfnConfigurationSet.ReputationOptionsProperty", jsii_struct_bases=[])
    class ReputationOptionsProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpointemail-configurationset-reputationoptions.html
        """
        reputationMetricsEnabled: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnConfigurationSet.ReputationOptionsProperty.ReputationMetricsEnabled``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpointemail-configurationset-reputationoptions.html#cfn-pinpointemail-configurationset-reputationoptions-reputationmetricsenabled
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-pinpointemail.CfnConfigurationSet.SendingOptionsProperty", jsii_struct_bases=[])
    class SendingOptionsProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpointemail-configurationset-sendingoptions.html
        """
        sendingEnabled: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnConfigurationSet.SendingOptionsProperty.SendingEnabled``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpointemail-configurationset-sendingoptions.html#cfn-pinpointemail-configurationset-sendingoptions-sendingenabled
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-pinpointemail.CfnConfigurationSet.TagsProperty", jsii_struct_bases=[])
    class TagsProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpointemail-configurationset-tags.html
        """
        key: str
        """``CfnConfigurationSet.TagsProperty.Key``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpointemail-configurationset-tags.html#cfn-pinpointemail-configurationset-tags-key
        """

        value: str
        """``CfnConfigurationSet.TagsProperty.Value``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpointemail-configurationset-tags.html#cfn-pinpointemail-configurationset-tags-value
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-pinpointemail.CfnConfigurationSet.TrackingOptionsProperty", jsii_struct_bases=[])
    class TrackingOptionsProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpointemail-configurationset-trackingoptions.html
        """
        customRedirectDomain: str
        """``CfnConfigurationSet.TrackingOptionsProperty.CustomRedirectDomain``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpointemail-configurationset-trackingoptions.html#cfn-pinpointemail-configurationset-trackingoptions-customredirectdomain
        """


class CfnConfigurationSetEventDestination(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-pinpointemail.CfnConfigurationSetEventDestination"):
    """A CloudFormation ``AWS::PinpointEmail::ConfigurationSetEventDestination``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpointemail-configurationseteventdestination.html
    cloudformationResource:
        AWS::PinpointEmail::ConfigurationSetEventDestination
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, configuration_set_name: str, event_destination_name: str, event_destination: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional["EventDestinationProperty"]]]=None) -> None:
        """Create a new ``AWS::PinpointEmail::ConfigurationSetEventDestination``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            configurationSetName: ``AWS::PinpointEmail::ConfigurationSetEventDestination.ConfigurationSetName``.
            eventDestinationName: ``AWS::PinpointEmail::ConfigurationSetEventDestination.EventDestinationName``.
            eventDestination: ``AWS::PinpointEmail::ConfigurationSetEventDestination.EventDestination``.
        """
        props: CfnConfigurationSetEventDestinationProps = {"configurationSetName": configuration_set_name, "eventDestinationName": event_destination_name}

        if event_destination is not None:
            props["eventDestination"] = event_destination

        jsii.create(CfnConfigurationSetEventDestination, self, [scope, id, props])

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
    @jsii.member(jsii_name="configurationSetEventDestinationName")
    def configuration_set_event_destination_name(self) -> str:
        return jsii.get(self, "configurationSetEventDestinationName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnConfigurationSetEventDestinationProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-pinpointemail.CfnConfigurationSetEventDestination.CloudWatchDestinationProperty", jsii_struct_bases=[])
    class CloudWatchDestinationProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpointemail-configurationseteventdestination-cloudwatchdestination.html
        """
        dimensionConfigurations: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnConfigurationSetEventDestination.DimensionConfigurationProperty"]]]
        """``CfnConfigurationSetEventDestination.CloudWatchDestinationProperty.DimensionConfigurations``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpointemail-configurationseteventdestination-cloudwatchdestination.html#cfn-pinpointemail-configurationseteventdestination-cloudwatchdestination-dimensionconfigurations
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-pinpointemail.CfnConfigurationSetEventDestination.DimensionConfigurationProperty", jsii_struct_bases=[])
    class DimensionConfigurationProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpointemail-configurationseteventdestination-dimensionconfiguration.html
        """
        defaultDimensionValue: str
        """``CfnConfigurationSetEventDestination.DimensionConfigurationProperty.DefaultDimensionValue``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpointemail-configurationseteventdestination-dimensionconfiguration.html#cfn-pinpointemail-configurationseteventdestination-dimensionconfiguration-defaultdimensionvalue
        """

        dimensionName: str
        """``CfnConfigurationSetEventDestination.DimensionConfigurationProperty.DimensionName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpointemail-configurationseteventdestination-dimensionconfiguration.html#cfn-pinpointemail-configurationseteventdestination-dimensionconfiguration-dimensionname
        """

        dimensionValueSource: str
        """``CfnConfigurationSetEventDestination.DimensionConfigurationProperty.DimensionValueSource``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpointemail-configurationseteventdestination-dimensionconfiguration.html#cfn-pinpointemail-configurationseteventdestination-dimensionconfiguration-dimensionvaluesource
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _EventDestinationProperty(jsii.compat.TypedDict, total=False):
        cloudWatchDestination: typing.Union[aws_cdk.cdk.Token, "CfnConfigurationSetEventDestination.CloudWatchDestinationProperty"]
        """``CfnConfigurationSetEventDestination.EventDestinationProperty.CloudWatchDestination``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpointemail-configurationseteventdestination-eventdestination.html#cfn-pinpointemail-configurationseteventdestination-eventdestination-cloudwatchdestination
        """
        enabled: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnConfigurationSetEventDestination.EventDestinationProperty.Enabled``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpointemail-configurationseteventdestination-eventdestination.html#cfn-pinpointemail-configurationseteventdestination-eventdestination-enabled
        """
        kinesisFirehoseDestination: typing.Union[aws_cdk.cdk.Token, "CfnConfigurationSetEventDestination.KinesisFirehoseDestinationProperty"]
        """``CfnConfigurationSetEventDestination.EventDestinationProperty.KinesisFirehoseDestination``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpointemail-configurationseteventdestination-eventdestination.html#cfn-pinpointemail-configurationseteventdestination-eventdestination-kinesisfirehosedestination
        """
        pinpointDestination: typing.Union[aws_cdk.cdk.Token, "CfnConfigurationSetEventDestination.PinpointDestinationProperty"]
        """``CfnConfigurationSetEventDestination.EventDestinationProperty.PinpointDestination``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpointemail-configurationseteventdestination-eventdestination.html#cfn-pinpointemail-configurationseteventdestination-eventdestination-pinpointdestination
        """
        snsDestination: typing.Union[aws_cdk.cdk.Token, "CfnConfigurationSetEventDestination.SnsDestinationProperty"]
        """``CfnConfigurationSetEventDestination.EventDestinationProperty.SnsDestination``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpointemail-configurationseteventdestination-eventdestination.html#cfn-pinpointemail-configurationseteventdestination-eventdestination-snsdestination
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-pinpointemail.CfnConfigurationSetEventDestination.EventDestinationProperty", jsii_struct_bases=[_EventDestinationProperty])
    class EventDestinationProperty(_EventDestinationProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpointemail-configurationseteventdestination-eventdestination.html
        """
        matchingEventTypes: typing.List[str]
        """``CfnConfigurationSetEventDestination.EventDestinationProperty.MatchingEventTypes``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpointemail-configurationseteventdestination-eventdestination.html#cfn-pinpointemail-configurationseteventdestination-eventdestination-matchingeventtypes
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-pinpointemail.CfnConfigurationSetEventDestination.KinesisFirehoseDestinationProperty", jsii_struct_bases=[])
    class KinesisFirehoseDestinationProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpointemail-configurationseteventdestination-kinesisfirehosedestination.html
        """
        deliveryStreamArn: str
        """``CfnConfigurationSetEventDestination.KinesisFirehoseDestinationProperty.DeliveryStreamArn``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpointemail-configurationseteventdestination-kinesisfirehosedestination.html#cfn-pinpointemail-configurationseteventdestination-kinesisfirehosedestination-deliverystreamarn
        """

        iamRoleArn: str
        """``CfnConfigurationSetEventDestination.KinesisFirehoseDestinationProperty.IamRoleArn``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpointemail-configurationseteventdestination-kinesisfirehosedestination.html#cfn-pinpointemail-configurationseteventdestination-kinesisfirehosedestination-iamrolearn
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-pinpointemail.CfnConfigurationSetEventDestination.PinpointDestinationProperty", jsii_struct_bases=[])
    class PinpointDestinationProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpointemail-configurationseteventdestination-pinpointdestination.html
        """
        applicationArn: str
        """``CfnConfigurationSetEventDestination.PinpointDestinationProperty.ApplicationArn``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpointemail-configurationseteventdestination-pinpointdestination.html#cfn-pinpointemail-configurationseteventdestination-pinpointdestination-applicationarn
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-pinpointemail.CfnConfigurationSetEventDestination.SnsDestinationProperty", jsii_struct_bases=[])
    class SnsDestinationProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpointemail-configurationseteventdestination-snsdestination.html
        """
        topicArn: str
        """``CfnConfigurationSetEventDestination.SnsDestinationProperty.TopicArn``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpointemail-configurationseteventdestination-snsdestination.html#cfn-pinpointemail-configurationseteventdestination-snsdestination-topicarn
        """


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnConfigurationSetEventDestinationProps(jsii.compat.TypedDict, total=False):
    eventDestination: typing.Union[aws_cdk.cdk.Token, "CfnConfigurationSetEventDestination.EventDestinationProperty"]
    """``AWS::PinpointEmail::ConfigurationSetEventDestination.EventDestination``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpointemail-configurationseteventdestination.html#cfn-pinpointemail-configurationseteventdestination-eventdestination
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-pinpointemail.CfnConfigurationSetEventDestinationProps", jsii_struct_bases=[_CfnConfigurationSetEventDestinationProps])
class CfnConfigurationSetEventDestinationProps(_CfnConfigurationSetEventDestinationProps):
    """Properties for defining a ``AWS::PinpointEmail::ConfigurationSetEventDestination``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpointemail-configurationseteventdestination.html
    """
    configurationSetName: str
    """``AWS::PinpointEmail::ConfigurationSetEventDestination.ConfigurationSetName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpointemail-configurationseteventdestination.html#cfn-pinpointemail-configurationseteventdestination-configurationsetname
    """

    eventDestinationName: str
    """``AWS::PinpointEmail::ConfigurationSetEventDestination.EventDestinationName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpointemail-configurationseteventdestination.html#cfn-pinpointemail-configurationseteventdestination-eventdestinationname
    """

@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnConfigurationSetProps(jsii.compat.TypedDict, total=False):
    deliveryOptions: typing.Union["CfnConfigurationSet.DeliveryOptionsProperty", aws_cdk.cdk.Token]
    """``AWS::PinpointEmail::ConfigurationSet.DeliveryOptions``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpointemail-configurationset.html#cfn-pinpointemail-configurationset-deliveryoptions
    """
    reputationOptions: typing.Union[aws_cdk.cdk.Token, "CfnConfigurationSet.ReputationOptionsProperty"]
    """``AWS::PinpointEmail::ConfigurationSet.ReputationOptions``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpointemail-configurationset.html#cfn-pinpointemail-configurationset-reputationoptions
    """
    sendingOptions: typing.Union[aws_cdk.cdk.Token, "CfnConfigurationSet.SendingOptionsProperty"]
    """``AWS::PinpointEmail::ConfigurationSet.SendingOptions``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpointemail-configurationset.html#cfn-pinpointemail-configurationset-sendingoptions
    """
    tags: typing.List["CfnConfigurationSet.TagsProperty"]
    """``AWS::PinpointEmail::ConfigurationSet.Tags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpointemail-configurationset.html#cfn-pinpointemail-configurationset-tags
    """
    trackingOptions: typing.Union[aws_cdk.cdk.Token, "CfnConfigurationSet.TrackingOptionsProperty"]
    """``AWS::PinpointEmail::ConfigurationSet.TrackingOptions``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpointemail-configurationset.html#cfn-pinpointemail-configurationset-trackingoptions
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-pinpointemail.CfnConfigurationSetProps", jsii_struct_bases=[_CfnConfigurationSetProps])
class CfnConfigurationSetProps(_CfnConfigurationSetProps):
    """Properties for defining a ``AWS::PinpointEmail::ConfigurationSet``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpointemail-configurationset.html
    """
    name: str
    """``AWS::PinpointEmail::ConfigurationSet.Name``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpointemail-configurationset.html#cfn-pinpointemail-configurationset-name
    """

class CfnDedicatedIpPool(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-pinpointemail.CfnDedicatedIpPool"):
    """A CloudFormation ``AWS::PinpointEmail::DedicatedIpPool``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpointemail-dedicatedippool.html
    cloudformationResource:
        AWS::PinpointEmail::DedicatedIpPool
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, pool_name: typing.Optional[str]=None, tags: typing.Optional[typing.List["TagsProperty"]]=None) -> None:
        """Create a new ``AWS::PinpointEmail::DedicatedIpPool``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            poolName: ``AWS::PinpointEmail::DedicatedIpPool.PoolName``.
            tags: ``AWS::PinpointEmail::DedicatedIpPool.Tags``.
        """
        props: CfnDedicatedIpPoolProps = {}

        if pool_name is not None:
            props["poolName"] = pool_name

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnDedicatedIpPool, self, [scope, id, props])

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
    @jsii.member(jsii_name="dedicatedIpPoolName")
    def dedicated_ip_pool_name(self) -> str:
        return jsii.get(self, "dedicatedIpPoolName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnDedicatedIpPoolProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-pinpointemail.CfnDedicatedIpPool.TagsProperty", jsii_struct_bases=[])
    class TagsProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpointemail-dedicatedippool-tags.html
        """
        key: str
        """``CfnDedicatedIpPool.TagsProperty.Key``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpointemail-dedicatedippool-tags.html#cfn-pinpointemail-dedicatedippool-tags-key
        """

        value: str
        """``CfnDedicatedIpPool.TagsProperty.Value``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpointemail-dedicatedippool-tags.html#cfn-pinpointemail-dedicatedippool-tags-value
        """


@jsii.data_type(jsii_type="@aws-cdk/aws-pinpointemail.CfnDedicatedIpPoolProps", jsii_struct_bases=[])
class CfnDedicatedIpPoolProps(jsii.compat.TypedDict, total=False):
    """Properties for defining a ``AWS::PinpointEmail::DedicatedIpPool``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpointemail-dedicatedippool.html
    """
    poolName: str
    """``AWS::PinpointEmail::DedicatedIpPool.PoolName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpointemail-dedicatedippool.html#cfn-pinpointemail-dedicatedippool-poolname
    """

    tags: typing.List["CfnDedicatedIpPool.TagsProperty"]
    """``AWS::PinpointEmail::DedicatedIpPool.Tags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpointemail-dedicatedippool.html#cfn-pinpointemail-dedicatedippool-tags
    """

class CfnIdentity(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-pinpointemail.CfnIdentity"):
    """A CloudFormation ``AWS::PinpointEmail::Identity``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpointemail-identity.html
    cloudformationResource:
        AWS::PinpointEmail::Identity
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, name: str, dkim_signing_enabled: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.cdk.Token]]]=None, feedback_forwarding_enabled: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.cdk.Token]]]=None, mail_from_attributes: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional["MailFromAttributesProperty"]]]=None, tags: typing.Optional[typing.List["TagsProperty"]]=None) -> None:
        """Create a new ``AWS::PinpointEmail::Identity``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            name: ``AWS::PinpointEmail::Identity.Name``.
            dkimSigningEnabled: ``AWS::PinpointEmail::Identity.DkimSigningEnabled``.
            feedbackForwardingEnabled: ``AWS::PinpointEmail::Identity.FeedbackForwardingEnabled``.
            mailFromAttributes: ``AWS::PinpointEmail::Identity.MailFromAttributes``.
            tags: ``AWS::PinpointEmail::Identity.Tags``.
        """
        props: CfnIdentityProps = {"name": name}

        if dkim_signing_enabled is not None:
            props["dkimSigningEnabled"] = dkim_signing_enabled

        if feedback_forwarding_enabled is not None:
            props["feedbackForwardingEnabled"] = feedback_forwarding_enabled

        if mail_from_attributes is not None:
            props["mailFromAttributes"] = mail_from_attributes

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnIdentity, self, [scope, id, props])

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
    @jsii.member(jsii_name="identityDnsRecordName1")
    def identity_dns_record_name1(self) -> str:
        """
        cloudformationAttribute:
            IdentityDNSRecordName1
        """
        return jsii.get(self, "identityDnsRecordName1")

    @property
    @jsii.member(jsii_name="identityDnsRecordName2")
    def identity_dns_record_name2(self) -> str:
        """
        cloudformationAttribute:
            IdentityDNSRecordName2
        """
        return jsii.get(self, "identityDnsRecordName2")

    @property
    @jsii.member(jsii_name="identityDnsRecordName3")
    def identity_dns_record_name3(self) -> str:
        """
        cloudformationAttribute:
            IdentityDNSRecordName3
        """
        return jsii.get(self, "identityDnsRecordName3")

    @property
    @jsii.member(jsii_name="identityDnsRecordValue1")
    def identity_dns_record_value1(self) -> str:
        """
        cloudformationAttribute:
            IdentityDNSRecordValue1
        """
        return jsii.get(self, "identityDnsRecordValue1")

    @property
    @jsii.member(jsii_name="identityDnsRecordValue2")
    def identity_dns_record_value2(self) -> str:
        """
        cloudformationAttribute:
            IdentityDNSRecordValue2
        """
        return jsii.get(self, "identityDnsRecordValue2")

    @property
    @jsii.member(jsii_name="identityDnsRecordValue3")
    def identity_dns_record_value3(self) -> str:
        """
        cloudformationAttribute:
            IdentityDNSRecordValue3
        """
        return jsii.get(self, "identityDnsRecordValue3")

    @property
    @jsii.member(jsii_name="identityName")
    def identity_name(self) -> str:
        return jsii.get(self, "identityName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnIdentityProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-pinpointemail.CfnIdentity.MailFromAttributesProperty", jsii_struct_bases=[])
    class MailFromAttributesProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpointemail-identity-mailfromattributes.html
        """
        behaviorOnMxFailure: str
        """``CfnIdentity.MailFromAttributesProperty.BehaviorOnMxFailure``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpointemail-identity-mailfromattributes.html#cfn-pinpointemail-identity-mailfromattributes-behavioronmxfailure
        """

        mailFromDomain: str
        """``CfnIdentity.MailFromAttributesProperty.MailFromDomain``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpointemail-identity-mailfromattributes.html#cfn-pinpointemail-identity-mailfromattributes-mailfromdomain
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-pinpointemail.CfnIdentity.TagsProperty", jsii_struct_bases=[])
    class TagsProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpointemail-identity-tags.html
        """
        key: str
        """``CfnIdentity.TagsProperty.Key``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpointemail-identity-tags.html#cfn-pinpointemail-identity-tags-key
        """

        value: str
        """``CfnIdentity.TagsProperty.Value``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpointemail-identity-tags.html#cfn-pinpointemail-identity-tags-value
        """


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnIdentityProps(jsii.compat.TypedDict, total=False):
    dkimSigningEnabled: typing.Union[bool, aws_cdk.cdk.Token]
    """``AWS::PinpointEmail::Identity.DkimSigningEnabled``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpointemail-identity.html#cfn-pinpointemail-identity-dkimsigningenabled
    """
    feedbackForwardingEnabled: typing.Union[bool, aws_cdk.cdk.Token]
    """``AWS::PinpointEmail::Identity.FeedbackForwardingEnabled``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpointemail-identity.html#cfn-pinpointemail-identity-feedbackforwardingenabled
    """
    mailFromAttributes: typing.Union[aws_cdk.cdk.Token, "CfnIdentity.MailFromAttributesProperty"]
    """``AWS::PinpointEmail::Identity.MailFromAttributes``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpointemail-identity.html#cfn-pinpointemail-identity-mailfromattributes
    """
    tags: typing.List["CfnIdentity.TagsProperty"]
    """``AWS::PinpointEmail::Identity.Tags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpointemail-identity.html#cfn-pinpointemail-identity-tags
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-pinpointemail.CfnIdentityProps", jsii_struct_bases=[_CfnIdentityProps])
class CfnIdentityProps(_CfnIdentityProps):
    """Properties for defining a ``AWS::PinpointEmail::Identity``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpointemail-identity.html
    """
    name: str
    """``AWS::PinpointEmail::Identity.Name``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpointemail-identity.html#cfn-pinpointemail-identity-name
    """

__all__ = ["CfnConfigurationSet", "CfnConfigurationSetEventDestination", "CfnConfigurationSetEventDestinationProps", "CfnConfigurationSetProps", "CfnDedicatedIpPool", "CfnDedicatedIpPoolProps", "CfnIdentity", "CfnIdentityProps", "__jsii_assembly__"]

publication.publish()
