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
from asyncio import CancelledError

from octobot_channels import CHANNEL_WILDCARD, CONSUMER_CALLBACK_TYPE
from octobot_channels.channels.exchange.exchange_channel import ExchangeChannel
from octobot_channels.consumer import Consumer
from octobot_channels.producer import Producer


class TickerProducer(Producer):
    async def push(self, symbol, ticker):
        await self.perform(symbol, ticker)

    async def perform(self, symbol, ticker):
        try:
            if CHANNEL_WILDCARD in self.channel.consumers or symbol in self.channel.consumers:  # and price_ticker_is_initialized
                self.channel.exchange_manager.get_symbol_data(symbol).update_symbol_price_ticker(ticker)
                await self.send(symbol, ticker)
                await self.send(CHANNEL_WILDCARD, ticker)
        except CancelledError:
            self.logger.info("Update tasks cancelled.")
        except Exception as e:
            self.logger.error(f"exception when triggering update: {e}")
            self.logger.exception(e)

    async def send(self, symbol, ticker):
        for consumer in self.channel.get_consumers(symbol=symbol):
            await consumer.queue.put({
                "symbol": symbol,
                "ticker": ticker
            })


class TickerConsumer(Consumer):
    async def consume(self):
        while not self.should_stop:
            try:
                data = await self.queue.get()
                await self.callback(symbol=data["symbol"], ticker=data["ticker"])
            except Exception as e:
                self.logger.exception(f"Exception when calling callback : {e}")


class TickerChannel(ExchangeChannel):
    def new_consumer(self, callback: CONSUMER_CALLBACK_TYPE, size:int = 0, symbol:str = CHANNEL_WILDCARD):
        self._add_new_consumer_and_run(TickerConsumer(callback, size=size), symbol=symbol)
