# coding: utf-8

"""
    Call Recorder API

    Call Recorder API   # noqa: E501

    OpenAPI spec version: 1.0.0
    
"""

import pprint
import re  # noqa: F401

import six


class DeleteMetaFilesRequest(object):
    """NOTE: 

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'api_key': 'str',
        'ids': 'list[int]',
        'parent_id': 'int'
    }

    attribute_map = {
        'api_key': 'api_key',
        'ids': 'ids',
        'parent_id': 'parent_id'
    }

    def __init__(self, api_key=None, ids=None, parent_id=None):  # noqa: E501
        """DeleteMetaFilesRequest - a model defined in spec"""  # noqa: E501
        self._api_key = None
        self._ids = None
        self._parent_id = None
        self.discriminator = None
        self.api_key = api_key
        if ids is not None:
            self.ids = ids
        if parent_id is not None:
            self.parent_id = parent_id

    @property
    def api_key(self):
        """Gets the api_key of this DeleteMetaFilesRequest.  # noqa: E501


        :return: The api_key of this DeleteMetaFilesRequest.  # noqa: E501
        :rtype: str
        """
        return self._api_key

    @api_key.setter
    def api_key(self, api_key):
        """Sets the api_key of this DeleteMetaFilesRequest.


        :param api_key: The api_key of this DeleteMetaFilesRequest.  # noqa: E501
        :type: str
        """
        if api_key is None:
            raise ValueError("Invalid value for `api_key`, must not be `None`")  # noqa: E501

        self._api_key = api_key

    @property
    def ids(self):
        """Gets the ids of this DeleteMetaFilesRequest.  # noqa: E501


        :return: The ids of this DeleteMetaFilesRequest.  # noqa: E501
        :rtype: list[int]
        """
        return self._ids

    @ids.setter
    def ids(self, ids):
        """Sets the ids of this DeleteMetaFilesRequest.


        :param ids: The ids of this DeleteMetaFilesRequest.  # noqa: E501
        :type: list[int]
        """

        self._ids = ids

    @property
    def parent_id(self):
        """Gets the parent_id of this DeleteMetaFilesRequest.  # noqa: E501


        :return: The parent_id of this DeleteMetaFilesRequest.  # noqa: E501
        :rtype: int
        """
        return self._parent_id

    @parent_id.setter
    def parent_id(self, parent_id):
        """Sets the parent_id of this DeleteMetaFilesRequest.


        :param parent_id: The parent_id of this DeleteMetaFilesRequest.  # noqa: E501
        :type: int
        """

        self._parent_id = parent_id

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(DeleteMetaFilesRequest, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, DeleteMetaFilesRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
