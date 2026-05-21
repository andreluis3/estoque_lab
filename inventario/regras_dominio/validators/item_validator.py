from inventario.regras_dominio.exceptions.business_exceptions import ValidationError

class ItemValidator:
    @staticmethod
    def validar_e_normalizar(dados: dict) -> dict:
        """Garante a higienização completa e valida a integridade estrutural do item."""
        
        # Copia dicionário para evitar efeitos colaterais
        item = dados.copy()
        
        # Tratamento e Normalização (Redução de dados espelho / duplicados)
        nome_cru = item.get("nome", "")
        tipo_cru = item.get("tipo", "")
        caixa_cru = item.get("caixa", "")
        
        if not nome_cru or not str(nome_cru).strip():
            raise ValidationError("O campo 'Nome' é estritamente obrigatório.")
        if not tipo_cru or not str(tipo_cru).strip():
            raise ValidationError("O campo 'Tipo' é estritamente obrigatório.")
        if not caixa_cru or not str(caixa_cru).strip():
            raise ValidationError("O campo 'Caixa' é estritamente obrigatório.")
            
        # Normalização estrutural enterprise
        item["nome"] = str(nome_cru).strip().title()
        item["tipo"] = str(tipo_cru).strip().lower()
        item["modelo"] = str(item.get("modelo", "")).strip().upper() or "GENÉRICO"
        item["caixa"] = str(caixa_cru).strip().upper()
        
        item["localizacao"] = str(item.get("localizacao", "")).strip() or "Não informado"
        item["slot"] = str(item.get("slot", "")).strip() or "Não informado"
        
        # Validação numérica
        try:
            qtd = int(item.get("quantidade", 0))
            if qtd < 0:
                raise ValidationError("A quantidade não pode ser um valor negativo.")
            item["quantidade"] = qtd
        except (ValueError, TypeError):
            raise ValidationError("O valor informado para 'Quantidade' é inválido.")
            
        # Restrição de tamanho de string (Prevenir buffer transbordado ou UI quebrada)
        if len(item["nome"]) > 100:
            raise ValidationError("O nome do componente excede o limite permitido de 100 caracteres.")
            
        return item