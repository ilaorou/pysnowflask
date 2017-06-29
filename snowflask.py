#!/usr/bin/python
# -*- coding:utf-8 -*-

import time


# import uuid
# mac = uuid.UUID(int=uuid.getnode()).hex[-12:]

class Snowflask():
    workId = 0
    threadId = 0
    sequence = 0
    sequenceMask = 16383
    lastTimestamp = 0
    workerIdShift = 16
    threadIdShift = 12
    timestampShift = 22

    def __init__(self, workId):
        if workId > 0 and workId < 16:
            self.workId = workId
        else:
            raise ("workId out of range(0~16)")

    def setThead(self, threadId):
        if threadId >= 0 and threadId < 16:
            self.threadId = threadId
        else:
            raise ("threadId out of range(0~16)")

    def timeGen(self):
        return int(round(time.time() * 1000)) - 1000000000000

    def tilNextMillis(self):
        timestamp = self.timeGen()
        if timestamp < self.lastTimestamp:
            raise ("clock is moving backwards.  Rejecting requests until %d." % self.lastTimestamp);

        return timestamp

    def nextIds(self, threadId, sequence):
        self.setThead(threadId)
        if sequence < 0 or sequence > self.sequenceMask:
            raise ("sequence out of range(0~%s)" % self.sequenceMask)
        timestamp = self.tilNextMillis()
        self.lastTimestamp = timestamp
        temp = timestamp << self.timestampShift | self.workId << self.workerIdShift | self.threadId << self.threadIdShift
        result = []
        for i in range(1, sequence):
            result.append(temp | i)
        return result

    def nextId(self, threadId):
        self.setThead(threadId)
        timestamp = self.tilNextMillis()
        if timestamp == self.lastTimestamp:
            self.sequence = self.sequence + 1 & self.sequenceMask
            if self.sequence == 0:
                timestamp = self.tilNextMillis()
        else:
            self.sequence = 0
        self.lastTimestamp = timestamp
        return timestamp << self.timestampShift | self.workId << self.workerIdShift | self.threadId << self.threadIdShift | self.sequence
