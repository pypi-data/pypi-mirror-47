# coding: utf-8
# Copyright (c) 2016, 2019, Oracle and/or its affiliates. All rights reserved.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ProtectionRuleExclusion(object):
    """
    Allows specified types of requests to bypass the protection rule. If the requests matches any of the criteria in the `exclusions` field, the protection rule will not be executed. Rules can have more than one exclusion and exclusions are applied to requests disjunctively.
    """

    #: A constant which can be used with the target property of a ProtectionRuleExclusion.
    #: This constant has a value of "REQUEST_COOKIES"
    TARGET_REQUEST_COOKIES = "REQUEST_COOKIES"

    #: A constant which can be used with the target property of a ProtectionRuleExclusion.
    #: This constant has a value of "REQUEST_COOKIE_NAMES"
    TARGET_REQUEST_COOKIE_NAMES = "REQUEST_COOKIE_NAMES"

    #: A constant which can be used with the target property of a ProtectionRuleExclusion.
    #: This constant has a value of "ARGS"
    TARGET_ARGS = "ARGS"

    #: A constant which can be used with the target property of a ProtectionRuleExclusion.
    #: This constant has a value of "ARGS_NAMES"
    TARGET_ARGS_NAMES = "ARGS_NAMES"

    def __init__(self, **kwargs):
        """
        Initializes a new ProtectionRuleExclusion object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param target:
            The value to assign to the target property of this ProtectionRuleExclusion.
            Allowed values for this property are: "REQUEST_COOKIES", "REQUEST_COOKIE_NAMES", "ARGS", "ARGS_NAMES", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type target: str

        :param exclusions:
            The value to assign to the exclusions property of this ProtectionRuleExclusion.
        :type exclusions: list[str]

        """
        self.swagger_types = {
            'target': 'str',
            'exclusions': 'list[str]'
        }

        self.attribute_map = {
            'target': 'target',
            'exclusions': 'exclusions'
        }

        self._target = None
        self._exclusions = None

    @property
    def target(self):
        """
        Gets the target of this ProtectionRuleExclusion.
        The target of the exclusion.

        Allowed values for this property are: "REQUEST_COOKIES", "REQUEST_COOKIE_NAMES", "ARGS", "ARGS_NAMES", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The target of this ProtectionRuleExclusion.
        :rtype: str
        """
        return self._target

    @target.setter
    def target(self, target):
        """
        Sets the target of this ProtectionRuleExclusion.
        The target of the exclusion.


        :param target: The target of this ProtectionRuleExclusion.
        :type: str
        """
        allowed_values = ["REQUEST_COOKIES", "REQUEST_COOKIE_NAMES", "ARGS", "ARGS_NAMES"]
        if not value_allowed_none_or_none_sentinel(target, allowed_values):
            target = 'UNKNOWN_ENUM_VALUE'
        self._target = target

    @property
    def exclusions(self):
        """
        Gets the exclusions of this ProtectionRuleExclusion.

        :return: The exclusions of this ProtectionRuleExclusion.
        :rtype: list[str]
        """
        return self._exclusions

    @exclusions.setter
    def exclusions(self, exclusions):
        """
        Sets the exclusions of this ProtectionRuleExclusion.

        :param exclusions: The exclusions of this ProtectionRuleExclusion.
        :type: list[str]
        """
        self._exclusions = exclusions

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
