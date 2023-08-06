#!/usr/bin/env python3
# -*- encoding=utf-8 -*-

# description:
# author:jack
# create_time: 2019-06-13

"""
    desc:pass
"""
import os
from dueros.Bot import Bot
from dueros.directive.DPL.Document import Document
from dueros.directive.DPL.RenderDocument import RenderDocument


class DPLBot(Bot):

    def __init__(self, request_data):
        super(DPLBot, self).__init__(request_data)
        self.add_launch_handler(self.launchRequest)
        self.add_intent_handler('dpl_demo1', self.dpl_demo1)
        self.add_intent_handler('dpl_demo2', self.dpl_demo2)
        self.add_intent_handler('dpl_demo3', self.dpl_demo3)
        self.add_intent_handler('dpl_demo4', self.dpl_demo4)
        self.add_intent_handler('dpl_demo5', self.dpl_demo5)
        self.add_intent_handler('dpl_demo6', self.dpl_demo6)
        self.add_common_default_intent_handler(self.default_intent)
        self.add_session_ended_handler(self.ended)

        self.add_event_listener('UserEvent', self.handle_event)

    def handle_event(self, event):
        print(event)

    def ended(self):
        self.end_session()

    def default_intent(self):
        self.wait_answer()
        return {
            'outputSpeech': '欢迎来到猜数字游戏'
        }

    def launchRequest(self):
        '''
        打开调用名
        '''
        self.wait_answer()
        directive = get_dpl_directive(os.path.abspath('.') + '/doc/launch.json')
        return {
            #'directives': [directive],
            'outputSpeech': '欢迎来到猜数字游戏'
        }

    def dpl_demo1(self):
        self.wait_answer()
        self.set_expect_speech(False)
        directive = get_dpl_directive(os.path.abspath('.') + '/doc/demo1.json')
        return {
            'directives': [directive],
            'outputSpeech': '简单图片'
        }

    def dpl_demo2(self):
        self.wait_answer()
        self.set_expect_speech(False)
        directive = get_dpl_directive(os.path.abspath('.') + '/doc/demo2.json')
        return {
            'directives': [directive],
            'outputSpeech': '长文本'
        }

    def dpl_demo3(self):
        self.wait_answer()
        directive = get_dpl_directive(os.path.abspath('.') + '/doc/demo3.json')
        return {
            'directives': [directive],
            'outputSpeech': '短文本'
        }

    def dpl_demo4(self):
        self.wait_answer()
        directive = get_dpl_directive(os.path.abspath('.') + '/doc/demo4.json')
        return {
            'directives': [directive],
            'outputSpeech': '右图详情'
        }

    def dpl_demo5(self):
        self.wait_answer()
        directive = get_dpl_directive(os.path.abspath('.') + '/doc/demo5.json')
        return {
            'directives': [directive],
            'outputSpeech': '左图详情'
        }

    def dpl_demo6(self):
        self.wait_answer()
        self.set_expect_speech(False)
        directive = get_dpl_directive(os.path.abspath('.') + '/doc/demo6.json')
        return {
            'directives': [directive],
            'outputSpeech': '左图详情'
        }


def get_dpl_directive(path):
    doc = Document()
    render = RenderDocument()
    doc.init_data(Document.get_document_from_path(path))
    render.set_document(doc)
    return render


if __name__ == '__main__':
    pass