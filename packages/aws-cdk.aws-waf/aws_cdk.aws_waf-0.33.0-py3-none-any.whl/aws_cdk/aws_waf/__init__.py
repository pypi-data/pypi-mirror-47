import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-waf", "0.33.0", __name__, "aws-waf@0.33.0.jsii.tgz")
class CfnByteMatchSet(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-waf.CfnByteMatchSet"):
    """A CloudFormation ``AWS::WAF::ByteMatchSet``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-bytematchset.html
    cloudformationResource:
        AWS::WAF::ByteMatchSet
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, name: str, byte_match_tuples: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional[typing.List[typing.Union["ByteMatchTupleProperty", aws_cdk.cdk.Token]]]]]=None) -> None:
        """Create a new ``AWS::WAF::ByteMatchSet``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            name: ``AWS::WAF::ByteMatchSet.Name``.
            byteMatchTuples: ``AWS::WAF::ByteMatchSet.ByteMatchTuples``.
        """
        props: CfnByteMatchSetProps = {"name": name}

        if byte_match_tuples is not None:
            props["byteMatchTuples"] = byte_match_tuples

        jsii.create(CfnByteMatchSet, self, [scope, id, props])

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
    @jsii.member(jsii_name="byteMatchSetId")
    def byte_match_set_id(self) -> str:
        return jsii.get(self, "byteMatchSetId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnByteMatchSetProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _ByteMatchTupleProperty(jsii.compat.TypedDict, total=False):
        targetString: str
        """``CfnByteMatchSet.ByteMatchTupleProperty.TargetString``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-bytematchset-bytematchtuples.html#cfn-waf-bytematchset-bytematchtuples-targetstring
        """
        targetStringBase64: str
        """``CfnByteMatchSet.ByteMatchTupleProperty.TargetStringBase64``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-bytematchset-bytematchtuples.html#cfn-waf-bytematchset-bytematchtuples-targetstringbase64
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-waf.CfnByteMatchSet.ByteMatchTupleProperty", jsii_struct_bases=[_ByteMatchTupleProperty])
    class ByteMatchTupleProperty(_ByteMatchTupleProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-bytematchset-bytematchtuples.html
        """
        fieldToMatch: typing.Union[aws_cdk.cdk.Token, "CfnByteMatchSet.FieldToMatchProperty"]
        """``CfnByteMatchSet.ByteMatchTupleProperty.FieldToMatch``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-bytematchset-bytematchtuples.html#cfn-waf-bytematchset-bytematchtuples-fieldtomatch
        """

        positionalConstraint: str
        """``CfnByteMatchSet.ByteMatchTupleProperty.PositionalConstraint``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-bytematchset-bytematchtuples.html#cfn-waf-bytematchset-bytematchtuples-positionalconstraint
        """

        textTransformation: str
        """``CfnByteMatchSet.ByteMatchTupleProperty.TextTransformation``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-bytematchset-bytematchtuples.html#cfn-waf-bytematchset-bytematchtuples-texttransformation
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _FieldToMatchProperty(jsii.compat.TypedDict, total=False):
        data: str
        """``CfnByteMatchSet.FieldToMatchProperty.Data``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-bytematchset-bytematchtuples-fieldtomatch.html#cfn-waf-bytematchset-bytematchtuples-fieldtomatch-data
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-waf.CfnByteMatchSet.FieldToMatchProperty", jsii_struct_bases=[_FieldToMatchProperty])
    class FieldToMatchProperty(_FieldToMatchProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-bytematchset-bytematchtuples-fieldtomatch.html
        """
        type: str
        """``CfnByteMatchSet.FieldToMatchProperty.Type``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-bytematchset-bytematchtuples-fieldtomatch.html#cfn-waf-bytematchset-bytematchtuples-fieldtomatch-type
        """


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnByteMatchSetProps(jsii.compat.TypedDict, total=False):
    byteMatchTuples: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union["CfnByteMatchSet.ByteMatchTupleProperty", aws_cdk.cdk.Token]]]
    """``AWS::WAF::ByteMatchSet.ByteMatchTuples``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-bytematchset.html#cfn-waf-bytematchset-bytematchtuples
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-waf.CfnByteMatchSetProps", jsii_struct_bases=[_CfnByteMatchSetProps])
class CfnByteMatchSetProps(_CfnByteMatchSetProps):
    """Properties for defining a ``AWS::WAF::ByteMatchSet``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-bytematchset.html
    """
    name: str
    """``AWS::WAF::ByteMatchSet.Name``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-bytematchset.html#cfn-waf-bytematchset-name
    """

class CfnIPSet(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-waf.CfnIPSet"):
    """A CloudFormation ``AWS::WAF::IPSet``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-ipset.html
    cloudformationResource:
        AWS::WAF::IPSet
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, name: str, ip_set_descriptors: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional[typing.List[typing.Union[aws_cdk.cdk.Token, "IPSetDescriptorProperty"]]]]]=None) -> None:
        """Create a new ``AWS::WAF::IPSet``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            name: ``AWS::WAF::IPSet.Name``.
            ipSetDescriptors: ``AWS::WAF::IPSet.IPSetDescriptors``.
        """
        props: CfnIPSetProps = {"name": name}

        if ip_set_descriptors is not None:
            props["ipSetDescriptors"] = ip_set_descriptors

        jsii.create(CfnIPSet, self, [scope, id, props])

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
    @jsii.member(jsii_name="ipSetId")
    def ip_set_id(self) -> str:
        return jsii.get(self, "ipSetId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnIPSetProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.interface(jsii_type="@aws-cdk/aws-waf.CfnIPSet.IPSetDescriptorProperty")
    class IPSetDescriptorProperty(jsii.compat.Protocol):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-ipset-ipsetdescriptors.html
        """
        @staticmethod
        def __jsii_proxy_class__():
            return _IPSetDescriptorPropertyProxy

        @property
        @jsii.member(jsii_name="type")
        def type(self) -> str:
            """``CfnIPSet.IPSetDescriptorProperty.Type``.

            See:
                http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-ipset-ipsetdescriptors.html#cfn-waf-ipset-ipsetdescriptors-type
            """
            ...

        @property
        @jsii.member(jsii_name="value")
        def value(self) -> str:
            """``CfnIPSet.IPSetDescriptorProperty.Value``.

            See:
                http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-ipset-ipsetdescriptors.html#cfn-waf-ipset-ipsetdescriptors-value
            """
            ...


    class _IPSetDescriptorPropertyProxy():
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-ipset-ipsetdescriptors.html
        """
        __jsii_type__ = "@aws-cdk/aws-waf.CfnIPSet.IPSetDescriptorProperty"
        @property
        @jsii.member(jsii_name="type")
        def type(self) -> str:
            """``CfnIPSet.IPSetDescriptorProperty.Type``.

            See:
                http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-ipset-ipsetdescriptors.html#cfn-waf-ipset-ipsetdescriptors-type
            """
            return jsii.get(self, "type")

        @property
        @jsii.member(jsii_name="value")
        def value(self) -> str:
            """``CfnIPSet.IPSetDescriptorProperty.Value``.

            See:
                http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-ipset-ipsetdescriptors.html#cfn-waf-ipset-ipsetdescriptors-value
            """
            return jsii.get(self, "value")



@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnIPSetProps(jsii.compat.TypedDict, total=False):
    ipSetDescriptors: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnIPSet.IPSetDescriptorProperty"]]]
    """``AWS::WAF::IPSet.IPSetDescriptors``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-ipset.html#cfn-waf-ipset-ipsetdescriptors
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-waf.CfnIPSetProps", jsii_struct_bases=[_CfnIPSetProps])
class CfnIPSetProps(_CfnIPSetProps):
    """Properties for defining a ``AWS::WAF::IPSet``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-ipset.html
    """
    name: str
    """``AWS::WAF::IPSet.Name``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-ipset.html#cfn-waf-ipset-name
    """

class CfnRule(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-waf.CfnRule"):
    """A CloudFormation ``AWS::WAF::Rule``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-rule.html
    cloudformationResource:
        AWS::WAF::Rule
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, metric_name: str, name: str, predicates: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional[typing.List[typing.Union[aws_cdk.cdk.Token, "PredicateProperty"]]]]]=None) -> None:
        """Create a new ``AWS::WAF::Rule``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            metricName: ``AWS::WAF::Rule.MetricName``.
            name: ``AWS::WAF::Rule.Name``.
            predicates: ``AWS::WAF::Rule.Predicates``.
        """
        props: CfnRuleProps = {"metricName": metric_name, "name": name}

        if predicates is not None:
            props["predicates"] = predicates

        jsii.create(CfnRule, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnRuleProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="ruleId")
    def rule_id(self) -> str:
        return jsii.get(self, "ruleId")

    @jsii.data_type(jsii_type="@aws-cdk/aws-waf.CfnRule.PredicateProperty", jsii_struct_bases=[])
    class PredicateProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-rule-predicates.html
        """
        dataId: str
        """``CfnRule.PredicateProperty.DataId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-rule-predicates.html#cfn-waf-rule-predicates-dataid
        """

        negated: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnRule.PredicateProperty.Negated``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-rule-predicates.html#cfn-waf-rule-predicates-negated
        """

        type: str
        """``CfnRule.PredicateProperty.Type``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-rule-predicates.html#cfn-waf-rule-predicates-type
        """


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnRuleProps(jsii.compat.TypedDict, total=False):
    predicates: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnRule.PredicateProperty"]]]
    """``AWS::WAF::Rule.Predicates``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-rule.html#cfn-waf-rule-predicates
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-waf.CfnRuleProps", jsii_struct_bases=[_CfnRuleProps])
class CfnRuleProps(_CfnRuleProps):
    """Properties for defining a ``AWS::WAF::Rule``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-rule.html
    """
    metricName: str
    """``AWS::WAF::Rule.MetricName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-rule.html#cfn-waf-rule-metricname
    """

    name: str
    """``AWS::WAF::Rule.Name``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-rule.html#cfn-waf-rule-name
    """

class CfnSizeConstraintSet(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-waf.CfnSizeConstraintSet"):
    """A CloudFormation ``AWS::WAF::SizeConstraintSet``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-sizeconstraintset.html
    cloudformationResource:
        AWS::WAF::SizeConstraintSet
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, name: str, size_constraints: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "SizeConstraintProperty"]]]) -> None:
        """Create a new ``AWS::WAF::SizeConstraintSet``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            name: ``AWS::WAF::SizeConstraintSet.Name``.
            sizeConstraints: ``AWS::WAF::SizeConstraintSet.SizeConstraints``.
        """
        props: CfnSizeConstraintSetProps = {"name": name, "sizeConstraints": size_constraints}

        jsii.create(CfnSizeConstraintSet, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnSizeConstraintSetProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="sizeConstraintSetId")
    def size_constraint_set_id(self) -> str:
        return jsii.get(self, "sizeConstraintSetId")

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _FieldToMatchProperty(jsii.compat.TypedDict, total=False):
        data: str
        """``CfnSizeConstraintSet.FieldToMatchProperty.Data``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-sizeconstraintset-sizeconstraint-fieldtomatch.html#cfn-waf-sizeconstraintset-sizeconstraint-fieldtomatch-data
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-waf.CfnSizeConstraintSet.FieldToMatchProperty", jsii_struct_bases=[_FieldToMatchProperty])
    class FieldToMatchProperty(_FieldToMatchProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-sizeconstraintset-sizeconstraint-fieldtomatch.html
        """
        type: str
        """``CfnSizeConstraintSet.FieldToMatchProperty.Type``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-sizeconstraintset-sizeconstraint-fieldtomatch.html#cfn-waf-sizeconstraintset-sizeconstraint-fieldtomatch-type
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-waf.CfnSizeConstraintSet.SizeConstraintProperty", jsii_struct_bases=[])
    class SizeConstraintProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-sizeconstraintset-sizeconstraint.html
        """
        comparisonOperator: str
        """``CfnSizeConstraintSet.SizeConstraintProperty.ComparisonOperator``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-sizeconstraintset-sizeconstraint.html#cfn-waf-sizeconstraintset-sizeconstraint-comparisonoperator
        """

        fieldToMatch: typing.Union[aws_cdk.cdk.Token, "CfnSizeConstraintSet.FieldToMatchProperty"]
        """``CfnSizeConstraintSet.SizeConstraintProperty.FieldToMatch``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-sizeconstraintset-sizeconstraint.html#cfn-waf-sizeconstraintset-sizeconstraint-fieldtomatch
        """

        size: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnSizeConstraintSet.SizeConstraintProperty.Size``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-sizeconstraintset-sizeconstraint.html#cfn-waf-sizeconstraintset-sizeconstraint-size
        """

        textTransformation: str
        """``CfnSizeConstraintSet.SizeConstraintProperty.TextTransformation``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-sizeconstraintset-sizeconstraint.html#cfn-waf-sizeconstraintset-sizeconstraint-texttransformation
        """


@jsii.data_type(jsii_type="@aws-cdk/aws-waf.CfnSizeConstraintSetProps", jsii_struct_bases=[])
class CfnSizeConstraintSetProps(jsii.compat.TypedDict):
    """Properties for defining a ``AWS::WAF::SizeConstraintSet``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-sizeconstraintset.html
    """
    name: str
    """``AWS::WAF::SizeConstraintSet.Name``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-sizeconstraintset.html#cfn-waf-sizeconstraintset-name
    """

    sizeConstraints: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnSizeConstraintSet.SizeConstraintProperty"]]]
    """``AWS::WAF::SizeConstraintSet.SizeConstraints``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-sizeconstraintset.html#cfn-waf-sizeconstraintset-sizeconstraints
    """

class CfnSqlInjectionMatchSet(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-waf.CfnSqlInjectionMatchSet"):
    """A CloudFormation ``AWS::WAF::SqlInjectionMatchSet``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-sqlinjectionmatchset.html
    cloudformationResource:
        AWS::WAF::SqlInjectionMatchSet
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, name: str, sql_injection_match_tuples: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional[typing.List[typing.Union[aws_cdk.cdk.Token, "SqlInjectionMatchTupleProperty"]]]]]=None) -> None:
        """Create a new ``AWS::WAF::SqlInjectionMatchSet``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            name: ``AWS::WAF::SqlInjectionMatchSet.Name``.
            sqlInjectionMatchTuples: ``AWS::WAF::SqlInjectionMatchSet.SqlInjectionMatchTuples``.
        """
        props: CfnSqlInjectionMatchSetProps = {"name": name}

        if sql_injection_match_tuples is not None:
            props["sqlInjectionMatchTuples"] = sql_injection_match_tuples

        jsii.create(CfnSqlInjectionMatchSet, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnSqlInjectionMatchSetProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="sqlInjectionMatchSetId")
    def sql_injection_match_set_id(self) -> str:
        return jsii.get(self, "sqlInjectionMatchSetId")

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _FieldToMatchProperty(jsii.compat.TypedDict, total=False):
        data: str
        """``CfnSqlInjectionMatchSet.FieldToMatchProperty.Data``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-bytematchset-bytematchtuples-fieldtomatch.html#cfn-waf-sizeconstraintset-sizeconstraint-fieldtomatch-data
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-waf.CfnSqlInjectionMatchSet.FieldToMatchProperty", jsii_struct_bases=[_FieldToMatchProperty])
    class FieldToMatchProperty(_FieldToMatchProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-bytematchset-bytematchtuples-fieldtomatch.html
        """
        type: str
        """``CfnSqlInjectionMatchSet.FieldToMatchProperty.Type``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-bytematchset-bytematchtuples-fieldtomatch.html#cfn-waf-sizeconstraintset-sizeconstraint-fieldtomatch-type
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-waf.CfnSqlInjectionMatchSet.SqlInjectionMatchTupleProperty", jsii_struct_bases=[])
    class SqlInjectionMatchTupleProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-sqlinjectionmatchset-sqlinjectionmatchtuples.html
        """
        fieldToMatch: typing.Union[aws_cdk.cdk.Token, "CfnSqlInjectionMatchSet.FieldToMatchProperty"]
        """``CfnSqlInjectionMatchSet.SqlInjectionMatchTupleProperty.FieldToMatch``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-sqlinjectionmatchset-sqlinjectionmatchtuples.html#cfn-waf-sqlinjectionmatchset-sqlinjectionmatchtuples-fieldtomatch
        """

        textTransformation: str
        """``CfnSqlInjectionMatchSet.SqlInjectionMatchTupleProperty.TextTransformation``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-sqlinjectionmatchset-sqlinjectionmatchtuples.html#cfn-waf-sqlinjectionmatchset-sqlinjectionmatchtuples-texttransformation
        """


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnSqlInjectionMatchSetProps(jsii.compat.TypedDict, total=False):
    sqlInjectionMatchTuples: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnSqlInjectionMatchSet.SqlInjectionMatchTupleProperty"]]]
    """``AWS::WAF::SqlInjectionMatchSet.SqlInjectionMatchTuples``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-sqlinjectionmatchset.html#cfn-waf-sqlinjectionmatchset-sqlinjectionmatchtuples
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-waf.CfnSqlInjectionMatchSetProps", jsii_struct_bases=[_CfnSqlInjectionMatchSetProps])
class CfnSqlInjectionMatchSetProps(_CfnSqlInjectionMatchSetProps):
    """Properties for defining a ``AWS::WAF::SqlInjectionMatchSet``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-sqlinjectionmatchset.html
    """
    name: str
    """``AWS::WAF::SqlInjectionMatchSet.Name``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-sqlinjectionmatchset.html#cfn-waf-sqlinjectionmatchset-name
    """

class CfnWebACL(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-waf.CfnWebACL"):
    """A CloudFormation ``AWS::WAF::WebACL``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-webacl.html
    cloudformationResource:
        AWS::WAF::WebACL
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, default_action: typing.Union[aws_cdk.cdk.Token, "WafActionProperty"], metric_name: str, name: str, rules: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional[typing.List[typing.Union[aws_cdk.cdk.Token, "ActivatedRuleProperty"]]]]]=None) -> None:
        """Create a new ``AWS::WAF::WebACL``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            defaultAction: ``AWS::WAF::WebACL.DefaultAction``.
            metricName: ``AWS::WAF::WebACL.MetricName``.
            name: ``AWS::WAF::WebACL.Name``.
            rules: ``AWS::WAF::WebACL.Rules``.
        """
        props: CfnWebACLProps = {"defaultAction": default_action, "metricName": metric_name, "name": name}

        if rules is not None:
            props["rules"] = rules

        jsii.create(CfnWebACL, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnWebACLProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="webAclId")
    def web_acl_id(self) -> str:
        return jsii.get(self, "webAclId")

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _ActivatedRuleProperty(jsii.compat.TypedDict, total=False):
        action: typing.Union[aws_cdk.cdk.Token, "CfnWebACL.WafActionProperty"]
        """``CfnWebACL.ActivatedRuleProperty.Action``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-webacl-rules.html#cfn-waf-webacl-rules-action
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-waf.CfnWebACL.ActivatedRuleProperty", jsii_struct_bases=[_ActivatedRuleProperty])
    class ActivatedRuleProperty(_ActivatedRuleProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-webacl-rules.html
        """
        priority: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnWebACL.ActivatedRuleProperty.Priority``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-webacl-rules.html#cfn-waf-webacl-rules-priority
        """

        ruleId: str
        """``CfnWebACL.ActivatedRuleProperty.RuleId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-webacl-rules.html#cfn-waf-webacl-rules-ruleid
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-waf.CfnWebACL.WafActionProperty", jsii_struct_bases=[])
    class WafActionProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-webacl-action.html
        """
        type: str
        """``CfnWebACL.WafActionProperty.Type``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-webacl-action.html#cfn-waf-webacl-action-type
        """


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnWebACLProps(jsii.compat.TypedDict, total=False):
    rules: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnWebACL.ActivatedRuleProperty"]]]
    """``AWS::WAF::WebACL.Rules``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-webacl.html#cfn-waf-webacl-rules
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-waf.CfnWebACLProps", jsii_struct_bases=[_CfnWebACLProps])
class CfnWebACLProps(_CfnWebACLProps):
    """Properties for defining a ``AWS::WAF::WebACL``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-webacl.html
    """
    defaultAction: typing.Union[aws_cdk.cdk.Token, "CfnWebACL.WafActionProperty"]
    """``AWS::WAF::WebACL.DefaultAction``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-webacl.html#cfn-waf-webacl-defaultaction
    """

    metricName: str
    """``AWS::WAF::WebACL.MetricName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-webacl.html#cfn-waf-webacl-metricname
    """

    name: str
    """``AWS::WAF::WebACL.Name``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-webacl.html#cfn-waf-webacl-name
    """

