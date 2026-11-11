class ErrorCordenada (Exception):
    """La excepción se lanza si la coordenada no pertenece al tablero utilizado"""
    pass
class ErrorBarconocabe (Exception):
    """La excepción se lanza si el barco no cabe desde la posición inical en el tabelro o si se monta encima de otro"""
    pass