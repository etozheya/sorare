import ctypes
from ctypes import cdll

from Crypto.Util import number

from queries.vars import starkware_private_key


def sign_limit_order(limit_order):
    message = hash_limit_order(limit_order)
    return sign(starkware_private_key, message)


def hash_limit_order(limit_order):
    args = {
        'vault_id_sell': limit_order['vaultIdSell'],
        'vault_id_buy': limit_order['vaultIdBuy'],
        'amount_sell': limit_order['amountSell'],
        'amount_buy': limit_order['amountBuy'],
        'token_sell': limit_order['tokenSell'],
        'token_buy': limit_order['tokenBuy'],
        'nonce': limit_order['nonce'],
        'expiration_timestamp': limit_order['expirationTimestamp'],
        'fee_info': limit_order['feeInfo']}
    if args['fee_info']:
        return get_limit_order_msg_hash_with_fee(
            args, args['fee_info']['tokenId'],
            args['fee_info']['sourceVaultId'], args['fee_info']['feeLimit'])
    return get_limit_order_msg_hash(args)


def get_limit_order_msg_hash(args):
    if not args['token_sell'].startswith('0x') or \
            not args['token_buy'].startswith('0x'):
        raise
    args['amount_sell'] = int(args['amount_sell'])
    args['amount_buy'] = int(args['amount_buy'])
    args['token_sell'] = int(args['token_sell'], 16)
    args['token_buy'] = int(args['token_buy'], 16)
    return hash_msg(args)


def get_limit_order_msg_hash_with_fee(
        args, token_id, source_vault_id, fee_limit):
    if not args['token_sell'].startswith('0x') or \
            not args['token_buy'].startswith('0x'):
        raise
    args['amount_sell'] = int(args['amount_sell'])
    args['amount_buy'] = int(args['amount_buy'])
    args['token_sell'] = int(args['token_sell'], 16)
    args['token_buy'] = int(args['token_buy'], 16)
    token_id = int(token_id, 16)
    return hash_limit_order_msg_with_fee(
        args, token_id, source_vault_id, fee_limit)


def hash_msg(args):
    condition = None
    packed_message = 0 << 31
    packed_message = packed_message + args['vault_id_sell']
    packed_message = packed_message << 31
    packed_message = packed_message + args['vault_id_buy']
    packed_message = packed_message << 63
    packed_message = packed_message + args['amount_sell']
    packed_message = packed_message << 63
    packed_message = packed_message + args['amount_buy']
    packed_message = packed_message << 31
    packed_message = packed_message + args['nonce']
    packed_message = packed_message << 22
    packed_message = packed_message + args['expiration_timestamp']
    message_hash = None
    if condition:
        pass
    else:
        message_hash = pedersen([pedersen([pedersen([args['token_sell'], args['token_buy']]), condition]), hex(packed_message)])
    return int(message_hash, 16)


def pedersen(arr):
    use_crypto_cpp = True
    if use_crypto_cpp:
        if type(arr[0]) == str:
            arr[0] = int(arr[0], 16)
        if type(arr[1]) == str:
            arr[1] = int(arr[1], 16)
        return number.long_to_hex(pedersen(arr[0], arr[1]))
    else:
        point = shiftPoint
        for i in range(len(arr)):
            x = int(arr[i], 16)
            for j in range(252):
                pt = constantPoints[2 + i * 252 + j]
                if x & 1 != 0:
                    point = point.add(pt)
                x = x >> 1
        return number.long_to_hex(point.getX().to_int())


def crypto_pedersen(x, y):
    libcrypto = cdll.LoadLibrary(
        path.join(__dirname, '..', '..', 'build', 'Release', 'crypto'))

    libcrypto.Hash.argtypes = [ctypes.c_char_p, ctypes.c_char_p,
                               ctypes.c_char_p]
    libcrypto.Hash.restype = ctypes.c_int

    libcrypto.Verify.argtypes = [ctypes.c_char_p, ctypes.c_char_p,
                                 ctypes.c_char_p, ctypes.c_char_p]
    libcrypto.Verify.restype = ctypes.c_bool

    libcrypto.Sign.argtypes = [ctypes.c_char_p, ctypes.c_char_p,
                               ctypes.c_char_p, ctypes.c_char_p]
    libcrypto.Sign.restype = ctypes.c_int

    libcrypto.GetPublicKey.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    libcrypto.GetPublicKey.restype = ctypes.c_int
    x_buf = x.to_bytes(32, 'little')
    y_buf = y.to_bytes(32, 'little')
    res_buf = bytearray(1024)
    res = libcrypto.Hash(x_buf, y_buf, res_buf)
    assert res == 0, 'Error: ' + res_buf.decode('utf-8')
    return int.from_bytes(res_buf, 'little')
