from __future__ import annotations
from typing import cast, Union, Any, Callable, List
from logging import Logger
from src.libs.Web3Client.Web3Client import Web3Client
from web3.types import FilterParams, LogReceipt
from abc import ABC
import logging
import time
from web3.types import BlockParams

class Watcher(ABC):
    """
    Base class representing a blockchain watcher.
    
    1. Set a filter with either setFilter() or setFilterParams().
    2. Register as many callbacks as you wish with addHandler().
    3. Start the watcher with run().

    The filter will be used to sieve the blockchain for corresponding
    log entries; each time a log is found, it is passed to the handlers.
    The handlers are executed in the same order they are provided.
    
    Glossary: A log entry is an event submitted by a smart contract; for
    this reason, "log entry" will be used interchangeably with "event".
    
    Nota bene: Please use a websocket URI to run the watcher, otherwise
    you might run into errors (for example 'filter not found') or slow
    execution.
    
    Docs: https://web3py.readthedocs.io/en/stable/filters.html
    """

    # Settable
    logger: Logger = logging # type: ignore
    filterParams: Union[FilterParams, BlockParams] = {}
    handlers: List[Callable[..., Any]] = []
    doAsync: bool = True
    pollInterval: int = 2
    
    # Derived
    filter: Any = None
    

    def __init__(self, client: Web3Client ) -> None:
        self.client = client
        pass
    
    def addHandler(self, handler: Callable[[LogReceipt], None]) -> Watcher:
        """
        Add a handler to the queue; the handler will process the log
        entry in the order they were provided.
        """
        self.handlers.append(handler)
        return self
    
    def setFilterParams(self, params: Union[FilterParams, BlockParams]) -> Watcher:
        """
        Given valid filter parameters, create and set the filter to
        use to sieve the blockchain logs.
        """
        self.filterParams = params
        self.setFilter(self.client.w3.eth.filter(self.filterParams))
        return self

    def setFilter(self, filter: Any) -> Watcher:
        """
        Set the filter to use to sieve the blockchain logs.
        """
        self.filter: Any = filter
        return self

    def setLogger(self, logger: Logger) -> Watcher:
        self.logger = logger
        return self

    def loop(self, filter: Any, pollInterval: int) -> None:
        """
        Infinite loop where we look for new log entries and fire
        the handlers to process them
        """
        while True:
            newLogs = cast(List[LogReceipt], filter.get_new_entries())
            if (not newLogs):
                self.logger.debug("Watcher: No new log entry found")
            for logEntry in newLogs:
                self.logger.debug("Watcher: New log entry!")
                self.handleLogEntry(logEntry)
            time.sleep(self.pollInterval)

    def handleLogEntry(self, logEntry: LogReceipt) -> None:
        """
        Given a log entry, run all handlers in the order they
        were added
        """
        for handler in self.handlers:
            handler(logEntry)

    def run(self, pollInterval: int) -> None:
        """
        Start watching for whatever block or logEntry
        was set as a filter
        """
        self.loop(self.filter, pollInterval)