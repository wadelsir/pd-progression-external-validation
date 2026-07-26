"""Outcome construction and MDS-UPDRS Part III record-selection utilities."""

from __future__ import annotations

from typing import Iterable

import numpy as np
import pandas as pd

DEFAULT_RAPID_PROGRESSION_THRESHOLD = 5.0793

# Lower values have higher priority.
EXAM_STATE_PRIORITY = {
    "off": 1,
    "untreated": 2,
    "unmedicated": 2,
    "standard": 3,
    "unspecified": 3,
    "on": 4,
    "unknown": 5,
}


def _normalise_exam_state(value: object) -> str:
    """Map heterogeneous medication/examination-state labels to a common category."""
    if pd.isna(value):
        return "unknown"
    text = str(value).strip().lower()
    if "off" in text:
        return "off"
    if "untreat" in text:
        return "untreated"
    if "unmed" in text:
        return "unmedicated"
    if "on" in text:
        return "on"
    if "standard" in text:
        return "standard"
    if text in {"", "na", "n/a", "none", "unknown"}:
        return "unknown"
    return "unspecified"


def select_preferred_mds_updrs_records(
    data: pd.DataFrame,
    *,
    participant_col: str,
    visit_col: str,
    score_col: str,
    exam_state_col: str,
    assessment_date_col: str | None = None,
    record_id_col: str | None = None,
) -> pd.DataFrame:
    """Retain one preferred MDS-UPDRS Part III record per participant and visit.

    Priority is OFF medication, untreated/unmedicated, standard/unspecified,
    ON medication, and finally unknown. Non-missing total scores are preferred.
    Assessment date and record identifier provide deterministic tie-breaking.
    """
    required = {participant_col, visit_col, score_col, exam_state_col}
    missing = sorted(required.difference(data.columns))
    if missing:
        raise KeyError(f"Missing required columns: {missing}")

    frame = data.copy()
    frame["_normalised_exam_state"] = frame[exam_state_col].map(_normalise_exam_state)
    frame["_exam_state_priority"] = frame["_normalised_exam_state"].map(EXAM_STATE_PRIORITY)
    frame["_score_missing"] = pd.to_numeric(frame[score_col], errors="coerce").isna().astype(int)

    sort_cols: list[str] = [participant_col, visit_col, "_score_missing", "_exam_state_priority"]
    ascending: list[bool] = [True, True, True, True]

    if assessment_date_col and assessment_date_col in frame.columns:
        frame[assessment_date_col] = pd.to_datetime(frame[assessment_date_col], errors="coerce")
        sort_cols.append(assessment_date_col)
        ascending.append(True)
    if record_id_col and record_id_col in frame.columns:
        sort_cols.append(record_id_col)
        ascending.append(True)

    selected = (
        frame.sort_values(sort_cols, ascending=ascending, kind="mergesort")
        .drop_duplicates([participant_col, visit_col], keep="first")
        .drop(columns=["_score_missing", "_exam_state_priority"])
        .reset_index(drop=True)
    )
    return selected


def build_annualized_outcome(
    selected_records: pd.DataFrame,
    *,
    participant_col: str,
    visit_col: str,
    score_col: str,
    baseline_visit: str = "BL",
    followup_visit: str = "V06",
    assessment_date_col: str | None = None,
    expected_followup_years: float = 2.0,
    rapid_progression_threshold: float = DEFAULT_RAPID_PROGRESSION_THRESHOLD,
    allowed_exam_states: Iterable[str] = ("off", "untreated", "unmedicated"),
) -> pd.DataFrame:
    """Construct annualized MDS-UPDRS Part III change and binary progression outcome."""
    required = {participant_col, visit_col, score_col}
    missing = sorted(required.difference(selected_records.columns))
    if missing:
        raise KeyError(f"Missing required columns: {missing}")

    frame = selected_records.copy()
    frame[score_col] = pd.to_numeric(frame[score_col], errors="coerce")

    if "_normalised_exam_state" in frame.columns:
        frame = frame[frame["_normalised_exam_state"].isin(set(allowed_exam_states))].copy()

    base = frame[frame[visit_col].astype(str) == baseline_visit].copy()
    follow = frame[frame[visit_col].astype(str) == followup_visit].copy()

    base_cols = [participant_col, score_col]
    follow_cols = [participant_col, score_col]
    if assessment_date_col and assessment_date_col in frame.columns:
        base_cols.append(assessment_date_col)
        follow_cols.append(assessment_date_col)

    base = base[base_cols].rename(columns={score_col: "baseline_np3tot"})
    follow = follow[follow_cols].rename(columns={score_col: "followup_np3tot"})

    if assessment_date_col and assessment_date_col in frame.columns:
        base = base.rename(columns={assessment_date_col: "baseline_date"})
        follow = follow.rename(columns={assessment_date_col: "followup_date"})

    outcome = base.merge(follow, on=participant_col, how="inner", validate="one_to_one")
    outcome["absolute_change"] = outcome["followup_np3tot"] - outcome["baseline_np3tot"]

    if {"baseline_date", "followup_date"}.issubset(outcome.columns):
        baseline_date = pd.to_datetime(outcome["baseline_date"], errors="coerce")
        followup_date = pd.to_datetime(outcome["followup_date"], errors="coerce")
        years = (followup_date - baseline_date).dt.days / 365.25
        valid = years.gt(0)
        outcome["followup_years"] = np.where(valid, years, expected_followup_years)
    else:
        outcome["followup_years"] = float(expected_followup_years)

    outcome["annualized_change"] = outcome["absolute_change"] / outcome["followup_years"]
    outcome["rapid_progression"] = (
        outcome["annualized_change"] >= float(rapid_progression_threshold)
    ).astype(int)
    outcome["rapid_progression_threshold"] = float(rapid_progression_threshold)

    return outcome.reset_index(drop=True)
