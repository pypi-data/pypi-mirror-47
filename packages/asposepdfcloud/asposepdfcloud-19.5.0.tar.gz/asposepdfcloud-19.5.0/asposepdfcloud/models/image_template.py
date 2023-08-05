# coding: utf-8

"""
    Aspose.PDF Cloud API Reference


   Copyright (c) 2019 Aspose.PDF Cloud
 Permission is hereby granted, free of charge, to any person obtaining a copy
 of this software and associated documentation files (the "Software"), to deal
 in the Software without restriction, including without limitation the rights
 to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:
 The above copyright notice and this permission notice shall be included in all
 copies or substantial portions of the Software.
 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 SOFTWARE.



    OpenAPI spec version: 2.0
    
"""


from pprint import pformat
from six import iteritems
import re


class ImageTemplate(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
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
        'image_path': 'str',
        'image_src_type': 'ImageSrcType',
        'left_margin': 'float',
        'right_margin': 'float',
        'top_margin': 'float',
        'bottom_margin': 'float',
        'page_width': 'float',
        'page_height': 'float',
        'margin_info': 'MarginInfo'
    }

    attribute_map = {
        'image_path': 'ImagePath',
        'image_src_type': 'ImageSrcType',
        'left_margin': 'LeftMargin',
        'right_margin': 'RightMargin',
        'top_margin': 'TopMargin',
        'bottom_margin': 'BottomMargin',
        'page_width': 'PageWidth',
        'page_height': 'PageHeight',
        'margin_info': 'MarginInfo'
    }

    def __init__(self, image_path=None, image_src_type=None, left_margin=None, right_margin=None, top_margin=None, bottom_margin=None, page_width=None, page_height=None, margin_info=None):
        """
        ImageTemplate - a model defined in Swagger
        """

        self._image_path = None
        self._image_src_type = None
        self._left_margin = None
        self._right_margin = None
        self._top_margin = None
        self._bottom_margin = None
        self._page_width = None
        self._page_height = None
        self._margin_info = None

        self.image_path = image_path
        self.image_src_type = image_src_type
        if left_margin is not None:
          self.left_margin = left_margin
        if right_margin is not None:
          self.right_margin = right_margin
        if top_margin is not None:
          self.top_margin = top_margin
        if bottom_margin is not None:
          self.bottom_margin = bottom_margin
        if page_width is not None:
          self.page_width = page_width
        if page_height is not None:
          self.page_height = page_height
        if margin_info is not None:
          self.margin_info = margin_info

    @property
    def image_path(self):
        """
        Gets the image_path of this ImageTemplate.
        A path for image.

        :return: The image_path of this ImageTemplate.
        :rtype: str
        """
        return self._image_path

    @image_path.setter
    def image_path(self, image_path):
        """
        Sets the image_path of this ImageTemplate.
        A path for image.

        :param image_path: The image_path of this ImageTemplate.
        :type: str
        """
        if image_path is None:
            raise ValueError("Invalid value for `image_path`, must not be `None`")

        self._image_path = image_path

    @property
    def image_src_type(self):
        """
        Gets the image_src_type of this ImageTemplate.
        Image type.

        :return: The image_src_type of this ImageTemplate.
        :rtype: ImageSrcType
        """
        return self._image_src_type

    @image_src_type.setter
    def image_src_type(self, image_src_type):
        """
        Sets the image_src_type of this ImageTemplate.
        Image type.

        :param image_src_type: The image_src_type of this ImageTemplate.
        :type: ImageSrcType
        """
        if image_src_type is None:
            raise ValueError("Invalid value for `image_src_type`, must not be `None`")

        self._image_src_type = image_src_type

    @property
    def left_margin(self):
        """
        Gets the left_margin of this ImageTemplate.

        :return: The left_margin of this ImageTemplate.
        :rtype: float
        """
        return self._left_margin

    @left_margin.setter
    def left_margin(self, left_margin):
        """
        Sets the left_margin of this ImageTemplate.

        :param left_margin: The left_margin of this ImageTemplate.
        :type: float
        """

        self._left_margin = left_margin

    @property
    def right_margin(self):
        """
        Gets the right_margin of this ImageTemplate.

        :return: The right_margin of this ImageTemplate.
        :rtype: float
        """
        return self._right_margin

    @right_margin.setter
    def right_margin(self, right_margin):
        """
        Sets the right_margin of this ImageTemplate.

        :param right_margin: The right_margin of this ImageTemplate.
        :type: float
        """

        self._right_margin = right_margin

    @property
    def top_margin(self):
        """
        Gets the top_margin of this ImageTemplate.

        :return: The top_margin of this ImageTemplate.
        :rtype: float
        """
        return self._top_margin

    @top_margin.setter
    def top_margin(self, top_margin):
        """
        Sets the top_margin of this ImageTemplate.

        :param top_margin: The top_margin of this ImageTemplate.
        :type: float
        """

        self._top_margin = top_margin

    @property
    def bottom_margin(self):
        """
        Gets the bottom_margin of this ImageTemplate.

        :return: The bottom_margin of this ImageTemplate.
        :rtype: float
        """
        return self._bottom_margin

    @bottom_margin.setter
    def bottom_margin(self, bottom_margin):
        """
        Sets the bottom_margin of this ImageTemplate.

        :param bottom_margin: The bottom_margin of this ImageTemplate.
        :type: float
        """

        self._bottom_margin = bottom_margin

    @property
    def page_width(self):
        """
        Gets the page_width of this ImageTemplate.

        :return: The page_width of this ImageTemplate.
        :rtype: float
        """
        return self._page_width

    @page_width.setter
    def page_width(self, page_width):
        """
        Sets the page_width of this ImageTemplate.

        :param page_width: The page_width of this ImageTemplate.
        :type: float
        """

        self._page_width = page_width

    @property
    def page_height(self):
        """
        Gets the page_height of this ImageTemplate.

        :return: The page_height of this ImageTemplate.
        :rtype: float
        """
        return self._page_height

    @page_height.setter
    def page_height(self, page_height):
        """
        Sets the page_height of this ImageTemplate.

        :param page_height: The page_height of this ImageTemplate.
        :type: float
        """

        self._page_height = page_height

    @property
    def margin_info(self):
        """
        Gets the margin_info of this ImageTemplate.

        :return: The margin_info of this ImageTemplate.
        :rtype: MarginInfo
        """
        return self._margin_info

    @margin_info.setter
    def margin_info(self, margin_info):
        """
        Sets the margin_info of this ImageTemplate.

        :param margin_info: The margin_info of this ImageTemplate.
        :type: MarginInfo
        """

        self._margin_info = margin_info

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in iteritems(self.swagger_types):
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

        return result

    def to_str(self):
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        if not isinstance(other, ImageTemplate):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
