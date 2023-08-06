############################################################
# -*- coding: utf-8 -*-
#
# MOUNTCONTROL
#
# Python-based Tool for interaction with the 10micron mounts
# GUI with PyQT5 for python
# Python  v3.6.5
#
# Michael Würtenberger
# (c) 2018
#
# Licence APL2.0
#
############################################################
# standard libraries
import unittest
import unittest.mock as mock
import socket
# external packages
# local imports
from mountcontrol.connection import Connection


class TestConnection(unittest.TestCase):

    def setUp(self):
        pass

    #
    #
    # testing the command analyses against structural faults
    #
    #

    def test_responses_withoutCommand_analyseCommand(self):
        conn = Connection()
        chunksToReceive, getData, minBytes = conn._analyseCommand('')
        self.assertEqual(False, getData)
        self.assertEqual(0, minBytes)
        self.assertEqual(0, chunksToReceive)

    def test_responses_typeA_analyseCommand(self):
        conn = Connection()
        command = ':AP#'
        chunksToReceive, getData, minBytes = conn._analyseCommand(command)
        self.assertEqual(False, getData)
        self.assertEqual(0, minBytes)
        self.assertEqual(0, chunksToReceive)

    def test_responses_typeB_analyseCommand(self):
        conn = Connection()
        command = ':FLIP#'
        chunksToReceive, getData, minBytes = conn._analyseCommand(command)
        self.assertEqual(True, getData)
        self.assertEqual(1, minBytes)
        self.assertEqual(0, chunksToReceive)

    def test_responses_typeC_analyseCommand(self):
        conn = Connection()
        command = ':GTMP1#'
        chunksToReceive, getData, minBytes = conn._analyseCommand(command)
        self.assertEqual(True, getData)
        self.assertEqual(0, minBytes)
        self.assertEqual(1, chunksToReceive)

    def test_responses_typeAB_analyseCommand(self):
        conn = Connection()
        command = ':AP#:FLIP#'
        chunksToReceive, getData, minBytes = conn._analyseCommand(command)
        self.assertEqual(True, getData)
        self.assertEqual(1, minBytes)
        self.assertEqual(0, chunksToReceive)

    def test_responses_typeAC_analyseCommand(self):
        conn = Connection()
        command = ':AP#:GTMP1#'
        chunksToReceive, getData, minBytes = conn._analyseCommand(command)
        self.assertEqual(True, getData)
        self.assertEqual(0, minBytes)
        self.assertEqual(1, chunksToReceive)

    def test_responses_typeBC_analyseCommand(self):
        conn = Connection()
        command = ':FLIP#:GTMP1#'
        chunksToReceive, getData, minBytes = conn._analyseCommand(command)
        self.assertEqual(True, getData)
        self.assertEqual(1, minBytes)
        self.assertEqual(1, chunksToReceive)

    def test_responses_typeABC_analyseCommand(self):
        conn = Connection()
        command = ':AP#:FLIP#:GTMP1#'
        chunksToReceive, getData, minBytes = conn._analyseCommand(command)
        self.assertEqual(True, getData)
        self.assertEqual(1, minBytes)
        self.assertEqual(1, chunksToReceive)

    def test_responses_typeABCABC_analyseCommand(self):
        conn = Connection()
        command = ':AP#:FLIP#:GTMP1#:AP#:FLIP#:GTMP1#'
        chunksToReceive, getData, minBytes = conn._analyseCommand(command)
        self.assertEqual(True, getData)
        self.assertEqual(2, minBytes)
        self.assertEqual(2, chunksToReceive)

    def test_responses_typeABBCCABC_analyseCommand(self):
        conn = Connection()
        command = ':AP#:FLIP#:FLIP#:GTMP1#:GTMP1#:AP#:FLIP#:GTMP1#'
        chunksToReceive, getData, minBytes = conn._analyseCommand(command)
        self.assertEqual(True, getData)
        self.assertEqual(3, minBytes)
        self.assertEqual(3, chunksToReceive)

        #
        #
        # testing the connection without host presence
        #
        #

    def test_ok(self):
        with mock.patch('socket.socket') as m_socket:
            m_socket.return_value.recv.return_value = '10micron GM1000HPS#'.encode()
            conn = Connection(host=('192.168.2.15', 3492))
            suc, response, chunks = conn.communicate(':GVN#')
            m_socket.return_value.connect.assert_called_with(('192.168.2.15', 3492))
            m_socket.return_value.sendall.assert_called_with(':GVN#'.encode())
        self.assertEqual(True, suc)
        self.assertEqual('10micron GM1000HPS', response[0])

    def test_no_host_defined(self):
        with mock.patch('socket.socket') as m_socket:
            m_socket.return_value.recv.return_value = '10micron GM1000HPS#'.encode()
            conn = Connection()
            suc, response, chunks = conn.communicate(':GVN#')
        self.assertEqual(False, suc)
        self.assertEqual('', response)

    def test_no_port_defined(self):
        with mock.patch('socket.socket') as m_socket:
            m_socket.return_value.recv.return_value = '10micron GM1000HPS#'.encode()
            conn = Connection(host='192.168.2.15')
            suc, response, chunks = conn.communicate(':GVN#')
        self.assertEqual(False, suc)
        self.assertEqual('', response)

    def test_no_response(self):
        with mock.patch('socket.socket') as m_socket:
            m_socket.return_value.recv.return_value = '10micron GM1000HPS#'.encode()
            conn = Connection(host=('192.168.2.15', 3492))
            suc, response, chunks = conn.communicate('')
        self.assertEqual(True, suc)
        self.assertEqual('', response)

    def test_no_chunk(self):
        with mock.patch('socket.socket') as m_socket:
            m_socket.return_value.recv.return_value = ''.encode
            conn = Connection(host=('192.168.2.15', 3492))
            suc, response, chunks = conn.communicate('')
        self.assertEqual(True, suc)
        self.assertEqual('', response)

    def test_connect_timeout(self):
        with mock.patch('socket.socket') as m_socket:
            m_socket.return_value.recv.return_value = '10micron GM1000HPS#'.encode()
            m_socket.return_value.connect.side_effect = socket.timeout
            conn = Connection(host=('192.168.2.15', 3492))
            suc, response, chunks = conn.communicate(':GVN#')
        self.assertEqual(False, suc)

    def test_sendall_timeout(self):
        with mock.patch('socket.socket') as m_socket:
            m_socket.return_value.recv.return_value = '10micron GM1000HPS#'.encode()
            m_socket.return_value.sendall.side_effect = socket.timeout
            conn = Connection(host=('192.168.2.15', 3492))
            suc, response, chunks = conn.communicate(':GVN#')
        self.assertEqual(False, suc)

    def test_recv_timeout(self):
        with mock.patch('socket.socket') as m_socket:
            m_socket.return_value.recv.return_value = '10micron GM1000HPS#'.encode()
            m_socket.return_value.recv.side_effect = socket.timeout
            conn = Connection(host=('192.168.2.15', 3492))
            suc, response, chunks = conn.communicate(':GVN#')
        self.assertEqual(False, suc)

    def test_connect_socket_error(self):
        with mock.patch('socket.socket') as m_socket:
            m_socket.return_value.recv.return_value = '10micron GM1000HPS#'.encode()
            m_socket.return_value.connect.side_effect = socket.error
            conn = Connection(host=('192.168.2.15', 3492))
            suc, response, chunks = conn.communicate(':GVN#')
        self.assertEqual(False, suc)

    def test_sendall_socket_error(self):
        with mock.patch('socket.socket') as m_socket:
            m_socket.return_value.recv.return_value = '10micron GM1000HPS#'.encode()
            m_socket.return_value.sendall.side_effect = socket.error
            conn = Connection(host=('192.168.2.15', 3492))
            suc, response, chunks = conn.communicate(':GVN#')
        self.assertEqual(False, suc)

    def test_recv_socket_error(self):
        with mock.patch('socket.socket') as m_socket:
            m_socket.return_value.recv.return_value = '10micron GM1000HPS#'.encode()
            m_socket.return_value.recv.side_effect = socket.error
            conn = Connection(host=('192.168.2.15', 3492))
            suc, response, chunks = conn.communicate(':GVN#')
        self.assertEqual(False, suc)

    def test_connect_exception(self):
        with mock.patch('socket.socket') as m_socket:
            m_socket.return_value.recv.return_value = '10micron GM1000HPS#'.encode()
            m_socket.return_value.connect.side_effect = Exception('Test')
            conn = Connection(host=('192.168.2.15', 3492))
            suc, response, chunks = conn.communicate(':GVN#')
        self.assertEqual(False, suc)

    def test_sendall_exception(self):
        with mock.patch('socket.socket') as m_socket:
            m_socket.return_value.recv.return_value = '10micron GM1000HPS#'.encode()
            m_socket.return_value.sendall.side_effect = Exception('Test')
            conn = Connection(host=('192.168.2.15', 3492))
            suc, response, chunks = conn.communicate(':GVN#')
        self.assertEqual(False, suc)

    def test_recv_exception(self):
        with mock.patch('socket.socket') as m_socket:
            m_socket.return_value.recv.return_value = '10micron GM1000HPS#'.encode()
            m_socket.return_value.recv.side_effect = Exception('Test')
            conn = Connection(host=('192.168.2.15', 3492))
            suc, response, chunks = conn.communicate(':GVN#')
        self.assertEqual(False, suc)

    def test_commands_valid_A(self):
        conn = Connection()
        for command in conn.COMMAND_A:
            self.assertTrue(command in conn.COMMANDS)

    def test_commands_valid_B(self):
        conn = Connection()
        for command in conn.COMMAND_B:
            self.assertTrue(command in conn.COMMANDS)

    def test_valid_commandSet_1(self):
        conn = Connection()
        suc = conn._validCommandSet(':AP#')
        self.assertTrue(suc)

    def test_valid_commandSet_2(self):
        conn = Connection()
        suc = conn._validCommandSet(':AP#:AP#:AP#')
        self.assertTrue(suc)

    def test_invalid_commandSet_1(self):
        conn = Connection()
        suc = conn._validCommandSet(':test#')
        self.assertFalse(suc)

    def test_invalid_commandSet_2(self):
        conn = Connection()
        suc = conn._validCommandSet(':AP#:test#')
        self.assertFalse(suc)

    def test_invalid_command_1(self):
        conn = Connection()
        suc = conn._validCommand(':AP#')
        self.assertTrue(suc)

    def test_invalid_command_2(self):
        conn = Connection()
        suc = conn._validCommand(':test#')
        self.assertFalse(suc)

    def test_communicate_invalid_command_1(self):
        conn = Connection()
        suc, msg, num = conn.communicate(':test#')
        self.assertFalse(suc)

    def test_communicate_invalid_command_2(self):
        conn = Connection()
        suc, msg, num = conn.communicate(':AP#:test#')
        self.assertFalse(suc)
