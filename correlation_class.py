#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 14 18:59:27 2025

@author: kpetchsaiprasert
"""

import numpy as np
import pandas as pd
from scipy import stats

class Correlation:
    def __init__(self, x=None, y=None, df=None):
        """
        Initialize with either:
        - x and y (lists, arrays, or Series of equal length), OR
        - df (pandas DataFrame for full correlation matrix).
        """
        self.x = np.array(x) if x is not None else None
        self.y = np.array(y) if y is not None else None
        self.df = df
        
        if self.x is not None and self.y is not None:
            if self.x.shape != self.y.shape:
                raise ValueError("x and y must have the same length")
                
    # ----- Pairwise Correlation -----
    def pearson(self):
        if self.x is None or self.y is None:
            raise ValueError("x and y must be provided for pairwise correlation")
        
        r, p = stats.pearsonr(self.x, self.y)
        return {"method": "spearman", "correlation": r, "p_value": p}
    
    def spearman(self):
        if self.x is None or self.y is None:
            raise ValueError("x and y must be provided for pairwise correlation")
            
        r, p = stats.spearmanr(self.x, self.y)
        return {"method": "spearman", "correlation": r, "p_value": p}
    
    def kendall(self):
        if self.x is None or self.y is None:
            raise ValueError("x and y must be provided for pairwise correlation")
        
        r, p = stats.kendalltau(self.x, self.y)
        return {"method": "kendall", "correlation": r, "p_value": p}
    
    # ------ DataFrame Correlation -----
    def _df_corr_with_pvalues(self, method="pearson"):
        cols = self.df.columns
        n = len(cols)
        
        corr_matrix = pd.DataFrame(np.zeros((n, n)), columns=cols, index=cols)
        pval_matrix = pd.DataFrame(np.zeros((n, n)), columns=cols, index=cols)
        
        for i in range(n):
            for j in range(n):
                if i == j:
                    corr_matrix.iloc[i, j] = 1.0
                    pval_matrix.iloc[i, j] = 0.0
                    
                else:
                    x = self.df.iloc[:, i]
                    y = self.df.iloc[:, j]
                    
                    if method == "pearson":
                        r, p = stats.pearsonr(x, y)
                    elif method == "spearman":
                        r, p = stats.spearmanr(x, y)
                    elif method == "kendall":
                        r, p = stats.kendalltau(x, y)
                    else:
                        raise ValueError("Invalid method. Choose 'pearson', 'spearman', or 'kendall'.")
                        
                    corr_matrix.iloc[i, j] = r
                    pval_matrix.iloc[i, j] = p
            
            return corr_matrix, pval_matrix
        
    def corr(self, method="pearson", return_pvalues=False):
        """
        Compute correlation.
        - For pairwise (x,y), returns dict with r and p.
        - For DataFrame, returns correlation matrix (and p-values if requested).
        """
        
        method = method.lower()
        
        # Pairwise case
        if self.df is None:
            if method == "pearson":
                return self.pearson()
            elif method == "spearman":
                return self.spearman()
            elif method == "kendall":
                return self.kendall()
            else:
                raise ValueError("Invalid method. Choose 'pearson', 'spearman', or 'kendall'.")
            
        # DataFrame case
        else:
            corr_matrix, pval_matrix = self._df_corr_with_pvalues(method)
            if return_pvalues:
                return{"correlation": corr_matrix, "p_values": pval_matrix}
            return corr_matrix
            
# ----------------------- Example Usage -----------------------
if __name__ == "__main__":
    # Pairwise example
    x = [1, 2, 3, 4, 5]
    y = [2, 1, 4, 3, 7]
    corr_pair = Correlation(x, y)
    print(corr_pair.pearson())
    print(corr_pair.spearman())
    
    
    # DataFrame example
    data = {
        "A": [1, 2, 3, 4, 5],
        "B": [2, 1, 4, 3, 7],
        "C": [5, 3, 6, 2, 1]
    }
    df = pd.DataFrame(data)
    corr_matrix = Correlation(df=df)
    
    # Correlation only
    print(corr_matrix.corr("pearson"))
    
    # Correlation + P-values
    results = corr_matrix.corr("spearman", return_pvalues=True)
    print("Correlation:\n", results["correlation"])
    print("P-values:\n", results["p_values"])
                                        