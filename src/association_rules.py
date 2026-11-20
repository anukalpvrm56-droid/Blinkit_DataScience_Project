"""
Association Rule Mining Module
[Aligned with UPES Course Plan CSDS2002P - Unit V & Lab Exp 8]

Concepts Covered:
- Unit V, Lab Exp 8: Frequent Itemsets & Market Basket Association Rules
- Mathematical Metrics: Support, Confidence, Lift
"""
import pandas as pd
import numpy as np
from src.data_pipeline import get_merged_orders

def mine_category_association_rules(min_support: float = 0.05, min_confidence: float = 0.20) -> pd.DataFrame:
    """
    [Unit V, Lab Exp 8: Market Basket Association Analysis]
    Analyzes cross-category customer buying habits.
    
    Mathematical Definitions:
    - Support(A): Fraction of customers who bought category A.
    - Support(A -> B): Fraction of customers who bought both A and B.
    - Confidence(A -> B): P(B | A) = Support(A -> B) / Support(A)
    - Lift(A -> B): Confidence(A -> B) / Support(B)
      * Lift > 1.0 indicates positive association (A and B are bought together more than chance).
      * Lift = 1.0 indicates independence.
      * Lift < 1.0 indicates negative association.
    """
    df = get_merged_orders()
    
    # Create customer-category basket matrix (1 if customer purchased category, else 0)
    basket = df.groupby(["customer_id", "category"])["order_id"].count().unstack().fillna(0)
    basket_binary = (basket > 0).astype(int)
    
    total_customers = len(basket_binary)
    categories = list(basket_binary.columns)
    
    # 1. Compute Individual Support P(A)
    single_support = basket_binary.sum(axis=0) / total_customers
    
    rules = []
    
    # 2. Compute Pairwise Support P(A & B), Confidence, and Lift
    for i in range(len(categories)):
        cat_A = categories[i]
        supp_A = single_support[cat_A]
        if supp_A < min_support:
            continue
            
        for j in range(len(categories)):
            if i == j:
                continue
            cat_B = categories[j]
            supp_B = single_support[cat_B]
            if supp_B < min_support:
                continue
                
            # Both A and B purchased by same customer
            both = (basket_binary[cat_A] & basket_binary[cat_B]).sum()
            supp_AB = both / total_customers
            
            if supp_AB >= min_support:
                confidence = supp_AB / supp_A
                lift = confidence / supp_B if supp_B > 0 else 0.0
                
                if confidence >= min_confidence:
                    rules.append({
                        "Antecedent (If Bought)": cat_A,
                        "Consequent (Also Buys)": cat_B,
                        "Support (%)": round(supp_AB * 100, 2),
                        "Confidence (%)": round(confidence * 100, 2),
                        "Lift": round(lift, 3)
                    })
                    
    rules_df = pd.DataFrame(rules)
    if not rules_df.empty:
        rules_df = rules_df.sort_values("Lift", ascending=False).reset_index(drop=True)
    return rules_df

if __name__ == "__main__":
    print("Testing Association Rule Mining...")
    rules = mine_category_association_rules(min_support=0.04, min_confidence=0.15)
    print(f"Discovered {len(rules)} association rules:")
    print(rules.head(10).to_string(index=False))
