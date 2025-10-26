from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class PowerRecords(BaseModel):
    """
    Slim to whatever needed
    """

    minutes_1_utc: datetime = Field(
        ..., alias="Minutes1UTC", description="UTC timestamp for the minute"
    )
    minutes_1_dk: datetime = Field(
        ..., alias="Minutes1DK", description="Denmark local timestamp for the minute"
    )
    co2_emission: float = Field(..., alias="CO2Emission")
    production_ge_100_mw: float = Field(..., alias="ProductionGe100MW")
    production_lt_100_mw: float = Field(..., alias="ProductionLt100MW")
    solar_power: float = Field(..., alias="SolarPower")
    offshore_wind_power: float = Field(..., alias="OffshoreWindPower")
    onshore_wind_power: float = Field(..., alias="OnshoreWindPower")
    exchange_sum: float = Field(..., alias="Exchange_Sum")

    exchange_dk1_de: float = Field(..., alias="Exchange_DK1_DE")
    exchange_dk1_nl: float = Field(..., alias="Exchange_DK1_NL")
    exchange_dk1_gb: float = Field(..., alias="Exchange_DK1_GB")
    exchange_dk1_no: float = Field(..., alias="Exchange_DK1_NO")
    exchange_dk1_se: float = Field(..., alias="Exchange_DK1_SE")
    exchange_dk1_dk2: float = Field(..., alias="Exchange_DK1_DK2")
    exchange_dk2_de: float = Field(..., alias="Exchange_DK2_DE")
    exchange_dk2_se: float = Field(..., alias="Exchange_DK2_SE")
    exchange_bornholm_se: float = Field(..., alias="Exchange_Bornholm_SE")

    a_frr_activated_dk1: float = Field(..., alias="aFRR_ActivatedDK1")
    a_frr_activated_dk2: float = Field(..., alias="aFRR_ActivatedDK2")

    m_frr_activated_dk1: Optional[float] = Field(None, alias="mFRR_ActivatedDK1")
    m_frr_activated_dk2: Optional[float] = Field(None, alias="mFRR_ActivatedDK2")

    imbalance_dk1: Optional[float] = Field(None, alias="ImbalanceDK1")
    imbalance_dk2: Optional[float] = Field(None, alias="ImbalanceDK2")
