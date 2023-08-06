import pytest
from _pytest import logging

from plenum.common.constants import NODE, TXN_TYPE, GET_TXN, CONFIG_LEDGER_ID, DOMAIN_LEDGER_ID
from plenum.test.helper import sdk_gen_request, checkDiscardMsg
from plenum.test.test_config_req_handler import READ_CONF, TestConfigReqHandler
from plenum.test.testing_utils import FakeSomething


@pytest.fixture(scope='function')
def test_node(test_node):
    test_node.view_changer = FakeSomething(view_change_in_progress=True,
                                           view_no=1,
                                           instance_changes=None)
    test_node.init_config_req_handler = lambda: TestConfigReqHandler(test_node.configLedger,
                                                                     test_node.states[CONFIG_LEDGER_ID],
                                                                     test_node.states[DOMAIN_LEDGER_ID],
                                                                     bls_store=FakeSomething())
    test_node.register_req_handler(test_node.init_config_req_handler(), CONFIG_LEDGER_ID)
    return test_node


def test_client_write_request_discard_in_view_change_with_dict(test_node):
    test_node.send_nack_to_client = check_nack_msg

    msg = sdk_gen_request({TXN_TYPE: NODE}).as_dict
    test_node.unpackClientMsg(msg, "frm")
    checkDiscardMsg([test_node, ], msg, "view change in progress")


def test_client_get_request_not_discard_in_view_change_with_dict(test_node):
    sender = "frm"
    msg = sdk_gen_request({TXN_TYPE: GET_TXN}).as_dict

    def post_to_client_in_box(received_msg, received_frm):
        assert received_frm == sender
        assert received_msg == msg

    test_node.postToClientInBox = post_to_client_in_box

    def discard(received_msg, reason, logMethod, cliOutput):
        assert False, "Message {} was discard with '{}'".format(received_msg, reason)

    test_node.discard = discard

    test_node.unpackClientMsg(msg, sender)


def test_client_read_request_not_discard_in_view_change_with_dict(test_node):
    sender = "frm"
    msg = sdk_gen_request({TXN_TYPE: READ_CONF}).as_dict

    def post_to_client_in_box(received_msg, received_frm):
        assert received_frm == sender
        assert received_msg == msg

    test_node.postToClientInBox = post_to_client_in_box

    def discard(received_msg, reason, logMethod, cliOutput):
        assert False, "Message {} was discard with '{}'".format(received_msg, reason)

    test_node.discard = discard

    test_node.unpackClientMsg(msg, sender)


def test_client_msg_discard_in_view_change_with_request(test_node):
    test_node.send_nack_to_client = check_nack_msg

    msg = sdk_gen_request({TXN_TYPE: NODE})
    test_node.unpackClientMsg(msg, "frm")
    checkDiscardMsg([test_node, ], msg.as_dict, "view change in progress")


def check_nack_msg(req_key, reason, to_client):
    assert "Client request is discarded since view " \
           "change is in progress" == reason
