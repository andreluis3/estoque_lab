class ValidationError(Exception):
    """Disparada quando os dados de entrada violam restrições sanitárias básicas."""
    pass

class BusinessRuleError(Exception):
    """Disparada quando uma operação viola diretrizes operacionais do laboratório."""
    pass