class CfnXssMatchSet(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-waf.CfnXssMatchSet"):
    """A CloudFormation ``AWS::WAF::XssMatchSet``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-xssmatchset.html
    cloudformationResource:
        AWS::WAF::XssMatchSet
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, name: str, xss_match_tuples: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "XssMatchTupleProperty"]]]) -> None:
        """Create a new ``AWS::WAF::XssMatchSet``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            name: ``AWS::WAF::XssMatchSet.Name``.
            xssMatchTuples: ``AWS::WAF::XssMatchSet.XssMatchTuples``.
        """
        props: CfnXssMatchSetProps = {"name": name, "xssMatchTuples": xss_match_tuples}

        jsii.create(CfnXssMatchSet, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnXssMatchSetProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="xssMatchSetId")
    def xss_match_set_id(self) -> str:
        return jsii.get(self, "xssMatchSetId")

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _FieldToMatchProperty(jsii.compat.TypedDict, total=False):
        data: str
        """``CfnXssMatchSet.FieldToMatchProperty.Data``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-xssmatchset-xssmatchtuple-fieldtomatch.html#cfn-waf-xssmatchset-xssmatchtuple-fieldtomatch-data
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-waf.CfnXssMatchSet.FieldToMatchProperty", jsii_struct_bases=[_FieldToMatchProperty])
    class FieldToMatchProperty(_FieldToMatchProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-xssmatchset-xssmatchtuple-fieldtomatch.html
        """
        type: str
        """``CfnXssMatchSet.FieldToMatchProperty.Type``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-xssmatchset-xssmatchtuple-fieldtomatch.html#cfn-waf-xssmatchset-xssmatchtuple-fieldtomatch-type
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-waf.CfnXssMatchSet.XssMatchTupleProperty", jsii_struct_bases=[])
    class XssMatchTupleProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-xssmatchset-xssmatchtuple.html
        """
        fieldToMatch: typing.Union[aws_cdk.cdk.Token, "CfnXssMatchSet.FieldToMatchProperty"]
        """``CfnXssMatchSet.XssMatchTupleProperty.FieldToMatch``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-xssmatchset-xssmatchtuple.html#cfn-waf-xssmatchset-xssmatchtuple-fieldtomatch
        """

        textTransformation: str
        """``CfnXssMatchSet.XssMatchTupleProperty.TextTransformation``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-xssmatchset-xssmatchtuple.html#cfn-waf-xssmatchset-xssmatchtuple-texttransformation
        """


@jsii.data_type(jsii_type="@aws-cdk/aws-waf.CfnXssMatchSetProps", jsii_struct_bases=[])
class CfnXssMatchSetProps(jsii.compat.TypedDict):
    """Properties for defining a ``AWS::WAF::XssMatchSet``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-xssmatchset.html
    """
    name: str
    """``AWS::WAF::XssMatchSet.Name``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-xssmatchset.html#cfn-waf-xssmatchset-name
    """

    xssMatchTuples: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnXssMatchSet.XssMatchTupleProperty"]]]
    """``AWS::WAF::XssMatchSet.XssMatchTuples``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-xssmatchset.html#cfn-waf-xssmatchset-xssmatchtuples
    """

__all__ = ["CfnByteMatchSet", "CfnByteMatchSetProps", "CfnIPSet", "CfnIPSetProps", "CfnRule", "CfnRuleProps", "CfnSizeConstraintSet", "CfnSizeConstraintSetProps", "CfnSqlInjectionMatchSet", "CfnSqlInjectionMatchSetProps", "CfnWebACL", "CfnWebACLProps", "CfnXssMatchSet", "CfnXssMatchSetProps", "__jsii_assembly__"]

publication.publish()
