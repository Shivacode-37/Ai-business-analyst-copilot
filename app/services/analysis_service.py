from app.analytics.metrics_engine import compute_advanced_metrics
from app.services.summary_service import summarize_business
from app.reports.executive_report import generate_executive_report

from app.schema.detector import detect_schema
from app.schema.mapper import validate_mapping
from app.preprocessing.normalize import normalize_columns


class AnalysisService:
    @staticmethod
    def analyze(df):

        # Normalize columns
        df = normalize_columns(df)

        # Detect and validate schema
        mapping = detect_schema(df.columns.tolist())
        mapping = validate_mapping(
            mapping,
            df.columns.tolist(),
        )

        # Validate required business columns
        required = {
            "sales": mapping.sales,
            "profit": mapping.profit,
            "category": mapping.category,
            "region": mapping.region,
            "date": mapping.order_date,
        }

        missing = [name for name, value in required.items() if value is None]

        if missing:
            raise ValueError(
                "Unsupported dataset. Missing required business columns: "
                + ", ".join(missing)
            )

        # Compute metrics
        metrics = compute_advanced_metrics(
            df,
            mapping,
        )

        # Generate business summary and executive report
        summary = summarize_business(metrics)
        executive_report = generate_executive_report(metrics)

        return {
            "metrics": metrics,
            "summary": summary,
            "executive_report": executive_report,
        }
