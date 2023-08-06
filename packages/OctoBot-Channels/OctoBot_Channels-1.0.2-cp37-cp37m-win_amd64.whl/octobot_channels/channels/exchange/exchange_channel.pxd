# cython: language_level=3
#  Drakkar-Software OctoBot-Channels
#  Copyright (c) Drakkar-Software, All rights reserved.
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3.0 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library.
from octobot_channels.channels.channel cimport Channel, Channels
from octobot_channels.consumer cimport Consumer

cdef class ExchangeChannel(Channel):
    cdef public object exchange_manager # TODO replace
    cdef public object exchange # TODO replace

    cdef int filter_send_counter
    cdef bint should_send_filter

    cpdef void will_send(self)
    cpdef void has_send(self)

    cpdef object get_consumers(self, str symbol)
    cpdef list get_consumers_by_timeframe(self, object time_frame, str symbol)
    cpdef void _add_new_consumer_and_run(self, Consumer consumer, str symbol =*, object time_frame =*)

cdef class ExchangeChannels(Channels):
    pass
