import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr, spearmanr
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import warnings
warnings.filterwarnings('ignore')

# Set random seed for reproducibility
np.random.seed(42)

class CorrelationAnalyzer:
    def __init__(self, n_samples=1000):
        """
        Initialize the correlation analyzer
        
        Parameters:
        n_samples (int): Number of data points to generate
        """
        self.n_samples = n_samples
        self.data = None
        
    def generate_sample_data(self):
        """Generate sample data with known relationships"""
        # Generate 3 independent variables
        x1 = np.random.normal(0, 1, self.n_samples)  # Standard normal
        x2 = np.random.uniform(-2, 2, self.n_samples)  # Uniform distribution
        x3 = np.random.exponential(1, self.n_samples)  # Exponential distribution
        
        # Generate 2 dependent variables with known relationships
        noise1 = np.random.normal(0, 0.5, self.n_samples)
        noise2 = np.random.normal(0, 0.7, self.n_samples)
        
        # y1 depends on x1 and x2 with some noise
        y1 = 2.5 * x1 + 1.8 * x2 - 0.5 * x3 + noise1
        
        # y2 depends on x2 and x3 with some noise
        y2 = -1.2 * x1 + 3.0 * x2 + 1.5 * x3 + noise2
        
        # Create DataFrame
        self.data = pd.DataFrame({
            'X1': x1,
            'X2': x2,
            'X3': x3,
            'Y1': y1,
            'Y2': y2
        })
        
        print(f"Generated {self.n_samples} samples with 3 independent and 2 dependent variables")
        print(f"Data shape: {self.data.shape}")
        return self.data
    
    def load_custom_data(self, data):
        """
        Load custom data
        
        Parameters:
        data (DataFrame): DataFrame with columns ['X1', 'X2', 'X3', 'Y1', 'Y2']
        """
        required_cols = ['X1', 'X2', 'X3', 'Y1', 'Y2']
        if not all(col in data.columns for col in required_cols):
            raise ValueError(f"Data must contain columns: {required_cols}")
        
        self.data = data[required_cols].copy()
        self.n_samples = len(self.data)
        print(f"Loaded custom data with {self.n_samples} samples")
        return self.data
    
    def calculate_correlations(self):
        """Calculate various correlation measures"""
        if self.data is None:
            raise ValueError("No data available. Generate or load data first.")
        
        # Separate independent and dependent variables
        X = self.data[['X1', 'X2', 'X3']]
        Y = self.data[['Y1', 'Y2']]
        
        correlations = {}
        
        # Pearson correlations
        print("=== PEARSON CORRELATIONS ===")
        pearson_corr = {}
        for y_col in Y.columns:
            pearson_corr[y_col] = {}
            print(f"\n{y_col} correlations:")
            for x_col in X.columns:
                corr, p_value = pearsonr(X[x_col], Y[y_col])
                pearson_corr[y_col][x_col] = {'correlation': corr, 'p_value': p_value}
                significance = "***" if p_value < 0.001 else "**" if p_value < 0.01 else "*" if p_value < 0.05 else ""
                print(f"  {x_col}: r = {corr:.4f}, p = {p_value:.4f} {significance}")
        
        correlations['pearson'] = pearson_corr
        
        # Spearman correlations (rank-based, captures non-linear relationships)
        print("\n=== SPEARMAN CORRELATIONS ===")
        spearman_corr = {}
        for y_col in Y.columns:
            spearman_corr[y_col] = {}
            print(f"\n{y_col} correlations:")
            for x_col in X.columns:
                corr, p_value = spearmanr(X[x_col], Y[y_col])
                spearman_corr[y_col][x_col] = {'correlation': corr, 'p_value': p_value}
                significance = "***" if p_value < 0.001 else "**" if p_value < 0.01 else "*" if p_value < 0.05 else ""
                print(f"  {x_col}: ρ = {corr:.4f}, p = {p_value:.4f} {significance}")
        
        correlations['spearman'] = spearman_corr
        
        return correlations
    
    def multiple_regression_analysis(self):
        """Perform multiple regression analysis"""
        if self.data is None:
            raise ValueError("No data available. Generate or load data first.")
        
        X = self.data[['X1', 'X2', 'X3']]
        Y = self.data[['Y1', 'Y2']]
        
        # Standardize features for better interpretation
        scaler = StandardScaler()
        X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=X.columns)
        
        print("\n=== MULTIPLE REGRESSION ANALYSIS ===")
        regression_results = {}
        
        for y_col in Y.columns:
            # Fit regression model
            model = LinearRegression()
            model.fit(X_scaled, Y[y_col])
            
            # Predictions and R²
            y_pred = model.predict(X_scaled)
            r2 = r2_score(Y[y_col], y_pred)
            
            # Store results
            regression_results[y_col] = {
                'r2_score': r2,
                'coefficients': dict(zip(X.columns, model.coef_)),
                'intercept': model.intercept_
            }
            
            print(f"\n{y_col} Multiple Regression:")
            print(f"  R² Score: {r2:.4f}")
            print(f"  Intercept: {model.intercept_:.4f}")
            print("  Standardized Coefficients:")
            for var, coef in zip(X.columns, model.coef_):
                print(f"    {var}: {coef:.4f}")
        
        return regression_results
    
    def create_correlation_matrix(self):
        """Create and display correlation matrix heatmap"""
        if self.data is None:
            raise ValueError("No data available. Generate or load data first.")
        
        # Calculate correlation matrix for all variables
        corr_matrix = self.data.corr()
        
        # Create heatmap
        plt.figure(figsize=(10, 8))
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
        sns.heatmap(corr_matrix, mask=mask, annot=True, cmap='coolwarm', center=0,
                   square=True, fmt='.3f', cbar_kws={"shrink": .8})
        plt.title('Correlation Matrix Heatmap', fontsize=16, pad=20)
        plt.tight_layout()
        plt.show()
        
        return corr_matrix
    
    def create_scatter_plots(self):
        """Create scatter plots showing relationships"""
        if self.data is None:
            raise ValueError("No data available. Generate or load data first.")
        
        # Create subplots
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        fig.suptitle('Scatter Plots: Independent vs Dependent Variables', fontsize=16)
        
        X_vars = ['X1', 'X2', 'X3']
        Y_vars = ['Y1', 'Y2']
        
        for j, y_var in enumerate(Y_vars):
            for i, x_var in enumerate(X_vars):
                ax = axes[j, i]
                
                # Scatter plot
                ax.scatter(self.data[x_var], self.data[y_var], alpha=0.6, s=20)
                
                # Add trend line
                z = np.polyfit(self.data[x_var], self.data[y_var], 1)
                p = np.poly1d(z)
                ax.plot(self.data[x_var].sort_values(), p(self.data[x_var].sort_values()), "r--", alpha=0.8)
                
                # Calculate and display correlation
                corr, _ = pearsonr(self.data[x_var], self.data[y_var])
                ax.set_title(f'{x_var} vs {y_var}\nr = {corr:.3f}')
                ax.set_xlabel(x_var)
                ax.set_ylabel(y_var)
                ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    def summary_report(self):
        """Generate a comprehensive summary report"""
        if self.data is None:
            raise ValueError("No data available. Generate or load data first.")
        
        print("="*60)
        print("COMPREHENSIVE CORRELATION ANALYSIS REPORT")
        print("="*60)
        
        # Basic statistics
        print("\n1. DESCRIPTIVE STATISTICS:")
        print(self.data.describe().round(4))
        
        # Calculate correlations
        correlations = self.calculate_correlations()
        
        # Multiple regression
        regression_results = self.multiple_regression_analysis()
        
        # Strongest correlations summary
        print("\n=== STRONGEST CORRELATIONS SUMMARY ===")
        for y_var in ['Y1', 'Y2']:
            pearson_corrs = [(x_var, abs(correlations['pearson'][y_var][x_var]['correlation'])) 
                           for x_var in ['X1', 'X2', 'X3']]
            pearson_corrs.sort(key=lambda x: x[1], reverse=True)
            
            print(f"\n{y_var} - Ranked by absolute Pearson correlation:")
            for i, (x_var, corr) in enumerate(pearson_corrs, 1):
                original_corr = correlations['pearson'][y_var][x_var]['correlation']
                p_val = correlations['pearson'][y_var][x_var]['p_value']
                print(f"  {i}. {x_var}: r = {original_corr:.4f} (p = {p_val:.4f})")
        
        # Create visualizations
        print("\n=== GENERATING VISUALIZATIONS ===")
        self.create_correlation_matrix()
        self.create_scatter_plots()
        
        return {
            'correlations': correlations,
            'regression_results': regression_results,
            'data_summary': self.data.describe()
        }

# Example usage
if __name__ == "__main__":
    # Initialize analyzer
    analyzer = CorrelationAnalyzer(n_samples=500)
    
    # Generate sample data
    data = analyzer.generate_sample_data()
    
    # Run comprehensive analysis
    results = analyzer.summary_report()
    
    print("\n" + "="*60)
    print("ANALYSIS COMPLETE!")
    print("="*60)
    
    # Example of using custom data:
    # custom_data = pd.DataFrame({
    #     'X1': your_x1_data,
    #     'X2': your_x2_data,
    #     'X3': your_x3_data,
    #     'Y1': your_y1_data,
    #     'Y2': your_y2_data
    # })
    # analyzer.load_custom_data(custom_data)
    # results = analyzer.summary_report()