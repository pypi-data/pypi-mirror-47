# coding: utf-8

"""
    Marketing API v.1.0

    IMPORTANT: This swagger links to Criteo production environment. Any test applied here will thus impact real campaigns.  # noqa: E501

    OpenAPI spec version: v.1.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from criteo_marketing.api_client import ApiClient


class CategoriesApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def get_categories(self, authorization, **kwargs):  # noqa: E501
        """Gets categories  # noqa: E501

        Get the list of categories with the specified filters.  If a category is requested but is missing from current user's portfolio, it will not be included in the list.  If neither campaign ids nor advertisers ids are provided, then the user's portfolio will be used.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_categories(authorization, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str authorization: JWT Bearer Token (required)
        :param str campaign_ids: Optional. One or more campaign ids, E.g., 78, 12932, 45236. If the campaign ids requested are not liked to advertisers in the user's portfolio, they will be skipped.
        :param str advertiser_ids: Optional. One or more advertiser ids, E.g., 78, 12932, 45236. If the advertiser ids requested are not part of the user's portfolio, they will be skipped.
        :param str category_hash_codes: Optional. One or more category hash codes.
        :param bool enabled_only: Optional. Returns only categories you can bid on. Defaults to false.
        :return: list[CategoryMessage]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_categories_with_http_info(authorization, **kwargs)  # noqa: E501
        else:
            (data) = self.get_categories_with_http_info(authorization, **kwargs)  # noqa: E501
            return data

    def get_categories_with_http_info(self, authorization, **kwargs):  # noqa: E501
        """Gets categories  # noqa: E501

        Get the list of categories with the specified filters.  If a category is requested but is missing from current user's portfolio, it will not be included in the list.  If neither campaign ids nor advertisers ids are provided, then the user's portfolio will be used.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_categories_with_http_info(authorization, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str authorization: JWT Bearer Token (required)
        :param str campaign_ids: Optional. One or more campaign ids, E.g., 78, 12932, 45236. If the campaign ids requested are not liked to advertisers in the user's portfolio, they will be skipped.
        :param str advertiser_ids: Optional. One or more advertiser ids, E.g., 78, 12932, 45236. If the advertiser ids requested are not part of the user's portfolio, they will be skipped.
        :param str category_hash_codes: Optional. One or more category hash codes.
        :param bool enabled_only: Optional. Returns only categories you can bid on. Defaults to false.
        :return: list[CategoryMessage]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['authorization', 'campaign_ids', 'advertiser_ids', 'category_hash_codes', 'enabled_only']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_categories" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'authorization' is set
        if ('authorization' not in local_var_params or
                local_var_params['authorization'] is None):
            raise ValueError("Missing the required parameter `authorization` when calling `get_categories`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'campaign_ids' in local_var_params:
            query_params.append(('campaignIds', local_var_params['campaign_ids']))  # noqa: E501
        if 'advertiser_ids' in local_var_params:
            query_params.append(('advertiserIds', local_var_params['advertiser_ids']))  # noqa: E501
        if 'category_hash_codes' in local_var_params:
            query_params.append(('categoryHashCodes', local_var_params['category_hash_codes']))  # noqa: E501
        if 'enabled_only' in local_var_params:
            query_params.append(('enabledOnly', local_var_params['enabled_only']))  # noqa: E501

        header_params = {}
        if 'authorization' in local_var_params:
            header_params['Authorization'] = local_var_params['authorization']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'text/json', 'application/xml', 'text/xml', 'text/html'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Authorization']  # noqa: E501

        return self.api_client.call_api(
            '/v1/categories', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[CategoryMessage]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def update_categories(self, authorization, category_updates_per_catalog, **kwargs):  # noqa: E501
        """Enables/disables categories  # noqa: E501

        Update categories for multiple catalogs.<br />  Please note that all validations need to pass before applying the requested changes;  the subsequent validation error messages will be returned in the response.<br />  Please note that bidding will still happen for disabled categories, but using the Camapign's bid.  If the call is successful, full details about the changed categories will be returned.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_categories(authorization, category_updates_per_catalog, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str authorization: JWT Bearer Token (required)
        :param list[CategoryUpdatesPerCatalog] category_updates_per_catalog: The list of categories to be enabled/disabled, grouped by catalog. (required)
        :return: list[CategoryUpdatesPerCatalog]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.update_categories_with_http_info(authorization, category_updates_per_catalog, **kwargs)  # noqa: E501
        else:
            (data) = self.update_categories_with_http_info(authorization, category_updates_per_catalog, **kwargs)  # noqa: E501
            return data

    def update_categories_with_http_info(self, authorization, category_updates_per_catalog, **kwargs):  # noqa: E501
        """Enables/disables categories  # noqa: E501

        Update categories for multiple catalogs.<br />  Please note that all validations need to pass before applying the requested changes;  the subsequent validation error messages will be returned in the response.<br />  Please note that bidding will still happen for disabled categories, but using the Camapign's bid.  If the call is successful, full details about the changed categories will be returned.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_categories_with_http_info(authorization, category_updates_per_catalog, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str authorization: JWT Bearer Token (required)
        :param list[CategoryUpdatesPerCatalog] category_updates_per_catalog: The list of categories to be enabled/disabled, grouped by catalog. (required)
        :return: list[CategoryUpdatesPerCatalog]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['authorization', 'category_updates_per_catalog']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update_categories" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'authorization' is set
        if ('authorization' not in local_var_params or
                local_var_params['authorization'] is None):
            raise ValueError("Missing the required parameter `authorization` when calling `update_categories`")  # noqa: E501
        # verify the required parameter 'category_updates_per_catalog' is set
        if ('category_updates_per_catalog' not in local_var_params or
                local_var_params['category_updates_per_catalog'] is None):
            raise ValueError("Missing the required parameter `category_updates_per_catalog` when calling `update_categories`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}
        if 'authorization' in local_var_params:
            header_params['Authorization'] = local_var_params['authorization']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        if 'category_updates_per_catalog' in local_var_params:
            body_params = local_var_params['category_updates_per_catalog']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'text/json', 'application/xml', 'text/xml', 'text/html'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'text/json', 'application/xml', 'text/xml', 'application/x-www-form-urlencoded', 'text/html'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Authorization']  # noqa: E501

        return self.api_client.call_api(
            '/v1/categories', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[CategoryUpdatesPerCatalog]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)
