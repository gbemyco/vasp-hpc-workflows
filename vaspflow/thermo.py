def hydrogen_adsorption_free_energy(
    clean_ev: float,
    adsorbed_ev: float,
    h2_ev: float,
    zpe_correction_ev: float = 0.0,
    entropy_correction_ev: float = 0.0,
) -> float:
    """Return ΔG_H* in eV using the computational hydrogen electrode."""
    delta_e = adsorbed_ev - clean_ev - 0.5 * h2_ev
    return delta_e + zpe_correction_ev - entropy_correction_ev
