import torch

def chernoff_coef(vec1, vec2, alpha):
    """
    The Chernoff coefficient c is a similarity measure C_{alpha}(P||Q)
    = sum_k[p_k^alpha * q_k^(1-alpha)] e[0,1] between two (probability) 
    distributions P and Q. The alpha parameter determines if we want to
    measure whether Q includes elements that are not in P.
    """
    if alpha < 0 or alpha > 1:
        raise ValueError("alpha must be in [0,1]")
    # use log to avoid underflow
    return torch.sum(torch.exp((torch.log(vec1) * alpha) +
                               (torch.log(vec2) * (1-alpha))), axis=0)

def normalize_vector(vector):
    """Normalize a vector to have sum 1."""
    return torch.nan_to_num(torch.divide(vector, torch.sum(vector)))

def divergence(vec1, vec2, alpha):
    """
    Calculate divergence between two vectors.
    Atom divergence is 1 - Chernoff coefficient, with alpha=0.5.
    Compound divergence is 1 - Chernoff coefficient, with alpha=0.1.
    """
    return float(1 - chernoff_coef(normalize_vector(vec1), normalize_vector(vec2), alpha))
