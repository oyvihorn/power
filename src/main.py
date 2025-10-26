from typing import Any, List, Dict
import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import logging
import time
from pydantic import ValidationError
import models
import plotting
import pandas as pd
import pickle

logger = logging.getLogger("energidataservice")

API_URL: str = "https://api.energidataservice.dk/dataset/PowerSystemRightNow?limit=5"
CYCLE_TIME: int = 61
SAVE_INTERVAL: int = 10
AVG_COLUMNS = ["Exchange_Sum", "ProductionGe100MW"]


def main() -> None:
    """
    Extract data from api.energidataservice.dk, calculate 5 min average and stores and plots
    data.
    Todo: split out methods into seperate files, main is crowded.
    """
    df_final: pd.DataFrame = None
    fig = plotting.setup_plot()

    with requests.Session() as session:
        try:
            while True:
                start_time = time.time()
                power_json = api_call(session, API_URL)

                if power_json is None:
                    logger.warning("failed to get values from API")
                    continue

                records = power_json.get("records")
                feed_logger(records)
                validate_records(records)
                df_records = dataframe_setup(records)
                # dataframe_qa(df_records)

                if df_final is None:
                    df_final = records_average(df_records)
                else:
                    df_final = pd.concat(
                        [df_final, records_average(df_records)], ignore_index=True
                    )

                plotting.update_plot(fig, df_final)
                store_data(df_final)
                wait_time(start_time)

        except ValidationError as val:
            logger.error(f"Could not validate record {val}")
        except Exception as err:
            logger.error(f"Exception {str(type(err))} while working", exc_info=True)


def api_call(session: requests.Session, API_URL) -> List[Dict[str, Any]]:
    try:

        response = request_retry_session(session).get(url=API_URL, timeout=15)
        if response.status_code != 200:
            logger.warning(f"Error calling api, status code: {response.status_code}")
            return None

        return response.json()

    except requests.RequestException as err:
        # This catches connection errors, timeouts, DNS failures, etc.
        logger.warning(f"Error calling api {err}")
        raise


def request_retry_session(
    session,
    retries: int = 3,
    backoff_factor: float = 0.5,
    status_forcelist=(500, 502, 503, 504),
):
    """
    Use 3 retries.
    Backoff factor is wait time beween retries.
    """
    session = session
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def validate_records(records: List[Dict[str, Any]]):
    for record in records:
        models.PowerRecords.model_validate(record)


def feed_logger(records: List[Dict[str, Any]]) -> None:
    """
    Todo: a lot
    """
    for record in records:
        print(" ", record.get("Minutes1UTC"), record.get("Exchange_Sum"))
        logger.info(" ", record.get("Minutes1UTC"), record.get("Exchange_Sum"))
    print("------")


def records_average(df_records: list[Dict[str, Any]]) -> pd.DataFrame:
    avg = df_records[AVG_COLUMNS].mean()
    current_record = df_records.iloc[-1]
    current_time = current_record["Minutes1UTC"]
    final = {}
    final["Minutes1UTC"] = current_time
    for col in AVG_COLUMNS:
        final[f"{col}_avg"] = avg[col]
        final[col] = current_record[col]

    return pd.DataFrame([final])


def dataframe_setup(records: List[Dict[str, Any]]) -> pd.DataFrame:
    df_records = pd.DataFrame([record for record in records])
    if not df_records.empty:
        df_records["Minutes1UTC"] = pd.to_datetime(df_records["Minutes1UTC"], utc=True)
        return df_records.sort_values("Minutes1UTC")


def dataframe_qa(df_records: pd.DataFrame) -> None:
    """
    check for missing vital attributes.
    """
    missing_timestamp = df_records["Minutes1UTC"].isnull().sum()
    if missing_timestamp > 0:
        raise ValueError("Missing timestamp for record")

    # missing_exchange_sum = df_records["Exchange_Sum"].isnull().sum()
    # if missing_exchange_sum > 0:
    #     raise ValueError("Missing exchange sum for record")


def store_data(df_final: pd.DataFrame) -> None:
    """
    Todo: what is best storage format for end user, parquet, pickle.
    """
    if len(df_final) % SAVE_INTERVAL == 0:
        with open("energidata.p", "wb") as file:
            pickle.dump(df_final, file)


def wait_time(start_time: time.time) -> None:
    end_time = time.time()
    wait_time = CYCLE_TIME - (end_time - start_time)
    if wait_time > 0:
        time.sleep(wait_time)


if __name__ == "__main__":
    main()
