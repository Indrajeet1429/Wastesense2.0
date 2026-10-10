
"""Inference interface for WASTESENSE expected-resource models."""

from pathlib import Path
from typing import Any, Mapping

import numpy as np
import pandas as pd
from catboost import CatBoostRegressor


ROOT = Path(__file__).resolve().parents[2]
MODEL_DIR = ROOT / "ml" / "artifacts" / "models"

RESOURCE_FEATURES = [
    "active_tasks",
    "cpu_capacity",
    "memory_capacity",
    "avg_priority",
    "max_priority",
    "elapsed_minutes",
    "trace_hour",
    "day_of_trace",
    "is_peak_period",
]

POWER_FEATURES = [
    "machine_count",
    "total_active_tasks",
    "total_cpu_capacity",
    "total_memory_capacity",
    "mean_avg_priority",
    "max_priority",
    "elapsed_minutes",
    "trace_hour",
    "day_of_trace",
    "is_peak_period",
    "pdu_pdu10",
    "pdu_pdu6",
    "pdu_pdu7",
    "pdu_pdu8",
    "pdu_pdu9",
]


def _load_model(filename: str, expected_features: list[str]) -> CatBoostRegressor:
    """Load a model and verify its stored feature names."""
    path = MODEL_DIR / filename

    if not path.is_file():
        raise FileNotFoundError(f"Model artifact not found: {path}")

    model = CatBoostRegressor()
    model.load_model(str(path))

    actual_features = list(model.feature_names_)
    if actual_features != expected_features:
        raise ValueError(
            f"Feature mismatch in {filename}. "
            f"Expected {expected_features}; found {actual_features}"
        )

    return model


def _validate_features(
    data: Mapping[str, Any],
    feature_names: list[str],
) -> pd.DataFrame:
    """Validate and arrange a single input row in model feature order."""
    missing = [name for name in feature_names if name not in data]
    if missing:
        raise ValueError(f"Missing required input features: {missing}")

    row = pd.DataFrame(
        [{name: data[name] for name in feature_names}],
        columns=feature_names,
    )

    row = row.apply(pd.to_numeric, errors="raise")

    values = row.to_numpy(dtype=float)
    if not np.isfinite(values).all():
        raise ValueError("Input features must all be finite numbers.")

    return row


def _predict_resource(
    model: CatBoostRegressor,
    data: Mapping[str, Any],
    target_name: str,
    actual_value: Any = None,
) -> dict[str, Any]:
    """Predict one resource and optionally compare with its actual value."""
    row = _validate_features(data, RESOURCE_FEATURES)

    if float(row.iloc[0]["cpu_capacity"]) <= 0:
        raise ValueError("cpu_capacity must be positive.")
    if float(row.iloc[0]["memory_capacity"]) <= 0:
        raise ValueError("memory_capacity must be positive.")
    if float(row.iloc[0]["active_tasks"]) < 0:
        raise ValueError("active_tasks cannot be negative.")

    prediction = float(model.predict(row)[0])

    result = {
        "resource": target_name,
        "expected": max(0.0, prediction),
        "actual": None,
        "excess": None,
        "model": "CatBoost",
    }

    if actual_value is not None:
        actual = float(actual_value)
        if not np.isfinite(actual) or actual < 0:
            raise ValueError(
                f"Actual {target_name} must be finite and non-negative."
            )

        result["actual"] = actual
        result["excess"] = actual - result["expected"]

    return result


def analyze_workload(input_data: Mapping[str, Any]) -> dict[str, Any]:
    """
    Predict expected CPU and memory for one machine-time workload.

    Required:
        All RESOURCE_FEATURES.

    Optional:
        actual_cpu, actual_memory.

    Power prediction is deliberately not performed here because the power
    model operates on aggregated PDU-time rows, not individual machines.
    """
    if not isinstance(input_data, Mapping):
        raise TypeError("input_data must be a mapping, such as a dictionary.")

    cpu_model = _load_model(
        "expected_resource_cpu.cbm",
        RESOURCE_FEATURES,
    )
    memory_model = _load_model(
        "expected_resource_memory.cbm",
        RESOURCE_FEATURES,
    )

    cpu = _predict_resource(
        cpu_model,
        input_data,
        "cpu",
        input_data.get("actual_cpu"),
    )
    memory = _predict_resource(
        memory_model,
        input_data,
        "memory",
        input_data.get("actual_memory"),
    )

    return {
        "status": "prediction_completed",
        "prediction_level": "machine-time",
        "resources": {
            "cpu": cpu,
            "memory": memory,
        },
        "power": {
            "status": "not_predicted",
            "reason": (
                "Power prediction requires aggregated PDU-time features. "
                "Use the dedicated PDU-time interface when implemented."
            ),
        },
        "waste_analysis": {
            "status": "not_implemented",
            "reason": (
                "Waste scores, root causes, persistence, and savings "
                "must be added and validated in later stages."
            ),
        },
    }
