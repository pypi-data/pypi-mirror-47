import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_ec2
import aws_cdk.aws_iam
import aws_cdk.aws_kms
import aws_cdk.aws_lambda
import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-secretsmanager", "0.33.0", __name__, "aws-secretsmanager@0.33.0.jsii.tgz")
@jsii.data_type(jsii_type="@aws-cdk/aws-secretsmanager.AttachedSecretOptions", jsii_struct_bases=[])
class AttachedSecretOptions(jsii.compat.TypedDict):
    """Options to add a secret attachment to a secret."""
    target: "ISecretAttachmentTarget"
    """The target to attach the secret to."""

@jsii.enum(jsii_type="@aws-cdk/aws-secretsmanager.AttachmentTargetType")
class AttachmentTargetType(enum.Enum):
    """The type of service or database that's being associated with the secret."""
    Instance = "Instance"
    """A database instance."""
    Cluster = "Cluster"
    """A database cluster."""

class CfnResourcePolicy(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-secretsmanager.CfnResourcePolicy"):
    """A CloudFormation ``AWS::SecretsManager::ResourcePolicy``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-resourcepolicy.html
    cloudformationResource:
        AWS::SecretsManager::ResourcePolicy
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, resource_policy: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token], secret_id: str) -> None:
        """Create a new ``AWS::SecretsManager::ResourcePolicy``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            resourcePolicy: ``AWS::SecretsManager::ResourcePolicy.ResourcePolicy``.
            secretId: ``AWS::SecretsManager::ResourcePolicy.SecretId``.
        """
        props: CfnResourcePolicyProps = {"resourcePolicy": resource_policy, "secretId": secret_id}

        jsii.create(CfnResourcePolicy, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnResourcePolicyProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="resourcePolicySecretArn")
    def resource_policy_secret_arn(self) -> str:
        return jsii.get(self, "resourcePolicySecretArn")


@jsii.data_type(jsii_type="@aws-cdk/aws-secretsmanager.CfnResourcePolicyProps", jsii_struct_bases=[])
class CfnResourcePolicyProps(jsii.compat.TypedDict):
    """Properties for defining a ``AWS::SecretsManager::ResourcePolicy``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-resourcepolicy.html
    """
    resourcePolicy: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
    """``AWS::SecretsManager::ResourcePolicy.ResourcePolicy``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-resourcepolicy.html#cfn-secretsmanager-resourcepolicy-resourcepolicy
    """

    secretId: str
    """``AWS::SecretsManager::ResourcePolicy.SecretId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-resourcepolicy.html#cfn-secretsmanager-resourcepolicy-secretid
    """

class CfnRotationSchedule(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-secretsmanager.CfnRotationSchedule"):
    """A CloudFormation ``AWS::SecretsManager::RotationSchedule``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-rotationschedule.html
    cloudformationResource:
        AWS::SecretsManager::RotationSchedule
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, secret_id: str, rotation_lambda_arn: typing.Optional[str]=None, rotation_rules: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional["RotationRulesProperty"]]]=None) -> None:
        """Create a new ``AWS::SecretsManager::RotationSchedule``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            secretId: ``AWS::SecretsManager::RotationSchedule.SecretId``.
            rotationLambdaArn: ``AWS::SecretsManager::RotationSchedule.RotationLambdaARN``.
            rotationRules: ``AWS::SecretsManager::RotationSchedule.RotationRules``.
        """
        props: CfnRotationScheduleProps = {"secretId": secret_id}

        if rotation_lambda_arn is not None:
            props["rotationLambdaArn"] = rotation_lambda_arn

        if rotation_rules is not None:
            props["rotationRules"] = rotation_rules

        jsii.create(CfnRotationSchedule, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnRotationScheduleProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="rotationScheduleSecretArn")
    def rotation_schedule_secret_arn(self) -> str:
        return jsii.get(self, "rotationScheduleSecretArn")

    @jsii.data_type(jsii_type="@aws-cdk/aws-secretsmanager.CfnRotationSchedule.RotationRulesProperty", jsii_struct_bases=[])
    class RotationRulesProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-rotationschedule-rotationrules.html
        """
        automaticallyAfterDays: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnRotationSchedule.RotationRulesProperty.AutomaticallyAfterDays``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-rotationschedule-rotationrules.html#cfn-secretsmanager-rotationschedule-rotationrules-automaticallyafterdays
        """


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnRotationScheduleProps(jsii.compat.TypedDict, total=False):
    rotationLambdaArn: str
    """``AWS::SecretsManager::RotationSchedule.RotationLambdaARN``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-rotationschedule.html#cfn-secretsmanager-rotationschedule-rotationlambdaarn
    """
    rotationRules: typing.Union[aws_cdk.cdk.Token, "CfnRotationSchedule.RotationRulesProperty"]
    """``AWS::SecretsManager::RotationSchedule.RotationRules``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-rotationschedule.html#cfn-secretsmanager-rotationschedule-rotationrules
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-secretsmanager.CfnRotationScheduleProps", jsii_struct_bases=[_CfnRotationScheduleProps])
class CfnRotationScheduleProps(_CfnRotationScheduleProps):
    """Properties for defining a ``AWS::SecretsManager::RotationSchedule``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-rotationschedule.html
    """
    secretId: str
    """``AWS::SecretsManager::RotationSchedule.SecretId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-rotationschedule.html#cfn-secretsmanager-rotationschedule-secretid
    """

class CfnSecret(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-secretsmanager.CfnSecret"):
    """A CloudFormation ``AWS::SecretsManager::Secret``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html
    cloudformationResource:
        AWS::SecretsManager::Secret
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, description: typing.Optional[str]=None, generate_secret_string: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional["GenerateSecretStringProperty"]]]=None, kms_key_id: typing.Optional[str]=None, name: typing.Optional[str]=None, secret_string: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        """Create a new ``AWS::SecretsManager::Secret``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            description: ``AWS::SecretsManager::Secret.Description``.
            generateSecretString: ``AWS::SecretsManager::Secret.GenerateSecretString``.
            kmsKeyId: ``AWS::SecretsManager::Secret.KmsKeyId``.
            name: ``AWS::SecretsManager::Secret.Name``.
            secretString: ``AWS::SecretsManager::Secret.SecretString``.
            tags: ``AWS::SecretsManager::Secret.Tags``.
        """
        props: CfnSecretProps = {}

        if description is not None:
            props["description"] = description

        if generate_secret_string is not None:
            props["generateSecretString"] = generate_secret_string

        if kms_key_id is not None:
            props["kmsKeyId"] = kms_key_id

        if name is not None:
            props["name"] = name

        if secret_string is not None:
            props["secretString"] = secret_string

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnSecret, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnSecretProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="secretArn")
    def secret_arn(self) -> str:
        return jsii.get(self, "secretArn")

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

    @jsii.data_type(jsii_type="@aws-cdk/aws-secretsmanager.CfnSecret.GenerateSecretStringProperty", jsii_struct_bases=[])
    class GenerateSecretStringProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-generatesecretstring.html
        """
        excludeCharacters: str
        """``CfnSecret.GenerateSecretStringProperty.ExcludeCharacters``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-generatesecretstring.html#cfn-secretsmanager-secret-generatesecretstring-excludecharacters
        """

        excludeLowercase: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnSecret.GenerateSecretStringProperty.ExcludeLowercase``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-generatesecretstring.html#cfn-secretsmanager-secret-generatesecretstring-excludelowercase
        """

        excludeNumbers: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnSecret.GenerateSecretStringProperty.ExcludeNumbers``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-generatesecretstring.html#cfn-secretsmanager-secret-generatesecretstring-excludenumbers
        """

        excludePunctuation: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnSecret.GenerateSecretStringProperty.ExcludePunctuation``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-generatesecretstring.html#cfn-secretsmanager-secret-generatesecretstring-excludepunctuation
        """

        excludeUppercase: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnSecret.GenerateSecretStringProperty.ExcludeUppercase``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-generatesecretstring.html#cfn-secretsmanager-secret-generatesecretstring-excludeuppercase
        """

        generateStringKey: str
        """``CfnSecret.GenerateSecretStringProperty.GenerateStringKey``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-generatesecretstring.html#cfn-secretsmanager-secret-generatesecretstring-generatestringkey
        """

        includeSpace: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnSecret.GenerateSecretStringProperty.IncludeSpace``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-generatesecretstring.html#cfn-secretsmanager-secret-generatesecretstring-includespace
        """

        passwordLength: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnSecret.GenerateSecretStringProperty.PasswordLength``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-generatesecretstring.html#cfn-secretsmanager-secret-generatesecretstring-passwordlength
        """

        requireEachIncludedType: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnSecret.GenerateSecretStringProperty.RequireEachIncludedType``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-generatesecretstring.html#cfn-secretsmanager-secret-generatesecretstring-requireeachincludedtype
        """

        secretStringTemplate: str
        """``CfnSecret.GenerateSecretStringProperty.SecretStringTemplate``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-generatesecretstring.html#cfn-secretsmanager-secret-generatesecretstring-secretstringtemplate
        """


