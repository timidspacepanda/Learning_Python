def check_null_hypothesis_rejected(p_value):
    alpha = 0.05
    if p_value < alpha:
        print("Reject the null hypothesis: There is a significant difference.")
    else:
        print("Fail to reject the null hypothesis: No significant difference.")
    
    