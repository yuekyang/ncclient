# Copyright 2009 Shikhar Bhushan
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from ncclient.operations.rpc import RPC

from ncclient.xml_ import *

from ncclient.operations import util

class CreateSubscription(RPC):
    "`create-subscription` RPC. Depends on the `:notification` capability."

    DEPENDS = [':notification']

    def request(self, filter=None, stream_name=None, start_time=None, stop_time=None):
        """Creates a subscription for notifications from the server.

        *filter* specifies the subset of notifications to receive (by
        default all notificaitons are received)

        :seealso: :ref:`filter_params`

        *stream_name* specifies the notification stream name. The
        default is None meaning all streams.

        *start_time* triggers the notification replay feature to
        replay notifications from the given time. The default is None,
        meaning that this is not a replay subscription. The format is
        an RFC 3339/ISO 8601 date and time.

        *stop_time* indicates the end of the notifications of
        interest. This parameter must be used with *start_time*. The
        default is None, meaning that (if *start_time* is present) the
        notifications will continue until the subscription is
        terminated. The format is an RFC 3339/ISO 8601 date and time.

        """
        node = new_ele_ns("create-subscription", NETCONF_NOTIFICATION_NS)
        if filter is not None:
            node.append(util.build_filter(filter))
        if stream_name is not None:
            sub_ele(node, "stream").text = stream_name

        if start_time is not None:
            sub_ele(node, "startTime").text = start_time

        if stop_time is not None:
            if start_time is None:
                raise ValueError("You must provide start_time if you provide stop_time")
            sub_ele(node, "stopTime").text = stop_time

        return self._request(node)

class EstablishSubscription(RPC):
    "`establish-subscription` RPC. Depends on the `:notification` capability."

    DEPENDS = [':notification']

    def request(self, stream=None, encoding=None,
                filter=None, subtree_filter=None, xpath_filter=None,
                period=None, no_synch_on_start=False, dampening_period=None):
        """Creates a subscription for notifications from the server.

        *filter* specifies the subset of notifications to receive (by
        default all notificaitons are received)

        :seealso: :ref:`filter_params`

        *stream_name* specifies the notification stream name. The
        default is None meaning all streams.

        *start_time* triggers the notification replay feature to
        replay notifications from the given time. The default is None,
        meaning that this is not a replay subscription. The format is
        an RFC 3339/ISO 8601 date and time.

        *stop_time* indicates the end of the notifications of
        interest. This parameter must be used with *start_time*. The
        default is None, meaning that (if *start_time* is present) the
        notifications will continue until the subscription is
        terminated. The format is an RFC 3339/ISO 8601 date and time.

        """
        ns = {
            None: IETF_NOTIFICATION_NS,
            'yp': IETF_PUSH_NS,
            }
        node = new_ele_ns("establish-subscription", IETF_NOTIFICATION_NS,
                          nsmap=ns)

        if stream is not None:
            sub_ele_ns(node, "stream", IETF_NOTIFICATION_NS).text = stream

        if encoding is not None:
            sub_ele_ns(node, "encoding", IETF_NOTIFICATION_NS).text = encoding

        if filter is not None:
            # node.append(util.build_filter(filter))
            node.append(filter)

        if subtree_filter is not None:
            node.append(util.build_filter(subtree_filter))

        if xpath_filter is not None:
            sub_ele_ns(node, "xpath-filter", IETF_PUSH_NS).text = xpath_filter

        if period is not None:
            sub_ele_ns(node, "period", IETF_PUSH_NS).text = str(period)

        if no_synch_on_start:
            sub_ele_ns(node, "no-synch-on-start", IETF_PUSH_NS)

        if dampening_period is not None:
            sub_ele_ns(node, "dampening-period", IETF_PUSH_NS).text = str(dampening_period)

        return self._request(node)

class DeleteSubscription(RPC):
    "`delete-subscription` RPC. Depends on the `:notification` capability."

    DEPENDS = [':notification']

    def request(self, subscription_id):
        """Creates a subscription for notifications from the server.

        *filter* specifies the subset of notifications to receive (by
        default all notificaitons are received)

        :seealso: :ref:`filter_params`

        *stream_name* specifies the notification stream name. The
        default is None meaning all streams.

        *start_time* triggers the notification replay feature to
        replay notifications from the given time. The default is None,
        meaning that this is not a replay subscription. The format is
        an RFC 3339/ISO 8601 date and time.

        *stop_time* indicates the end of the notifications of
        interest. This parameter must be used with *start_time*. The
        default is None, meaning that (if *start_time* is present) the
        notifications will continue until the subscription is
        terminated. The format is an RFC 3339/ISO 8601 date and time.

        """
        node = new_ele_ns("delete-subscription", IETF_NOTIFICATION_NS,
                          nsmap={None: IETF_NOTIFICATION_NS})
        if subscription_id is not None:
            sub_ele_ns(node, "subscription-id", IETF_NOTIFICATION_NS).text = \
                subscription_id

        return self._request(node)