@jsii.data_type(jsii_type="@aws-cdk/aws-secretsmanager.CfnSecretProps", jsii_struct_bases=[])
class CfnSecretProps(jsii.compat.TypedDict, total=False):
    """Properties for defining a ``AWS::SecretsManager::Secret``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html
    """
    description: str
    """``AWS::SecretsManager::Secret.Description``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html#cfn-secretsmanager-secret-description
    """

    generateSecretString: typing.Union[aws_cdk.cdk.Token, "CfnSecret.GenerateSecretStringProperty"]
    """``AWS::SecretsManager::Secret.GenerateSecretString``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html#cfn-secretsmanager-secret-generatesecretstring
    """

    kmsKeyId: str
    """``AWS::SecretsManager::Secret.KmsKeyId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html#cfn-secretsmanager-secret-kmskeyid
    """

    name: str
    """``AWS::SecretsManager::Secret.Name``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html#cfn-secretsmanager-secret-name
    """

    secretString: str
    """``AWS::SecretsManager::Secret.SecretString``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html#cfn-secretsmanager-secret-secretstring
    """

    tags: typing.List[aws_cdk.cdk.CfnTag]
    """``AWS::SecretsManager::Secret.Tags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html#cfn-secretsmanager-secret-tags
    """

class CfnSecretTargetAttachment(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-secretsmanager.CfnSecretTargetAttachment"):
    """A CloudFormation ``AWS::SecretsManager::SecretTargetAttachment``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secrettargetattachment.html
    cloudformationResource:
        AWS::SecretsManager::SecretTargetAttachment
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, secret_id: str, target_id: str, target_type: str) -> None:
        """Create a new ``AWS::SecretsManager::SecretTargetAttachment``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            secretId: ``AWS::SecretsManager::SecretTargetAttachment.SecretId``.
            targetId: ``AWS::SecretsManager::SecretTargetAttachment.TargetId``.
            targetType: ``AWS::SecretsManager::SecretTargetAttachment.TargetType``.
        """
        props: CfnSecretTargetAttachmentProps = {"secretId": secret_id, "targetId": target_id, "targetType": target_type}

        jsii.create(CfnSecretTargetAttachment, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnSecretTargetAttachmentProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="secretTargetAttachmentSecretArn")
    def secret_target_attachment_secret_arn(self) -> str:
        return jsii.get(self, "secretTargetAttachmentSecretArn")


@jsii.data_type(jsii_type="@aws-cdk/aws-secretsmanager.CfnSecretTargetAttachmentProps", jsii_struct_bases=[])
class CfnSecretTargetAttachmentProps(jsii.compat.TypedDict):
    """Properties for defining a ``AWS::SecretsManager::SecretTargetAttachment``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secrettargetattachment.html
    """
    secretId: str
    """``AWS::SecretsManager::SecretTargetAttachment.SecretId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secrettargetattachment.html#cfn-secretsmanager-secrettargetattachment-secretid
    """

    targetId: str
    """``AWS::SecretsManager::SecretTargetAttachment.TargetId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secrettargetattachment.html#cfn-secretsmanager-secrettargetattachment-targetid
    """

    targetType: str
    """``AWS::SecretsManager::SecretTargetAttachment.TargetType``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secrettargetattachment.html#cfn-secretsmanager-secrettargetattachment-targettype
    """

@jsii.interface(jsii_type="@aws-cdk/aws-secretsmanager.ISecret")
class ISecret(aws_cdk.cdk.IResource, jsii.compat.Protocol):
    """A secret in AWS Secrets Manager."""
    @staticmethod
    def __jsii_proxy_class__():
        return _ISecretProxy

    @property
    @jsii.member(jsii_name="secretArn")
    def secret_arn(self) -> str:
        """The ARN of the secret in AWS Secrets Manager.

        attribute:
            true
        """
        ...

    @property
    @jsii.member(jsii_name="secretValue")
    def secret_value(self) -> aws_cdk.cdk.SecretValue:
        """Retrieve the value of the stored secret as a ``SecretValue``.

        attribute:
            true
        """
        ...

    @property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        """The customer-managed encryption key that is used to encrypt this secret, if any.

        When not specified, the default
        KMS key for the account and region is being used.
        """
        ...

    @jsii.member(jsii_name="addRotationSchedule")
    def add_rotation_schedule(self, id: str, *, rotation_lambda: aws_cdk.aws_lambda.IFunction, automatically_after_days: typing.Optional[jsii.Number]=None) -> "RotationSchedule":
        """Adds a rotation schedule to the secret.

        Arguments:
            id: -
            options: -
            rotationLambda: THe Lambda function that can rotate the secret.
            automaticallyAfterDays: Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation. Default: 30
        """
        ...

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, grantee: aws_cdk.aws_iam.IGrantable, version_stages: typing.Optional[typing.List[str]]=None) -> aws_cdk.aws_iam.Grant:
        """Grants reading the secret value to some role.

        Arguments:
            grantee: the principal being granted permission.
            versionStages: the version stages the grant is limited to. If not specified, no restriction on the version stages is applied.
        """
        ...

    @jsii.member(jsii_name="secretJsonValue")
    def secret_json_value(self, key: str) -> aws_cdk.cdk.SecretValue:
        """Interpret the secret as a JSON object and return a field's value from it as a ``SecretValue``.

        Arguments:
            key: -
        """
        ...


class _ISecretProxy(jsii.proxy_for(aws_cdk.cdk.IResource)):
    """A secret in AWS Secrets Manager."""
    __jsii_type__ = "@aws-cdk/aws-secretsmanager.ISecret"
    @property
    @jsii.member(jsii_name="secretArn")
    def secret_arn(self) -> str:
        """The ARN of the secret in AWS Secrets Manager.

        attribute:
            true
        """
        return jsii.get(self, "secretArn")

    @property
    @jsii.member(jsii_name="secretValue")
    def secret_value(self) -> aws_cdk.cdk.SecretValue:
        """Retrieve the value of the stored secret as a ``SecretValue``.

        attribute:
            true
        """
        return jsii.get(self, "secretValue")

    @property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        """The customer-managed encryption key that is used to encrypt this secret, if any.

        When not specified, the default
        KMS key for the account and region is being used.
        """
        return jsii.get(self, "encryptionKey")

    @jsii.member(jsii_name="addRotationSchedule")
    def add_rotation_schedule(self, id: str, *, rotation_lambda: aws_cdk.aws_lambda.IFunction, automatically_after_days: typing.Optional[jsii.Number]=None) -> "RotationSchedule":
        """Adds a rotation schedule to the secret.

        Arguments:
            id: -
            options: -
            rotationLambda: THe Lambda function that can rotate the secret.
            automaticallyAfterDays: Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation. Default: 30
        """
        options: RotationScheduleOptions = {"rotationLambda": rotation_lambda}

        if automatically_after_days is not None:
            options["automaticallyAfterDays"] = automatically_after_days

        return jsii.invoke(self, "addRotationSchedule", [id, options])

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, grantee: aws_cdk.aws_iam.IGrantable, version_stages: typing.Optional[typing.List[str]]=None) -> aws_cdk.aws_iam.Grant:
        """Grants reading the secret value to some role.

        Arguments:
            grantee: the principal being granted permission.
            versionStages: the version stages the grant is limited to. If not specified, no restriction on the version stages is applied.
        """
        return jsii.invoke(self, "grantRead", [grantee, version_stages])

    @jsii.member(jsii_name="secretJsonValue")
    def secret_json_value(self, key: str) -> aws_cdk.cdk.SecretValue:
        """Interpret the secret as a JSON object and return a field's value from it as a ``SecretValue``.

        Arguments:
            key: -
        """
        return jsii.invoke(self, "secretJsonValue", [key])


@jsii.interface(jsii_type="@aws-cdk/aws-secretsmanager.ISecretAttachmentTarget")
class ISecretAttachmentTarget(jsii.compat.Protocol):
    """A secret attachment target."""
    @staticmethod
    def __jsii_proxy_class__():
        return _ISecretAttachmentTargetProxy

    @jsii.member(jsii_name="asSecretAttachmentTarget")
    def as_secret_attachment_target(self) -> "SecretAttachmentTargetProps":
        """Renders the target specifications."""
        ...


class _ISecretAttachmentTargetProxy():
    """A secret attachment target."""
    __jsii_type__ = "@aws-cdk/aws-secretsmanager.ISecretAttachmentTarget"
    @jsii.member(jsii_name="asSecretAttachmentTarget")
    def as_secret_attachment_target(self) -> "SecretAttachmentTargetProps":
        """Renders the target specifications."""
        return jsii.invoke(self, "asSecretAttachmentTarget", [])


@jsii.interface(jsii_type="@aws-cdk/aws-secretsmanager.ISecretTargetAttachment")
class ISecretTargetAttachment(ISecret, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _ISecretTargetAttachmentProxy

    @property
    @jsii.member(jsii_name="secretTargetAttachmentSecretArn")
    def secret_target_attachment_secret_arn(self) -> str:
        """Same as ``secretArn``.

        attribute:
            true
        """
        ...


class _ISecretTargetAttachmentProxy(jsii.proxy_for(ISecret)):
    __jsii_type__ = "@aws-cdk/aws-secretsmanager.ISecretTargetAttachment"
    @property
    @jsii.member(jsii_name="secretTargetAttachmentSecretArn")
    def secret_target_attachment_secret_arn(self) -> str:
        """Same as ``secretArn``.

        attribute:
            true
        """
        return jsii.get(self, "secretTargetAttachmentSecretArn")


class RotationSchedule(aws_cdk.cdk.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-secretsmanager.RotationSchedule"):
    """A rotation schedule."""
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, secret: "ISecret", rotation_lambda: aws_cdk.aws_lambda.IFunction, automatically_after_days: typing.Optional[jsii.Number]=None) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            secret: The secret to rotate.
            rotationLambda: THe Lambda function that can rotate the secret.
            automaticallyAfterDays: Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation. Default: 30
        """
        props: RotationScheduleProps = {"secret": secret, "rotationLambda": rotation_lambda}

        if automatically_after_days is not None:
            props["automaticallyAfterDays"] = automatically_after_days

        jsii.create(RotationSchedule, self, [scope, id, props])


@jsii.data_type_optionals(jsii_struct_bases=[])
class _RotationScheduleOptions(jsii.compat.TypedDict, total=False):
    automaticallyAfterDays: jsii.Number
    """Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation.

    Default:
        30
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-secretsmanager.RotationScheduleOptions", jsii_struct_bases=[_RotationScheduleOptions])
class RotationScheduleOptions(_RotationScheduleOptions):
    """Options to add a rotation schedule to a secret."""
    rotationLambda: aws_cdk.aws_lambda.IFunction
    """THe Lambda function that can rotate the secret."""

@jsii.data_type(jsii_type="@aws-cdk/aws-secretsmanager.RotationScheduleProps", jsii_struct_bases=[RotationScheduleOptions])
class RotationScheduleProps(RotationScheduleOptions, jsii.compat.TypedDict):
    """Construction properties for a RotationSchedule."""
    secret: "ISecret"
    """The secret to rotate."""

@jsii.implements(ISecret)
class Secret(aws_cdk.cdk.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-secretsmanager.Secret"):
    """Creates a new secret in AWS SecretsManager."""
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, description: typing.Optional[str]=None, encryption_key: typing.Optional[aws_cdk.aws_kms.IKey]=None, generate_secret_string: typing.Optional["SecretStringGenerator"]=None, name: typing.Optional[str]=None) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            description: An optional, human-friendly description of the secret. Default: - No description.
            encryptionKey: The customer-managed encryption key to use for encrypting the secret value. Default: - A default KMS key for the account and region is used.
            generateSecretString: Configuration for how to generate a secret value. Default: - 32 characters with upper-case letters, lower-case letters, punctuation and numbers (at least one from each category), per the default values of ``SecretStringGenerator``.
            name: A name for the secret. Note that deleting secrets from SecretsManager does not happen immediately, but after a 7 to 30 days blackout period. During that period, it is not possible to create another secret that shares the same name. Default: - A name is generated by CloudFormation.
        """
        props: SecretProps = {}

        if description is not None:
            props["description"] = description

        if encryption_key is not None:
            props["encryptionKey"] = encryption_key

        if generate_secret_string is not None:
            props["generateSecretString"] = generate_secret_string

        if name is not None:
            props["name"] = name

        jsii.create(Secret, self, [scope, id, props])

    @jsii.member(jsii_name="fromSecretArn")
    @classmethod
    def from_secret_arn(cls, scope: aws_cdk.cdk.Construct, id: str, secret_arn: str) -> "ISecret":
        """
        Arguments:
            scope: -
            id: -
            secretArn: -
        """
        return jsii.sinvoke(cls, "fromSecretArn", [scope, id, secret_arn])

    @jsii.member(jsii_name="fromSecretAttributes")
    @classmethod
    def from_secret_attributes(cls, scope: aws_cdk.cdk.Construct, id: str, *, secret_arn: str, encryption_key: typing.Optional[aws_cdk.aws_kms.IKey]=None) -> "ISecret":
        """Import an existing secret into the Stack.

        Arguments:
            scope: the scope of the import.
            id: the ID of the imported Secret in the construct tree.
            attrs: the attributes of the imported secret.
            secretArn: The ARN of the secret in SecretsManager.
            encryptionKey: The encryption key that is used to encrypt the secret, unless the default SecretsManager key is used.
        """
        attrs: SecretAttributes = {"secretArn": secret_arn}

        if encryption_key is not None:
            attrs["encryptionKey"] = encryption_key

        return jsii.sinvoke(cls, "fromSecretAttributes", [scope, id, attrs])

    @jsii.member(jsii_name="addRotationSchedule")
    def add_rotation_schedule(self, id: str, *, rotation_lambda: aws_cdk.aws_lambda.IFunction, automatically_after_days: typing.Optional[jsii.Number]=None) -> "RotationSchedule":
        """Adds a rotation schedule to the secret.

        Arguments:
            id: -
            options: -
            rotationLambda: THe Lambda function that can rotate the secret.
            automaticallyAfterDays: Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation. Default: 30
        """
        options: RotationScheduleOptions = {"rotationLambda": rotation_lambda}

        if automatically_after_days is not None:
            options["automaticallyAfterDays"] = automatically_after_days

        return jsii.invoke(self, "addRotationSchedule", [id, options])

    @jsii.member(jsii_name="addTargetAttachment")
    def add_target_attachment(self, id: str, *, target: "ISecretAttachmentTarget") -> "SecretTargetAttachment":
        """Adds a target attachment to the secret.

        Arguments:
            id: -
            options: -
            target: The target to attach the secret to.

        Returns:
            an AttachedSecret
        """
        options: AttachedSecretOptions = {"target": target}

        return jsii.invoke(self, "addTargetAttachment", [id, options])

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, grantee: aws_cdk.aws_iam.IGrantable, version_stages: typing.Optional[typing.List[str]]=None) -> aws_cdk.aws_iam.Grant:
        """Grants reading the secret value to some role.

        Arguments:
            grantee: -
            versionStages: -
        """
        return jsii.invoke(self, "grantRead", [grantee, version_stages])

    @jsii.member(jsii_name="secretJsonValue")
    def secret_json_value(self, json_field: str) -> aws_cdk.cdk.SecretValue:
        """Interpret the secret as a JSON object and return a field's value from it as a ``SecretValue``.

        Arguments:
            jsonField: -
        """
        return jsii.invoke(self, "secretJsonValue", [json_field])

    @property
    @jsii.member(jsii_name="secretArn")
    def secret_arn(self) -> str:
        """The ARN of the secret in AWS Secrets Manager."""
        return jsii.get(self, "secretArn")

    @property
    @jsii.member(jsii_name="secretValue")
    def secret_value(self) -> aws_cdk.cdk.SecretValue:
        """Retrieve the value of the stored secret as a ``SecretValue``."""
        return jsii.get(self, "secretValue")

    @property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        """The customer-managed encryption key that is used to encrypt this secret, if any.

        When not specified, the default
        KMS key for the account and region is being used.
        """
        return jsii.get(self, "encryptionKey")


