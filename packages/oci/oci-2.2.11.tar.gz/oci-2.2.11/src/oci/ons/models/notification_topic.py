# coding: utf-8
# Copyright (c) 2016, 2019, Oracle and/or its affiliates. All rights reserved.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class NotificationTopic(object):
    """
    The properties that define a topic.
    """

    #: A constant which can be used with the lifecycle_state property of a NotificationTopic.
    #: This constant has a value of "ACTIVE"
    LIFECYCLE_STATE_ACTIVE = "ACTIVE"

    #: A constant which can be used with the lifecycle_state property of a NotificationTopic.
    #: This constant has a value of "DELETING"
    LIFECYCLE_STATE_DELETING = "DELETING"

    #: A constant which can be used with the lifecycle_state property of a NotificationTopic.
    #: This constant has a value of "CREATING"
    LIFECYCLE_STATE_CREATING = "CREATING"

    def __init__(self, **kwargs):
        """
        Initializes a new NotificationTopic object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param name:
            The value to assign to the name property of this NotificationTopic.
        :type name: str

        :param topic_id:
            The value to assign to the topic_id property of this NotificationTopic.
        :type topic_id: str

        :param compartment_id:
            The value to assign to the compartment_id property of this NotificationTopic.
        :type compartment_id: str

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this NotificationTopic.
            Allowed values for this property are: "ACTIVE", "DELETING", "CREATING", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type lifecycle_state: str

        :param description:
            The value to assign to the description property of this NotificationTopic.
        :type description: str

        :param time_created:
            The value to assign to the time_created property of this NotificationTopic.
        :type time_created: datetime

        :param etag:
            The value to assign to the etag property of this NotificationTopic.
        :type etag: str

        :param freeform_tags:
            The value to assign to the freeform_tags property of this NotificationTopic.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this NotificationTopic.
        :type defined_tags: dict(str, dict(str, object))

        :param api_endpoint:
            The value to assign to the api_endpoint property of this NotificationTopic.
        :type api_endpoint: str

        """
        self.swagger_types = {
            'name': 'str',
            'topic_id': 'str',
            'compartment_id': 'str',
            'lifecycle_state': 'str',
            'description': 'str',
            'time_created': 'datetime',
            'etag': 'str',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))',
            'api_endpoint': 'str'
        }

        self.attribute_map = {
            'name': 'name',
            'topic_id': 'topicId',
            'compartment_id': 'compartmentId',
            'lifecycle_state': 'lifecycleState',
            'description': 'description',
            'time_created': 'timeCreated',
            'etag': 'etag',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags',
            'api_endpoint': 'apiEndpoint'
        }

        self._name = None
        self._topic_id = None
        self._compartment_id = None
        self._lifecycle_state = None
        self._description = None
        self._time_created = None
        self._etag = None
        self._freeform_tags = None
        self._defined_tags = None
        self._api_endpoint = None

    @property
    def name(self):
        """
        **[Required]** Gets the name of this NotificationTopic.
        The name of the topic. Avoid entering confidential information.


        :return: The name of this NotificationTopic.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this NotificationTopic.
        The name of the topic. Avoid entering confidential information.


        :param name: The name of this NotificationTopic.
        :type: str
        """
        self._name = name

    @property
    def topic_id(self):
        """
        **[Required]** Gets the topic_id of this NotificationTopic.
        The `OCID`__ of the topic.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :return: The topic_id of this NotificationTopic.
        :rtype: str
        """
        return self._topic_id

    @topic_id.setter
    def topic_id(self, topic_id):
        """
        Sets the topic_id of this NotificationTopic.
        The `OCID`__ of the topic.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :param topic_id: The topic_id of this NotificationTopic.
        :type: str
        """
        self._topic_id = topic_id

    @property
    def compartment_id(self):
        """
        **[Required]** Gets the compartment_id of this NotificationTopic.
        The `OCID`__ of the compartment for the topic.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :return: The compartment_id of this NotificationTopic.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this NotificationTopic.
        The `OCID`__ of the compartment for the topic.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :param compartment_id: The compartment_id of this NotificationTopic.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def lifecycle_state(self):
        """
        **[Required]** Gets the lifecycle_state of this NotificationTopic.
        The lifecycle state of the topic.

        Allowed values for this property are: "ACTIVE", "DELETING", "CREATING", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The lifecycle_state of this NotificationTopic.
        :rtype: str
        """
        return self._lifecycle_state

    @lifecycle_state.setter
    def lifecycle_state(self, lifecycle_state):
        """
        Sets the lifecycle_state of this NotificationTopic.
        The lifecycle state of the topic.


        :param lifecycle_state: The lifecycle_state of this NotificationTopic.
        :type: str
        """
        allowed_values = ["ACTIVE", "DELETING", "CREATING"]
        if not value_allowed_none_or_none_sentinel(lifecycle_state, allowed_values):
            lifecycle_state = 'UNKNOWN_ENUM_VALUE'
        self._lifecycle_state = lifecycle_state

    @property
    def description(self):
        """
        Gets the description of this NotificationTopic.
        The description of the topic. Avoid entering confidential information.


        :return: The description of this NotificationTopic.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this NotificationTopic.
        The description of the topic. Avoid entering confidential information.


        :param description: The description of this NotificationTopic.
        :type: str
        """
        self._description = description

    @property
    def time_created(self):
        """
        **[Required]** Gets the time_created of this NotificationTopic.
        The time the topic was created.


        :return: The time_created of this NotificationTopic.
        :rtype: datetime
        """
        return self._time_created

    @time_created.setter
    def time_created(self, time_created):
        """
        Sets the time_created of this NotificationTopic.
        The time the topic was created.


        :param time_created: The time_created of this NotificationTopic.
        :type: datetime
        """
        self._time_created = time_created

    @property
    def etag(self):
        """
        Gets the etag of this NotificationTopic.
        For optimistic concurrency control. See `if-match`.


        :return: The etag of this NotificationTopic.
        :rtype: str
        """
        return self._etag

    @etag.setter
    def etag(self, etag):
        """
        Sets the etag of this NotificationTopic.
        For optimistic concurrency control. See `if-match`.


        :param etag: The etag of this NotificationTopic.
        :type: str
        """
        self._etag = etag

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this NotificationTopic.
        Free-form tags for this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace. For more information, see `Resource Tags`__.

        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :return: The freeform_tags of this NotificationTopic.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this NotificationTopic.
        Free-form tags for this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace. For more information, see `Resource Tags`__.

        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :param freeform_tags: The freeform_tags of this NotificationTopic.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this NotificationTopic.
        Defined tags for this resource. Each key is predefined and scoped to a namespace. For more information, see `Resource Tags`__.

        Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :return: The defined_tags of this NotificationTopic.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this NotificationTopic.
        Defined tags for this resource. Each key is predefined and scoped to a namespace. For more information, see `Resource Tags`__.

        Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :param defined_tags: The defined_tags of this NotificationTopic.
        :type: dict(str, dict(str, object))
        """
        self._defined_tags = defined_tags

    @property
    def api_endpoint(self):
        """
        **[Required]** Gets the api_endpoint of this NotificationTopic.
        The endpoint for managing topic subscriptions or publishing messages to the topic.


        :return: The api_endpoint of this NotificationTopic.
        :rtype: str
        """
        return self._api_endpoint

    @api_endpoint.setter
    def api_endpoint(self, api_endpoint):
        """
        Sets the api_endpoint of this NotificationTopic.
        The endpoint for managing topic subscriptions or publishing messages to the topic.


        :param api_endpoint: The api_endpoint of this NotificationTopic.
        :type: str
        """
        self._api_endpoint = api_endpoint

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
