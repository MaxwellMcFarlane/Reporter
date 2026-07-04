import argparse
import os
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yaml

from dataset import Dataset
from plotter import plot_2d_scatter_colored, save_plot
from utils import console_log, is_number


class Run:
    _DEFAULT_PLOT_CONFIG = {
        "xlabel": "",
        "ylabel": "",
        "xscale": 1,
        "yscale": 1,
        "xlim": [],
        "ylim": [],
        "title": "",
        "type": None,
        "fontsize": 12,
        "figsize": (24, 12),
        "legend_loc": "best",
        "key": [],
    }

    def __init__(self, name, run_dict: dict | None = None, outdir: str = ".", msglvl: int = 0):
        run_dict = run_dict or {}

        self.name = name
        self.data = run_dict.get("data", {})
        self.xval = run_dict.get("xval")
        self.xmatch = run_dict.get("xmatch")
        self.yval = run_dict.get("yval")
        self.ymatch = run_dict.get("ymatch")
        self.zval = run_dict.get("zval")
        self.zmatch = run_dict.get("zmatch")
        self.description = run_dict.get("description")
        self.outfile = run_dict.get("outfile", "plot")
        self.plot_config = self._build_plot_config(run_dict.get("plot-config", {}), msglvl)
        self.outdir = outdir
        self.msglvl = msglvl
        self.testcases = {}

        for required in ["xval", "yval", "zval", "data"]:
            if required not in run_dict:
                console_log(
                    f"For Run ({name}) : {required} not found, unable to set from configuration YAML.",
                    msglvl,
                    "warn",
                )

        console_log(f"****** RUN ({name}) created. ******", msglvl, "info")

    def _build_plot_config(self, raw_plot_cfg: dict, msglvl: int) -> dict:
        cfg = dict(self._DEFAULT_PLOT_CONFIG)
        for key, default_val in cfg.items():
            if key not in raw_plot_cfg:
                continue
            try:
                if key in ["xscale", "yscale"]:
                    cfg[key] = float(raw_plot_cfg[key])
                elif key in ["xlim", "ylim"]:
                    cfg[key] = list(raw_plot_cfg[key])
                else:
                    cfg[key] = raw_plot_cfg[key]
            except Exception as exc:
                console_log(
                    f"For Run ({self.name}) : {exc} not found, unable to set from configuration YAML.",
                    msglvl,
                    "warn",
                )
        return cfg

    def plot(self):
        console_log(f"Plotting {self.plot_config['type']} for {self.name}", self.msglvl)
        plotters = {
            "line-2d": self.plot_line_2d,
            "pie": self.plot_pie,
            "stacked-bar": self.plot_stacked_bar,
            "scatter-2d": self.plot_scatter_2d,
            "box-whisker": self.plot_box_whisker,
        }
        plot_fn = plotters.get(self.plot_config["type"])
        if plot_fn is None:
            console_log(f"Plot Type for {self.name} cannot be determined.", self.msglvl, "warn")
            return
        plot_fn()

    def check_key(self, tc: Dataset):
        key_cfg = self.plot_config.get("key", {})
        entry = key_cfg.get(tc.name, {}) if isinstance(key_cfg, dict) else {}
        return entry.get("color", "black"), entry.get("style", "solid")

    def plot_line_2d(self) -> None:
        console_log("2D Plot being generated", self.msglvl + 1, "info")
        fig = plt.figure(figsize=self.plot_config["figsize"])
        ax = fig.add_subplot(111)
        console_log(f"Number of TestCases : {len(self.testcases)}", self.msglvl + 1, "info")

        for tc in self.testcases.values():
            if len(tc.x) == 0 or len(tc.y) == 0:
                continue
            x = tc.x * self.plot_config["xscale"] if is_number(tc.x.iloc[0]) else tc.x
            y = tc.y * self.plot_config["yscale"] if is_number(tc.y.iloc[0]) else tc.y
            color, ls = self.check_key(tc)
            plt.plot(x, y, label=f"{tc.name}", color=color, linestyle=ls)

        if len(self.plot_config["xlim"]) != 0:
            ax.set_xlim(self.plot_config["xlim"])
        if len(self.plot_config["ylim"]) != 0:
            ax.set_ylim(self.plot_config["ylim"])
        ax.set_xlabel(self.plot_config["xlabel"], fontsize=self.plot_config["fontsize"])
        ax.set_ylabel(self.plot_config["ylabel"], fontsize=self.plot_config["fontsize"])
        ax.set_title(self.plot_config["title"], fontsize=self.plot_config["fontsize"])
        ax.grid(True)
        plt.legend(loc=self.plot_config["legend_loc"])
        plt.tight_layout()
        save_plot(f"{self.outfile}", self.outdir, self.msglvl + 1)

    def plot_stacked_bar(self):
        for tc in self.testcases.values():
            fig = plt.figure(figsize=self.plot_config["figsize"])
            ax = fig.add_subplot(111)
            df_plot = tc.df.copy()
            x_col = tc.cols[0]

            # For stacked bars, prefer all numeric series from the original CSV
            # so a single run can include Spending/Income/Cashflow together.
            try:
                full_df = pd.read_csv(tc.dfile)
                if x_col in full_df.columns:
                    numeric_cols = [
                        c for c in full_df.columns
                        if c != x_col and pd.api.types.is_numeric_dtype(full_df[c])
                    ]
                    if len(numeric_cols) >= 2:
                        df_plot = full_df[[x_col] + numeric_cols]
            except Exception:
                pass

            ax = df_plot.plot(x=x_col, kind="bar", stacked=True)
            ax.set_xlabel(self.plot_config["xlabel"], fontsize=self.plot_config["fontsize"])
            ax.set_ylabel(self.plot_config["ylabel"], fontsize=self.plot_config["fontsize"])
            ax.set_title(self.plot_config["title"], fontsize=self.plot_config["fontsize"])
            plt.legend(loc=self.plot_config["legend_loc"])
            plt.xticks(rotation=0)
            plt.grid(axis="y", linestyle="--", alpha=0.3)
            plt.tight_layout()
            save_plot(self.outfile, self.outdir, self.msglvl + 1)

    def plot_box_whisker(self):
        console_log("Box Whisker Plot being generated", self.msglvl + 1, "info")
        fig = plt.figure(figsize=self.plot_config["figsize"])
        fig.add_subplot(111)
        console_log(f"Number of TestCases : {len(self.testcases)}", self.msglvl + 1, "info")

        for tc in self.testcases.values():
            x_col = getattr(tc, "x_label", tc.cols[0] if len(tc.cols) > 0 else None)
            y_col = getattr(tc, "y_label", tc.cols[1] if len(tc.cols) > 1 else None)
            if x_col is None or y_col is None or x_col not in tc.df.columns or y_col not in tc.df.columns:
                console_log(f"Skipping testcase {tc.name}: invalid box-whisker columns.", self.msglvl + 1, "warn")
                continue

            box = tc.df.pivot(columns=x_col, values=y_col)
            box.boxplot(fontsize=self.plot_config["fontsize"])
            plt.ylim((0, 1.1 * np.max(box.max())))
            plt.title(self.plot_config["title"], fontsize=self.plot_config["fontsize"])
            plt.ylabel(self.plot_config["ylabel"], fontsize=self.plot_config["fontsize"])
            plt.tight_layout()
            save_plot(f"box_whisker_{tc.name}", self.outdir, self.msglvl + 1)

            console_log("Description Stats", self.msglvl + 1, "pass")
            stats_table = box.describe().transpose()
            data_name = getattr(tc, "data_name", tc.name)

            outfile = f"{self.outdir}/latency_table_{data_name}.csv"
            console_log(f"Writing Latency Report --> {outfile}", self.msglvl + 1, "pass")
            stats_table.to_csv(outfile, float_format="%.2f", index_label="Index")

            outfile = f"{self.outdir}/latency_data_pretty_{data_name}.csv"
            console_log(f"Writing Latency Report --> {outfile}", self.msglvl + 1, "pass")
            drop_cols = [c for c in ["count", "25%", "50%", "75%"] if c in stats_table.columns]
            stats_table.drop(drop_cols, axis=1).to_csv(outfile, float_format="%.2f", index_label="Index")

    def plot_scatter_2d(self):
        console_log("Scatter Plot being generated", self.msglvl + 1, "info")
        console_log(f"Number of TestCases : {len(self.testcases)}", self.msglvl + 1, "info")

        for tc in self.testcases.values():
            res_norm = tc.df.replace(np.inf, np.nan).dropna().copy()
            operations = getattr(tc, "operations", [])
            if not operations and "Operation" in res_norm.columns:
                operations = res_norm["Operation"].dropna().unique().tolist()
            if not operations:
                console_log(f"No operations found for scatter plot in testcase: {tc.name}", self.msglvl + 1, "warn")
                continue

            op_cols = ["OperandA", "OperandB", "OperandC"]
            if not all(col in res_norm.columns for col in op_cols):
                console_log(f"Skipping scatter plot for {tc.name}: missing operand columns.", self.msglvl + 1, "warn")
                continue
            res_norm[["OperandA(Log)", "OperandB(Log)", "OperandC(Log)"]] = np.log10(np.abs(res_norm[op_cols]))

            for op in operations:
                df = res_norm[res_norm["Operation"] == op]
                if len(df) < 1:
                    console_log(f"Operation wasn't found in results for Scatter Plot : {op}", self.msglvl + 1, "warn")
                    continue
                plot_2d_scatter_colored(
                    df,
                    x_label="OperandA(Log)",
                    y_label="OperandB(Log)",
                    z_label="Latency",
                    title=self.plot_config["title"],
                )
                data_name = getattr(tc, "data_name", tc.name)
                outfile = f"{self.outfile}_{str(op).lower()}_{data_name}_scatter".replace(" ", "")
                save_plot(outfile, self.outdir, self.msglvl)

    def plot_pie(self) -> None:
        console_log("Plot Pie being generated", self.msglvl + 1, "info")
        console_log(f"Number of TestCases : {len(self.testcases)}", self.msglvl + 1, "info")

        for tc in self.testcases.values():
            fig = plt.figure(figsize=self.plot_config["figsize"])
            ax = fig.add_subplot(111)

            df_cell_area = getattr(tc, "df_cell_area", None)
            blocks = getattr(self, "blocks", None)
            filt = getattr(self, "filter", None)
            y_label = getattr(tc, "y_label", None)
            if (
                df_cell_area is not None
                and isinstance(blocks, list)
                and len(blocks) > 1
                and isinstance(filt, dict)
                and y_label in df_cell_area.columns
                and "name" in filt
                and "value" in filt
            ):
                mask_filter = df_cell_area[filt["name"]] == float(filt["value"])
                df_base = df_cell_area[mask_filter]
                top_block_name = blocks[0]
                sub_block_names = blocks[1:]

                df_top = df_base[df_base["Instance"] == top_block_name]
                df_subs = df_base[df_base["Instance"].isin(sub_block_names)]

                total_area = df_top[y_label].sum()
                sum_sub_areas = df_subs[y_label].sum()
                other_area = total_area - sum_sub_areas

                slices = df_subs[y_label].tolist()
                labels = df_subs["Instance"].tolist()
                if other_area > 0:
                    slices.append(other_area)
                    labels.append("other")
                plt.pie(x=slices, labels=labels, autopct="%1.1f%%")

            ax.set_xlabel(self.plot_config["xlabel"], fontsize=self.plot_config["fontsize"])
            ax.set_ylabel(self.plot_config["ylabel"], fontsize=self.plot_config["fontsize"])
            ax.set_title(self.plot_config["title"], fontsize=self.plot_config["fontsize"])
            ax.grid(True)
            plt.legend()
            plt.tight_layout()
            save_plot(self.outfile, self.outdir, self.msglvl + 1)


