import matplotlib.pyplot as plt
import pandas as pd


def setup_plot() -> plt.Figure:
    fig = plt.figure(figsize=(12, 8))

    plt.subplot(2, 1, 1)
    plt.title("Production On Plant > 100MW – 5min mean ")
    plt.ylabel("ProductionGe100MW_avg")

    plt.subplot(2, 1, 2)
    plt.title("Energi data service – 5‑min mean")
    plt.xlabel("Time (UTC)")
    plt.ylabel("Exchange_Sum_avg (5‑min mean)")

    plt.tight_layout()
    plt.ion()  # interactive no  blocking
    plt.show()
    return fig


def update_plot(fig: plt.Figure, df_records: pd.DataFrame) -> None:
    plt.subplot(2, 1, 1)
    plt.plot(
        df_records["Minutes1UTC"],
        df_records["ProductionGe100MW_avg"],
        marker="o",
        linestyle="-",
        color="#1f77b4",
    )
    plt.legend(loc="upper left")
    plt.grid(True, ls=":", alpha=0.5)

    plt.subplot(2, 1, 2)
    plt.plot(
        df_records["Minutes1UTC"],
        df_records["Exchange_Sum_avg"],
        marker="o",
        linestyle="-",
        color="#ff7f0e",
    )
    plt.legend(loc="upper left")
    plt.grid(True, ls=":", alpha=0.5)

    fig.autofmt_xdate()

    plt.draw()
    plt.pause(0.001)
