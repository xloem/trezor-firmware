from micropython import const

from trezor import ui, wire
from trezor.messages.AuthorizeCoinJoin import AuthorizeCoinJoin
from trezor.messages.Success import Success
from trezor.strings import format_amount
from trezor.ui.components.tt.text import Text

from apps.common import authorization
from apps.common.confirm import require_confirm, require_hold_to_confirm
from apps.common.paths import validate_path

from .authorization import FEE_PER_ANONYMITY_DECIMALS
from .common import BIP32_WALLET_DEPTH
from .keychain import validate_path_against_script_type, with_keychain
from .sign_tx.layout import format_coin_amount

if False:
    from apps.common.coininfo import CoinInfo
    from apps.common.keychain import Keychain

_MAX_COORDINATOR_LEN = const(18)


@with_keychain
async def authorize_coinjoin(
    ctx: wire.Context, msg: AuthorizeCoinJoin, keychain: Keychain, coin: CoinInfo
) -> Success:
    if len(msg.coordinator) > _MAX_COORDINATOR_LEN or not all(
        32 <= ord(x) <= 126 for x in msg.coordinator
    ):
        raise wire.DataError("Invalid coordinator name.")

    if not msg.address_n:
        raise wire.DataError("Empty path not allowed.")

    validation_path = msg.address_n + [0] * BIP32_WALLET_DEPTH
    await validate_path(
        ctx,
        keychain,
        validation_path,
        validate_path_against_script_type(
            coin, address_n=validation_path, script_type=msg.script_type
        ),
    )

    text = Text("Authorize CoinJoin", ui.ICON_RECOVERY)
    text.normal("Do you really want to")
    text.normal("take part in a CoinJoin")
    text.normal("transaction at:")
    text.mono(msg.coordinator)
    await require_confirm(ctx, text)

    text = Text("Authorize CoinJoin", ui.ICON_RECOVERY)
    if msg.fee_per_anonymity:
        text.normal("Fee per anonymity set:")
        text.bold(
            "{} %".format(
                format_amount(msg.fee_per_anonymity, FEE_PER_ANONYMITY_DECIMALS)
            )
        )
    text.normal("Maximum total fees:")
    text.bold(
        format_coin_amount(
            msg.max_total_fee,
            coin,
            msg.amount_unit,
        )
    )
    await require_hold_to_confirm(ctx, text)

    authorization.set(msg)

    return Success(message="CoinJoin authorized")