class ReportMaestro:
    def __init__(self, config_file: str = "", outdir: str = "."):
        self.config_file = config_file
        self.outdir = outdir
        self.author = ""
        self.runset = []
        self.runcases = {}
        self.msglvl = 0

    def read_config(self, msglvl=0):
        console_log("Reading Aggregate Config file.", msglvl, "info")
        try:
            with open(self.config_file, "r") as infile:
                data = yaml.full_load(infile)
        except OSError:
            console_log(f"Could not open : {self.config_file} or malformed file", msglvl, "err")
            return

        self.runset = data.get("runset", [])
        author = data.get("author", {})
        self.author = f"{author.get('first name', '')} {author.get('last name', '')} ({author.get('trigram', '')})".strip()

        style = data.get("report_settings", {}).get("style")
        if style:
            plt.style.use(style)
        else:
            console_log("Default Matplotlib Style is set.", msglvl, "info")

        console_log(f"Author : {self.author}", msglvl + 1, "info")
        console_log(f"Number of Testcase(s) : {len(self.runset)}", msglvl + 1, "info")

    @staticmethod
    def mkdir(dir_path: str = "run"):
        os.makedirs(dir_path, exist_ok=True)

    def run_testcases(self, msglvl=0):
        console_log("Running configuration setting testcases.", msglvl, "info")
        console_log(f"Number of Testcase(s) : {len(self.runset)}", msglvl, "info")

        for run_cfg in self.runset:
            run_name = list(run_cfg.keys())[0]
            outdir = f"{self.outdir}/{run_name}"
            self.mkdir(outdir)
            run = Run(name=run_name, run_dict=run_cfg[run_name], outdir=outdir, msglvl=msglvl + 1)

            for fname, dfile in run.data.items():
                run.testcases[fname] = Dataset(
                    name=fname,
                    dfile=dfile,
                    xname=run.xval,
                    yname=run.yval,
                    zname=run.zval,
                    xmatch=run.xmatch,
                    ymatch=run.ymatch,
                    zmatch=run.zmatch,
                    msglvl=msglvl + 1,
                )
            self.runcases[run_name] = run

    def add_testcase(self, run: Run, tc: Dataset):
        if run.name not in self.runcases:
            self.runcases[run.name] = run
        self.runcases[run.name].testcases[tc.name] = tc

    def report_runcases(self, msglvl=0):
        console_log("****** Generating Reports ******", msglvl, "info")
        for run_cfg in self.runset:
            run_name = list(run_cfg.keys())[0]
            run = self.runcases.get(run_name)
            if run is not None:
                run.plot()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Utility For Generating Reports for FPU Performance.")
    parser.add_argument("--config", type=str, help="Path Report Config File")
    parser.add_argument("--outdir", type=str, help="Output Directory of Report", default="outputs")
    parser.add_argument("--quiet", type=bool, help="Disable Runtime Warnings", default=False, nargs="?", const=True)
    args = parser.parse_args()

    if args.quiet:
        warnings.filterwarnings("ignore")

    if args.config:
        agg = ReportMaestro(args.config, args.outdir)
        agg.read_config(msglvl=0)
        agg.run_testcases(msglvl=1)
        agg.report_runcases(msglvl=1)
    else:
        print("No Arguements provided...")
