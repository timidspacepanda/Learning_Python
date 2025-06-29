from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

def check_null_hypothesis_rejected(p_value):
    alpha = 0.05
    if p_value < alpha:
        print("Reject the null hypothesis: There is a significant difference.")
    else:
        print("Fail to reject the null hypothesis: No significant difference.")

def evaluate_regression(y_true, y_pred):  
    """Evaluate regression model and plot actual vs predicted values."""
    mse = mean_squared_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)

    print("\nRunning regression evaluation ...")
    print(f"Mean Squared Error: {mse:.4f}")
    print(f"R-squared Score: {r2:.4f}")

    # Plot actual vs predicted
    plt.scatter(y_true, y_pred)
    plt.plot([min(y_true), max(y_true)], [min(y_true), max(y_true)], color='red', linestyle='--')
    plt.xlabel("Actual")
    plt.ylabel("Predicted")
    plt.title("Actual vs. Predicted Values")
    plt.title("Actual vs. Predicted Values")
    plt.grid(True)
    plt.show()