# This Python file uses the following encoding: utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


MORPHENE_100_PERCENT = 10000
MORPHENE_1_PERCENT = 100
MORPHENE_VOTING_MANA_REGENERATION_SECONDS = 432000

STATE_BYTES_SCALE = 10000
STATE_TRANSACTION_BYTE_SIZE = 174
STATE_TRANSFER_FROM_SAVINGS_BYTE_SIZE = 229
STATE_LIMIT_ORDER_BYTE_SIZE = 1940
EXEC_FOLLOW_CUSTOM_OP_SCALE = 20
RC_DEFAULT_EXEC_COST = 100000
MORPHENE_RC_REGEN_TIME = 60 * 60 * 24 * 5

state_object_size_info = {'authority_base_size': 4 * STATE_BYTES_SCALE,
                          'authority_account_member_size': 18 * STATE_BYTES_SCALE,
                          'authority_key_member_size': 35 * STATE_BYTES_SCALE,
                          'account_object_base_size': 480 * STATE_BYTES_SCALE,
                          'account_authority_object_base_size': 40 * STATE_BYTES_SCALE,
                          'account_recovery_request_object_base_size': 32 * STATE_BYTES_SCALE,
                          'convert_request_object_base_size': 48 * STATE_BYTES_SCALE,
                          'escrow_object_base_size': 119 * STATE_BYTES_SCALE,
                          'transaction_object_base_size': 35 * STATE_TRANSACTION_BYTE_SIZE,
                          'transaction_object_byte_size': 1 * STATE_TRANSACTION_BYTE_SIZE,
                          'vesting_delegation_object_base_size': 60 * STATE_BYTES_SCALE,
                          'vesting_delegation_expiration_object_base_size': 44 * STATE_BYTES_SCALE,
                          'withdraw_vesting_route_object_base_size': 43 * STATE_BYTES_SCALE,
                          'witness_object_base_size': 266 * STATE_BYTES_SCALE,
                          'witness_object_url_char_size': 1 * STATE_BYTES_SCALE,
                          'witness_vote_object_base_size': 40 * STATE_BYTES_SCALE}

resource_execution_time = {"account_create_operation_exec_time": 57700,
                           "account_create_with_delegation_operation_exec_time": 57700,
                           "account_update_operation_exec_time": 14000,
                           "account_witness_proxy_operation_exec_time": 117000,
                           "account_witness_vote_operation_exec_time": 23000,
                           "change_recovery_account_operation_exec_time": 12000,
                           "claim_account_operation_exec_time": 10000,
                           "create_claimed_account_operation_exec_time": 57700,
                           "delegate_vesting_shares_operation_exec_time": 19900,
                           "escrow_approve_operation_exec_time": 9900,
                           "escrow_dispute_operation_exec_time": 11500,
                           "escrow_release_operation_exec_time": 17200,
                           "escrow_transfer_operation_exec_time": 19100,
                           "request_account_recovery_operation_exec_time": 54400,
                           "set_withdraw_vesting_route_operation_exec_time": 17900,
                           "transfer_operation_exec_time": 9600,
                           "withdraw_vesting_operation_exec_time": 10400,
                           "witness_set_properties_operation_exec_time": 9500,
                           "witness_update_operation_exec_time": 9500}

operation_exec_info = {}
