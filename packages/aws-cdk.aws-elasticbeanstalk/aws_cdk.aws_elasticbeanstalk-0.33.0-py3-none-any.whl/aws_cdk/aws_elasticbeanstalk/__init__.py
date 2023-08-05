import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-elasticbeanstalk", "0.33.0", __name__, "aws-elasticbeanstalk@0.33.0.jsii.tgz")
class CfnApplication(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticbeanstalk.CfnApplication"):
    """A CloudFormation ``AWS::ElasticBeanstalk::Application``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk.html
    cloudformationResource:
        AWS::ElasticBeanstalk::Application
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, application_name: typing.Optional[str]=None, description: typing.Optional[str]=None, resource_lifecycle_config: typing.Optional[typing.Union[typing.Optional["ApplicationResourceLifecycleConfigProperty"], typing.Optional[aws_cdk.cdk.Token]]]=None) -> None:
        """Create a new ``AWS::ElasticBeanstalk::Application``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            applicationName: ``AWS::ElasticBeanstalk::Application.ApplicationName``.
            description: ``AWS::ElasticBeanstalk::Application.Description``.
            resourceLifecycleConfig: ``AWS::ElasticBeanstalk::Application.ResourceLifecycleConfig``.
        """
        props: CfnApplicationProps = {}

        if application_name is not None:
            props["applicationName"] = application_name

        if description is not None:
            props["description"] = description

        if resource_lifecycle_config is not None:
            props["resourceLifecycleConfig"] = resource_lifecycle_config

        jsii.create(CfnApplication, self, [scope, id, props])

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
    @jsii.member(jsii_name="applicationName")
    def application_name(self) -> str:
        return jsii.get(self, "applicationName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnApplicationProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticbeanstalk.CfnApplication.ApplicationResourceLifecycleConfigProperty", jsii_struct_bases=[])
    class ApplicationResourceLifecycleConfigProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-application-applicationresourcelifecycleconfig.html
        """
        serviceRole: str
        """``CfnApplication.ApplicationResourceLifecycleConfigProperty.ServiceRole``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-application-applicationresourcelifecycleconfig.html#cfn-elasticbeanstalk-application-applicationresourcelifecycleconfig-servicerole
        """

        versionLifecycleConfig: typing.Union[aws_cdk.cdk.Token, "CfnApplication.ApplicationVersionLifecycleConfigProperty"]
        """``CfnApplication.ApplicationResourceLifecycleConfigProperty.VersionLifecycleConfig``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-application-applicationresourcelifecycleconfig.html#cfn-elasticbeanstalk-application-applicationresourcelifecycleconfig-versionlifecycleconfig
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticbeanstalk.CfnApplication.ApplicationVersionLifecycleConfigProperty", jsii_struct_bases=[])
    class ApplicationVersionLifecycleConfigProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-application-applicationversionlifecycleconfig.html
        """
        maxAgeRule: typing.Union[aws_cdk.cdk.Token, "CfnApplication.MaxAgeRuleProperty"]
        """``CfnApplication.ApplicationVersionLifecycleConfigProperty.MaxAgeRule``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-application-applicationversionlifecycleconfig.html#cfn-elasticbeanstalk-application-applicationversionlifecycleconfig-maxagerule
        """

        maxCountRule: typing.Union[aws_cdk.cdk.Token, "CfnApplication.MaxCountRuleProperty"]
        """``CfnApplication.ApplicationVersionLifecycleConfigProperty.MaxCountRule``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-application-applicationversionlifecycleconfig.html#cfn-elasticbeanstalk-application-applicationversionlifecycleconfig-maxcountrule
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticbeanstalk.CfnApplication.MaxAgeRuleProperty", jsii_struct_bases=[])
    class MaxAgeRuleProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-application-maxagerule.html
        """
        deleteSourceFromS3: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnApplication.MaxAgeRuleProperty.DeleteSourceFromS3``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-application-maxagerule.html#cfn-elasticbeanstalk-application-maxagerule-deletesourcefroms3
        """

        enabled: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnApplication.MaxAgeRuleProperty.Enabled``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-application-maxagerule.html#cfn-elasticbeanstalk-application-maxagerule-enabled
        """

        maxAgeInDays: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnApplication.MaxAgeRuleProperty.MaxAgeInDays``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-application-maxagerule.html#cfn-elasticbeanstalk-application-maxagerule-maxageindays
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticbeanstalk.CfnApplication.MaxCountRuleProperty", jsii_struct_bases=[])
    class MaxCountRuleProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-application-maxcountrule.html
        """
        deleteSourceFromS3: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnApplication.MaxCountRuleProperty.DeleteSourceFromS3``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-application-maxcountrule.html#cfn-elasticbeanstalk-application-maxcountrule-deletesourcefroms3
        """

        enabled: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnApplication.MaxCountRuleProperty.Enabled``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-application-maxcountrule.html#cfn-elasticbeanstalk-application-maxcountrule-enabled
        """

        maxCount: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnApplication.MaxCountRuleProperty.MaxCount``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-application-maxcountrule.html#cfn-elasticbeanstalk-application-maxcountrule-maxcount
        """


@jsii.data_type(jsii_type="@aws-cdk/aws-elasticbeanstalk.CfnApplicationProps", jsii_struct_bases=[])
class CfnApplicationProps(jsii.compat.TypedDict, total=False):
    """Properties for defining a ``AWS::ElasticBeanstalk::Application``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk.html
    """
    applicationName: str
    """``AWS::ElasticBeanstalk::Application.ApplicationName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk.html#cfn-elasticbeanstalk-application-name
    """

    description: str
    """``AWS::ElasticBeanstalk::Application.Description``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk.html#cfn-elasticbeanstalk-application-description
    """

    resourceLifecycleConfig: typing.Union["CfnApplication.ApplicationResourceLifecycleConfigProperty", aws_cdk.cdk.Token]
    """``AWS::ElasticBeanstalk::Application.ResourceLifecycleConfig``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk.html#cfn-elasticbeanstalk-application-resourcelifecycleconfig
    """

class CfnApplicationVersion(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticbeanstalk.CfnApplicationVersion"):
    """A CloudFormation ``AWS::ElasticBeanstalk::ApplicationVersion``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-version.html
    cloudformationResource:
        AWS::ElasticBeanstalk::ApplicationVersion
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, application_name: str, source_bundle: typing.Union[aws_cdk.cdk.Token, "SourceBundleProperty"], description: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::ElasticBeanstalk::ApplicationVersion``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            applicationName: ``AWS::ElasticBeanstalk::ApplicationVersion.ApplicationName``.
            sourceBundle: ``AWS::ElasticBeanstalk::ApplicationVersion.SourceBundle``.
            description: ``AWS::ElasticBeanstalk::ApplicationVersion.Description``.
        """
        props: CfnApplicationVersionProps = {"applicationName": application_name, "sourceBundle": source_bundle}

        if description is not None:
            props["description"] = description

        jsii.create(CfnApplicationVersion, self, [scope, id, props])

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
    @jsii.member(jsii_name="applicationVersionName")
    def application_version_name(self) -> str:
        return jsii.get(self, "applicationVersionName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnApplicationVersionProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticbeanstalk.CfnApplicationVersion.SourceBundleProperty", jsii_struct_bases=[])
    class SourceBundleProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-sourcebundle.html
        """
        s3Bucket: str
        """``CfnApplicationVersion.SourceBundleProperty.S3Bucket``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-sourcebundle.html#cfn-beanstalk-sourcebundle-s3bucket
        """

        s3Key: str
        """``CfnApplicationVersion.SourceBundleProperty.S3Key``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-sourcebundle.html#cfn-beanstalk-sourcebundle-s3key
        """


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnApplicationVersionProps(jsii.compat.TypedDict, total=False):
    description: str
    """``AWS::ElasticBeanstalk::ApplicationVersion.Description``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-version.html#cfn-elasticbeanstalk-applicationversion-description
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-elasticbeanstalk.CfnApplicationVersionProps", jsii_struct_bases=[_CfnApplicationVersionProps])
class CfnApplicationVersionProps(_CfnApplicationVersionProps):
    """Properties for defining a ``AWS::ElasticBeanstalk::ApplicationVersion``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-version.html
    """
    applicationName: str
    """``AWS::ElasticBeanstalk::ApplicationVersion.ApplicationName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-version.html#cfn-elasticbeanstalk-applicationversion-applicationname
    """

    sourceBundle: typing.Union[aws_cdk.cdk.Token, "CfnApplicationVersion.SourceBundleProperty"]
    """``AWS::ElasticBeanstalk::ApplicationVersion.SourceBundle``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-version.html#cfn-elasticbeanstalk-applicationversion-sourcebundle
    """

class CfnConfigurationTemplate(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticbeanstalk.CfnConfigurationTemplate"):
    """A CloudFormation ``AWS::ElasticBeanstalk::ConfigurationTemplate``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-configurationtemplate.html
    cloudformationResource:
        AWS::ElasticBeanstalk::ConfigurationTemplate
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, application_name: str, description: typing.Optional[str]=None, environment_id: typing.Optional[str]=None, option_settings: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional[typing.List[typing.Union[aws_cdk.cdk.Token, "ConfigurationOptionSettingProperty"]]]]]=None, platform_arn: typing.Optional[str]=None, solution_stack_name: typing.Optional[str]=None, source_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional["SourceConfigurationProperty"]]]=None) -> None:
        """Create a new ``AWS::ElasticBeanstalk::ConfigurationTemplate``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            applicationName: ``AWS::ElasticBeanstalk::ConfigurationTemplate.ApplicationName``.
            description: ``AWS::ElasticBeanstalk::ConfigurationTemplate.Description``.
            environmentId: ``AWS::ElasticBeanstalk::ConfigurationTemplate.EnvironmentId``.
            optionSettings: ``AWS::ElasticBeanstalk::ConfigurationTemplate.OptionSettings``.
            platformArn: ``AWS::ElasticBeanstalk::ConfigurationTemplate.PlatformArn``.
            solutionStackName: ``AWS::ElasticBeanstalk::ConfigurationTemplate.SolutionStackName``.
            sourceConfiguration: ``AWS::ElasticBeanstalk::ConfigurationTemplate.SourceConfiguration``.
        """
        props: CfnConfigurationTemplateProps = {"applicationName": application_name}

        if description is not None:
            props["description"] = description

        if environment_id is not None:
            props["environmentId"] = environment_id

        if option_settings is not None:
            props["optionSettings"] = option_settings

        if platform_arn is not None:
            props["platformArn"] = platform_arn

        if solution_stack_name is not None:
            props["solutionStackName"] = solution_stack_name

        if source_configuration is not None:
            props["sourceConfiguration"] = source_configuration

        jsii.create(CfnConfigurationTemplate, self, [scope, id, props])

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
    @jsii.member(jsii_name="configurationTemplateName")
    def configuration_template_name(self) -> str:
        return jsii.get(self, "configurationTemplateName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnConfigurationTemplateProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _ConfigurationOptionSettingProperty(jsii.compat.TypedDict, total=False):
        resourceName: str
        """``CfnConfigurationTemplate.ConfigurationOptionSettingProperty.ResourceName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-configurationtemplate-configurationoptionsetting.html#cfn-elasticbeanstalk-configurationtemplate-configurationoptionsetting-resourcename
        """
        value: str
        """``CfnConfigurationTemplate.ConfigurationOptionSettingProperty.Value``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-configurationtemplate-configurationoptionsetting.html#cfn-elasticbeanstalk-configurationtemplate-configurationoptionsetting-value
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticbeanstalk.CfnConfigurationTemplate.ConfigurationOptionSettingProperty", jsii_struct_bases=[_ConfigurationOptionSettingProperty])
    class ConfigurationOptionSettingProperty(_ConfigurationOptionSettingProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-configurationtemplate-configurationoptionsetting.html
        """
        namespace: str
        """``CfnConfigurationTemplate.ConfigurationOptionSettingProperty.Namespace``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-configurationtemplate-configurationoptionsetting.html#cfn-elasticbeanstalk-configurationtemplate-configurationoptionsetting-namespace
        """

        optionName: str
        """``CfnConfigurationTemplate.ConfigurationOptionSettingProperty.OptionName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-configurationtemplate-configurationoptionsetting.html#cfn-elasticbeanstalk-configurationtemplate-configurationoptionsetting-optionname
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticbeanstalk.CfnConfigurationTemplate.SourceConfigurationProperty", jsii_struct_bases=[])
    class SourceConfigurationProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-configurationtemplate-sourceconfiguration.html
        """
        applicationName: str
        """``CfnConfigurationTemplate.SourceConfigurationProperty.ApplicationName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-configurationtemplate-sourceconfiguration.html#cfn-elasticbeanstalk-configurationtemplate-sourceconfiguration-applicationname
        """

        templateName: str
        """``CfnConfigurationTemplate.SourceConfigurationProperty.TemplateName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-configurationtemplate-sourceconfiguration.html#cfn-elasticbeanstalk-configurationtemplate-sourceconfiguration-templatename
        """


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnConfigurationTemplateProps(jsii.compat.TypedDict, total=False):
    description: str
    """``AWS::ElasticBeanstalk::ConfigurationTemplate.Description``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-configurationtemplate.html#cfn-elasticbeanstalk-configurationtemplate-description
    """
    environmentId: str
    """``AWS::ElasticBeanstalk::ConfigurationTemplate.EnvironmentId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-configurationtemplate.html#cfn-elasticbeanstalk-configurationtemplate-environmentid
    """
    optionSettings: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnConfigurationTemplate.ConfigurationOptionSettingProperty"]]]
    """``AWS::ElasticBeanstalk::ConfigurationTemplate.OptionSettings``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-configurationtemplate.html#cfn-elasticbeanstalk-configurationtemplate-optionsettings
    """
    platformArn: str
    """``AWS::ElasticBeanstalk::ConfigurationTemplate.PlatformArn``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-configurationtemplate.html#cfn-elasticbeanstalk-configurationtemplate-platformarn
    """
    solutionStackName: str
    """``AWS::ElasticBeanstalk::ConfigurationTemplate.SolutionStackName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-configurationtemplate.html#cfn-elasticbeanstalk-configurationtemplate-solutionstackname
    """
    sourceConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnConfigurationTemplate.SourceConfigurationProperty"]
    """``AWS::ElasticBeanstalk::ConfigurationTemplate.SourceConfiguration``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-configurationtemplate.html#cfn-elasticbeanstalk-configurationtemplate-sourceconfiguration
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-elasticbeanstalk.CfnConfigurationTemplateProps", jsii_struct_bases=[_CfnConfigurationTemplateProps])
class CfnConfigurationTemplateProps(_CfnConfigurationTemplateProps):
    """Properties for defining a ``AWS::ElasticBeanstalk::ConfigurationTemplate``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-configurationtemplate.html
    """
    applicationName: str
    """``AWS::ElasticBeanstalk::ConfigurationTemplate.ApplicationName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-configurationtemplate.html#cfn-elasticbeanstalk-configurationtemplate-applicationname
    """

class CfnEnvironment(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticbeanstalk.CfnEnvironment"):
    """A CloudFormation ``AWS::ElasticBeanstalk::Environment``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-environment.html
    cloudformationResource:
        AWS::ElasticBeanstalk::Environment
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, application_name: str, cname_prefix: typing.Optional[str]=None, description: typing.Optional[str]=None, environment_name: typing.Optional[str]=None, option_settings: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional[typing.List[typing.Union[aws_cdk.cdk.Token, "OptionSettingProperty"]]]]]=None, platform_arn: typing.Optional[str]=None, solution_stack_name: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None, template_name: typing.Optional[str]=None, tier: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional["TierProperty"]]]=None, version_label: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::ElasticBeanstalk::Environment``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            applicationName: ``AWS::ElasticBeanstalk::Environment.ApplicationName``.
            cnamePrefix: ``AWS::ElasticBeanstalk::Environment.CNAMEPrefix``.
            description: ``AWS::ElasticBeanstalk::Environment.Description``.
            environmentName: ``AWS::ElasticBeanstalk::Environment.EnvironmentName``.
            optionSettings: ``AWS::ElasticBeanstalk::Environment.OptionSettings``.
            platformArn: ``AWS::ElasticBeanstalk::Environment.PlatformArn``.
            solutionStackName: ``AWS::ElasticBeanstalk::Environment.SolutionStackName``.
            tags: ``AWS::ElasticBeanstalk::Environment.Tags``.
            templateName: ``AWS::ElasticBeanstalk::Environment.TemplateName``.
            tier: ``AWS::ElasticBeanstalk::Environment.Tier``.
            versionLabel: ``AWS::ElasticBeanstalk::Environment.VersionLabel``.
        """
        props: CfnEnvironmentProps = {"applicationName": application_name}

        if cname_prefix is not None:
            props["cnamePrefix"] = cname_prefix

        if description is not None:
            props["description"] = description

        if environment_name is not None:
            props["environmentName"] = environment_name

        if option_settings is not None:
            props["optionSettings"] = option_settings

        if platform_arn is not None:
            props["platformArn"] = platform_arn

        if solution_stack_name is not None:
            props["solutionStackName"] = solution_stack_name

        if tags is not None:
            props["tags"] = tags

        if template_name is not None:
            props["templateName"] = template_name

        if tier is not None:
            props["tier"] = tier

        if version_label is not None:
            props["versionLabel"] = version_label

        jsii.create(CfnEnvironment, self, [scope, id, props])

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
    @jsii.member(jsii_name="environmentEndpointUrl")
    def environment_endpoint_url(self) -> str:
        """
        cloudformationAttribute:
            EndpointURL
        """
        return jsii.get(self, "environmentEndpointUrl")

    @property
    @jsii.member(jsii_name="environmentName")
    def environment_name(self) -> str:
        return jsii.get(self, "environmentName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnEnvironmentProps":
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

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _OptionSettingProperty(jsii.compat.TypedDict, total=False):
        resourceName: str
        """``CfnEnvironment.OptionSettingProperty.ResourceName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-option-settings.html#cfn-elasticbeanstalk-environment-optionsetting-resourcename
        """
        value: str
        """``CfnEnvironment.OptionSettingProperty.Value``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-option-settings.html#cfn-beanstalk-optionsettings-value
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticbeanstalk.CfnEnvironment.OptionSettingProperty", jsii_struct_bases=[_OptionSettingProperty])
    class OptionSettingProperty(_OptionSettingProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-option-settings.html
        """
        namespace: str
        """``CfnEnvironment.OptionSettingProperty.Namespace``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-option-settings.html#cfn-beanstalk-optionsettings-namespace
        """

        optionName: str
        """``CfnEnvironment.OptionSettingProperty.OptionName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-option-settings.html#cfn-beanstalk-optionsettings-optionname
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticbeanstalk.CfnEnvironment.TierProperty", jsii_struct_bases=[])
    class TierProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-environment-tier.html
        """
        name: str
        """``CfnEnvironment.TierProperty.Name``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-environment-tier.html#cfn-beanstalk-env-tier-name
        """

        type: str
        """``CfnEnvironment.TierProperty.Type``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-environment-tier.html#cfn-beanstalk-env-tier-type
        """

        version: str
        """``CfnEnvironment.TierProperty.Version``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-environment-tier.html#cfn-beanstalk-env-tier-version
        """


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnEnvironmentProps(jsii.compat.TypedDict, total=False):
    cnamePrefix: str
    """``AWS::ElasticBeanstalk::Environment.CNAMEPrefix``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-environment.html#cfn-beanstalk-environment-cnameprefix
    """
    description: str
    """``AWS::ElasticBeanstalk::Environment.Description``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-environment.html#cfn-beanstalk-environment-description
    """
    environmentName: str
    """``AWS::ElasticBeanstalk::Environment.EnvironmentName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-environment.html#cfn-beanstalk-environment-name
    """
    optionSettings: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnEnvironment.OptionSettingProperty"]]]
    """``AWS::ElasticBeanstalk::Environment.OptionSettings``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-environment.html#cfn-beanstalk-environment-optionsettings
    """
    platformArn: str
    """``AWS::ElasticBeanstalk::Environment.PlatformArn``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-environment.html#cfn-beanstalk-environment-platformarn
    """
    solutionStackName: str
    """``AWS::ElasticBeanstalk::Environment.SolutionStackName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-environment.html#cfn-beanstalk-environment-solutionstackname
    """
    tags: typing.List[aws_cdk.cdk.CfnTag]
    """``AWS::ElasticBeanstalk::Environment.Tags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-environment.html#cfn-elasticbeanstalk-environment-tags
    """
    templateName: str
    """``AWS::ElasticBeanstalk::Environment.TemplateName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-environment.html#cfn-beanstalk-environment-templatename
    """
    tier: typing.Union[aws_cdk.cdk.Token, "CfnEnvironment.TierProperty"]
    """``AWS::ElasticBeanstalk::Environment.Tier``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-environment.html#cfn-beanstalk-environment-tier
    """
    versionLabel: str
    """``AWS::ElasticBeanstalk::Environment.VersionLabel``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-environment.html#cfn-beanstalk-environment-versionlabel
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-elasticbeanstalk.CfnEnvironmentProps", jsii_struct_bases=[_CfnEnvironmentProps])
class CfnEnvironmentProps(_CfnEnvironmentProps):
    """Properties for defining a ``AWS::ElasticBeanstalk::Environment``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-environment.html
    """
    applicationName: str
    """``AWS::ElasticBeanstalk::Environment.ApplicationName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-environment.html#cfn-beanstalk-environment-applicationname
    """

__all__ = ["CfnApplication", "CfnApplicationProps", "CfnApplicationVersion", "CfnApplicationVersionProps", "CfnConfigurationTemplate", "CfnConfigurationTemplateProps", "CfnEnvironment", "CfnEnvironmentProps", "__jsii_assembly__"]

publication.publish()
