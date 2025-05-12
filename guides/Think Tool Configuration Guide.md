---
tags:
  - decision_making
  - frameworks
  - business_logic
---
CONFIGURATION EXPLANATION:  
The think tool is a decision-making framework for systematically analyzing user requests before taking action. Its configuration requires:  

1. **Rule Identification**  
   - List relevant policies (e.g., cancellation timeframes, baggage allowances, payment restrictions)  
   - Example: Checking "24h booking window" or membership tier rules for baggage  

2. **Data Validation**  
   - Collect mandatory user data (IDs, profile info, transaction details)  
   - Example: Verifying user membership level to calculate baggage fees  

3. **Compliance Checks**  
   - Ensure proposed actions align with operational policies  
   - Example: Confirming no flight segments have been used before cancellation  

4. **Iterative Verification**  
   - Cross-validate scenarios with multiple variables  
   - Example: Calculating fees based on membership tiers (regular/silver/gold) for baggage rules  

This structured approach ensures decisions consider all business logic constraints while maintaining policy adherence. The examples demonstrate application across scenarios like cancellations, bookings with complex baggage requirements, and payment method validation.