@jsii.data_type(jsii_type="@aws-cdk/aws-secretsmanager.SecretAttachmentTargetProps", jsii_struct_bases=[])
class SecretAttachmentTargetProps(jsii.compat.TypedDict):
    """Attachment target specifications."""
    targetId: str
    """The id of the target to attach the secret to."""

    targetType: "AttachmentTargetType"
    """The type of the target to attach the secret to."""

@jsii.data_type_optionals(jsii_struct_bases=[])
class _SecretAttributes(jsii.compat.TypedDict, total=False):
    encryptionKey: aws_cdk.aws_kms.IKey
    """The encryption key that is used to encrypt the secret, unless the default SecretsManager key is used."""

@jsii.data_type(jsii_type="@aws-cdk/aws-secretsmanager.SecretAttributes", jsii_struct_bases=[_SecretAttributes])
class SecretAttributes(_SecretAttributes):
    """Attributes required to import an existing secret into the Stack."""
    secretArn: str
    """The ARN of the secret in SecretsManager."""

@jsii.data_type(jsii_type="@aws-cdk/aws-secretsmanager.SecretProps", jsii_struct_bases=[])
class SecretProps(jsii.compat.TypedDict, total=False):
    """The properties required to create a new secret in AWS Secrets Manager."""
    description: str
    """An optional, human-friendly description of the secret.

    Default:
        - No description.
    """

    encryptionKey: aws_cdk.aws_kms.IKey
    """The customer-managed encryption key to use for encrypting the secret value.

    Default:
        - A default KMS key for the account and region is used.
    """

    generateSecretString: "SecretStringGenerator"
    """Configuration for how to generate a secret value.

    Default:
        - 32 characters with upper-case letters, lower-case letters, punctuation and numbers (at least one from each
          category), per the default values of ``SecretStringGenerator``.
    """

    name: str
    """A name for the secret.

    Note that deleting secrets from SecretsManager does not happen immediately, but after a 7 to
    30 days blackout period. During that period, it is not possible to create another secret that shares the same name.

    Default:
        - A name is generated by CloudFormation.
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-secretsmanager.SecretStringGenerator", jsii_struct_bases=[])
class SecretStringGenerator(jsii.compat.TypedDict, total=False):
    """Configuration to generate secrets such as passwords automatically."""
    excludeCharacters: str
    """A string that includes characters that shouldn't be included in the generated password.

    The string can be a minimum
    of ``0`` and a maximum of ``4096`` characters long.

    Default:
        no exclusions
    """

    excludeLowercase: bool
    """Specifies that the generated password shouldn't include lowercase letters.

    Default:
        false
    """

    excludeNumbers: bool
    """Specifies that the generated password shouldn't include digits.

    Default:
        false
    """

    excludePunctuation: bool
    """Specifies that the generated password shouldn't include punctuation characters.

    Default:
        false
    """

    excludeUppercase: bool
    """Specifies that the generated password shouldn't include uppercase letters.

    Default:
        false
    """

    generateStringKey: str
    """The JSON key name that's used to add the generated password to the JSON structure specified by the ``secretStringTemplate`` parameter.

    If you specify ``generateStringKey`` then ``secretStringTemplate``
    must be also be specified.
    """

    includeSpace: bool
    """Specifies that the generated password can include the space character.

    Default:
        false
    """

    passwordLength: jsii.Number
    """The desired length of the generated password.

    Default:
        32
    """

    requireEachIncludedType: bool
    """Specifies whether the generated password must include at least one of every allowed character type.

    Default:
        true
    """

    secretStringTemplate: str
    """A properly structured JSON string that the generated password can be added to.

    The ``generateStringKey`` is
    combined with the generated random string and inserted into the JSON structure that's specified by this parameter.
    The merged JSON string is returned as the completed SecretString of the secret. If you specify ``secretStringTemplate``
    then ``generateStringKey`` must be also be specified.
    """

@jsii.implements(ISecretTargetAttachment, ISecret)
class SecretTargetAttachment(aws_cdk.cdk.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-secretsmanager.SecretTargetAttachment"):
    """An attached secret."""
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, secret: "ISecret", target: "ISecretAttachmentTarget") -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            secret: The secret to attach to the target.
            target: The target to attach the secret to.
        """
        props: SecretTargetAttachmentProps = {"secret": secret, "target": target}

        jsii.create(SecretTargetAttachment, self, [scope, id, props])

    @jsii.member(jsii_name="fromSecretTargetAttachmentSecretArn")
    @classmethod
    def from_secret_target_attachment_secret_arn(cls, scope: aws_cdk.cdk.Construct, id: str, secret_target_attachment_secret_arn: str) -> "ISecretTargetAttachment":
        """
        Arguments:
            scope: -
            id: -
            secretTargetAttachmentSecretArn: -
        """
        return jsii.sinvoke(cls, "fromSecretTargetAttachmentSecretArn", [scope, id, secret_target_attachment_secret_arn])

    @jsii.member(jsii_name="addRotationSchedule")
    def add_rotation_schedule(self, id: str, *, rotation_lambda: aws_cdk.aws_lambda.IFunction, automatically_after_days: typing.Optional[jsii.Number]=None) -> "RotationSchedule":
        """Adds a rotation schedule to the secret.

        Arguments:
            id: -
            options: -
            rotationLambda: THe Lambda function that can rotate the secret.
            automaticallyAfterDays: Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation. Default: 30
        """
        options: RotationScheduleOptions = {"rotationLambda": rotation_lambda}

        if automatically_after_days is not None:
            options["automaticallyAfterDays"] = automatically_after_days

        return jsii.invoke(self, "addRotationSchedule", [id, options])

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, grantee: aws_cdk.aws_iam.IGrantable, version_stages: typing.Optional[typing.List[str]]=None) -> aws_cdk.aws_iam.Grant:
        """Grants reading the secret value to some role.

        Arguments:
            grantee: -
            versionStages: -
        """
        return jsii.invoke(self, "grantRead", [grantee, version_stages])

    @jsii.member(jsii_name="secretJsonValue")
    def secret_json_value(self, json_field: str) -> aws_cdk.cdk.SecretValue:
        """Interpret the secret as a JSON object and return a field's value from it as a ``SecretValue``.

        Arguments:
            jsonField: -
        """
        return jsii.invoke(self, "secretJsonValue", [json_field])

    @property
    @jsii.member(jsii_name="secretArn")
    def secret_arn(self) -> str:
        """The ARN of the secret in AWS Secrets Manager."""
        return jsii.get(self, "secretArn")

    @property
    @jsii.member(jsii_name="secretTargetAttachmentSecretArn")
    def secret_target_attachment_secret_arn(self) -> str:
        """Same as ``secretArn``.

        attribute:
            true
        """
        return jsii.get(self, "secretTargetAttachmentSecretArn")

    @property
    @jsii.member(jsii_name="secretValue")
    def secret_value(self) -> aws_cdk.cdk.SecretValue:
        """Retrieve the value of the stored secret as a ``SecretValue``."""
        return jsii.get(self, "secretValue")

    @property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        """The customer-managed encryption key that is used to encrypt this secret, if any.

        When not specified, the default
        KMS key for the account and region is being used.
        """
        return jsii.get(self, "encryptionKey")


@jsii.data_type(jsii_type="@aws-cdk/aws-secretsmanager.SecretTargetAttachmentProps", jsii_struct_bases=[AttachedSecretOptions])
class SecretTargetAttachmentProps(AttachedSecretOptions, jsii.compat.TypedDict):
    """Construction properties for an AttachedSecret."""
    secret: "ISecret"
    """The secret to attach to the target."""

__all__ = ["AttachedSecretOptions", "AttachmentTargetType", "CfnResourcePolicy", "CfnResourcePolicyProps", "CfnRotationSchedule", "CfnRotationScheduleProps", "CfnSecret", "CfnSecretProps", "CfnSecretTargetAttachment", "CfnSecretTargetAttachmentProps", "ISecret", "ISecretAttachmentTarget", "ISecretTargetAttachment", "RotationSchedule", "RotationScheduleOptions", "RotationScheduleProps", "Secret", "SecretAttachmentTargetProps", "SecretAttributes", "SecretProps", "SecretStringGenerator", "SecretTargetAttachment", "SecretTargetAttachmentProps", "__jsii_assembly__"]

publication.publish()
