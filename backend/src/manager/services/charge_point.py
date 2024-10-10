
##Charge point status
import logging
from charge_point_node.main import OnConnectionMessage


async def update_charge_point_status(charge_point_id: str, status: str,) -> None:
  logging.info(f"Start process update charge point status (event={charge_point_id}, status={status})")