from typing import Dict

def summarize_business(metrics: Dict) -> Dict:
    """
    Extracts structured decision signals from metrics.
    """

    health = metrics["business_health"]
    collapse = metrics["structural_collapse_by_category"]
    inefficiency = metrics["structural_inefficiency_by_category"]

    # Check structural collapse
    collapse_risk = collapse["loss_consistency_ratio"].max()

    #  Highest inefficiency category
    highest_risk_row = inefficiency.iloc[0]
    highest_risk_category = highest_risk_row["category"]
    highest_loss_ratio = highest_risk_row["avg_loss_ratio"]

    #  Determine risk level
    if collapse_risk > 0:
        risk_level = "Severe (Structural Collapse Detected)"
    elif highest_loss_ratio > 0.35:
        risk_level = "High (Structural Inefficiency)"
    elif highest_loss_ratio > 0.25:
        risk_level = "Moderate"
    else:
        risk_level = "Low"

    summary = {
        "health_score": health["health_score"],
        "profit_margin_pct": health["profit_margin_pct"],
        "loss_order_pct": health["loss_order_pct"],
        "highest_risk_category": highest_risk_category,
        "highest_loss_ratio": round(highest_loss_ratio * 100, 2),
        "risk_level": risk_level
    }

    return summary

def generate_executive_summary(summary: Dict) -> str:
    """
    Converts structured summary into executive-ready explanation.
    Deterministic — no hallucination.
    """

    explanation = f"""
Business Health Score: {summary['health_score']}/100.

Overall profit margin stands at {summary['profit_margin_pct']}%.
However, {summary['loss_order_pct']}% of orders are loss-making.

The highest structural inefficiency is observed in the 
{summary['highest_risk_category']} category, where approximately 
{summary['highest_loss_ratio']}% of orders consistently generate losses.

Risk Classification: {summary['risk_level']}.

Although aggregate profitability remains positive, 
margin concentration and pricing inefficiencies increase volatility risk. 
Strategic review of discounting, cost structure, and customer segmentation is recommended.
"""

    return explanation.strip()

def answer_business_question(question: str, metrics: Dict) -> str:
    """
    Deterministic business Q&A engine.
    Routes question to appropriate metric.
    """

    question = question.lower()

    summary = summarize_business(metrics)

    if "health" in question:
        return f"The overall business health score is {summary['health_score']}/100."

    elif "margin" in question:
        return f"The current profit margin is {summary['profit_margin_pct']}%."

    elif "loss" in question and "category" in question:
        return (
            f"The category with highest structural inefficiency is "
            f"{summary['highest_risk_category']} "
            f"with approximately {summary['highest_loss_ratio']}% "
            f"loss-making orders."
        )

    elif "risk" in question:
        return f"Risk classification is: {summary['risk_level']}."

    else:
        return "Question not recognized. Please ask about health, margin, risk, or loss categories."

